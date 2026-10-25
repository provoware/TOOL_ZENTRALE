# Geprüfte Grundlage B001–B003

## Repositorygrenzen

Ein Schreibziel: `provoware/TOOL_ZENTRALE`; technischer Slug `TOOL_ZENTRALE`.
Der geplante lokale Container heißt PROVOWARE, der Git-Root liegt darunter.
Der Ausführungsort dieser Sitzung /workspace/TOOL_ZENTRALE ist nur ein Checkout.
Produktanzeigename und Checkoutpfad dürfen abweichen. Keine verschachtelten Repos.
Andere Repositories sind Lesereferenzen. Nutzdaten liegen außerhalb Git/Release.

## Quellen und Prüfumfang

Referenz: `provoware/TOOL_2026_Multi@096dc03ae362eed8141b0dbc0c8e91ab0b8daa2d`; vollständiger Baum mit 356 Dateien.
Gezielt gelesen: 15 Dateien; Git-Blobhashes der Scratchkopien exakt geprüft.
Quelltexte und vorhandene Legacytests wurden gelesen, nicht ausgeführt oder übernommen.
Quellebelege mit Blob-/SHA-256-Hash: `governance/foundation.json`.
Keine eigenständige Lizenzdatei im fixierten Baum: Codeübernahme bleibt ungeklärt.

## Nutzungsfälle statt Desktopdetails

Alle Web-Ziele sind PLANNED; CODE_READ/DOCUMENTATION_READ belegt ausschließlich die Quellenlektüre.

| Fall / Eigentümer | Ziel und Eingabe | Ergebnis / Zustand | Fehler und Anpassungsbedarf |
|---|---|---|---|
| UC01 / Songs | Song speichern und wieder öffnen; Titel, Text und Abschnitte | gleicher Text nach erneutem Öffnen; Entwurf → gespeichert; vorige Fassung bleibt gesichert | Titelkollision, Abbruch, ungültiger Abschnitt; DB-Revision und Browser-Draftschutz neu; Dateipfad ist kein Webvertrag |
| UC02 / Songs | Ältere Songfassung wiederherstellen; Song-ID und ausgewählte Fassung | früherer Text; vorheriger aktueller Stand gesichert; gespeichert → wiederhergestellt | fremde Fassung oder falscher Ordner; Bestätigung und atomare DB-Revision statt Dateinamenlogik |
| UC03 / Projekte | Projekt finden und sicher organisieren; Projektname, Status und Arbeitsbestand | zugeordnetes Projekt; unabhängige Kopie; offen, aktiv, fertig, archiviert | Namenskollision, unzulässige Datei oder volle Sicherung; Websuche und explizite Assetrechte; keine hostweiten Dateipfade |
| UC04 / Plugin-Katalog | Werkzeug katalogisieren und bewusst aktivieren; bekannte Modul-ID und Metadaten | validierter Katalog; keine Ausführung; registriert oder deaktiviert | unbekannte ID, falsche Version, Zusatzpfad; Desktopprotokoll mit Zoom ist kein Webmodulvertrag |
| UC05 / Importwerkzeug | Import vor dem Schreiben verstehen; Archiv mit Metadaten und Arbeitsdateien | geplante Anzahl, Konflikte und danach autorisierte neue Kopie; Vorschau → bestätigt → angewandt | Traversal, Duplikate, übergroße Dateien; Legacyfunktion schreibt direkt; Vorschau muss eigenständig gebaut werden |
| UC06 / Medien | Medien prüfen und wiederfinden; freigegebene Asset-ID und Typ | Vorschau oder verständlicher fehlender Verweis; verfügbar, fehlt oder gesperrt | Symlink, fremder Typ, fehlende Datei; Legacy erwartet absolute Hostpfade; Browser erhält ausschließlich IDs |
| UC07 / Schnellnotizen | Schnellnotiz einmalig sichern; Notiztext und Request-ID | dauerhaft bestätigte einzelne Notiz; Entwurf → bestätigt; Fehler erhält Eingabe | Doppelanfrage, Schreibabbruch, volle Datei; Legacy liest und ersetzt die Gesamtdatei ohne Request-ID; Serialisierung und Idempotenz neu |
| UC08 / Gemeinsamer Speicherdienst | Geschützte Daten unabhängig sichern; bestätigter Datenstand und Ziel | prüfbares Paket mit manifestierten Ein-/Ausschlüssen; geplant → geprüft → gesichert | fehlender Anhang, beschädigtes Backup; Legacydokumentation ist kein Web-SQLite-Restorebeleg |

## Gemeinsame Bausteine und Übernahmegrenzen

