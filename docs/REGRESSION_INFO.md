# Lernende Regression und automatische Hilfe

**Start:** `python3 scripts/assist.py` – prüft selbstständig und erklärt das Ergebnis.
**Ansichten aktualisieren:** `python3 scripts/assist.py --refresh`.
Mit `--changed scripts/render_todo.py` gezielt prüfen; unbekannte Pfade
oder keine Pfadangabe erweitern auf alle vorhandenen Tests.

## Was automatisch geschieht

1. Register, Testzuordnung und Informationsdateien prüfen.
2. Passende Tests ausführen; jeder Fehler, Timeout oder Inhaltswechsel verhindert PASS.
3. Bericht und Lernkandidaten unter `work/regression/latest.json` speichern.
4. Die drei nächsten bedingten Schritte aus der Route anzeigen.

Push, Pull Request und manueller Workflowstart lösen dieselbe Hilfe in CI aus.
Es läuft kein dauernder Hintergrunddienst. --refresh verändert ausschließlich
die fünf bekannten abgeleiteten Ansichten, niemals Produktcode oder Nutzdaten.

## Wie das System lernt

Ein fehlgeschlagener Lauf erzeugt automatisch Kandidaten mit Prüf-ID und
stabiler Signatur (Test-ID bei gezielter Auswahl, Suite-ID im Gesamtlauf).
Wiederholungen werden gezählt, solange der lokale Bericht
vorliegt (höchstens 100 Kandidaten, auch über erfolgreiche Folgeläufe hinweg).
Es werden keine Rohfehlertexte oder Nutzinhalte in Git gespeichert.
Ursache reproduzieren, Negativtest ergänzen, Trigger und Schutzregel prüfen,
dann das führende Register gezielt erweitern. Keine ungeprüfte Selbstreparatur.
Der Bericht ist lokaler Prüfbeleg, keine signierte Freigabe. Alte Ergebnisse
sind bei verändertem Dateiinhalt, Plan oder Python-Kontext STALE.

Prüfen: `python3 scripts/assist.py --verify-report` (führt keine Tests erneut aus).
Ein frischer Bericht mit FAIL bleibt FAIL. Ein gültiger Bericht hebt weder
Schrittstatus noch Gatefreigaben automatisch an; Q001 bleibt bis zur
verbindlichen Einbindung in die Schritt-/Gateprüfung offen.

## Registrierte Fehlerfamilien

| ID | Klasse | Problem | Sichere nächste Hilfe |
|---|---|---|---|
| RG001 | CONFIRMED | Unbelegter Schrittabschluss | Voraussetzungen und echte Evidenz korrigieren |
| RG002 | PREVENTIVE | Defekter Abhängigkeitsgraph | Fehlerhafte Route gezielt korrigieren |
| RG003 | CONFIRMED | Blockade oder Abweichung übergangen | Erste offene Abweichung auflösen |
| RG004 | PREVENTIVE | Veraltete Dateiinformation | Hilfe mit --refresh starten |
| RG005 | PREVENTIVE | Symlink im registrierten Scope | Verknüpfung und Scope prüfen |
| RG006 | PREVENTIVE | Veralteter oder fehlgeschlagener Laufbericht | Prüfhilfe erneut ausführen; keine Gatefreigabe ableiten |
| RG007 | PREVENTIVE | Unbekannte Testzuordnung | Zuordnung ergänzen und Negativtest behalten |
| RG008 | PREVENTIVE | Wiederholungsfehler ohne Lernbeleg | Minimalfall reproduzieren und Register erweitern |

## Pflege und Grenzen

Quelle: `governance/regressions.yaml` (JSON-kompatibles YAML, ohne Zusatzpaket).
Diese Infodatei wird daraus erzeugt. CONFIRMED bezieht sich auf belegte
Entwicklungsfehler, PREVENTIVE auf Schutzfälle; keine behaupteten Produktfehler.
Die Hilfe prüft Entwicklungsartefakte. Browser, Datenbank, Barrierefreiheit
und Offlineinstallation bleiben bis zur vorhandenen Anwendung NOT_TESTED.
