# TOOL_ZENTRALE – Arbeitsvertrag

1. Führendes Remote: https://github.com/provoware/TOOL_ZENTRALE.
   Vor Änderungen Remote-Stand prüfen; bei Übergabe geprüfte Änderungen auf
   Arbeitsbranch synchronisieren und PR verlinken. Bei fehlendem Zugriff
   ausdrücklich „nur lokal“ melden; keine dauernde Hintergrundsynchronisation.
   Nutzerauftrag und vorhandene Änderungen prüfen; Referenzrepos nur lesen.
   Basis-SHA, Planrevision, Scope und Dateihashes vor jedem Patch erfassen.
2. Quellen: `blueprint/architecture.yaml` = Sollstruktur;
   `governance/route.json` = Aufgaben, Status, Abweichungswarteschlange;
   Git = Ist-Inhalt; Testläufe = Nachweise. Ansichten nie manuell pflegen.
3. Ein Writer je Dateiscope. Subagent erhält genau eine Aufgabe, Trigger,
   erlaubte Pfade, Basis, Abnahme und Ergebnisformat. Prüfer schreiben nicht.
4. Vor Beginn drei logische Schritte voraussehen; Folgeschritte sind bedingt,
   keine Freigabe. Blocker zuerst. Abweichungen begründet in `iteration_queue`
   registrieren und vor regulären Aufgaben der nächsten Iteration abarbeiten.
   Bei Daten-/Sicherheitsgefahr laufende Arbeit sofort sicher anhalten.
5. Kleine reversible Patches: M 1500 Zeichen/30 Zeilen/2 Dateien;
   S 6000/120/3; K 12000/250/5, hinzugefügt plus entfernt.
   Ausnahme vorher begründen, messen und Rückweg dokumentieren.
6. Vorher Basis/Scope/Abhängigkeiten prüfen; nachher direkte Tests und bei
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
