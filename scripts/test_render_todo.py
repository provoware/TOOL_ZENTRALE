"""Offline self-tests for the plan-only GitHub task view."""

import copy
import unittest
from xml.etree import ElementTree

import render_todo


class TestTodo(unittest.TestCase):
    def setUp(self):
        self.route = render_todo.load_route(render_todo.ROUTE)
        self.route = copy.deepcopy(self.route)

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
