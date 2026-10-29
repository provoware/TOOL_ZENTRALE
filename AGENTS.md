# TOOL_ZENTRALE – Arbeitsvertrag

1. Jede Iteration beginnt mit MAIN-VORPRÜFUNG, erst danach mit Planung.
   Read-only Startprüfung: `python3 scripts/assist.py --main-preflight` auf sauberem
   lokalen main; BLOCKED bedeutet STOP, auch bei API-/Netzausfall.
   Führendes Remote: https://github.com/provoware/TOOL_ZENTRALE.
   Lokale Restarbeit, unveröffentlichte Commits und offene PRs gegen GitHub-Main
   abgleichen. Zusammenhängende, geprüfte und autorisierte übertragbare Teile
   zuerst integrieren; erwarteten Head-SHA und gültige CI verlangen.
   Danach Main-Baum, Main-CI und lokalen Stand prüfen; bei nichts Übertragbarem
   NO-OP dokumentieren. Ergebnis: `work/iteration/start.json`.
   Blockierte Teile begründet registrieren; ungeprüfte Main-Basis sperrt den
   Start eines neuen Entwicklungsplans. Bei fehlendem Zugriff „nur lokal“ melden.
   Vor Übergabe geprüfte Änderungen synchronisieren; beauftragte Merges und
   anschließende Main-Prüfung abschließen. Keine Hintergrundsynchronisation.
   Nutzerauftrag/fremde Änderungen beachten; Referenzrepos nur lesen.
   Basis-SHA, Planrevision, Scope und Dateihashes vor jedem Patch erfassen.
2. Quellen: `blueprint/architecture.yaml` = Sollstruktur;
   `governance/route.json` = Aufgaben, Status, Abweichungswarteschlange;
   Git = Ist-Inhalt; Testläufe = Nachweise. Ansichten nie manuell pflegen.
3. Ein Writer je Dateiscope. Subagent erhält genau eine Aufgabe, Trigger,
   erlaubte Pfade, Basis, Abnahme und Ergebnisformat. Prüfer schreiben nicht.
4. Erst nach abgeschlossener Main-Vorprüfung drei logische Schritte planen.
   Registrierte Blocker zuerst bearbeiten; Folgeschritte sind bedingt,
   keine Freigabe. Blocker zuerst. Abweichungen begründet in `iteration_queue`
   registrieren und vor regulären Aufgaben der nächsten Iteration abarbeiten.
   Bei Daten-/Sicherheitsgefahr laufende Arbeit sofort sicher anhalten.
5. Kleine reversible Patches: M 1500 Zeichen/30 Zeilen/2 Dateien;
   S 6000/120/3; K 12000/250/5, hinzugefügt plus entfernt.
   Ausnahme vorher begründen, messen und Rückweg dokumentieren.
6. VERIFIED nur über `python3 scripts/complete_step.py ID` nach aktuellem
   vollständigem Prüflauf; Scope, Testbytes, Plan und Toolchain bleiben gebunden.
   Gate CHECKED ist keine Freigabe. APPROVED erfordert gebundene menschliche
   Entscheidungsakte und freigegebenes Vorgängergate.
   Vorher Basis/Scope/Abhängigkeiten prüfen; nachher direkte Tests und bei
   Risiko Negativfälle. Kein VERIFIED ohne passende Evidenz; kein Gate-PASS
   aus Modelltests. G-1/G0 bleiben ohne dokumentierte Abnahme offen.
7. Regressionsquelle: `governance/regressions.yaml`; Infodatei erzeugen,
   nicht separat pflegen. `python3 scripts/assist.py --refresh` aktualisiert
   Ansichten und prüft selbstständig. Berichte/Lernkandidaten bleiben in
   `work/regression/`; Ursache und Negativtest vor Regelübernahme prüfen.
   Keine automatische Quellcodereparatur oder Gatefreigabe.
   Trigger: nach Änderungen `python3 scripts/render_todo.py`, dann
   `python3 scripts/project_state.py`. Vor Übergabe beide mit `--check`
   und `python3 -m unittest discover -s scripts -p 'test_*.py'` ausführen.
