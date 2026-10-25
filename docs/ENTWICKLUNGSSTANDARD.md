# TOOL_ZENTRALE – verbindlicher Entwicklungsstandard

Stand: 25.10.2026 · Entwurf 1.0 · Gültigkeit erst nach Planfreigabe

## 01. Architekturvertrag

**Ein Git-Repository:** provoware/TOOL_ZENTRALE.
**Lokales Arbeitsverzeichnis:** PROVOWARE/TOOL_ZENTRALE/.
Keine untergeordneten Git-Repositories und keine unkontrollierten Imports aus
benachbarten Projekten. Andere PROVOWARE-Repositories dienen als Referenzen;
Quellübernahme nur nach Herkunfts-, Lizenz-, Test- und Sicherheitsprüfung.

Schichten: HTML/JS-Shell -> HTTP/API -> Anwendungsfall -> Fachmodell ->
Adapter (SQLite, Dateien, später FFmpeg). Fachmodelle dürfen HTTP, SQL und
Webframeworks nicht importieren. Der Kern kennt ausschließlich die
versionierten Modulverträge, nicht interne Implementierungsdateien.

**Feature-first:** Ein Werkzeug besitzt seinen festen Bereich
app/features/<slug>/{manifest.yaml,backend/,public/,tests/,help/}.
Backendcode und publizierte Assets sind getrennt. Der Server veröffentlicht
nur explizit freigegebene Dateien unter public/, niemals das Feature-Root.
Gemeinsame Funktionen liegen nur bei tatsächlicher Mehrfachnutzung in
app/shared oder app/core. Zweite informelle Kernimplementierungen sind verboten.

## 02. Minimaler Technikstack

Defaultentscheidung für die spätere Implementierung:
Python-Backend mit geprüftem ASGI-Framework (FastAPI Kandidat),
Python-sqlite3, semantisches HTML, CSS-Grid/Flex und native ES-Module.
Möglichst kein schwerer Frontend-Bundler im ersten MVP. Exakte Versionen und
Lizenz-/Supportentscheidung erst in P010 pinnen. Abhängigkeit nur einführen,
wenn Standardbibliothek und vorhandener Vertrag unzureichend sind.
Lokaler Server nur auf 127.0.0.1; externer Zugriff ist ein eigener
Sicherheits-/Hostingbeschluss.

## 03. Eine Quelle je Sachverhalt

| Sachverhalt | Autoritativ | Abgeleitete Sicht |
|---|---|---|
 Soll-Dateien, Codes, Modulgraph, Simulation | blueprint/architecture.yaml | Impact-Index, Diagramm, Dateibaum |
 Aufgabenstatus/Abhängigkeiten/Gates | governance/route.json | Arbeitsübersicht |
 Produkt-/API-/DB-/Modulversionen | governance/versions.json nach P011 | Releaseansicht |
 Bestätigte Fehlerfamilien | governance/regressions.yaml nach P014 | Trigger-/Testempfehlungen |
 Tatsächliche Quelldateien | Git-Commit und Dateihash | File-State-Index |
 Wirkliche Testnachweise | konkreter CI-/Testlauf mit SHA und Toolchain | Gate-Zeugnis |
 Laufzeitfehler | geschütztes, redigiertes Ereignislog außerhalb Git | Diagnosebericht |

Geplante Dateien starten als **VIRTUAL** und werden nur bei freigegebener
Schritt-ID angelegt. Status: VIRTUAL -> RESERVED -> SCAFFOLDED ->
IMPLEMENTED -> VERIFIED -> FROZEN; Sonderstatus BLOCKED/DEPRECATED.
Ein Stub oder Kommentar darf nie als bestandene Implementierung gelten.
Manifest und Laufzeitregister werden niemals ungeprüft bidirektional
synchronisiert; der Ist-Zustand wird anhand echter Quellen abgeglichen.

## 04. Patchbudgets – jeweils alle Grenzen gleichzeitig

| Klasse | Hinzugefügt + entfernt (Unicode-Zeichen) | Änderungszeilen +/- | Dateien |
|---|---:|---:|---:|
| M / Micro | 1.500 | 30 | 2 |
| S / Standard | 6.000 | 120 | 3 |
| K / Kontrolliert | 12.000 | 250 | 5 |

