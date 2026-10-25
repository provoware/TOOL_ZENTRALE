# Iteration: Regression und selbstständig arbeitende Hilfen

Basis: GitHub PR #2, Commit `8755c005532a1a539bfc1a31883dee6c6c67359e`.
Vorheriger GitHub-Pflichtlauf #9 erfolgreich. Lokaler HEAD ist weiterhin der
ältere Ausgangscommit; bereits veröffentlichte lokale Änderungen wurden
anhand des Inhaltsschnappschusses bewahrt. Keine fremden Patches übergangen.

## Analyse und Entscheidung

Der bestehende Vertrag plant lernende Regression und nennt bereits einen
YAML-Katalog. Ein zweiter Fehlerkatalog oder ein Hintergrunddienst würde
Pflege und Betrieb erschweren. Deshalb eine Quelle, eine daraus erzeugte
Infodatei und ein gemeinsamer Einstieg für lokal und CI, ohne Zusatzpakete.
Die lesende Einzelaufgabe eines Subagenten bestätigte diesen Integrationsweg.
Q001 wird zuerst konkret bearbeitet: reale Prüfergebnisse an Inhalte und
Python-Kontext binden. Q002 und Q003 bleiben als nächste bedingte Arbeiten.

## Umgesetzter Umfang

- Acht registrierte Entwicklungs-Fehlerfamilien mit Belegklasse, Ursache,
  Triggern, vorhandenen Schutztests und verständlicher nächster Hilfe.
- Prüfhilfe validiert Test-IDs, Informationsstände und Testergebnisse.
  Unbekannter Impact erweitert die Suite; Fehler und Timeouts verhindern PASS.
- --refresh pflegt nur fünf bekannte abgeleitete Dateien, anschließend Prüfung.
- Lokale Berichte binden Vorher-/Nachher-Inhalt, Plan, Register, Python,
  Source-SHA und ausgeführte Prüfungen. --verify-report erkennt veraltete Läufe.
- Fehlgeschlagene Prüfungen werden als lokale Lernkandidaten registriert;
  derselbe Kandidat erhält einen Wiederholungszähler. Keine Rohfehlermeldungen
  in Kandidaten, keine automatische Beförderung zur bestätigten Ursache.
- Push/PR/manueller Workflow führen die Hilfe aus. Bericht als CI-Artefakt,
  14 Tage Aufbewahrung; Kandidaten bleiben außerhalb des Git-Bestands.

## Grenzen

Lernen bedeutet dokumentierte Anpassung belegter Regeln und Testzuordnungen,
kein automatisch trainiertes Modell. Lokale Zähler bleiben nur erhalten,
solange der lokale Bericht existiert; kein globaler oder ewiger Fehlerspeicher.
Suitefehler werden als Suite-Kandidat erfasst; Konsole und gezielter Folgelauf
liefern den konkreten Testfall. Neue Fehlerfamilien benötigen Ursachenprüfung.
Berichte sind nicht signiert und ersetzen keine unabhängige Freigabe.
Die bestehende Route akzeptiert weiterhin einfache Evidenzobjekte; Q001 ist
noch nicht vollständig abgeschlossen. Kein VERIFIED und keine Gatefreigabe
wurden allein durch neue Berichte angehoben. Keine Produkt-/Browserprüfung.

## Reproduktion und Rückweg

`python3 scripts/assist.py --refresh` und danach
`python3 scripts/assist.py --verify-report` müssen erfolgreich sein.
Gezielte Auswahl: `python3 scripts/assist.py --changed scripts/render_todo.py`.
Unbekannte Pfade: vollständige Entwicklungssuite als konservativer Fallback.
Direkte Tests: `python3 -m unittest discover -s scripts -p 'test_*.py'`.

Code in getrennten Verantwortlichkeiten: Register/Infogenerator, Evidenz,
Prüforchestrierung/Tests. Reine Registerdaten und generierte Ansichten sind
als Daten-/Generierungsausnahme EX-REG-01 gekennzeichnet; kein Quellcodebudget
wird damit aufgehoben. Rückweg: nur eigene neue Dateien/Hunks anhand des
Basisstands entfernen und abgeleitete Ansichten neu erzeugen. Keine Nutzdaten
oder externen Repositories wurden geändert.

## Review und Nachbesserungen

Der unabhängige lesende Review fand vier konkrete Lücken: ausgeschlossene
Ansichten fehlten im Evidenzfingerprint, Pflichtchecks waren nicht vollständig
gebunden, frühe Fehler schrieben keinen neuen FAIL-Bericht, beschädigte
Kandidaten konnten den Abschluss blockieren. Alle vier sind korrigiert.
Zusätzliche Negativtests prüfen Ausgabedrift, fehlende Pflichtchecks,
frühen Abbruch und beschädigte Historie. Kandidaten bleiben über erfolgreiche
Folgeläufe erhalten, begrenzt auf 100 Einträge; keine Endlossammlung.

## Abschließende Nachweise

28 Tests bestanden; gezielte Auswahl (zehn Routen-Schutzfälle) erfolgreich.
Echte Driftproben an README, Hashregister und Kurzstatus wurden als STALE
abgelehnt und anschließend bytegenau zurückgenommen. Fehlende Pflichtchecks,
Timeouteffekt, früher Abbruch und beschädigte Berichte sind negativ geprüft.
Codebudgets je Paket eingehalten: Orchestrierung/Tests unter 12000 Zeichen
und 250 +/- Zeilen; Evidenz/Tests sowie Registergenerator ebenfalls darunter.
