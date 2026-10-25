# TOOL_ZENTRALE

**PROVOWARE – geplante modulare HTML-Webanwendung für Kreativarbeit, Projekte und Organisation.**

Status: **Planung / noch keine lauffähige Anwendung** (25.10.2026).
Dieses Repository enthält zunächst ausschließlich freizugebende Architektur-
und Entwicklungsunterlagen. Der existierende Desktopcode aus
[TOOL_2026_Multi](https://github.com/provoware/TOOL_2026_Multi) bleibt unangetastet.

## Einstieg für Laien

Die Anwendung wird später lokal im Browser unter Linux/Kubuntu gestartet,
mit verständlicher Führung, vergrößerbarer Oberfläche, Tastaturbedienung,
kontextbezogener Hilfe und sicheren Speicher-/Wiederherstellungswegen.
**Es gibt aktuell noch nichts zu installieren oder auszuführen.**

## Verbindliche Planunterlagen

1. [Masterplan 3.1 – 112 nummerierte Schritte / 13 Gates](docs/MASTERPLAN_V3_1.txt)
2. [UX und Barrierefreiheit – WCAG 2.2 AA als Ziel](docs/UX_BARRIEREFREIHEIT.md)
3. [Entwicklungs- und Patchstandard](docs/ENTWICKLUNGSSTANDARD.md)
4. [Überarbeiteter Auftrag](docs/PROMPT_OPTIMIERT.txt)
5. [Primärquellen und Projektbelege](docs/QUELLEN.md)
6. [Architektur-Blueprint – virtuelle Dateien, Kurzcodes, Szenarien](blueprint/architecture.yaml)
7. [Maschinenlesbare Entwicklungsroute](governance/route.json)
8. [Arbeitsregeln für Programmierung und Prüfer](AGENTS.md)

## Fixierte Identität

- Repository: `provoware/TOOL_ZENTRALE`
- Lokaler Projektpfad: `PROVOWARE/TOOL_ZENTRALE/`
- Ein Git-Repository, ein fester Kern, funktionsorientierte Modulbereiche.
- Andere PROVOWARE-Projekte dienen nur als lesbare Referenzen.
- Nutzerdateien, Datenbanken, echte Backups und persönliche Logs gehören
  **nicht** in dieses öffentliche Repository.

## Freigabegrenze

Ein grüner Architekturgraph oder eine vollständige Outline ist kein echter
Funktionstest. Eine spätere Implementierung benötigt eigene Freigabe,
gezielte Tests und dokumentierte Qualitätsgates.

Änderungen an der Planung werden über Pull Requests begutachtet.
