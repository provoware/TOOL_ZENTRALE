# Schichten, Dateikatalog und Codelegende B004–B006

**Nachweis:** statisches Modell und tatsächlicher Dateibestand; keine Produktprüfung.
**Bestand:** 77 vorhanden, 134 nur geplant; 55 Codes.

PRESENT bedeutet vorhandene Datei, nicht implementierte oder geprüfte Produktfunktion.
VIRTUAL bedeutet nur Sollpfad. Es werden keine Produktstubs angelegt.
Die eigene erzeugte Ansicht ist eingerechnet; --check prüft ihre Existenz und Aktualität.

## Schichten und Grenzen

Domain bleibt unabhängig von API, UI und Speicherimplementierung. UI kennt nur UI/API.
Core importiert keine Fachmodulinterna. Pluginpfade benötigen den Capability-Vertrag.
Laufzeitabhängigkeiten und Prüfbeziehungen sind getrennt; Zyklen sind unzulässig.
Diese Regeln gelten für den geplanten Graphen. Reale Import-/Browserprüfung folgt mit Produktcode.

| Schicht | Verantwortung | Darf nutzen | Erlaubte Verbraucher |
|---|---|---|---|
| UI | Zustände, Eingaben und Hilfe verständlich darstellen | UI, API | UI |
| API | Anfragen, Rechte, Grenzen und sichere Antworten prüfen | API, SERVICE, CORE | UI, API |
| SERVICE | Fachliche Anwendungsfälle über stabile Grenzen orchestrieren | SERVICE, DOMAIN, STORAGE, CORE, PLUGIN | API, SERVICE |
| DOMAIN | Fachwerte und Regeln ohne Transport- oder Speichertechnik validieren | DOMAIN | SERVICE, DOMAIN, STORAGE, CORE, PLUGIN |
| STORAGE | Persistenz, Transaktionen und kontrollierten Dateizugriff kapseln | STORAGE, DOMAIN, CORE | SERVICE, STORAGE |
| CORE | Gemeinsame Konfiguration, Identität, Diagnose und Sicherheitsgrenzen führen | CORE, DOMAIN | API, SERVICE, STORAGE, CORE, PLUGIN |
| PLUGIN | Deklarative Registrierung und erlaubte lokale Starter kontrollieren | PLUGIN, DOMAIN, CORE | SERVICE, PLUGIN |
| QA | Verträge und negative Fälle unabhängig prüfen | — | — |
| GOV | Planung, Nachweise und Entscheidungen nachvollziehbar führen | — | — |
| TOOL | Entwicklungs- und Startvorgänge begrenzt unterstützen | — | — |

<details><summary>Vollständigen Dateikatalog anzeigen</summary>

## Dateiabgleich

