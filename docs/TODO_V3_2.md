# TOOL_ZENTRALE – intelligente TODO V3.2

> **Planungsdokument.** Keine Produktimplementierung; Gatefreigaben nur aus geprüften Entscheidungsakten.

![Grafischer Fortschritt: nach Gates und gesamt](assets/todo_progress.svg)

**Gesamt:** 9/112 Hauptschritte (8 %) · **Unteraufgaben:** 4/22 · **G−1:** OPEN.

## Bedienung und verbindliche Regeln

- `[ ]` = offen, `[x]` = mit Nachweis abgeschlossen; GitHub zeigt die Kästchen an.
- **Autoritative Quelle:** [`governance/route.json`](../governance/route.json), nicht die Markdown-Datei. Nur dort Status und commitgebundene Evidenz ändern.
- **Abhaken:** `progress_overrides.ID = VERIFIED` und `evidence_by_step.ID = {record, sha256}` nur über `python3 scripts/complete_step.py ID` erzeugen; danach Ansichten aktualisieren.
- GitHub-Dateiansicht: Kästchen zeigen den Status, Änderungen erfolgen über einen prüfbaren Datei-/Pull-Request-Patch. Bloßes Anklicken ist kein Nachweis.
- **NO-OP** nur mit dokumentierter Begründung und gültiger Evidenz im Schrittbericht, niemals durch blindes Abhaken.
- **PATCH-KARTE:** `ID | GRUND | EFFEKT | UMFANG | M/S/K | RISIKO | DATEIEN | CHECK | SHA | STATUS`; vor Umsetzung Scope und Budget prüfen.
- Für eine neue Aufgabe werden **Grund, Effekt und Dateiumfang erst bei READY** konkretisiert. Keine 112 spekulativen Dateilisten pflegen.
- **Testregel:** direkte Prüfung je Patch, Negativtest bei Risiko; breite Integrationsprüfungen an Gates und vor Release.
- **Synchronisierung:** `python3 scripts/render_todo.py --check` validiert Status, Checkliste und Grafik ohne Änderungen.

## Nummerierte Checkliste

<details open>
<summary><strong>G-1 – Architektur und Blueprint</strong> (9/12; 75 %)</summary>

- [x] **B001** Stabile PROVOWARE-Identität und Repositorygrenze `PLAN` · `R1`
- [x] **B002** Altbestand rückwärts in Nutzungsfälle zerlegen `PLAN` · `R1`
- [x] **B003** Gemeinsame Bausteine und Wiederverwendungsgrenzen `PLAN` · `R2`
- [x] **B004** Stabile Schichten und erlaubte Richtung `PLAN` · `R1`
- [x] **B005** Virtuellen Dateikatalog mit Stabilitätsklassen aufstellen `PLAN` · `R2`
  - [x] `B005.01` Dateikatalog mit echter Bestandsliste und Medien-/Importmodulen abgleichen
- [x] **B006** Semantische Kurzcode-Legende `PLAN` · `R2`
- [x] **B007** Verträge, Datenformate und Rechte `PLAN` · `R1`
  - [x] `B007.01` Notizvertrag und Fremdplugin-Vertrauensstufen festlegen
- [x] **B008** Drei durchgängige Funktionssimulationen formulieren `PLAN` · `R2`
  - [x] `B008.01` Fuenf neue Szenarien inklusive negativen Faellen modellieren
- [x] **B009** Architektur-Prüfautomat spezifizieren `PLAN` · `R2`
  - [x] `B009.01` Dynamischen Schema-/Graphvalidator statt fixer Sollzahlen definieren
- [ ] **B010** Virtuellen Dry-Run und Fault-Katalog beurteilen `PLAN` · `R2`
  - [ ] `B010.01` TXT-Abbruch-/Doppelrequest- und Offline-Fault-Tests simulieren
- [ ] **B011** Minimalen echten Durchstich spezifizieren `PLAN` · `R1`
- [ ] **B012** Architekturfreigabe G-1 und offene Entscheidungen `PLAN` · `R1`

</details>

<details>
<summary><strong>G0 – Bestandsaufnahme</strong> (0/8; 0 %)</summary>

