# TOOL_ZENTRALE – UX, Sehschwäche und Barrierefreiheit

Stand: 25.10.2026 · Version 1.0 · **Planungsstandard, keine Konformitätserklärung**

## 01. Produktziel und Maßstab

TOOL_ZENTRALE ist eine lokal gestartete Browseranwendung für Kreativarbeit,
Dokumente, Aufgaben, Projekte, Medien und später geprüfte Erweiterungen.
Das Mindestziel für die Benutzeroberfläche ist **WCAG 2.2 Level AA**.
Zusätzlich sollen praktische Aufgaben auch mit Bildschirmvergrößerung,
reduzierter Sehkraft, eingeschränkter Feinmotorik und wenig Technikerfahrung
verständlich und sicher ausführbar sein. WCAG-Konformität wird erst nach
echter Prüfung eines konkreten Releasekandidaten festgestellt.

Keine pauschale Behauptung, dass ein einzelner „barrierefreier Modus“ alle
Bedürfnisse erfüllt. Der W3C-Bericht zu Sehschwäche dokumentiert ausdrücklich,
dass Bedürfnisse bei Kontrast, Helligkeit und Vergrößerung stark variieren.

## 02. Vorrangige Nutzungsszenarien

| Kennung | Situation | Ziel und beobachtbare Akzeptanz |
|---|---|---|
| U01 | Anfänger beim ersten Start | Startzustand erklärt genau eine Hauptaktion; ohne Fachwort einen Song beginnen |
| U02 | Sehschwach, 200 % Textgröße | Alle Beschriftungen und Kontrollen lesbar, nichts abgeschnitten |
| U03 | Sehschwach, 400 % Browserzoom | Wesentliche Wege bleiben im Reflow ohne horizontales Seitenpendeln erreichbar |
| U04 | Geringe Kontrastwahrnehmung | Inhalt und Status bleiben mit eigenem Farbschema erkennbar |
| U05 | Lichtempfindlichkeit | Gedimmtes Farbschema ohne grelle Pflichtflächen wählbar |
| U06 | Nur Tastatur / eingeschränkte Handmotorik | Erstellung, Speichern, Suche und Abbruch ohne Maus möglich |
| U07 | Screenreader | Überschriften, Labels, Status und Dialoge werden sinnvoll angesagt |
| U08 | Anfänger macht Eingabefehler | Fehlermeldung nennt Feld, Ursache und nächste Korrektur |
| U09 | Browser/Server wird unterbrochen | Keine stille Überschreibung; vorhandener Stand/Draft klar erkennbar |
| U10 | Viele Werkzeuge installiert | Navigation zeigt zuerst laufende Aufgabe, weitere Module sind auffindbar |

## 03. Messbare Darstellungsregeln

| ID | Verbindliche Anforderung | Prüfverfahren |
|---|---|---|
| V01 | Normaler Text mindestens 4,5:1 Kontrast | Berechnung jeder Tokenkombination, kein Aufrunden |
| V02 | Großer Text mindestens 3:1 | Kontrastprüfung, WCAG-Definition für großen Text beachten |
| V03 | Erforderliche UI-Konturen/Zustände mindestens 3:1 | Nichttext-Kontrastprüfung |
| V04 | Text 200 % vergrößern ohne Inhalts-/Funktionsverlust | manuelle Ansicht/Formularprüfung |
| V05 | Reflow bei 320 CSS px Breite; Ausnahme nur sachlich zwingender zweidimensionaler Inhalt | 400-%-Zoom-Test bei 1280 CSS px plus Engansicht |
| V06 | WCAG-2.2-AA-Zielgröße 24×24 CSS px oder zulässige Ausnahme | Trefferziel- und Nachbarabstandsprüfung |
| V07 | Produktintern bevorzugt mindestens 44×44 CSS px für Hauptaktionen | visuelle Messung auf typischen Oberflächen |
| V08 | Fokus klar sichtbar und nicht verdeckt | alle Tab-/Dialog-/Menüpfade |
| V09 | Status nicht ausschließlich über Farbe | Farbblindheits-/Graustufen- und Textprüfung |
| V10 | Vergrößerung und eigene Browser-/OS-Farben werden nicht blockiert | Forced-colors-/Zoom-/Kontrastdurchlauf |
| V11 | Keine zwanghaften Animationen; reduzierte Bewegung respektieren | prefers-reduced-motion |
| V12 | Sprache verständlich, keine unerklärten Kürzel | Redaktionstest mit Laien |

44×44 CSS px für Hauptaktionen ist unsere **zusätzliche Designvorgabe**,
nicht die allgemeine WCAG-2.2-AA-Mindestforderung. Tabellen und Medien-
Zeitleisten dürfen zweidimensionale Ansichten benötigen, müssen aber einen
bedienbaren Alternativweg besitzen, wenn die Funktion das erlaubt.

## 04. Anzeigeprofile ohne starre Festlegung

1. **Standard:** ruhiges, kontrastreiches, luftiges Layout ohne überfüllte
   Armaturen; echte Textbeschriftungen, klare Hierarchie.
