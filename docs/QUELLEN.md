# TOOL_ZENTRALE – Forschungs- und Referenzquellen

Abruf-/Planstand: **25. Oktober 2026**. Die folgenden Quellen werden nach
Prüfung des Originaldokuments zitiert; einzelne Projektempfehlungen sind
aus ihnen **abgeleitet**, nicht wörtliche Normforderungen.

## 01. Vorhandener Projektstand

- Ziel: https://github.com/provoware/TOOL_ZENTRALE
  - bei Bestandsaufnahme nur README.md;
  - main-Basis: 6e9f8638f7a7b6334a23d51988d0e3ef9d82a37c;
  - öffentlich; keine Repository-Rulesets zurückgemeldet.
- Referenzanwendung: https://github.com/provoware/TOOL_2026_Multi
  - zuvor geprüfte main-Referenz:
    096dc03ae362eed8141b0dbc0c8e91ab0b8daa2d;
  - Python/PySide6; Fachmodule nur nach Qt-freier Eignungsprüfung übernehmen.
- Architektur-/Fehler-/Datenideen als Lesereferenzen:
  - https://github.com/provoware/DATENBANKTOOL
  - https://github.com/provoware/PROVOWARE
  - https://github.com/provoware/PROVOWARE-LAIENTOOL
  - https://github.com/provoware/DB_TOOL_2026
  - https://github.com/provoware/PROVOWARE_MASTER_BOOK_2026
  - https://github.com/provoware/PROVOWARE_VIDEO_AUTOMATION_2026
  - https://github.com/provoware/DUPLIKATE-FINDER2026
  - https://github.com/provoware/Schnellprompter-Tool-2026

## 02. W3C/WAI – zwingend für UX-Entscheidungen

| Thema | Primärquelle | Planableitung |
|---|---|---|
| WCAG 2.2 | https://www.w3.org/TR/WCAG22/ | Zielstandard Level AA, später nachweisen |
| Textkontrast | https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html | 4,5:1 normal; 3:1 groß |
| Nichttextkontrast | https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html | 3:1 für erforderliche UI-Information |
| Reflow | https://www.w3.org/WAI/WCAG22/Understanding/reflow.html | 320-CSS-px-Ansicht |
| Textvergrößerung | https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html | 200 % ohne Verlust |
| Zielgrößen | https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html | 24×24 px Mindestregel mit Ausnahmen |
| Sehschwäche | https://www.w3.org/TR/low-vision-needs/ | unterschiedliche Kontrast-/Helligkeitsprofile |
| Verständlichkeit | https://www.w3.org/TR/coga-usable/design_guide.html | Schlüsselaktion sichtbar; klare Sprache |
| Tastatur | https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/ | vorhersehbare Fokusführung |
| Dialoge | https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/ | Fokus hinein und zurück, Escape |
| Formularlabels | https://www.w3.org/WAI/tutorials/forms/labels/ | sichtbare Namen, korrekte label-Zuordnung |
| Echte Nutzungstests | https://www.w3.org/WAI/test-evaluate/involving-users/ | automatische + manuelle + Nutzerprüfung |

## 03. Entwicklung, Qualität, Sicherheit und Daten

- NIST Secure Software Development Framework SP 800-218:
  https://csrc.nist.gov/projects/ssdf
- OWASP Application Security Verification Standard 5.0.0:
  https://asvs.owasp.org/
- GitHub Repository Rulesets:
  https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets
- GitHub Actions Workflow Syntax / Pfadfilter:
  https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax
- SQLite Online Backup API:
  https://www.sqlite.org/backup.html
- JSON Schema Draft 2020-12:
  https://json-schema.org/draft/2020-12
- OpenAPI-Spezifikation (verfügbare Versionen):
  https://spec.openapis.org/oas/
- Playwright Accessibility Testing:
  https://playwright.dev/docs/accessibility-testing

## 04. Sicherheit gegen Fehlinterpretation

- „WCAG-AA geplant“ ist keine bestandene Konformitätsprüfung.
- Die W3C-24-px-Anforderung für Ziele hat normative Ausnahmen; die intern
  empfohlenen 44 px für Hauptaktionen sind eine zusätzliche UX-Vorgabe.
- Ein formal gültiger Blueprint belegt weder Browserbedienung noch
  transaktionale Datenintegrität. Echter Vertikaldurchstich folgt später.
- Die empfohlenen Architektur- und Patchbudgets sind unsere
  Projektentscheidungen, keine angeblichen externen Normforderungen.
- Für Quellen aus fremden Repositories vor tatsächlicher Quellcodeübernahme
  Commits, Lizenz und jeweilige Evidenz neu prüfen.
