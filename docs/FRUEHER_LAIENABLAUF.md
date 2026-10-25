# Verbindliche Priorität: erster nutzbarer Laienablauf

Diese Änderung des Entwicklungsplans ergänzt Masterplan 3.1 und Delta 3.2.
Stabile IDs bleiben erhalten. Maßgeblich sind explizite Abhängigkeiten und
Gate-Mitglieder in route.json, keine aufsteigend sortierten P-Nummern.

## Frühes Ergebnis

Nach geprüfter Shell G4 folgt in G5 unmittelbar:
P047 Songmodell → P048 Bibliothek → P049 Editor → P050 Wiederherstellung
→ P056 Speichern, Schließen, Wiederöffnen und Export als echte Browserreise.
Profile, Charaktere, Buch und Wiki sind dafür keine Voraussetzungen mehr.
G5 wird erst nach tatsächlicher Funktions-/UX-Prüfung und dokumentierter
Freigabe als APPROVED behandelt. Diese Planänderung gibt G5 nicht frei.

Danach beginnt G6 mit P063: Projekt finden und Importvorschau verstehen.
Erst anschließend folgen Aufgaben/Kalender/Links, Profile/Charaktere und die
zusätzlichen Schreibwerkzeuge. P064 prüft das vollständige G6-Bündel.
Die verlagerten Aufgaben bleiben registriert und gehen nicht verloren.
Gate-Mitglieder sind vollständig in route.json aufgeführt, G5 hat fünf
Hauptschritte, G6 sechzehn. „first/last“ kennzeichnet Reihenfolge, keinen Zahlenbereich.

## Abnahme mit Laien

1. Eine sichtbare Hauptaktion „Neuen Song schreiben“ wählen; Titel und Text
   eingeben. Hilfe erklärt die Aktion ohne technische Begriffe.
2. Speichern auslösen. Erst nach dauerhaftem Speichern erscheint „Gespeichert“;
   bei Fehler bleibt der Entwurf erhalten, mit verständlichem Korrekturweg.
3. Editor schließen, Song über Bibliothek wieder öffnen. Titel und Text sind
   identisch. Abbruch, Doppelklick, Serverunterbrechung und Versionskonflikt
   dürfen keinen stillen Verlust verursachen.

Pflichtproben: Tastatur, sichtbarer Fokus, 200 % Textvergrößerung, 400 % Zoom,
klare Speicher-/Fehleranzeige und praktische Aufgabe mit echten Erstnutzern.
Automatische Browserreise ergänzt die manuelle Probe; WCAG bleibt bis zur
realen Prüfung Ziel. Aktuell existiert keine Oberfläche: NOT_TESTED.

## Kontrollierte Grenzen

API-, Speicher- und E2E-Pfade wurden bei den betroffenen Gates gezielt ergänzt.
Kein allgemeiner app/-Schreibfreibrief: jeder Produktpatch benötigt zusätzlich
seinen konkreten Schritt-Scope und reale Tests. G-1 und G0 bleiben offen.