Gezählt wird der inhaltliche Diff ohne Header; UTF-8-Bytezahl zusätzlich
aufzeichnen. Bevorzugt eine Verantwortlichkeit je Patch. Ausnahmen nur bei
atomar unteilbarer Migration, dokumentierter reiner Daten-/Textgenerierung
oder zwingender Sicherheit mit eigener Ausnahme-ID, Scope, SHA und Rollback.
Initiales vollständiges Planungsdokument darf als dokumentierte
**einmalige Planbootstrap-Ausnahme** größer sein; das ist kein Freibrief
für spätere Quellcodepatches.

Warnschwelle: etwa 250 Zeilen pro Python-/JavaScript-Datei,
Funktionen bevorzugt kompakt und einzeln prüfbar. Eine künstliche Zerlegung,
die Komplexität oder versteckte Abhängigkeiten erhöht, ist nicht erwünscht.
Bei größerem Verantwortungsumfang einen echten Modulzuschnitt prüfen.

## 05. Vor-, Nach- und Gateprüfung

**Vor jedem Patch:** exakten Repo-/Plan-/Branch-SHA, Scope, Dateistände,
Platzhalter/Code-IDs, Historie, Fehlerfamilien, relevante Tests und
Budgetklasse bestimmen; fehlende Berechtigung, Basiskonflikt oder doppelter
Writer = STOP.

**Nach jedem Patch:** Diff/Zeichen/Dateien prüfen, Syntax/Format/Imports,
betroffene Verträge, minimale direkt zugeordnete Unit-/API-Tests,
Testresultat mit Quell-SHA protokollieren. Keine unbelegte Aussage „grün“.

**Bei Hochrisikoänderung sofort:** API-Schema, Datenmigration,
Sicherheit/Capabilities, Nutzdatenpfad, Authentifizierung,
Datei-/Prozesszugriff, Releaseverträge – passende Negativevidenz.

**Bündel-/Gateabschluss:** breitere Integrations-, Browser-,
Barrierefreiheits-/Sicherheits- und Datensicherungstests nach Risikomatrix.
Am Releasegate vollständiger Satz. Testcache nur bei identischem Code,
Testdefinition, Abhängigkeiten, Toolchain und Konfiguration; sonst ungültig.
Niemals alle Prüfungen bis zum Ende eines großen Bündels verschieben.

## 06. Wirkungsgesteuerte Testauswahl

1. Geänderte Pfade und Codes gegen manifestierte Eigentümer auflösen.
2. Rückwärts alle konsumierenden Komponenten im Abhängigkeitsgraph ermitteln.
3. Zugeordnete Tests sowie Regressionen früherer Fehlerfamilien auswählen.
4. Kritische Verträge erzwingen zusätzliche Negativprüfungen.
5. Unbekannte Pfade, veraltete Abhängigkeitsdaten oder fehlerhafte Auswahl
   lösen sichere Erweiterung statt Weglassen der Prüfung aus.
6. Gate-Protokoll trennt BLUEPRINT-PASS, MODELL-PASS, TEST-PASS und GATE-PASS.

GitHub Actions soll einen kleinen **immer laufenden Pflichtcheck** erhalten.
Gezielte Unterprüfungen können pfadabhängig sein, dürfen aber keinen
verpflichtenden Check dauerhaft auf Pending stehen lassen. Branch-Rulesets
und Pflichtchecks erst nach vorhandenen funktionierenden Workflowläufen
aktivieren. PR statt Direktcommit auf main.

## 07. Sichere Versionsführung

Sechs getrennte Achsen:

1. Produkt: SemVer MAJOR.MINOR.PATCH.
2. Build: voller Git-SHA + Artefakthash.
3. API: expliziter major-Kompatibilitätsvertrag, z. B. /api/v1.
4. SQLite-Schema: aufsteigende Migrationen mit Hash, Journal und Tests.
5. Module/Plugins: Manifest-/Capability-Vertragsmajor, Mindestkernversion.
6. Import-/Konfigformate: eigene Schema-Versionen.

Kein automatisches Synchron-Hochzählen aller Achsen bei Mini-Patches.
Releaseeinträge enthalten Herkunft, Daten-/API-/Plugin-Kompatibilität,
Backup-/Restore-Evidence und Rückkehrgrenze. DB-Rollback nicht als triviales
Umkehren einer Migration verkaufen; bei irreversiblen Änderungen muss der
Wiederherstellungsweg vorher validiert werden.

## 08. Datenintegrität und Sicherheit

- Nutzdaten/Anhänge/Backups/Logs in separatem lokalen App-Datenverzeichnis
  außerhalb des öffentlichen Git-Repositories und des Releasepakets.
- SQLite-Transaktionen statt Zwischenzuständen; Parameterbindung statt
  zusammengesetzter SQL-Strings, Migrationschecksummen, Integritätsprobe.
