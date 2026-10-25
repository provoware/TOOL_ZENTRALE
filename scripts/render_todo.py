#!/usr/bin/env python3
"""Generate the V3.2 GitHub checklist and accessible SVG from route.json.

Usage: python3 scripts/render_todo.py [--check]
The route and SHA-bound evidence remain authoritative; Markdown is a view.
"""

import argparse
import json
import re
from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
ROUTE = ROOT / "governance/route.json"
TODO = ROOT / "docs/TODO_V3_2.md"
GRAPH = ROOT / "docs/assets/todo_progress.svg"
GATE_LABELS = {
    "G-1": "Architektur und Blueprint",
    "G0": "Bestandsaufnahme",
    "G1": "Entwicklungsautomatik",
    "G2": "Backend und Datenkern",
    "G3": "Import und Datensicherung",
    "G4": "Bedienoberfläche",
    "G5": "Songs und Kreativfunktionen",
    "G6": "Projekte",
    "G7": "Medien und Dateien",
    "G8": "Werkzeuge und Plugins",
    "G9": "Fehlerlernen und Regression",
    "G10": "Qualitätsabschluss",
    "G11": "Release und Betrieb",
}
DONE = "VERIFIED"
STATUSES = {"PLANNED", "READY", "PATCHED", "VERIFIED", "BLOCKED", "DEPRECATED"}


def load_route(path):
    payload = json.loads(path.read_text(encoding="utf-8"))
    steps, gates = payload["steps"], payload["gates"]
    if len(steps) != 112 or list(gates) != list(GATE_LABELS):
        raise ValueError("Erwartet 112 stabile Hauptschritte und 13 Gates")
    if not all(key in steps for key in ("B001", "B012", "P001", "P100")):
        raise ValueError("Stabile Schrittnummern fehlen")
    return payload


def evidence_valid(entry):
    return isinstance(entry, dict) and all(
        isinstance(entry.get(field), str) and entry[field].strip()
        for field in ("source_sha", "test_run", "result")
    ) and entry["result"] == "PASS" and bool(re.fullmatch(r"[0-9a-f]{40}", entry["source_sha"]))


def resolve(route):
    steps = route["steps"]
    statuses = route.get("progress_overrides", {})
    evidence = route.get("evidence_by_step", {})
    ids = set(steps)
    for parent in steps.values():
        ids.update(sub["id"] for sub in parent.get("substeps", []))
    if set(statuses) - ids or set(evidence) - ids:
        raise ValueError("Unbekannte Status-/Evidenz-ID; Abbruch")
    actual = {}
    for step_id, step in steps.items():
        for sub in step.get("substeps", []):
            sub_id = sub["id"]
            sub_status = statuses.get(sub_id, route["default_step_and_gate_status"])
            if sub_status not in STATUSES:
                raise ValueError(f"{sub_id}: unbekannter Status {sub_status}")
            if sub_status == DONE and not evidence_valid(evidence.get(sub_id)):
                raise ValueError(f"{sub_id}: VERIFIED ohne aktuellen Prüfnachweis")
            actual[sub_id] = sub_status == DONE
        status = statuses.get(step_id, route["default_step_and_gate_status"])
        if status not in STATUSES:
            raise ValueError(f"{step_id}: unbekannter Status {status}")
        if status == DONE and not evidence_valid(evidence.get(step_id)):
            raise ValueError(f"{step_id}: VERIFIED ohne aktuellen Prüfnachweis")
        if status == DONE and any(not actual[sub["id"]] for sub in step.get("substeps", [])):
            raise ValueError(f"{step_id}: VERIFIED vor Abschluss der Unteraufgaben")
        actual[step_id] = status == DONE
    return actual


def stats(route, actual):
    output = {}
    for gate_id in route["gates"]:
        ids = [sid for sid, item in route["steps"].items() if item["gate"] == gate_id]
        output[gate_id] = (sum(actual[sid] for sid in ids), len(ids))
    return output