| Pfad | Ist | Besitzer | Stabilität | Katalog |
|---|---|---|---|---|
| `.github/workflows/ci.yml` | VIRTUAL | TOOL | S1 | CONFIRMED |
| `.github/workflows/todo-check.yml` | PRESENT | TOOL | S1 | CONFIRMED |
| `.gitignore` | PRESENT | TOOL | S1 | CONFIRMED |
| `AGENTS.md` | PRESENT | GOV | S1 | CONFIRMED |
| `README.md` | PRESENT | GOV | S1 | CONFIRMED |
| `Start_TOOL_ZENTRALE.desktop` | VIRTUAL | TOOL | S1 | CONFIRMED |
| `app/__init__.py` | VIRTUAL | CORE | S2 | CONFIRMED |
| `app/api/contracts.py` | VIRTUAL | API | S1 | CONFIRMED |
| `app/api/health.py` | VIRTUAL | API | S1 | CONFIRMED |
| `app/api/router.py` | VIRTUAL | API | S1 | CONFIRMED |
| `app/core/backup.py` | VIRTUAL | SERVICE | S1 | RESERVED |
| `app/core/capabilities.py` | VIRTUAL | CORE | S1 | RESERVED |
| `app/core/capability_guard.py` | VIRTUAL | PLUGIN | S1 | RESERVED |
| `app/core/config.py` | VIRTUAL | CORE | S1 | CONFIRMED |
| `app/core/declarative_loader.py` | VIRTUAL | PLUGIN | S1 | RESERVED |
| `app/core/errors.py` | VIRTUAL | CORE | S1 | CONFIRMED |
| `app/core/imports.py` | VIRTUAL | SERVICE | S1 | RESERVED |
| `app/core/logging.py` | VIRTUAL | CORE | S1 | CONFIRMED |
| `app/core/module_registry.py` | VIRTUAL | CORE | S1 | RESERVED |
| `app/core/security.py` | VIRTUAL | CORE | S1 | CONFIRMED |
| `app/core/text_catalog.py` | VIRTUAL | CORE | S1 | RESERVED |
| `app/core/trusted_launcher.py` | VIRTUAL | PLUGIN | S1 | RESERVED |
| `app/core/versions.py` | VIRTUAL | CORE | S1 | CONFIRMED |
| `app/features/import_tool/backend/routes.py` | VIRTUAL | API | S1 | RESERVED |
| `app/features/import_tool/help/de.md` | VIRTUAL | UI | S2 | RESERVED |
| `app/features/import_tool/manifest.yaml` | VIRTUAL | GOV | S1 | CONFIRMED |
| `app/features/import_tool/public/import_ui.js` | VIRTUAL | UI | S2 | RESERVED |
| `app/features/import_tool/tests/test_import.py` | VIRTUAL | QA | S2 | RESERVED |
| `app/features/media/backend/domain.py` | VIRTUAL | DOMAIN | S2 | RESERVED |
| `app/features/media/backend/routes.py` | VIRTUAL | API | S2 | RESERVED |
| `app/features/media/backend/service.py` | VIRTUAL | SERVICE | S1 | RESERVED |
| `app/features/media/help/de.md` | VIRTUAL | UI | S2 | RESERVED |
| `app/features/media/manifest.yaml` | VIRTUAL | GOV | S1 | CONFIRMED |
| `app/features/media/public/media.js` | VIRTUAL | UI | S2 | RESERVED |
| `app/features/media/tests/test_media.py` | VIRTUAL | QA | S2 | RESERVED |
| `app/features/plugin_catalog/backend/launch_routes.py` | VIRTUAL | API | S1 | RESERVED |
| `app/features/plugin_catalog/backend/routes.py` | VIRTUAL | API | S1 | RESERVED |
| `app/features/plugin_catalog/backend/service.py` | VIRTUAL | SERVICE | S1 | RESERVED |
| `app/features/plugin_catalog/backend/trusted_launch.py` | VIRTUAL | SERVICE | S1 | RESERVED |
| `app/features/plugin_catalog/help/de.md` | VIRTUAL | UI | S2 | RESERVED |
| `app/features/plugin_catalog/manifest.yaml` | VIRTUAL | GOV | S1 | RESERVED |
| `app/features/plugin_catalog/public/catalog.js` | VIRTUAL | UI | S1 | RESERVED |
| `app/features/plugin_catalog/public/launch.js` | VIRTUAL | UI | S2 | RESERVED |
| `app/features/plugin_catalog/tests/test_api.py` | VIRTUAL | QA | S2 | RESERVED |
| `app/features/plugin_catalog/tests/test_denial.py` | VIRTUAL | QA | S2 | RESERVED |
| `app/features/plugin_catalog/tests/test_manifest.py` | VIRTUAL | QA | S2 | RESERVED |
| `app/features/plugin_catalog/tests/test_trusted_launch.py` | VIRTUAL | QA | S2 | RESERVED |
| `app/features/projects/backend/domain.py` | VIRTUAL | DOMAIN | S1 | RESERVED |
| `app/features/projects/backend/repository.py` | VIRTUAL | STORAGE | S1 | RESERVED |
| `app/features/projects/backend/routes.py` | VIRTUAL | API | S1 | RESERVED |
| `app/features/projects/backend/search.py` | VIRTUAL | SERVICE | S1 | RESERVED |
| `app/features/projects/help/de.md` | VIRTUAL | UI | S2 | RESERVED |
| `app/features/projects/manifest.yaml` | VIRTUAL | GOV | S1 | RESERVED |
| `app/features/projects/public/search.js` | VIRTUAL | UI | S1 | RESERVED |
| `app/features/projects/tests/test_api.py` | VIRTUAL | QA | S2 | RESERVED |
| `app/features/projects/tests/test_search.py` | VIRTUAL | QA | S2 | RESERVED |
| `app/features/quick_notes/backend/routes.py` | VIRTUAL | API | S1 | RESERVED |
| `app/features/quick_notes/backend/service.py` | VIRTUAL | SERVICE | S1 | RESERVED |
| `app/features/quick_notes/help/de.md` | VIRTUAL | UI | S2 | RESERVED |
| `app/features/quick_notes/manifest.yaml` | VIRTUAL | GOV | S1 | CONFIRMED |
| `app/features/quick_notes/public/quick_note.js` | VIRTUAL | UI | S2 | RESERVED |
| `app/features/quick_notes/tests/test_append.py` | VIRTUAL | QA | S2 | RESERVED |
| `app/features/quick_notes/tests/test_e2e.py` | VIRTUAL | QA | S2 | RESERVED |
| `app/features/songs/backend/domain.py` | VIRTUAL | DOMAIN | S1 | CONFIRMED |
| `app/features/songs/backend/repository.py` | VIRTUAL | STORAGE | S1 | CONFIRMED |
| `app/features/songs/backend/routes.py` | VIRTUAL | API | S1 | CONFIRMED |
| `app/features/songs/backend/service.py` | VIRTUAL | SERVICE | S1 | CONFIRMED |
| `app/features/songs/help/de.md` | VIRTUAL | UI | S2 | RESERVED |
| `app/features/songs/manifest.yaml` | VIRTUAL | GOV | S1 | CONFIRMED |
| `app/features/songs/public/editor.js` | VIRTUAL | UI | S1 | CONFIRMED |
| `app/features/songs/tests/test_api.py` | VIRTUAL | QA | S2 | CONFIRMED |
| `app/features/songs/tests/test_domain.py` | VIRTUAL | QA | S2 | CONFIRMED |
| `app/features/songs/tests/test_e2e.py` | VIRTUAL | QA | S2 | CONFIRMED |
| `app/features/songs/tests/test_save.py` | VIRTUAL | QA | S2 | CONFIRMED |
| `app/features/tasks/backend/domain.py` | VIRTUAL | DOMAIN | S2 | OPTIONAL |
| `app/main.py` | VIRTUAL | CORE | S1 | CONFIRMED |
| `app/shared/document.py` | VIRTUAL | DOMAIN | S1 | CONFIRMED |
| `app/shared/plugin_manifest.py` | VIRTUAL | DOMAIN | S1 | RESERVED |
| `app/shared/quick_note.py` | VIRTUAL | DOMAIN | S1 | RESERVED |
| `app/storage/backup_adapter.py` | VIRTUAL | STORAGE | S1 | RESERVED |
| `app/storage/db.py` | VIRTUAL | STORAGE | S1 | CONFIRMED |
| `app/storage/migration_ledger.py` | VIRTUAL | STORAGE | S1 | CONFIRMED |
| `app/storage/migrations/001_core.sql` | VIRTUAL | STORAGE | S1 | CONFIRMED |
| `app/storage/text_append.py` | VIRTUAL | STORAGE | S1 | RESERVED |
| `blueprint/architecture.yaml` | PRESENT | GOV | S0 | CONFIRMED |
| `blueprint/codes.yaml` | VIRTUAL | GOV | S1 | CONFIRMED |
| `blueprint/contracts/data.schema.json` | VIRTUAL | DOMAIN | S1 | CONFIRMED |
| `blueprint/contracts/openapi.yaml` | VIRTUAL | API | S1 | CONFIRMED |
| `blueprint/scenarios/import_preview.yaml` | VIRTUAL | QA | S2 | RESERVED |
| `blueprint/scenarios/media_open.yaml` | VIRTUAL | QA | S2 | RESERVED |
| `blueprint/scenarios/offline_launch.yaml` | VIRTUAL | QA | S2 | RESERVED |
| `blueprint/scenarios/plugin_load.yaml` | VIRTUAL | QA | S1 | CONFIRMED |
| `blueprint/scenarios/plugin_trusted_launch.yaml` | VIRTUAL | QA | S2 | RESERVED |
| `blueprint/scenarios/project_search.yaml` | VIRTUAL | QA | S1 | CONFIRMED |
| `blueprint/scenarios/quick_note_append.yaml` | VIRTUAL | QA | S2 | RESERVED |
| `blueprint/scenarios/song_save.yaml` | VIRTUAL | QA | S1 | CONFIRMED |
| `docs/ABSCHLUSS_UND_GATES.md` | PRESENT | GOV | S1 | CONFIRMED |
| `docs/ARBEITSWEISE.md` | PRESENT | GOV | S2 | CONFIRMED |
| `docs/ARCHITEKTUR_B004_B006.md` | PRESENT | GOV | S1 | CONFIRMED |
| `docs/AUDIT_2026_10_25.md` | PRESENT | GOV | S2 | CONFIRMED |
| `docs/ENTWICKLUNGSSTANDARD.md` | PRESENT | GOV | S1 | CONFIRMED |
| `docs/FRUEHER_LAIENABLAUF.md` | PRESENT | GOV | S1 | CONFIRMED |
| `docs/GRUNDLAGE_B001_B003.md` | PRESENT | GOV | S1 | CONFIRMED |
| `docs/ITERATION_REGRESSION.md` | PRESENT | GOV | S2 | CONFIRMED |
| `docs/MASTERPLAN_V3_1.txt` | PRESENT | GOV | S1 | CONFIRMED |
| `docs/MASTERPLAN_V3_2_DELTA.txt` | PRESENT | GOV | S1 | CONFIRMED |
| `docs/PROMPT_OPTIMIERT.txt` | PRESENT | GOV | S1 | CONFIRMED |
| `docs/QUELLEN.md` | PRESENT | GOV | S1 | CONFIRMED |
| `docs/REGRESSION_INFO.md` | PRESENT | GOV | S2 | CONFIRMED |
| `docs/STATUS_KURZ.md` | PRESENT | GOV | S2 | CONFIRMED |
| `docs/TODO_V3_2.md` | PRESENT | GOV | S1 | CONFIRMED |
| `docs/USER_GUIDE.md` | VIRTUAL | GOV | S2 | CONFIRMED |
| `docs/UX_BARRIEREFREIHEIT.md` | PRESENT | GOV | S1 | CONFIRMED |
| `docs/VERTRAEGE_B007_B009.md` | PRESENT | GOV | S1 | CONFIRMED |
| `docs/assets/todo_progress.svg` | PRESENT | GOV | S2 | CONFIRMED |
| `docs/decisions/0001-architecture.md` | VIRTUAL | GOV | S1 | CONFIRMED |
| `docs/operations.md` | VIRTUAL | GOV | S2 | RESERVED |
| `governance/decisions.md` | VIRTUAL | GOV | S1 | CONFIRMED |
| `governance/events.jsonl` | VIRTUAL | GOV | S1 | RESERVED |
| `governance/evidence/B001.json` | PRESENT | GOV | S1 | CONFIRMED |
| `governance/evidence/B002.json` | PRESENT | GOV | S1 | CONFIRMED |
| `governance/evidence/B003.json` | PRESENT | GOV | S1 | CONFIRMED |
| `governance/evidence/B004.json` | PRESENT | GOV | S1 | CONFIRMED |
| `governance/evidence/B005.01.json` | PRESENT | GOV | S1 | CONFIRMED |
| `governance/evidence/B005.json` | PRESENT | GOV | S1 | CONFIRMED |
| `governance/evidence/B006.json` | PRESENT | GOV | S1 | CONFIRMED |
| `governance/evidence/B007.01.json` | PRESENT | GOV | S1 | CONFIRMED |
| `governance/evidence/B007.json` | PRESENT | GOV | S1 | CONFIRMED |
| `governance/evidence/B008.01.json` | PRESENT | GOV | S1 | CONFIRMED |
| `governance/evidence/B008.json` | PRESENT | GOV | S1 | CONFIRMED |
| `governance/evidence/B009.01.json` | PRESENT | GOV | S1 | CONFIRMED |
| `governance/evidence/B009.json` | PRESENT | GOV | S1 | CONFIRMED |
| `governance/evidence/Q001.json` | PRESENT | GOV | S1 | CONFIRMED |
| `governance/evidence/Q002.json` | PRESENT | GOV | S1 | CONFIRMED |
| `governance/evidence/Q003.json` | PRESENT | GOV | S1 | CONFIRMED |
| `governance/file_state.json` | PRESENT | GOV | S2 | CONFIRMED |
| `governance/foundation.json` | PRESENT | GOV | S1 | CONFIRMED |
| `governance/modules.json` | VIRTUAL | GOV | S1 | RESERVED |
| `governance/regressions.yaml` | PRESENT | GOV | S1 | CONFIRMED |
| `governance/route.json` | PRESENT | GOV | S0 | CONFIRMED |
| `governance/versions.json` | VIRTUAL | GOV | S0 | CONFIRMED |
| `packaging/README.md` | VIRTUAL | GOV | S1 | CONFIRMED |
| `packaging/offline_manifest.json` | VIRTUAL | TOOL | S1 | CONFIRMED |
| `pyproject.toml` | VIRTUAL | TOOL | S1 | CONFIRMED |
| `requirements-dev.txt` | PRESENT | GOV | S1 | CONFIRMED |
| `requirements.lock` | VIRTUAL | TOOL | S1 | CONFIRMED |
| `scripts/api_contract_rules.py` | PRESENT | TOOL | S1 | CONFIRMED |
| `scripts/assist.py` | PRESENT | TOOL | S2 | CONFIRMED |
| `scripts/blueprint_contract.py` | PRESENT | TOOL | S1 | CONFIRMED |
| `scripts/blueprint_preview.py` | VIRTUAL | TOOL | S1 | RESERVED |
| `scripts/blueprint_validate.py` | VIRTUAL | TOOL | S1 | CONFIRMED |
| `scripts/blueprint_view.py` | PRESENT | TOOL | S1 | CONFIRMED |
| `scripts/check_governance.py` | PRESENT | TOOL | S1 | CONFIRMED |
| `scripts/complete_step.py` | PRESENT | TOOL | S1 | CONFIRMED |
| `scripts/completion_contract.py` | PRESENT | TOOL | S1 | CONFIRMED |
| `scripts/contract_rules.py` | PRESENT | TOOL | S1 | CONFIRMED |
| `scripts/contract_view.py` | PRESENT | TOOL | S1 | CONFIRMED |
| `scripts/foundation.py` | PRESENT | TOOL | S1 | CONFIRMED |
| `scripts/gate_contract.py` | PRESENT | TOOL | S1 | CONFIRMED |
| `scripts/impact_select.py` | VIRTUAL | TOOL | S1 | RESERVED |
| `scripts/install_offline.sh` | VIRTUAL | TOOL | S1 | CONFIRMED |
| `scripts/patch_guard.py` | VIRTUAL | TOOL | S1 | CONFIRMED |
| `scripts/plan_contract.py` | PRESENT | TOOL | S1 | CONFIRMED |
| `scripts/project_state.py` | PRESENT | TOOL | S2 | CONFIRMED |
| `scripts/regression_registry.py` | PRESENT | TOOL | S2 | CONFIRMED |
| `scripts/release_check.py` | VIRTUAL | TOOL | S1 | RESERVED |
| `scripts/render_todo.py` | PRESENT | TOOL | S1 | CONFIRMED |
| `scripts/route_guard.py` | VIRTUAL | TOOL | S1 | CONFIRMED |
| `scripts/run_evidence.py` | PRESENT | TOOL | S2 | CONFIRMED |
| `scripts/scaffold.py` | VIRTUAL | TOOL | S1 | RESERVED |
| `scripts/scenario_rules.py` | PRESENT | TOOL | S1 | CONFIRMED |
| `scripts/schema_examples.py` | PRESENT | TOOL | S1 | CONFIRMED |
| `scripts/start_tool.sh` | VIRTUAL | TOOL | S1 | CONFIRMED |
| `scripts/test_assist.py` | PRESENT | QA | S2 | CONFIRMED |
| `scripts/test_blueprint.py` | PRESENT | QA | S1 | CONFIRMED |
| `scripts/test_blueprint_contract.py` | PRESENT | QA | S1 | CONFIRMED |
| `scripts/test_blueprint_view.py` | PRESENT | QA | S1 | CONFIRMED |
| `scripts/test_close_transaction.py` | PRESENT | QA | S1 | CONFIRMED |
| `scripts/test_code_history.py` | PRESENT | QA | S1 | CONFIRMED |
| `scripts/test_completion.py` | PRESENT | QA | S1 | CONFIRMED |
| `scripts/test_contract_consistency.py` | PRESENT | QA | S1 | CONFIRMED |
| `scripts/test_contract_rules.py` | PRESENT | QA | S1 | CONFIRMED |
| `scripts/test_foundation.py` | PRESENT | QA | S1 | CONFIRMED |
| `scripts/test_gates.py` | PRESENT | QA | S1 | CONFIRMED |
| `scripts/test_project_state.py` | PRESENT | QA | S2 | CONFIRMED |
| `scripts/test_render_todo.py` | PRESENT | QA | S2 | CONFIRMED |
| `scripts/test_run_evidence.py` | PRESENT | QA | S2 | CONFIRMED |
| `scripts/test_scenario_rules.py` | PRESENT | QA | S1 | CONFIRMED |
| `tests/architecture/test_catalog.py` | VIRTUAL | QA | S2 | RESERVED |
| `tests/architecture/test_graph.py` | VIRTUAL | QA | S1 | CONFIRMED |
| `tests/architecture/test_route.py` | VIRTUAL | QA | S2 | RESERVED |
| `tests/e2e/test_accessibility.py` | VIRTUAL | QA | S2 | RESERVED |
| `tests/e2e/test_view_modes.py` | VIRTUAL | QA | S2 | RESERVED |
| `tests/integration/test_first_launch.py` | VIRTUAL | QA | S2 | RESERVED |
| `tests/integration/test_offline_install.py` | VIRTUAL | QA | S2 | RESERVED |
| `tests/security/test_permissions.py` | VIRTUAL | QA | S2 | CONFIRMED |
| `tests/unit/test_text_catalog.py` | VIRTUAL | QA | S1 | CONFIRMED |
| `web/css/components.css` | VIRTUAL | UI | S2 | RESERVED |
| `web/css/grid.css` | VIRTUAL | UI | S1 | CONFIRMED |
| `web/css/tokens.css` | VIRTUAL | UI | S1 | CONFIRMED |
| `web/help/index.md` | VIRTUAL | UI | S1 | RESERVED |
| `web/i18n/de.json` | VIRTUAL | UI | S1 | CONFIRMED |
| `web/i18n/en.json` | VIRTUAL | UI | S2 | OPTIONAL |
| `web/index.html` | VIRTUAL | UI | S1 | CONFIRMED |
| `web/js/api_client.js` | VIRTUAL | UI | S1 | CONFIRMED |
| `web/js/app.js` | VIRTUAL | UI | S1 | CONFIRMED |
| `web/js/components/grid.js` | VIRTUAL | UI | S1 | CONFIRMED |
| `web/js/components/help.js` | VIRTUAL | UI | S1 | RESERVED |
| `web/js/components/notifications.js` | VIRTUAL | UI | S1 | RESERVED |
| `web/js/components/view_modes.js` | VIRTUAL | UI | S2 | RESERVED |
| `web/js/state.js` | VIRTUAL | UI | S1 | CONFIRMED |

