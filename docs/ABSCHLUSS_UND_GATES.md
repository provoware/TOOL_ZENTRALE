# Verbindlicher Abschluss- und Gatevertrag

Diese Ergänzung ersetzt die frühere reine SHA-Formatprüfung. Sie regelt
Entwicklungsnachweise, keine automatische Produkt- oder Architekturfreigabe.
Basis dieser Iteration: PR #2 @ `037f9522be68599164209b9ca464d33f4ef34dfb`.

## Einen Schritt belegbar abschließen

1. Im Schritt `completion_inputs` als konkrete Code-/Testdateien festlegen.
   Verwaltungsdateien und erzeugte Ansichten sind kein erlaubter Prüfscope.
   Für Produktarbeit zusätzlich echte `completion_checks` festlegen; die
   Entwicklungssuite allein kann keinen Produktpatch zertifizieren.
2. `python3 scripts/assist.py --refresh` ausführen. Nur ein vollständiger
   aktueller PASS-Lauf genügt, keine gezielte Teilprüfung.
3. `python3 scripts/complete_step.py ID` erzeugt die Abschlussakte unter
   `governance/evidence/`, prüft Abhängigkeiten und Gateeintritt und trägt
   erst dann `{record, sha256}` und VERIFIED in route.json ein.
   Mehrere abhängige IDs können mit demselben geprüften Stand atomar
   abgeschlossen werden, etwa `... Q001 Q002 Q003`.
4. `python3 scripts/assist.py --refresh` erneuert die Anzeigen und prüft
   die nun verbindlich referenzierten Akten erneut.

Die Akte bindet Ziel-ID, kanonischen Plan, Basiscommit, alle erforderlichen
Checkresultate, Toolchain, Laufmanifest und die konkreten Scopehashes.
Eine Änderung an zugeordnetem Code, Test oder Plan macht sie ungültig.
Status-/Evidenzreferenzen, Planfreigabestatus und Gateentscheidungen sind aus
der Planidentität ausgeschlossen. So verursacht das Abschließen keinen
Hash-Zirkelschluss. Andere Dokumentationsdateien entwerten fachliche Belege
nicht automatisch. Geprüfte Produktbytes bleiben trotzdem exakt gebunden.

Die Commitbasis muss existieren und Vorfahr des ausgecheckten Stands sein.
Ein Arbeitsbaumtest ist ausdrücklich **Basiscommit plus geprüfte Scopebytes**,
keine Behauptung, sämtliche Dateien seien bereits in diesem Commit enthalten.
CI lädt volle Git-Historie, verwendet Python 3.12 und den gepinnten YAML-Parser.
Patchversion und konkrete Tests bleiben im Bericht sichtbar; die Validierung
verlangt dieselbe Python-Haupt-/Nebenversion, Implementierung und Parserversion.

Alte `{source_sha,test_run,result}`-Objekte werden abgelehnt. Fehlende Tests,
veränderte Akten, falsches Ziel, unbekannte Commitbasis und offene
Voraussetzungen verhindern VERIFIED. Status wird nicht heimlich zurückgestuft:
der Pflichtcheck scheitert, bis Beleg oder bewusste Neuplanung korrigiert ist.

## Gates: offen, geprüft, freigegeben

- OPEN: keine vollständige dokumentierte Entscheidung vorhanden.
- CHECKED: alle Gate-Mitglieder inklusive Unteraufgaben gültig VERIFIED,
  technische Aktenreferenzen in `evidence_sha256` gebunden.
- APPROVED: zusätzlich SHA-gebundene Entscheidungsakte unter
  `governance/approvals/`, passend zu Gate, Plan und technischer Evidenz.

Jedes spätere Gate und jeder READY-/PATCHED-/VERIFIED-Schritt benötigen ein
APPROVED des direkten Vorgängergates. Die drei Q-Korrekturaufgaben sind
vorgelagerte Entwicklungswerkzeuge und erteilen keine G-1-/G0-Freigabe.
Explizite `members` sind maßgeblich; first/last bezeichnet keinen ID-Zahlenbereich.

Eine menschliche Entscheidungsakte hat Schema `provoware-gate-approval/1`,
`gate_id`, `decision: APPROVED`, `approved_by`, UTC-Zeit `decided_at`,
`decision_url`, `plan_sha256` und `evidence_sha256`. Der Route-Eintrag nennt
state, evidence_sha256, approval und approval_sha256. Der Entscheidungsverweis
führt zu einer konkreten Diskussion/PR-/Issue-Antwort im führenden Repository.
Die freigebende Instanz ist im Plan begrenzt, aktuell Repositoryeigner provoware.

Die Software prüft Struktur und Inhaltsbindung. Sie kann mit einer lokalen
JSON-Datei keine menschliche Identität oder die tatsächliche Aussage hinter
einem Link beweisen. Deren Echtheit muss der Repositoryreview prüfen.
Die Prüfhilfe erstellt deshalb keine Freigabeakten und kennt kein Auto-Approve.
In dieser Iteration bleibt jede Gateentscheidung OPEN.

## Qualitätsprüfung und Rückweg

Permanente YAML-/Blueprintprüfung: doppelte Schlüssel, sichere Pfade, Codes,
Dateiziele, erlaubte Layerkanten, Zyklen, Szenarioketten und UX-/Gateverweise.
Tests prüfen zusätzlich Legacy-PASS, Scope-/Test-/Planänderung, fehlende Checks,
Commitexistenz, Gatevorgänger, veraltete Freigabe und die frühe Nutzerreise.
Ein unabhängiger lesender Subagent prüft die Integration; keine zweiten Writer.

Die reine Route-/Registerdatenrevision und erzeugte Anzeigen werden als
Daten-/Generierungsausnahme EX-COMP-01 dokumentiert. Quellcode wird nach
Verantwortung in Planidentität, Aktenprüfung, Abschlusswerkzeug und Modellprüfung
getrennt; gezielte Tests belegen jede Verantwortung. Kein Produktcode erzeugt.
Rückweg: nur eigene Hunks und neue Artefakte gegen den Basisstand prüfen,
Abschlussreferenzen zusammen mit ihren Akten entfernen und Ansichten erneuern.
Keine persönliche Datenmigration, kein Merge, kein Deployment.

## Ergebnis dieser Iteration

43 Unit-/Negativtests sowie permanente Governanceprüfung bestehen.
Codepakete bleiben innerhalb K: Evidenz/Tests 9378 Zeichen und 193 Zeilen;
Gates/Tests 8258/151; atomarer Abschluss/Tests 6830/158;
Plan-/Modellprüfung/Tests 5067/132. Integrationsänderungen bleiben ebenfalls
innerhalb K. Die abschließende Dateimessung berücksichtigt spätere Korrekturen.

Beim ersten echten Abschluss deckte der anschließende Pflichtlauf eine
verunreinigte Graph-Testfixture auf: sie entfernte die Q-Warteschlange,
behielt aber ihre neuen Evidenzreferenzen. Der Lauf wurde korrekt FAIL.
Die Fixture ist nun unabhängig von Live-Abschlüssen; Ursache und Schutz
sind als RG011 registriert. Betroffene eigene Abschlussakten wurden
zurückgenommen und nach der Korrektur aus einem neuen PASS-Lauf erzeugt.
Keine Fehlprüfung wurde als bestanden ausgegeben. Der lesende Abschlussreview
bestätigte Pfadprüfung, atomaren Rückweg und Gateeintritt ohne kritischen Restbefund.