2. **Vergrößert:** größere Schrift-/Abstandstokens, einspaltiger Arbeitsbereich,
   weniger gleichzeitig sichtbare Nebeninformationen.
3. **Gedimmt:** weniger Blendung und andere Farbkombinationen; nicht blind
   maximalen Kontrast für jeden erzwingen.
4. **Systemgesteuert:** Browserzoom, Betriebssystem-Farben, Forced Colors und
   reduzierte Bewegung respektieren. Nutzerwerte bleiben nachvollziehbar
   änderbar und werden lokal gespeichert.

Textgröße, Zeilenabstand, Breite und Kontrast nicht in jeder Moduldatei
separat kodieren, sondern ausschließlich über **UI-Design-Tokens**.
Anpassungen dürfen keinen Kontext, Entwurf oder Eingabefokus verlieren.
Ein Reset stellt sichere Standardwerte wieder her.

## 05. Einfache Informationsarchitektur

1. Start mit höchstens einer dominanten Hauptaktion je Arbeitskontext.
2. Hauptnavigation aus verständlichen Tätigkeiten: „Schreiben“, „Projekte“,
   „Aufgaben“, „Medien“, „Einstellungen“; Detailmodule erst bei Auswahl.
3. Überall erkennbar: aktuelles Modul, Projekt, geöffneter Inhalt, Speichern-
   Zustand und nächster sinnvoller Schritt.
4. Nie verschachtelte Navigationsmenüs mit unvorhersehbarer Bewegung.
5. Keine rein dekorativen Dashboards, überfüllte Kachelwände oder dauerhafte
   Tooltips, die wichtige Informationen überdecken.
6. Einstellungen und Hilfe bleiben an denselben Positionen. Benutzerdefinierte
   Ansicht darf die Tastaturlogik nicht verändern.
7. „Einfach“ und „Erweitert“ durch progressive Offenlegung; dieselben Daten,
   keine doppelt implementierten Arbeitsabläufe.

## 06. Formulare, Dialoge und verständliche Fehler

- Jedes Eingabefeld mit sichtbarem Namen und programmgesteuert zugeordnetem
  HTML-label; Placeholder **niemals** als einzigen Namen verwenden.
- Pflichtfelder und Formate vor der Eingabe erklären; Beispiele verfügbar.
- Fehler oben zusammenfassen **und** am betroffenen Feld zuordnen.
- Keine Fehlermeldung „500/ValidationError“. Besser: „Song konnte nicht
  gespeichert werden. Dein Entwurf ist noch vorhanden. Erneut versuchen.“
- Beim Erfolg ebenso verständliche Nachricht, aber keine störenden Popups
  nach jeder kleinen Änderung. Statusmeldungen für Screenreader passend,
  sparsam und ohne Ansageflut.
- Dialog: erkennbarer Titel, Fokus hinein, Tab-Fokus bleibt im echten Modal,
  Escape bei abbrechbaren Vorgängen, Fokus nach Schließen sinnvoll zurück.
- Destruktive Aktion mit Folgenbeschreibung und möglichst Undo statt
  unverständlichem „Sind Sie sicher?“. Keine stumme Löschung.
- Gespeicherte Version, ungespeicherter Entwurf und Konflikt sind eindeutig
  verschiedene Zustände. Speichern/Verwerfen/Abbrechen immer konsistent.

## 07. Tastatur und Screenreader als Primärpfade

- Semantisches HTML mit main, nav, headings, button, label, status und dialog;
  natives HTML ist Standard. ARIA nur für tatsächlich erforderliches Verhalten.
- Sichtbare Fokusposition; Tab-Reihenfolge folgt dem DOM und visuellen Ablauf.
- „Zum Inhalt springen“ für wiederkehrende Navigation.
- Keine reine Hover-/Drag-and-drop-Funktion ohne Maus-/Tastaturalternative.
- Tastaturbefehle dokumentieren, leicht abschalten; keine Konflikte mit Browser
  oder Hilfstechnologie. F1-Hilfe hat immer einen sichtbaren klickbaren Ersatz.
- Raster als **CSS-Layout**, nicht unbesehen als komplexe ARIA-Grid-Interaktion
  modellieren. Falls ein echtes Tabellen-Grid erforderlich ist: APG-Verhalten
  gesondert nachweisen.
- Unter Linux mindestens Firefox mit Orca für realitätsnahe manuelle Prüfung
  vorsehen; ein weiterer Browser-/Screenreader-Kombinationstest ist wünschenswert.

## 08. Drei Ebenen des Hilfesystems

1. **Sofort:** verständliche Feldbeschriftung, kurzer Hinweis vor problematischer
   Aktion, Status direkt neben dem Inhalt.
2. **Im Kontext:** „Was ist das?“, kleine Beispiele, verwandte Hilfeseite und
   Wiederherstellungsweg. Gleicher Einstieg auf jeder Modulansicht.
3. **Ausführlich:** durchsuchbare lokale Hilfe mit klaren Schrittfolgen,
   bebilderbaren Beispielen, Glossar und Fehler-ID. Ohne Internet nutzbar.