- [ ] **P001** Quellenstand fixieren `PLAN` · `R1`
- [ ] **P002** Funktionale Bestandsmatrix `PLAN` · `R1`
- [ ] **P003** Datenformat- und Schutzinventar `PLAN` · `R1`
- [ ] **P004** Andere Repositories fokussiert vergleichen `PLAN` · `R1`
- [ ] **P005** Historische Fehlerbibliothek einfrieren `PLAN` · `R1`
- [ ] **P006** Nutzungs-/Hostingentscheidung `PLAN` · `R1`
- [ ] **P007** MVP, Modulfolge und Nicht-Ziele `PLAN` · `R1`
- [ ] **P008** Route und Repositorynamen freigeben `PLAN` · `R1`

</details>

<details>
<summary><strong>G1 – Entwicklungsautomatik</strong> (0/8; 0 %)</summary>

- [ ] **P009** Vorhandenes Git-Repository kontrolliert einrichten `K` · `R1`
  - [ ] `P009.01` Launcher-, Workflow- und Packaging-Dateien registriert initialisieren
- [ ] **P010** Reproduzierbare Toolchain `S` · `R2`
  - [ ] `P010.01` Offline-Wheelhouse und kompatible Zielumgebung pinnen
- [ ] **P011** Produkt-/API-/DB-/Plugin-Versionsquelle `S` · `R1`
- [ ] **P012** Minimale Qualitätspipeline `S` · `R2`
- [ ] **P013** Ereignis-ID und Fehlerredaktion `S` · `R1`
- [ ] **P014** Erste Regressionfamilien registrieren `S` · `R1`
- [ ] **P015** Patch-Budget- und SHA-Guard `K` · `R1`
- [ ] **P016** Impact-Index und Recovery Capsule `S` · `R2`

</details>

<details>
<summary><strong>G2 – Backend und Datenkern</strong> (0/9; 0 %)</summary>

- [ ] **P017** Geschützter API-Start `S` · `R1`
  - [ ] `P017.01` Klickstart, Doppelstart und lokale Portprobe definieren
- [ ] **P018** API-Fehler- und Validierungskontrakt `S` · `R1`
- [ ] **P019** SQLite-Verbindung und Transaktionsschicht `K` · `R1`
- [ ] **P020** Schema-Migrationsledger `S` · `R1`
- [ ] **P021** Daten-Repository-Port `S` · `R2`
- [ ] **P022** Projekt-/Dokumentgrundmodell `S` · `R1`
- [ ] **P023** Datei-/Medienreferenzmodell `S` · `R2`
  - [ ] `P023.01` Append-only-Nutzdatei mit exklusiver Schreibgrenze implementieren
- [ ] **P024** API-Contract-Testpaket `S` · `R1`
- [ ] **P025** G2-Datenkern-Nachweis `K` · `R1`

</details>

<details>
<summary><strong>G3 – Import und Datensicherung</strong> (0/8; 0 %)</summary>

- [ ] **P026** Legacy-Snapshot und Importbericht `S` · `R1`
- [ ] **P027** JSON- und Textformatparser `S` · `R1`
- [ ] **P028** Import-Dry-Run mit Konfliktstrategie `K` · `R1`
- [ ] **P029** Transaktionaler Import in neue Datenbasis `K` · `R1`
- [ ] **P030** SQLite-Backup samt Manifest `S` · `R1`
- [ ] **P031** Anhänge und Ausnahmen im Backup `S` · `R1`
  - [ ] `P031.01` Tool-Notizdatei in konsistenten Backupvertrag integrieren
- [ ] **P032** Isolierter Restore mit Journal/Undo `K` · `R1`
- [ ] **P033** G3 vollständiger Migrations-Roundtrip `K` · `R1`

</details>

<details>
<summary><strong>G4 – Bedienoberfläche</strong> (0/10; 0 %)</summary>

- [ ] **P034** Semantische HTML-Grundhülle `S` · `R2`
  - [ ] `P034.01` Globale Schnellerfassung und Oeffnen-Schaltflaeche verbinden
- [ ] **P035** CSS-Farb-/Abstands-/Typografie-Tokens `S` · `R2`
  - [ ] `P035.01` Komfort-/Kompaktumschaltung ohne Kontextverlust anlegen