- Backup über SQLite-Online-Backup/API und separates Attachment-Manifest;
  Restore erst isoliert testen und Zielbestände schützen.
- Schutz gegen Traversal, Symlinks, Uploadgrößen, MIME-Tricks,
  HTML-/JS-Injection, CSRF je Auth-/Betriebsmodell und missbrauchbare Prozesse.
- FFmpeg nur über geprüften Argument-Adapter, nie Shellstring aus Nutzereingaben.
- Passwörter/Tokens/Privatpfade und Nutztexte nicht in Standardlogs.
- Plugin V1 ist deklarativer Katalog: ausführbarer Fremdcode standardmäßig AUS.
  Capability-Anfragen explizit verweigern, bis ein separater Sicherheitsbeschluss
  inklusive Sandbox-/Threat-Model vorliegt.
- Vor offener Netzbereitstellung: eigenständiges Auth-, TLS-, Mehrnutzer-,
  Rate-Limit-, Daten- und Angriffsmodell.

Sicherheitsanforderungen an OWASP ASVS 5.0.0 und NIST SSDF orientieren;
Anforderungen priorisieren, als Testfälle konkretisieren und nicht behaupten,
eine Checkliste mache das Produkt automatisch sicher.

## 09. Fehlerlernen und kontrollierte Selbstreparatur

Fehlerfamilie: stabile ID, Symptom, belegte Ursache, betroffene Codes,
Trigger, Negativtest, Schwere, letzter Nachweis und Schutzmaßnahme.
Historische Repos nur als Quellbeleg auswerten, keine erfundene Fehlergeschichte.
Automatischer Reparaturassistent darf höchstens begrenzte Hypothesen,
betroffenen Scope, Mini-Diff und Testvorschlag liefern.
**Kein ungeprüfter Auto-Merge, kein autonomer Restore auf Nutzdaten.**
Unbekannte oder wiederholte Fehler -> Stop und aussagefähiger Diagnosefall.

## 10. Logging und Debugging

Trennung: Entwickler-/Laufzeitereignisse, Nutzerhinweise und
Planungs-/Gateentscheidungen. Ereignis-ID, UTC-Zeit, Modul, Vorgang,
Schwere, versionsbezogene Korrelation, redigierte Details.
Kein unnötiges ständiges Schreiben in Git; CI-Evidence begrenzt auf
belegte Gate-/Releasefälle, Laufzeitlog in privatem Datenbereich.
Diagnoseablauf: reproduzieren, Minimalfall, Hypothesen, isolierter Test,
kleinstes Patchangebot, Negativregression, Evidenz, Freigabe.

## 11. Nutzerfreundliche Qualitätsgates

Technisch grüner Build ohne brauchbare UI ist nicht freigabefähig.
Die Pflichttests aus docs/UX_BARRIEREFREIHEIT.md gelten für jede
betroffene Oberfläche. G4 HTML/Zoom/Fokus, G5 Song-Speichern,
G6 Projekte, G8 Plugin-Verträge, G10 Gesamtaudit, G11 Pilot.
Manuelle Tests auf Kubuntu/Linux mit Browserzoom, Tastatur, Screenreader
und tatsächlichen Nutzungsaufgaben ergänzen Automatisierung.

## 12. Repository- und Freigabedisziplin

Ausgangsstand der ersten Planungsänderung:
main@6e9f8638f7a7b6334a23d51988d0e3ef9d82a37c.
Änderungen zunächst nur auf docs/blueprint-v3-1 und als Pull Request.
Die Planungsdokumente dürfen vor der Produktentwicklung eingebracht werden.
Eine Freigabe des Plans ist nicht die Freigabe zur autonomen Umsetzung.
Nach G-1/G0 können die ersten echten Bauskelette in getrennten PRs entstehen.
Pro Repo und Schritt ein autorisierter Writer; bei fremden Änderungen neu
abgleichen und niemals ungefragt überschreiben.

## 13. Primärreferenzen

- GitHub Rulesets: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets
- GitHub Actions Workflow Syntax: https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax
- NIST SSDF: https://csrc.nist.gov/projects/ssdf
- OWASP ASVS: https://asvs.owasp.org/
- SQLite Online Backup: https://www.sqlite.org/backup.html
- JSON Schema Draft 2020-12: https://json-schema.org/draft/2020-12
- OpenAPI-Spezifikationen: https://spec.openapis.org/oas/
- Playwright Accessibility Testing: https://playwright.dev/docs/accessibility-testing