def make_markdown(route, actual, totals):
    completed = sum(done for done, _ in totals.values())
    all_steps = sum(total for _, total in totals.values())
    sub_ids = [sub["id"] for item in route["steps"].values() for sub in item.get("substeps", [])]
    sub_done = sum(actual[sid] for sid in sub_ids)
    result = [
        "# TOOL_ZENTRALE – intelligente TODO V3.2",
        "",
        "> **Planungsdokument.** Keine Produktimplementierung und keine G−1-Freigabe.",
        "",
        "![Grafischer Fortschritt: nach Gates und gesamt](assets/todo_progress.svg)",
        "",
        f"**Gesamt:** {completed}/{all_steps} Hauptschritte ({100 * completed // all_steps} %) · "
        f"**Unteraufgaben:** {sub_done}/{len(sub_ids)} · **G−1:** NICHT FREIGEGEBEN.",
        "",
        "## Bedienung und verbindliche Regeln",
        "",
        "- `[ ]` = offen, `[x]` = mit Nachweis abgeschlossen; GitHub zeigt die Kästchen an.",
        "- **Autoritative Quelle:** [`governance/route.json`](../governance/route.json), "
        "nicht die Markdown-Datei. Nur dort Status und commitgebundene Evidenz ändern.",
        "- **Abhaken:** `progress_overrides.ID = VERIFIED` und "
        "`evidence_by_step.ID = {source_sha, test_run, result: PASS}` "
        "hinterlegen; anschließend `python3 scripts/render_todo.py` ausführen.",
        "- GitHub-Dateiansicht: Kästchen zeigen den Status, Änderungen erfolgen über einen "
        "prüfbaren Datei-/Pull-Request-Patch. Bloßes Anklicken ist kein Nachweis.",
        "- **NO-OP** nur mit dokumentierter Begründung und gültiger Evidenz "
        "im Schrittbericht, niemals durch blindes Abhaken.",
        "- **PATCH-KARTE:** `ID | GRUND | EFFEKT | UMFANG | M/S/K | RISIKO | "
        "DATEIEN | CHECK | SHA | STATUS`; vor Umsetzung Scope und Budget prüfen.",
        "- Für eine neue Aufgabe werden **Grund, Effekt und Dateiumfang erst bei "
        "READY** konkretisiert. Keine 112 spekulativen Dateilisten pflegen.",
        "- **Testregel:** direkte Prüfung je Patch, Negativtest bei Risiko; "
        "breite Integrationsprüfungen an Gates und vor Release.",
        "- **Synchronisierung:** `python3 scripts/render_todo.py --check` validiert "
        "Status, Checkliste und Grafik ohne Änderungen.",
        "",
        "## Nummerierte Checkliste",
        "",
    ]
    for gate_id, (done, total) in totals.items():
        label = GATE_LABELS[gate_id]
        result.append(f"<details{' open' if gate_id == 'G-1' else ''}>")
        result.append(f"<summary><strong>{gate_id} – {label}</strong> "
                      f"({done}/{total}; {100 * done // total} %)</summary>")
        result.append("")
        for sid, item in route["steps"].items():
            if item["gate"] != gate_id:
                continue
            checked = "x" if actual[sid] else " "
            result.append(f"- [{checked}] **{sid}** {item['title']} "
                          f"`{item['patch']}` · `{item['risk']}`")
            for sub in item.get("substeps", []):
                marker = "x" if actual[sub["id"]] else " "
                result.append(f"  - [{marker}] `{sub['id']}` {sub['title']}")
        result.extend(["", "</details>", ""])
    result.extend(["## Nächster Schritt und Warteschlange", ""])
    queued = [(sid, item) for sid, item in route["steps"].items() if not actual[sid]][:3]
    for index, (sid, item) in enumerate(queued):
        label = "JETZT (Planung)" if index == 0 else "DANACH (nicht freigegeben)"
        result.append(f"{index + 1}. **{sid} – {item['title']}** · {label}")
    result.extend([
        "", "**Patch-Karte beim Start ausfüllen:**",
        "", "```text",
        "ID:     [aus der Aufgabenroute]    GRUND: [max. 1 Satz]",
        "EFFEKT: [messbares Ergebnis]   UMFANG: [konkrete Dateien]",
        "PATCH:  [M/S/K]                RISIKO: [R1/R2]",
        "CHECK:  [betroffene Tests]      SHA: [Basis und Nachweis]",
        "```", "",
        "*Diese Datei und die SVG-Grafik sind aus `governance/route.json` erzeugt.*", "",
    ])
    return "\n".join(result)


def make_svg(totals):
    width, height, left, length = 930, 605, 330, 520
    completed = sum(x for x, _ in totals.values())
    total = sum(y for _, y in totals.values())
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" '
        f'aria-label="TOOL ZENTRALE Fortschritt {completed} von {total}">',
        '<title>TOOL_ZENTRALE – Entwicklungsfortschritt V3.2</title>',
        f'<desc>{completed} von {total} Hauptschritten bestätigt. '
        'Nur VERIFIED mit Nachweis zählt.</desc>',
        '<rect width="930" height="605" rx="18" fill="#102137"/>',
        '<text x="27" y="43" font-size="25" font-weight="700" '
        'font-family="Arial,sans-serif" fill="#F6FAFC">ENTWICKLUNGSFORTSCHRITT</text>',
        f'<text x="27" y="74" font-size="16" font-family="Arial,sans-serif" '
        f'fill="#D0E3E9">Gesamt {completed}/{total} ({100 * completed // total} %)' 
        ' – nur belegte Abschlüsse</text>',
    ]
    for position, (gate, (done, count)) in enumerate(totals.items()):
        y = 112 + position * 35
        name = escape(GATE_LABELS[gate])
        filled = round(length * done / count)
        lines.append(f'<text x="28" y="{y + 14}" fill="#EBF6FA" font-size="13" '
                     f'font-family="Arial,sans-serif">{gate} · {name}</text>')
        lines.append(f'<rect x="{left}" y="{y}" width="{length}" height="17" rx="8" '
                     'fill="#34465B"/>')
        if filled:
            lines.append(f'<rect x="{left}" y="{y}" width="{filled}" height="17" rx="8" '
                         'fill="#33D8B3"/>')
        lines.append(f'<text x="866" y="{y + 14}" fill="#EBF6FA" font-size="13" '
                     f'font-family="Arial,sans-serif">{done}/{count}</text>')
    lines.extend(['<text x="28" y="580" font-size="13" fill="#AFCCD5" '
                  'font-family="Arial,sans-serif">Statusquelle: governance/route.json · G−1 offen</text>',
                  '</svg>', ''])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Nur erzeugte Dateien vergleichen")
    args = parser.parse_args()
    route = load_route(ROUTE)
    actual = resolve(route)
    totals = stats(route, actual)
    targets = ((TODO, make_markdown(route, actual, totals)),
               (GRAPH, make_svg(totals)))
    for path, rendered in targets:
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != rendered:
                raise SystemExit(f"STALE: {path.relative_to(ROOT)} – Generator ausführen")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(rendered, encoding="utf-8")
    done = sum(value for value in actual.values() if value)
    print(f"TODO {'CHECK PASS' if args.check else 'GENERATED'}: {done} bestätigte "
          f"(Haupt-/Unter-)Schritte, {len(route['steps'])} Hauptschritte, "
          f"{len(route['gates'])} Gates")


if __name__ == "__main__":
    main()