Hilfetexte, UI-Begriffe und Diagnosehinweise liegen außerhalb des Codes in
versionierten Textressourcen mit stabilen Schlüssel-IDs. Fehlende Schlüssel
fallen in Entwicklerprüfungen auf; keine stillen leeren Schaltflächen.

## 09. Raster, Formen und visuelle Qualitätskontrolle

- Responsive Layout aus wenigen stabilen Zonen: Navigation, Arbeitsbereich,
  kontextuelle Seitenleiste, klare Status-/Hilfebereiche.
- Grid-Overlay ausschließlich im Debugmodus: überprüft Ränder, Lücken,
  Überdeckungen, Sprungmarken, Fokus und Textabschneidungen.
- Auf engem Fenster wird eine Seitenleiste zur zugänglichen Unteransicht,
  nicht zu unsichtbarem, dennoch fokussierbarem Inhalt.
- Kein festes Pixel-Layout für Text; Größen mit rem, %, minmax und
  contentbezogenen Schranken. CSS-Grid/Flex zur Darstellung, HTML-Struktur
  für die logische Lesereihenfolge.
- Farben, Fokuslinien und Textkontraste als automatisch überprüfbare
  Tokens. Theme-Wechsel muss offenen Editorzustand erhalten.

## 10. Abnahme- und Testmatrix je Gate

| Gate | Automatischer Nachweis | Manuelle Pflichtprobe |
|---|---|---|
| G-1 | Jede UX-Regel besitzt ID und künftigen Test-/Vertragsbezug | Szenarien mit unterschiedlichen Bedürfnissen beurteilen |
| G4 | HTML-/Label-/Kontrast-/ARIA-Basisprüfung, Layout-Screenshots | 200 % Text, 400 % Zoom, Tastatur, Fokus, sichtbare Fehler |
| G5 | Speichern/Reload/Draft/Fehler-E2E für Songs | Anfänger führt U01 und U08 ohne Anleitung aus |
| G6 | Suche/Leerergebnis/Filter/Modulnavigation | Sehschwacher Nutzer führt U02/U03/U04 aus |
| G8 | Plugin-Katalog als deklarativer Vertrag | Berechtigungen verständlich, keine unkontrollierte Aktivierung |
| G10 | Voller WCAG-AA-Prüfbericht + definierter Browser-Satz | Screenreader, Forced Colors, Dialoge, Regressionen |
| G11 | Release-Evidence mit offenen Einschränkungen | Begleitete reale Nutzungstests und dokumentierte Freigabe |

**Wichtig:** Automatisierte Prüfwerkzeuge erfassen nur einen Teil der möglichen
Barrieren. Mindestens drei bis fünf praktische Sitzungen mit unterschiedlichen
Nutzerbedürfnissen werden als frühe qualitative Pilotgröße vorgeschlagen,
nicht als statistischer Konformitätsnachweis. Aufgaben, Abbruchstellen,
Hilfeaufrufe, Fehlerkorrekturen und Zufriedenheit werden anonymisiert erfasst.
Der Nutzer muss sein eigenes Setup verwenden können.

## 11. Priorisierung nach Nutzen/Aufwand

**Unverzichtbar ab dem ersten HTML-Shell-Build:** semantische Elemente,
Tastaturzugriff, Kontrasttokens, lesbare Labels, Fokus, Zoom/Reflow,
Speicher-/Fehlerstatus, sichtbare Hilfe, Undo/Recovery.

**Sinnvoll mit geringem Zusatzaufwand:** lokale Anzeigeprofile,
Zoom-/Textgrößen-Einstellungen, wiederverwendbare Fehlerbausteine,
einheitliche Statuskomponenten und verständliche Leerseiten.

**Später, wenn realer Nutzen nachgewiesen ist:** Spracheingabe, komplexe
Personalisierung, modulübergreifender Assistent, alternative Darstellungsformen
für anspruchsvolle Medien-Zeitleisten.

## 12. Verbindliche Primärquellen

- W3C WCAG 2.2: https://www.w3.org/TR/WCAG22/
- W3C Kontrast Text: https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
- W3C Kontrast Bedienelemente: https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html
- W3C 200 % Text: https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html
- W3C Reflow: https://www.w3.org/WAI/WCAG22/Understanding/reflow.html
- W3C Zielgröße: https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html
- W3C Low Vision Needs: https://www.w3.org/TR/low-vision-needs/
- W3C COGA-Klarheit und einfache Handlungen: https://www.w3.org/TR/coga-usable/design_guide.html
- W3C Formularlabels: https://www.w3.org/WAI/tutorials/forms/labels/
- W3C Keyboard APG: https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/
- W3C Dialog APG: https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/
- W3C echte Nutzer einbeziehen: https://www.w3.org/WAI/test-evaluate/involving-users/
- Playwright Accessibility Testing: https://playwright.dev/docs/accessibility-testing

Quelle/Recherche geprüft am 25.10.2026. Einzelne Empfehlungen über WCAG-AA
hinaus sind interne Designziele und werden deshalb separat bezeichnet.