- [ ] **P036** Responsive Grid und Debug-Raster `S` · `R2`
- [ ] **P037** Navigation und Seitenzustände `S` · `R2`
- [ ] **P038** Gemeinsame Formularprimitive `S` · `R2`
- [ ] **P039** Speichern-Verwerfen-Abbrechen-Vertrag `S` · `R1`
- [ ] **P040** Textkatalog und fehlende Schlüssel `S` · `R2`
- [ ] **P041** Hilfestufen und F1-Kontext `S` · `R2`
- [ ] **P042** Erste Browser-End-to-End-Reisen `S` · `R2`
  - [ ] `P042.01` Notiz-E2E mit Unterbrechung und Tastatur pruefen
- [ ] **P043** G4 Layout-/Accessibility-Grundabnahme `K` · `R1`
  - [ ] `P043.01` Fruehe UI-Gates von spaeteren Fachmodulabnahmen trennen

</details>

<details>
<summary><strong>G5 – Songs und Kreativfunktionen</strong> (0/5; 0 %)</summary>

- [ ] **P047** Song-Dokumentenmodell `S` · `R1`
- [ ] **P048** Songbibliothek und Filter `S` · `R2`
- [ ] **P049** Songeditor mit Speicherzustand `K` · `R1`
- [ ] **P050** Song-Fassungen und Wiederherstellung `S` · `R1`
- [ ] **P056** Gemeinsame Suche/Export und kreatives MVP-Gate `K` · `R1`

</details>

<details>
<summary><strong>G6 – Projekte</strong> (0/16; 0 %)</summary>

- [ ] **P063** Entwicklungspool und Projektimporte `K` · `R1`
  - [ ] `P063.01` Benutzerfuehrung fuer Importvorschau und Konfliktliste anlegen
- [ ] **P057** Aufgaben- und Statusmodell `S` · `R2`
- [ ] **P058** Aufgabenoberfläche und Schnellaktionen `S` · `R2`
- [ ] **P059** Kalenderdaten und Ansichten `S` · `R2`
- [ ] **P060** Erinnerung mit klarer Browsergrenze `S` · `R2`
- [ ] **P061** Link-Schnellstarter `S` · `R2`
- [ ] **P062** Kontometadaten ohne Passworttresor `S` · `R1`
- [ ] **P044** Profil-Stammdaten `S` · `R2`
- [ ] **P045** Genre-Zufall und Favoriten `S` · `R2`
- [ ] **P046** Charakterfibel und Referenzen `S` · `R2`
- [ ] **P051** Allgemeiner Texteditor `S` · `R2`
- [ ] **P052** Textbuttons und Platzhalter `S` · `R2`
- [ ] **P053** Buch-/Kapitelwerkstatt `S` · `R2`
- [ ] **P054** Ideenarchiv und Kompositionskopien `S` · `R2`
- [ ] **P055** Wiki und Wissensverweise `S` · `R2`
- [ ] **P064** G6 modulübergreifende Nutzerreise `S` · `R2`

</details>

<details>
<summary><strong>G7 – Medien und Dateien</strong> (0/7; 0 %)</summary>

- [ ] **P065** Medienzugriffsvertrag `S` · `R1`
  - [ ] `P065.01` Medienmanifest, Bedienung und Security-Tests vollstaendig registrieren
- [ ] **P066** Audioplayer `S` · `R2`
- [ ] **P067** Bildvorschau `S` · `R2`
- [ ] **P068** FFmpeg-Adapter `K` · `R1`
- [ ] **P069** Jobwarteschlange und Wiederaufnahme `S` · `R1`
- [ ] **P070** Medienbackup und Referenzprüfung `S` · `R1`
- [ ] **P071** G7 Medien-Fault-Lab `K` · `R1`

</details>

<details>
<summary><strong>G8 – Werkzeuge und Plugins</strong> (0/7; 0 %)</summary>

- [ ] **P072** Deklaratives Modulmanifest `S` · `R1`
  - [ ] `P072.01` Registrierte Fremdtools getrennt von Fremdcode-Laufzeit definieren