8. Laien zuerst: kurze deutsche Statusmeldungen, eindeutige Hauptaktion,
   verständliche Fehlerhilfe, geschützte Entwürfe, Tastatur und Zoom.
   WCAG 2.2 AA ist Ziel, bis reale Prüfungen es belegen.
9. Keine Geheimnisse/Nutzdaten in Git, keine freie Fremdcodeausführung,
   keine Shellstrings aus Eingaben. Laufzeitdaten außerhalb des Repositorys.
10. Ergebnis: Ziel, geänderte Pfade, Umfang, Checks mit Ergebnis, Risiken,
    Rückweg und drei bedingte Folgeschritte. Details: `docs/ARBEITSWEISE.md`
    und `docs/ENTWICKLUNGSSTANDARD.md`. Produkt-/Merge-/Deploymentfreigabe
    niemals aus einer bloßen Plan- oder Generatorprüfung ableiten.


## Draft-PR-Schuldenbremse und Qualitätsvorrang (29.10.2026)

Die GitHub-PR-Bestandsaufnahme gehört **vor die Planung neuer optionaler Arbeiten**. Für offene Draft-PRs je Repository gilt: **0–5 = normal**, **6–10 = P1-Abarbeitung**, **ab 11 = P0-Abarbeitung**. Zielbestand: **höchstens fünf Drafts**. Maßgeblich ist die live über GitHub ermittelte Anzahl; bei API-Fehler/fehlendem Zugang lautet der Status UNBEKANNT, niemals 0.

- Bei Überschreiten der Grenze ist die **bestehende priorisierte To-do/Next Queue** maßgeblich: zuerst offene Arbeiten nach tatsächlichem Nutzen, Risiko, Alter, Blockern und Abhängigkeiten abarbeiten. Neue optionale Features zunächst nur dort vormerken, **keine zusätzlichen Drafts auf Vorrat**.
- Für jeden Draft den aktuellen HEAD, Zweck, Review, CI, Mergekonflikte, Sicherheitswirkung und Beziehungen (BLOCKS, REQUIRES, DUPLICATE, SUPERSEDES) erfassen. Klassifizieren: MERGE-BEREIT, KORREKTUR, BLOCKIERT, DUPLIKAT, ÜBERHOLT, GEPLANT.
- **Qualität vor Menge:** Fertigstellen mit minimaler Korrektur und passenden Negativ-/Regressionstests; Review, aktuelle CI, Schutzregeln und Abhängigkeiten vor Merge prüfen. Grün auf einem alten Commit ist kein Integrationsnachweis; grün auf PR-HEAD ersetzt nicht die Main-Nachkontrolle.
- **Nichts blind schließen oder mergen.** Duplikate/überholte Drafts nur mit Begründung, Quellen-/Nachfolgerverweis und gesichertem Arbeitsinhalt schließen. Unfertige Originalarbeit bleibt erhalten. Von Draft auf reviewbereit nur nach nachweislich erfüllten Projekt-Gates wechseln.
- Nach jedem Abschluss erneut zählen und in der To-do-Aufgabe dokumentieren: **vorher → nachher**, getesteter HEAD, Ergebnis, offene Blocker, nächste konkrete Handlung. Erst bei ≤5 Drafts wieder regulär optionale neue PRs priorisieren.
- **Ausnahmen:** P0-Sicherheits- und Datenintegritätsprobleme, zwingende Release-Gates und ein bereits freigegebener eingefrorener Plan haben Vorrang. Diese Regel **hebt keinen Freeze und keine Release-/Merge-Freigabe** auf. Bestehende kanonische/generierte To-do-Ansichten nicht manuell umschreiben; vorhandenen Generator bzw. Aufgaben-Workflow verwenden.

Zugehörige priorisierte GitHub-Aufgabe: https://github.com/provoware/TOOL_ZENTRALE/issues/8.
