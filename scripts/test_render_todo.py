"""Offline self-tests for the plan-only GitHub task view."""

import copy
import json
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch
from xml.etree import ElementTree

import render_todo


class TestTodo(unittest.TestCase):
    def setUp(self):
        self.route = render_todo.load_route(render_todo.ROUTE)
        self.route = copy.deepcopy(self.route)
        self.route["iteration_queue"] = []  # Isolate graph tests from live completion metadata.
        self.route["evidence_by_step"] = {}
        self.route["progress_overrides"] = {}
        self.route["gate_decisions"] = {}
        mock = patch('render_todo.evidence_valid', side_effect=lambda entry, *_: bool(entry))
        mock.start()
        self.addCleanup(mock.stop)

    def test_initial_view_is_not_approved(self):
        actual = render_todo.resolve(self.route)
        gates = render_todo.stats(self.route, actual)
        self.assertEqual(sum(n for n, _ in gates.values()), 0)
        self.assertEqual(sum(n for _, n in gates.values()), 112)
        self.assertIn("- [ ] **B001**", render_todo.make_markdown(self.route, actual, gates))

    def test_fake_completion_is_rejected(self):
        self.route["progress_overrides"]["B001"] = "VERIFIED"
        with self.assertRaisesRegex(ValueError, "Prüfnachweis"):
            render_todo.resolve(self.route)

    def test_valid_completion_updates_graph_and_checkbox(self):
        self.route["progress_overrides"]["B001"] = "VERIFIED"
        self.route["evidence_by_step"]["B001"] = {
            "source_sha": "a" * 40, "test_run": "plan-qa-001", "result": "PASS"
        }
        actual = render_todo.resolve(self.route)
        totals = render_todo.stats(self.route, actual)
        self.assertEqual(totals["G-1"][0], 1)
        self.assertIn("- [x] **B001**", render_todo.make_markdown(self.route, actual, totals))
        self.assertIn("1/112", render_todo.make_svg(totals))

    def test_parent_cannot_skip_substep(self):
        self.route["progress_overrides"]["B005"] = "VERIFIED"
        self.route["evidence_by_step"]["B005"] = {
            "source_sha": "a" * 40, "test_run": "plan-qa-005", "result": "PASS"
        }
        with self.assertRaisesRegex(ValueError, "Unteraufgaben"):
            render_todo.resolve(self.route)

    def mark_verified(self, sid):
        self.route["progress_overrides"][sid] = "VERIFIED"
        self.route["evidence_by_step"][sid] = {
            "source_sha": "a" * 40, "test_run": "plan-qa", "result": "PASS"
        }

    def test_completion_requires_dependencies(self):
        self.mark_verified("B002")
        with self.assertRaisesRegex(ValueError, "Abhaengigkeiten"):
            render_todo.resolve(self.route)

    def test_substep_inherits_parent_dependencies(self):
        self.mark_verified("B005.01")
        with self.assertRaisesRegex(ValueError, "Abhaengigkeiten"):
            render_todo.resolve(self.route)

    def test_dependency_graph_rejects_invalid_edges_and_cycles(self):
        for dependencies in (["UNKNOWN"], ["B001", "B001"], ["B002"]):
            with self.subTest(dependencies=dependencies):
                self.route["steps"]["B001"]["depends_on"] = dependencies
                with self.assertRaises(ValueError):
                    render_todo.resolve(self.route)

    def test_duplicate_substep_rejected(self):
        self.route["steps"]["B001"]["substeps"] = [{"id": "B002"}]
        with self.assertRaisesRegex(ValueError, "Doppelte"):
            render_todo.resolve(self.route)

    def test_preview_follows_dependencies_not_mapping_order(self):
        self.route["steps"] = dict(reversed(list(self.route["steps"].items())))
        actual = render_todo.resolve(self.route)
        self.assertEqual(render_todo.next_three(self.route, actual), ["B001", "B002", "B003"])

    def test_blocked_or_deprecated_chain_has_no_ready_successor(self):
        for status in ("BLOCKED", "DEPRECATED"):
            with self.subTest(status=status):
                self.route["progress_overrides"]["B001"] = status
                actual = render_todo.resolve(self.route)
                self.assertEqual(render_todo.next_three(self.route, actual), [])

    def test_iteration_deviation_precedes_normal_route(self):
        self.route["iteration_queue"] = [{
            "id": "D001", "title": "Befund beheben", "reason": "Blockade beheben",
            "status": "PLANNED", "depends_on": []
        }]
        actual = render_todo.resolve(self.route)
        self.assertEqual(render_todo.next_three(self.route, actual), ["D001", "B001", "B002"])
        markdown = render_todo.make_markdown(self.route, actual, render_todo.stats(self.route, actual))
        self.assertIn("Bedingte Vorschau", markdown)
        self.assertIn("Keine Ausfuehrungs- oder Gatefreigabe", markdown)

    def test_pending_deviation_blocks_regular_route_until_resolved(self):
        self.route["iteration_queue"] = [
            {"id": "D001", "reason": "Abhaengigkeit klaeren", "status": "PLANNED", "depends_on": ["B001"]},
            {"id": "D002", "reason": "Zweiter Befund", "status": "PLANNED", "depends_on": []},
        ]
        actual = render_todo.resolve(self.route)
        self.assertEqual(render_todo.next_three(self.route, actual), [])
        self.mark_verified("B001")
        actual = render_todo.resolve(self.route)
        self.assertEqual(render_todo.next_three(self.route, actual), ["D001", "D002", "B002"])

    def test_exact_main_step_identifiers_required(self):
        self.route["steps"]["OTHER"] = self.route["steps"].pop("B002")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "route.json"
            path.write_text(json.dumps(self.route), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Schrittnummern"):
                render_todo.load_route(path)

    def test_iteration_deviation_validation(self):
        entry = {"id": "D001", "reason": "Befund", "status": "PLANNED", "depends_on": []}
        for entries in ([dict(entry, id="")], [dict(entry, reason="")],
                        [entry, entry], [dict(entry, status="READY")]):
            with self.subTest(entries=entries):
                self.route["iteration_queue"] = entries
                with self.assertRaises(ValueError):
                    render_todo.resolve(self.route)

    def test_verified_deviation_needs_evidence_and_dependencies(self):
        self.route["iteration_queue"] = [{
            "id": "D001", "reason": "Befund", "status": "VERIFIED", "depends_on": ["B001"]
        }]
        with self.assertRaises(ValueError):
            render_todo.resolve(self.route)
        self.route["evidence_by_step"]["D001"] = {
            "source_sha": "a" * 40, "test_run": "qa", "result": "PASS"
        }
        with self.assertRaisesRegex(ValueError, "Abhaengigkeiten"):
            render_todo.resolve(self.route)
        self.mark_verified("B001")
        self.assertTrue(render_todo.resolve(self.route)["D001"])

    def test_accessible_svg_and_exact_checkboxes(self):
        actual = render_todo.resolve(self.route)
        totals = render_todo.stats(self.route, actual)
        svg = ElementTree.fromstring(render_todo.make_svg(totals))
        self.assertEqual(svg.tag, "{http://www.w3.org/2000/svg}svg")
        self.assertIsNotNone(svg.find("{http://www.w3.org/2000/svg}title"))
        markdown = render_todo.make_markdown(self.route, actual, totals)
        self.assertEqual(markdown.count("- [ ]"), 134)


if __name__ == "__main__":
    unittest.main()