- [ ] **P073** Modulregistrierung und Lifecycle `S` · `R2`
- [ ] **P074** Capability-Grenze `S` · `R1`
- [ ] **P075** Formularbaukasten als Datenmodell `S` · `R2`
- [ ] **P076** Modulhilfe und geordneter Katalog `S` · `R2`
- [ ] **P077** Entscheidung über Drittcode-Sandbox `K` · `R1`
  - [ ] `P077.01` Nur belegte Isolation zur Freigabe beliebigen Fremdcodes akzeptieren
- [ ] **P078** G8 Manifest-/Capability-Negativgate `S` · `R1`

</details>

<details>
<summary><strong>G9 – Fehlerlernen und Regression</strong> (0/7; 0 %)</summary>

- [ ] **P079** Fehlersignaturen und Klassifizierung `S` · `R2`
- [ ] **P080** Impact-basierte Testauswahl `S` · `R2`
  - [ ] `P080.01` Regressions-/Impacttrigger fuer Notizen, Starter und Plugins verbinden
- [ ] **P081** Ergebnis-Cache und Stale-Schutz `S` · `R1`
- [ ] **P082** Negative Fehlerfamilien `K` · `R1`
  - [ ] `P082.01` TXT-/Offline-/Plugin-Fault-Sammlung als Negativsuite ausfuehren
- [ ] **P083** Reparaturhypothesen statt Autonomie `S` · `R1`
- [ ] **P084** Evidenz-/Recovery-Capsule erzeugen `S` · `R2`
- [ ] **P085** G9 Regressions-/Reparaturtest `K` · `R1`

</details>

<details>
<summary><strong>G10 – Qualitätsabschluss</strong> (0/8; 0 %)</summary>

- [ ] **P086** Threat-Model aktualisieren `S` · `R1`
- [ ] **P087** Security-Prüfprofil nach OWASP ASVS `K` · `R1`
- [ ] **P088** API-/CSP-/Upload-Sicherheitsprobe `S` · `R1`
- [ ] **P089** Accessibility-Prüfmatrix `S` · `R2`
- [ ] **P090** Performance-Baseline `S` · `R2`
- [ ] **P091** Datenintegritäts-/Skalierungsprobe `S` · `R1`
- [ ] **P092** Konsistenz von Text, Hilfe, Release und Manifest `S` · `R2`
- [ ] **P093** G10 Vollregression des Releasekandidaten `K` · `R1`

</details>

<details>
<summary><strong>G11 – Release und Betrieb</strong> (0/7; 0 %)</summary>

- [ ] **P094** Release-Manifest und Versionstitel `S` · `R1`
- [ ] **P095** Paketbau und Herkunft `K` · `R1`
  - [ ] `P095.01` Offline-Paket am sauberen Kubuntu-Zielsystem testen
- [ ] **P096** Laienstart und Installationsassistent `S` · `R2`
  - [ ] `P096.01` Ein-Klick-Start und Kontexthilfe laienpraktisch abnehmen
- [ ] **P097** Updates und Rückkehr `K` · `R1`
- [ ] **P098** Pilot mit echten Anfängeraufgaben `S` · `R2`
- [ ] **P099** Endnutzer- und Betriebshandbuch `S` · `R2`
- [ ] **P100** G11 finale Freigabeentscheidung `K` · `R1`

</details>

## Nächster Schritt und Warteschlange

Bedingte Vorschau: Jeder Folgeschritt setzt den belegten Abschluss seiner Voraussetzungen voraus. Keine Ausfuehrungs- oder Gatefreigabe.
1. **B010 – Virtuellen Dry-Run und Fault-Katalog beurteilen** · Planung
2. **B011 – Minimalen echten Durchstich spezifizieren** · Planung
3. **B012 – Architekturfreigabe G-1 und offene Entscheidungen** · Planung

**Patch-Karte beim Start ausfüllen:**

```text
ID:     [aus der Aufgabenroute]    GRUND: [max. 1 Satz]
EFFEKT: [messbares Ergebnis]   UMFANG: [konkrete Dateien]
PATCH:  [M/S/K]                RISIKO: [R1/R2]
CHECK:  [betroffene Tests]      SHA: [Basis und Nachweis]
```

*Diese Datei und die SVG-Grafik sind aus `governance/route.json` erzeugt.*
