# Reproduzierbare Entwicklung für Laien

Diese Ergänzung setzt den aktuellen Auftrag zur Entwicklungsbasis um.
Sie ergänzt V3.2; bei Widersprüchen gelten hier die aktuellen Arbeitsregeln.
Sie erteilt keine G-1-/G0-Abnahme. Bestehende Produktplanung bleibt Entwurf.

## Eine Information, eine Quelle

Route: Aufgabenstatus und `iteration_queue`. Blueprint: geplante Komponenten.
Git-Inhalt: vorhandene Dateien. `governance/file_state.json`: erzeugte
Inhaltsschnappschüsse, keine zusätzliche manuelle Statusverwaltung.
`docs/STATUS_KURZ.md`, TODO und SVG: ausschließlich erzeugte Anzeigen.
Dateistatus `PRESENT_HASHED` bedeutet vorhanden und gehasht, niemals getestet.
Sollstatus VIRTUAL und Teststatus VERIFIED bleiben getrennte Dimensionen.

## Iteration und Abweichungen

1. Basis, Scope, Ziel und direkte Prüfungen fixieren; drei logische Schritte
   mit Vorbedingungen anzeigen. Nur den aktuellen Auftrag ausführen.
2. Änderung klein halten, direkt prüfen, Ergebnis und Grenzen dokumentieren.
3. Vor Übergabe Ansichten aktualisieren und nächste drei Schritte neu berechnen.

Eine notwendige Abweichung erhält in `route.json.iteration_queue` eine stabile
ID, title, reason, status und depends_on. Offene Einträge stehen in dokumentierter
Array-Reihenfolge vor der regulären Route. Abhängigkeiten bleiben verbindlich.
Keine automatische Umplanung nach vermeintlicher KI-Optimalität; Nutzen,
Entblockung und Aufwand müssen im reason nachvollziehbar sein.
Eine blockierte vorrangige Abweichung wird zuerst geklärt; kein stilles Überspringen.
Die Vorschau simuliert den Erfolg ihrer Vorgänger und stellt keine READY-Zusage dar.
Bei Sicherheits-/Datengefahr wird sofort angehalten; sonst erfolgt die Korrektur
als erste Arbeit der nächsten Iteration. Keine endlosen Reparaturschleifen:
nach zwei erfolglosen Hypothesen Ursache und sicheren nächsten Schritt berichten.

## Aktualisierungstrigger

| Ereignis | Aktion | Nachweis |
|---|---|---|
| Route, Status, Evidenz oder Warteschlange verändert | TODO und SVG neu erzeugen | render_todo.py --check |
| Beliebige versionierbare Projektdatei verändert, hinzugefügt oder entfernt | Kurzstatus und Hashregister neu erzeugen | project_state.py --check |
| Generator oder Statuslogik verändert | gezielte Unit-/Negativtests | Testausgabe |
| UX, Daten- oder Sicherheitsvertrag verändert | passende manuelle/negative Prüfungen planen und durchführen, sobald Oberfläche existiert | konkreter Lauf oder NOT_TESTED |
| Pull Request oder Push | Pflichtworkflow prüft Ansichten und Tests | CI-Lauf |

Lokal: `python3 scripts/render_todo.py`, dann `python3 scripts/project_state.py`.
Prüfen: beide mit `--check`; Tests gemäß AGENTS.md.
Keine laufende Dateibeobachtung und kein Hintergrunddienst: Trigger wirken beim
expliziten Aktualisieren und im CI. Ein veralteter Stand blockiert den Check.
Das Register schließt sich selbst und temporäre/ignorierte Dateien aus;
Änderungen seiner Bytes werden durch Vergleich mit Neuberechnung erkannt.

## Subagenten mit Einzelaufgaben

Auftrag: `ID | Ziel | Basis-SHA | Trigger | erlaubte Pfade | verbotene Pfade |
Abhängigkeiten | Abnahme | Prüfungen | Rückweg`.
Ergebnis: `ID | Befund/Änderung | Beleg | PASS/FAIL/NOT_TESTED | Restrisiko |
Empfehlung`. Nur unabhängige Aufgaben parallelisieren; gleiche Dateien haben
immer genau einen Writer. Integration und Schlussprüfung liegen beim Hauptagenten.
Subagenten müssen nicht für triviale Einzeländerungen gestartet werden.

## Einheitliche Begriffe und Grenzen

Schrittstatus verwendet die vom Generator unterstützten Werte PLANNED, READY,
PATCHED, VERIFIED, BLOCKED, DEPRECATED. ACTIVE/DONE/FAILED aus älteren
Prosatexten sind keine zusätzlich gültigen Route-Werte.
`governance/regressions.yaml` bleibt der vorgesehene Fehlerkatalogpfad;
ältere Erwähnungen von regressions.json sind überholt. Python-Dateien ab
250 Zeilen auf Verantwortlichkeit prüfen; keine künstliche Zerlegung.
M/S/K-Grenzen gelten gleichzeitig; bei echter Unteilbarkeit dokumentierte Ausnahme.
Keine Scheinprozente: Fortschritt zählt belegte Hauptschritte und ist weder
Zeitprognose noch Funktionsabdeckung. Im Planstand 0/112 bleibt ehrlich 0 %.

## Laiengerechte Statuskarte

Immer in dieser Reihenfolge: Was ist fertig? Was fehlt? Was blockiert?
Was passiert jetzt? Was folgt danach unter welchen Bedingungen?
Technische Belege sind verlinkbar, aber nicht Voraussetzung zum Verstehen.
Erfolg, Speichern, Prüfen und Freigabe sind unterschiedliche Aussagen.

## Automatische Hilfe und lernende Regression

Ein Aufruf `python3 scripts/assist.py` verbindet Registervalidierung,
Informationsprüfung, risikoabhängige Testauswahl und Laufbericht.
`--refresh` regeneriert ausschließlich REGRESSION_INFO.md, TODO, SVG,
Kurzstatus und Hashregister. Bei unbekanntem Impact läuft die vollständige
vorhandene Entwicklungssuite; kein doppelter Volltest im Pflichtworkflow.
Push, PR und manueller Workflowstart führen dieselbe Hilfe automatisch aus.

`governance/regressions.yaml` ist die einzige Fehlerfamilienquelle, bewusst
JSON-kompatibles YAML ohne neue Paketabhängigkeit. Die Infodatei wird erzeugt.
Berichte enthalten Source-SHA, Inhaltsschnappschuss, Plan-/Registerhash,
Python-Kontext, ausgeführte Check-IDs und tatsächliche Resultate.
Ein Lauf mit Inhaltsänderung während der Prüfung ist ungültig.
Lokale Beobachtungen werden als Kandidaten gezählt; verifizierte Ursachen
und Negativtests werden anschließend gezielt in die führende Quelle übernommen.
Es gibt keinen selbstständigen Quellcode-Writer, Merge oder privaten Datenzugriff.
Q001 ist damit begonnen; die verpflichtende Reportprüfung im Route-Abschluss
und die Gatebindung bleiben offen und werden nicht automatisch abgehakt.