| Baustein | Entscheidung | Abhängigkeiten und Begründung |
|---|---|---|
| Dokumentmodell und Parser | ADAPT_AFTER_LICENSE | stdlib; app.atomic_io; Datei-I/O im selben Modul; Dataclasses und Parser fachlich nützlich; Domain von Speicheradapter trennen |
| Suche/Sortieren in Songbibliothek | EXTRACT_LOGIC_AFTER_LICENSE | PySide6 wird bereits beim Modulimport geladen; Pure Hilfsfunktionen nur getrennt neu anbinden; keine Qt-Bibliothek im Webkern |
| Atomarer Dateischreibweg | ADOPT_PATTERN | stdlib plus verzögert importiertes app.performance.observe; Flush/Replace-Muster nutzen; nicht als Ersatz für DB-Transaktion oder Logs ungeprüft kopieren |
| Gemeinsame Suche | ADAPT_CONTRACT | stdlib, os.fwalk und lokale Pfade; Budgets und Abbruch übernehmen; nur autorisierte Datenbereiche; HTML-Ausgabe escapen |
| Projektarchivimport | SPLIT_PREVIEW_AND_APPLY | development_pool, module_archive, zipfile; Validierung von Mutation trennen; kein erster Schreibakt vor Vorschau |
| Modulregistrierung | DECLARATIVE_METADATA_ONLY | stdlib, atomic_io; UI-Protokoll mit set_zoom; Whitelist und Metadaten trennen; fremder Code bleibt deaktiviert |
| Medienregister | ADAPT_TO_ASSET_IDS | stdlib, atomic_io und absolute lokale Pfade; Datenhoheit bleibt im Adapter; nie absolute Pfade vom Browser übernehmen |
| Schnellnotizadapter | REIMPLEMENT_CONTRACT | stdlib, atomic_io; gesamter Altinhalt im Speicher; Einmalige Request-ID, Serialisierung und Versionsfelder fehlen; Verträge neu umsetzen |
| Backup und Hilfeführung | ADOPT_REQUIREMENTS | Dokumentierte manuelle Sicherung; keine neue App ausgeführt; Eine gemeinsame Sicherungs-/Hilfebasis mit fachlichen Adaptern; keine doppelte Schattenimplementierung |

## Gemeinsame Schnittstellen (geplant)

| Vertrag / Eigentümer | Schnittstelle | Grenze / Herkunft |
|---|---|---|
| document / Fachmodell / Songs | `DocumentPort.load/save(expected_revision)` | Domain kennt weder HTTP noch Dateisystem; Fachadapter bleiben eigenständig; CODE_READ |
| search / Gemeinsamer Suchdienst | `SearchPort.query(authorized_scope, query, limit)` | Nur freigegebene Daten und begrenzte Ergebnisse; keine freie Hostsuche; CODE_READ |
| tags / Gemeinsame Fachvalidierung | `TagSet.normalize(values)` | Ein Tagformat; Anzeige und Speicherung bleiben getrennt; CODE_READ |
| templates / Gemeinsamer Vorlagenrenderer | `TemplatePort.render(template_id, variables)` | Keine freie HTML-/Skriptausführung; fachliche Platzhalter explizit; OPEN |
| help / Gemeinsamer Hilfekatalog | `HelpPort.resolve(context_id, language)` | Ein Kontextschlüssel je Hilfe; verständliche Texte außerhalb Fachlogik; OPEN |
| logging / Kern / Diagnose | `EventSink.emit(code, severity, correlation_id, redacted_details)` | Keine Nutztexte, Tokens oder privaten Pfade; Nutzerhilfe und Diagnose getrennt; OPEN |
| versions / Dokumentrevisionsdienst | `RevisionPort.list/restore(id, expected_revision)` | Inhaltsfassungen von Produkt-/API-/DB-/Buildversionen trennen; CODE_READ |
| export / Gemeinsamer Exportdienst mit Formatadaptern | `ExportPort.render(document_id, revision, format)` | Arbeitsstand bleibt unverändert; Export ist kein Backup; CODE_READ |

## Offene Punkte in sinnvoller Reihenfolge

- **OPEN02 – Keine explizite Quelllizenz**: Herkunft und Erlaubnis vor jeder tatsächlichen Quellcodeübernahme klären; bis dahin nur Anforderungen und Muster (G0/vor Codeübernahme).
- **OPEN03 – Import implementiert; Freigabestatus offen**: Code und Tests enthalten Rückimport; die Dokumentation nennt ihn noch nicht freigegeben. Separate Freigabe prüfen und Webvorschau vor Anwendung planen (P026/P028).
- **OPEN04 – Noch keine lauffähige Webanwendung**: Erst Architekturabnahme und technische Basis, dann frühen Speichern/Wiederöffnen-Weg real prüfen (G-1/G0/G5).
- **OPEN05 – Datenort und Installationspaket konkretisieren**: Geschützten externen Datenordner, Python-Zielmatrix und Backup-/Offlineprobe im passenden Schritt festlegen (P006/P010/G11).

## Weiterentwicklung

Schichten, Dateikatalog und Codes ergänzen diese Grundlage in B004–B006.
Aktueller Abschlussstatus und konkrete Folgeschritte stehen in docs/STATUS_KURZ.md.
G-1/G0 bleiben bis zur dokumentierten Entscheidung offen.
Die Planung ist kein Nachweis einer funktionierenden Webanwendung.

Erzeugt aus `governance/foundation.json`; mit assist.py --refresh aktualisieren.