</details>

<details><summary>Vollständige Codelegende anzeigen</summary>

## Semantische Codelegende (geplante Schnittstellen)

| Code / Name | Pfad / Schicht | Schnittstelle | Verbraucher | Geplante Tests |
|---|---|---|---|---|
| KCFG / Konfiguration | `app/core/config.py` / CORE | Lokale Einstellungen laden, validieren und freigegeben bereitstellen | BSQL, FNOTE, KCAP, KLOG, KSEC, KTXT, KVER | TIMP, TMED, TNOTE, TPLG, TPSR, TPST, TSAV, TTXT, TVIEW |
| KLOG / Ereignisprotokoll | `app/core/logging.py` / CORE | Redigiertes Ereignis mit Code, Schwere und Korrelations-ID schreiben | BSQL, FNOTE, KERR, SIMP, SMED, SNOTE, SPLG, SPLX, SPSR, SSNG | TIMP, TMED, TNOTE, TPLG, TPSR, TPST, TSAV, TVIEW |
| KERR / Fehlerantworten | `app/core/errors.py` / CORE | Fehlercode in sichere API-Antwort und nächste Hilfe übersetzen | AIMP, AMED, ANOTE, APLG, APLX, APSR, ASNG | TIMP, TMED, TNOTE, TPLG, TPSR, TPST, TSAV, TVIEW |
| KSEC / Rechtepruefung | `app/core/security.py` / CORE | Aktion und Datenbereich gegen explizite Rechte prüfen | AIMP, AMED, ANOTE, APLG, APLX, APSR, ASNG, PCMD | TIMP, TMED, TNOTE, TPLG, TPSR, TPST, TSAV, TVIEW |
| KVER / Versionen | `app/core/versions.py` / CORE | Produkt-, API-, DB- und Buildkennung getrennt bereitstellen | SNOTE | TNOTE, TVIEW |
| KCAP / Faehigkeitsgrenzen | `app/core/capabilities.py` / CORE | Capability-Anfrage prüfen; unbekannte Fähigkeiten verweigern | KREG, PCMD, PLOD | TPLG, TPST |
| KREG / Modulregistrierung | `app/core/module_registry.py` / CORE | Bekannte Modul-ID anhand gültigen Vertrags registrieren | PCMD, PLOD | TPLG, TPST |
| KTXT / Textkatalog | `app/core/text_catalog.py` / CORE | Textschlüssel und Sprache auflösen; fehlenden Schlüssel diagnostizieren | — | TTXT |
| DDOC / Dokumentmodell | `app/shared/document.py` / DOMAIN | Dokument-ID, Inhalt und erwartete Revision fachlich validieren | DMED, DPRJ, DSNG | TMED, TPSR, TSAV |
| DSNG / Songmodell | `app/features/songs/backend/domain.py` / DOMAIN | Songtitel, Abschnitte und Metadaten ohne I/O validieren | BSON, SSNG | TSAV |
| DPRJ / Projektmodell | `app/features/projects/backend/domain.py` / DOMAIN | Projekt-ID, Titel und Status ohne I/O validieren | BPRJ, SPSR | TPSR |
| DPLG / Pluginmanifest | `app/shared/plugin_manifest.py` / DOMAIN | Deklarative Modulmetadaten und Vertragsversion validieren | PLOD | TPLG, TPST |
| BSQL / SQLite Transaktion | `app/storage/db.py` / STORAGE | Transaktion beginnen, bestätigen oder vollständig zurücknehmen | BPRJ, BSON, SIMP, SMED | TIMP, TMED, TPSR, TSAV |
| BSON / Song-Repository | `app/features/songs/backend/repository.py` / STORAGE | Song und Revision über parametrisierten Speicheradapter laden/sichern | SSNG | TSAV |
| BPRJ / Projekt-Repository | `app/features/projects/backend/repository.py` / STORAGE | Projekt und freigegebene Suchdaten aus Speicheradapter laden | SPSR | TPSR |
| SSNG / Song-Speicherung | `app/features/songs/backend/service.py` / SERVICE | Song mit erwarteter Revision speichern; Konflikt explizit melden | ASNG | TSAV |
| SPSR / Projektsuche | `app/features/projects/backend/search.py` / SERVICE | Begrenzte Projektsuche im erlaubten Datenbereich ausführen | APSR | TPSR |
| PLOD / Deklarativer Plugin-Lader | `app/core/declarative_loader.py` / PLUGIN | Geprüftes Manifest lesen; keinen fremden Programmcode ausführen | SPLG | TPLG, TPST |
| SPLG / Plugin-Katalog | `app/features/plugin_catalog/backend/service.py` / SERVICE | Validierte Katalogeinträge lesen und kontrolliert ändern | APLG | TPLG |
| ASNG / Song-API | `app/features/songs/backend/routes.py` / API | Songanfrage validieren und sicher an Speicherdienst weitergeben | USNG | TSAV |
| APSR / Such-API | `app/features/projects/backend/routes.py` / API | Suchanfrage begrenzen und autorisierte Ergebnisse zurückgeben | UPSR | TPSR |
| APLG / Plugin-API | `app/features/plugin_catalog/backend/routes.py` / API | Kataloganfrage prüfen und deklarative Metadaten zurückgeben | UPLG | TPLG |
| UGRD / UI-Raster | `web/js/components/grid.js` / UI | Layoutzustand aus verfügbarem Raum und Anzeigeprofil ableiten | UIMP, UMED, UNOTE, UPLG, UPLX, UPSR, USNG, UVIEW | TIMP, TMED, TNOTE, TPLG, TPSR, TPST, TSAV, TVIEW |
| USNG / Song-Editor | `app/features/songs/public/editor.js` / UI | Entwurf bearbeiten, speichern, abbrechen und Fehlerzustand erhalten | — | TSAV |
| UPSR / Projekt-Suche-UI | `app/features/projects/public/search.js` / UI | Suchtext erfassen und Ergebnisse samt Leerzustand anzeigen | — | TPSR |
| UPLG / Plugin-Katalog-UI | `app/features/plugin_catalog/public/catalog.js` / UI | Katalog und Rechte verständlich anzeigen; kein Fremdcode laden | — | TPLG |
| TSAV / Song-Speichertest | `app/features/songs/tests/test_save.py` / QA | Song-Speichern und Wiederöffnen einschließlich Konflikt/Abbruch prüfen | — | Prüfvertrag: USNG, ASNG, SSNG, BSON, BSQL |
| TPSR / Projektsuchtest | `app/features/projects/tests/test_search.py` / QA | Suchergebnis, Begrenzung und Leerzustand prüfen | — | Prüfvertrag: UPSR, APSR, SPSR, BPRJ |
| TPLG / Plugin-Schutztest | `app/features/plugin_catalog/tests/test_denial.py` / QA | Manifest-, Versions- und Capability-Verweigerung prüfen | — | Prüfvertrag: UPLG, APLG, SPLG, PLOD, KCAP |
| DNOTE / Schnellnotizmodell | `app/shared/quick_note.py` / DOMAIN | Notiztext und Request-ID fachlich begrenzen | SNOTE | TNOTE, TVIEW |
| FNOTE / TXT-Append-Adapter | `app/storage/text_append.py` / STORAGE | Serialisierten dauerhaften Text-Append ausführen; Teilende erkennen | SNOTE | TNOTE, TVIEW |
| SNOTE / Schnellnotizdienst | `app/features/quick_notes/backend/service.py` / SERVICE | Notiz idempotent mit serverseitiger Version dauerhaft bestätigen | ANOTE | TNOTE, TVIEW |
| ANOTE / Schnellnotiz-API | `app/features/quick_notes/backend/routes.py` / API | Notizanfrage prüfen und bestätigten Speicherstatus zurückgeben | UNOTE | TNOTE, TVIEW |
| UNOTE / Schnellnotiz-Einzeiler | `app/features/quick_notes/public/quick_note.js` / UI | Einzeilige Notiz erfassen; Entwurf bis Bestätigung erhalten | — | TNOTE, TVIEW |
| TNOTE / Notiz-Append-Regressionssuite | `app/features/quick_notes/tests/test_append.py` / QA | Doppelrequest, Schreibabbruch und Notizerhalt prüfen | — | Prüfvertrag: UNOTE, ANOTE, SNOTE, FNOTE |
| DMED / Medienmodell | `app/features/media/backend/domain.py` / DOMAIN | Medien-ID, Typ und Größenvertrag fachlich validieren | SMED | TMED |
| SMED / Mediendienste | `app/features/media/backend/service.py` / SERVICE | Freigegebenes Medium prüfen und sichere Vorschau bereitstellen | AMED | TMED |
| AMED / Medien-API | `app/features/media/backend/routes.py` / API | Medienanfrage anhand Asset-ID und Rechten validieren | UMED | TMED |
| UMED / Medienoberflaeche | `app/features/media/public/media.js` / UI | Vorschau oder verständlichen fehlenden Verweis anzeigen | — | TMED |
| TMED / Medien-Regressionssuite | `app/features/media/tests/test_media.py` / QA | Medientyp, Pfadgrenze und beschädigte Vorschau prüfen | — | Prüfvertrag: UMED, AMED, SMED |
| SIMP / Import-Preview-Service | `app/core/imports.py` / SERVICE | Import zuerst ohne Mutation prüfen und Konfliktvorschau liefern | AIMP | TIMP |
| AIMP / Import-API | `app/features/import_tool/backend/routes.py` / API | Importvorschau und gesondert bestätigte Anwendung anfordern | UIMP | TIMP |
| UIMP / Import-Dialog | `app/features/import_tool/public/import_ui.js` / UI | Umfang und Konflikte vor bewusst bestätigtem Import anzeigen | — | TIMP |
| TIMP / Import-UI-/Kollisionsregression | `app/features/import_tool/tests/test_import.py` / QA | Vorschau, Zielkonflikt und Unterbrechung ohne Quellmutation prüfen | — | Prüfvertrag: UIMP, AIMP, SIMP |
| LBOOT / Klickstarter | `scripts/start_tool.sh` / TOOL | Lokale Instanz prüfen und erst nach gültigem Health-Signal öffnen | — | TBOOT, TOFF |
| TBOOT / Klickstart-/Doppelstarttest | `tests/integration/test_first_launch.py` / QA | Erststart, Doppelstart und sichere Fehlerhilfe prüfen | — | Prüfvertrag: LBOOT |
| TOFF / Offlineinstallations-Test | `tests/integration/test_offline_install.py` / QA | Offlinepaket auf sauberem Zielsystem ohne Netzbedarf prüfen | — | Prüfvertrag: LBOOT |
| UVIEW / Komfort-/Kompaktmodus | `web/js/components/view_modes.js` / UI | Komfort-/Kompaktprofil ohne Entwurfs- oder Fokusverlust wechseln | — | TVIEW |
| TVIEW / Anzeigeprofil-Regressionssuite | `tests/e2e/test_view_modes.py` / QA | Anzeigeprofilwechsel einschließlich Notizentwurf prüfen | — | Prüfvertrag: UVIEW, UNOTE |
| PCMD / Gepruefter externer Starter | `app/core/trusted_launcher.py` / PLUGIN | Ausschließlich bestätigte lokale Argumentliste mit Capabilities starten | SPLX | TPST |
| SPLX / Sicherer Fremdstarterdienst | `app/features/plugin_catalog/backend/trusted_launch.py` / SERVICE | Freigegebenen Fremdstarter orchestrieren; Shellstrings verweigern | APLX | TPST |
| APLX / Fremdstarter-API | `app/features/plugin_catalog/backend/launch_routes.py` / API | Starteranfrage nach ID, Berechtigung und Vertrag prüfen | UPLX | TPST |
| UPLX / Fremdstarter-Oberflaeche | `app/features/plugin_catalog/public/launch.js` / UI | Startfolgen und Rechte vor bewusster Aktion verständlich anzeigen | — | TPST |
| TPST / Fremdstarter-Schutztests | `app/features/plugin_catalog/tests/test_trusted_launch.py` / QA | Shellinjektion, fehlende Capability und freien Drittcode verweigern | — | Prüfvertrag: UPLX, APLX, SPLX, PCMD, KCAP, PLOD |
| TTXT / Textkatalog-Vertragstest | `tests/unit/test_text_catalog.py` / QA | Fehlende Textschlüssel und kontrollierten Fallback prüfen | — | Prüfvertrag: KTXT |

</details>

## Einordnung und Pflege

Verbraucher und Testzuordnungen sind aus requires/verifies abgeleitet, keine zweite Codequelle.
Die transitive Testzuordnung ist ein Planbezug, kein Nachweis tatsächlicher Testausführung.
Historische IDs bleiben aus der vollständigen Git-Historie gesperrt; keine manuelle Schattenliste.
KTXT erhielt den fehlenden geplanten Prüfvertrag TTXT. Der Testpfad bleibt VIRTUAL.
Quellen: blueprint/architecture.yaml, Git und der bestehende File-State-Snapshot.
Aktualisieren: assist.py --refresh. Maschinenansicht ohne zusätzliche Datei: blueprint_view.py --json.
G-1/G0 bleiben ohne separate menschliche Entscheidungsakte offen.
