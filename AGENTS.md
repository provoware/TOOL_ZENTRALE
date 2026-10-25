# TOOL_ZENTRALE – Regeln für nachfolgende Entwicklungsarbeit

Status: Entwurf, mit dem Plan-Pull-Request zur Freigabe vorgelegt.
Nur das Repo `provoware/TOOL_ZENTRALE` ist für spätere Schreibarbeit vorgesehen.
Referenz-Repositories sind READ-ONLY, solange kein neuer Auftrag anderes erlaubt.

## 01. Autorisierung und Scope

- Aktuelle Freigabe: Planungsdokumente auf isoliertem Branch und PR.
- Kein Produktivcode, keine persönliche Datenmigration, kein Deployment
  ohne separate Benutzeranweisung.
- Ein Writer pro gemeinsamem Dateiscope. Prüfer liefern Befunde, keine
  stillen zusätzlichen Codepatches.
- Niemals fremde Änderungen übergehen. Vor jedem Patch Branch, HEAD,
  betroffene Dateihashes, Planrevision und Scope kontrollieren.
- Bei SHA-, Rechte- oder Zuständigkeitskonflikt: STOP und Finding melden.

## 02. Führende Dateien

- `blueprint/architecture.yaml`: Sollstruktur, virtuelle Komponenten,
  Modulbeziehungen, IDs und Szenarien.
- `governance/route.json`: P-/B-Schritte und Gates samt geplantem Status.
- `docs/MASTERPLAN_V3_1.txt`: ausführliche Begründungen und Route.
- `docs/UX_BARRIEREFREIHEIT.md`: messbare Nutzer- und Zugänglichkeitsziele.
- `docs/ENTWICKLUNGSSTANDARD.md`: Patch-, Test-, Daten-/Versionsregeln.

Ein generierter File-Impact-Index und Code-/Testkarte sind nur Projektionen,
keine zweite handgeführte Quelle. Laufzeitdaten strikt außerhalb von Git.

## 03. Patchbudgets

| Klasse | +/- Zeichen | +/- Zeilen | Dateien |
|---|---:|---:|---:|
| Micro | 1.500 | 30 | 2 |
| Standard | 6.000 | 120 | 3 |
| Kontrolliert | 12.000 | 250 | 5 |

Alle drei Grenzen gleichzeitig. Zeichen = hinzugefügt plus gelöscht ohne
Diffheader. Risiko schlägt Sparzwang: atomare Ausnahme nur mit eigener
Begründung, Testbeleg und Wiederherstellungsweg. Dokumentations-Bootstrap
dieses ersten Plan-PR ist eine einmalig kenntlich gemachte Ausnahme.
Keine globalen Suchen oder Volltests ohne passenden Änderungsanlass.

## 04. Architekturregeln

- Kern nur über stabile Schnittstellen, keine direkten Kernimporte aus
  willkürlichen Modulinterna.
- Modul unter `app/features/<slug>/` mit klar getrenntem Backend,
  expliziten Public-Assets, Tests und manifestierten Capabilities.
- Domain darf weder Webframework noch Datenbank implementierungsabhängig
  importieren. HTML-Shell kennt keine SQL-Details.
- Keine freie Ausführung fremder Plugin-Skripte in V1.
- Keine komplexe Abstraktion ohne belegte Mehrfachverwendung.
- Keine ungültigen JSON-Kommentare oder unbrauchbar erzeugten Leerdateien.

## 05. Vor- und Nachvalidierung

Vorher: exakte P-ID, Abhängigkeiten, Basis-SHA, erlaubte Pfade, Testfamilie,
Patchbudget, Konflikt- und Datenschutzhinweis.
Nachher: Diffumfang, Syntax, Imports, Struktur-/Vertragstest, zugeordnete
Regressionen und Hash/Evidence mit eindeutigem Ergebnis.
Bei Versions-/Sicherheits-/DB-Verträgen sofort strengere Negativevidenz.
Am Gate die vollständig definierte Bündelprüfung; kein PASS auf Vermutung.

## 06. UX ist kein Nachtrag

Für jede berührte Oberfläche gelten geplantes WCAG 2.2 AA, Tastatur,
sichtbarer Fokus, skalierbare Texte, Reflow, verständliche Hilfe und
Fehlerkorrektur. Automated Tests allein genügen nicht; zusätzlich
manuelle und reale Nutzerprüfungen. **Keine voreilige Barrierefreiheitszusage.**

## 07. Status und Schlussbericht

Jeder Schritt meldet: Ziel, Basis-SHA, nur geänderte Pfade,
Zeichen-/Dateiwerte, selektive Prüfungen, offene Risiken, Restore und
exakt einen erlaubten Folgeschritt. Status PLANNED/READY/PATCHED/VERIFIED
nicht ohne die jeweils erforderlichen Nachweise erhöhen.
G-1 vor G0; erst danach genehmigte Produktimplementation.
