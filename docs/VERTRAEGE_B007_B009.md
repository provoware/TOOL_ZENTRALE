# Verträge, Szenarien und Prüfautomat B007–B009

**Modell:** MODEL_CONTRACT_PASS. **Reale Browser-/DB-/Pluginausführung:** NOT_TESTED.
**Umfang:** 8 Szenarien, 34 Fälle, 55 Codes und 214 Sollpfade – dynamisch ermittelt.

## Daten und Versionen

Nutzdaten bleiben außerhalb Git/Release. Legacyquellen werden ausschließlich gelesen.
Dokumente, Notizen und Medien besitzen getrennte Speicher-/Rechtegrenzen.
Versionsachsen sind unabhängig; eine kleine Änderung erhöht nicht automatisch alle Werte.

| Achse | Geplanter Vertrag |
|---|---|
| product | semver |
| build | git_sha_plus_artifact_sha256 |
| api | explicit_major |
| database | monotonic_migration_integer |
| module | manifest_contract_major |
| config | format_schema_major |

## Request- und Antwortfelder (Sollschema)

Die Beispiele werden gegen den verwendeten JSON-Schema-Teilumfang geprüft.
Das ist keine implementierte Endpunktvalidierung oder Speicherbestätigung.

| Schema | Pflichtfelder und Typen |
|---|---|
| song_request | document_id: string, title: string, sections: array, expected_revision: integer, request_id: string |
| song_response | document_id: string, revision: integer, saved_at: string, saved: boolean |
| note_request | request_id: string, text: string |
| note_response | note_id: string, utc_iso8601: string, app_version: string, build_sha: string, durable: boolean |
| error | code: string, message: string, correlation_id: string, retryable: boolean, next_action: string |
| project_query | query: string, scope_id: string, limit: integer |
| project_response | project_ids: array, has_more: boolean |
| module_manifest | module_id: string, version: string, contract_major: integer, capabilities: array |
| catalog_response | module_id: string, catalog_enabled: boolean, executable: boolean |
| import_preview | source_id: string, strategy: string, apply: boolean |
| import_apply | preview_id: string, request_id: string, confirmed: boolean, expected_revision: integer |
| import_response | preview_id: string, conflict_ids: array, applied: boolean |
| media_request | asset_id: string, purpose: string |
| media_response | asset_id: string, mime: string, available: boolean |
| launch_request | tool_id: string, request_id: string, confirmed: boolean |
| launch_response | tool_id: string, started: boolean, correlation_id: string |

## API-Aktionen und Rechte

| API | Aktion / Capability |
|---|---|
| ASNG | read: songs.read, write: songs.write |
| APSR | query: projects.read |
| APLG | catalog: catalog.read, manage: catalog.manage |
| ANOTE | append: notes.append |
| AIMP | preview: projects.import_preview, apply: projects.import_apply |
| AMED | read: media.read |
| APLX | launch: tool.launch |

## Notizen und Fehlerhilfe

Gleiche Request-ID mit gleichem Inhalt: dieselbe Bestätigung, kein zweiter Schreibakt.
Gleiche ID mit anderem Inhalt: Konflikt, keine Mutation. Erfolg erst nach dauerhaftem Schreiben.
Zeit, Appversion und Buildkennung stammen vom Server. Clientseitige Versionsfelder werden abgelehnt.
Grenzen: 1000 Textzeichen und 8192 Notiz-Request-Bytes; Entwurf bei Fehler erhalten.
HTTP-Gesamtgrenze: 1048576 Bytes; engere Endpointbudgets stehen im Blueprint.
note_id im Datensatz entspricht der validierten Request-ID. Die bisherige TXT-Feldstruktur bleibt erhalten.
Fehler nennen Code, verständliche Meldung, Korrelation, Wiederholbarkeit und nächste Korrektur.

## Capabilities und Vertrauen

Standard und unbekannte Fähigkeiten: DENY. Katalogmetadaten erteilen keine Ausführungsrechte.
catalog.read, notes.append, songs.read, songs.write, projects.read, projects.import_preview, projects.import_apply, media.read, tool.launch, catalog.manage

| Vertrauensstufe | Geplanter Zugriff |
|---|---|
| BUILTIN | REVIEWED_MANIFEST_CAPABILITIES |
| DECLARATIVE | METADATA_ONLY |
| LOCAL_TOOL | EXPLICIT_ALLOWLIST_ONLY |
| FOREIGN_CODE | DENY |

## Szenariofälle (modelliert)

Die ursprünglichen drei und fünf ergänzenden Wege sind erhalten. Hinzu kommt der Notiz-ID-Konflikt.
Jeder Weg besitzt mindestens vier Fälle, positive/negative Erwartungen und erreichbare Schutzpunkte.
Vorstartprüfungen von LBOOT sind als guard_contracts deklariert, keine versteckten Laufzeitimporte.

<details><summary>Alle geplanten Fälle anzeigen</summary>

| Szenario / Fall | Art | Eingabe → erwartetes Verhalten |
|---|---|---|
| song_save / SNG_POS | POSITIVE | valid_song → stored_and_reopenable |
| song_save / SNG_INV | NEGATIVE | invalid_song → reject_without_mutation |
| song_save / SNG_REV | NEGATIVE | obsolete_revision → conflict_instead_of_overwrite |
| song_save / SNG_FAIL | NEGATIVE | interrupted_commit → transaction_rollback |
| project_search / PRJ_POS | POSITIVE | scoped_query → matching_sorted_results |
| project_search / PRJ_NOM | POSITIVE | no_matches → accessible_empty_state |
| project_search / PRJ_XSS | NEGATIVE | malicious_search_text → escaped_display |
| project_search / PRJ_OVR | NEGATIVE | overlarge_query → bounded_validation_error |
| plugin_load / PLG_POS | POSITIVE | trusted_declarative_manifest → metadata_loaded |
| plugin_load / PLG_CAP | NEGATIVE | unauthorized_capability → denied_without_execution |
| plugin_load / PLG_ABI | NEGATIVE | incompatible_contract_major → rejected |
| plugin_load / PLG_EXEC | NEGATIVE | executable_foreign_plugin → rejected_in_v1 |
| quick_note_append / NOTE_OK | POSITIVE | valid_one_line → append_and_reopen |
| quick_note_append / NOTE_DUP | POSITIVE | repeated_request_id → not_duplicated |
| quick_note_append / NOTE_DISK | NEGATIVE | disk_full → draft_kept_no_false_ack |
| quick_note_append / NOTE_TAIL | NEGATIVE | interrupted_append → partial_tail_detected |
| quick_note_append / NOTE_VER | POSITIVE | version_changed_mid_session → server_version_stamped |
| quick_note_append / NOTE_CONFLICT | NEGATIVE | same_request_id_different_text → conflict_without_second_write |
| offline_launch / BOOT_OK | POSITIVE | complete_offline_package → browser_open_and_health_ok |
| offline_launch / BOOT_MISS | NEGATIVE | missing_wheel → safe_guided_failure |
| offline_launch / BOOT_DBL | POSITIVE | double_start → one_server_reused |
| offline_launch / BOOT_PERM | NEGATIVE | unwritable_data_dir → no_corruption_clear_help |
| import_preview / IMP_OK | POSITIVE | valid_legacy_data → preview_counts_match |
| import_preview / IMP_DUP | NEGATIVE | conflicting_ids → visible_collision_list |
| import_preview / IMP_REF | NEGATIVE | broken_media_reference → no_hidden_loss |
| import_preview / IMP_FAIL | NEGATIVE | interrupted_apply → restore_or_transaction_recovery |
| media_open / MED_OK | POSITIVE | valid_image_or_audio → preview_visible |
| media_open / MED_BAD | NEGATIVE | corrupt_payload → safe_error |
| media_open / MED_PATH | NEGATIVE | traversal_or_symlink → denied |
| media_open / MED_BIG | NEGATIVE | overlarge_payload → bounded_rejection |
| plugin_trusted_launch / PLX_OK | POSITIVE | allowlisted_local_tool → approved_process_only |
| plugin_trusted_launch / PLX_CMD | NEGATIVE | shell_injection_attempt → denied |
| plugin_trusted_launch / PLX_PERM | NEGATIVE | unapproved_capability → denied |
| plugin_trusted_launch / PLX_FREE | NEGATIVE | arbitrary_python_plugin → disabled_without_isolation |

</details>

## Prüfautomat und Grenzen

Bestehende Werkzeuge unter assist.py ausführen; keine zweite Prüfarchitektur.
Die folgenden Phasen benennen feste Prüfdimensionen, keine ausführbare Planungssprache:
parse_unique_keys, contracts, ids_graph_layers, catalog, scenario_contracts, evidence_gates, views, regression_tests

Inputs sind Blueprint, Route, Regressionen, tatsächlicher Dateibestand und erreichbare Git-Historie.
Outputs sind Modellresultat, dynamische Zählwerte, abgeleitete Ansichten und lokaler Laufbeleg.
Bei Fehler FAIL und Abbruch. Keine Quellcode-Selbstreparatur und kein ungeprüfter PASS-Cache.
Nur bekannte Ansichten dürfen bei --refresh neu erzeugt werden; Berichte liegen in work/.
Die ausdrücklich stabilen 112 Haupt-IDs und 13 Gates bleiben geschützt; sonst keine festen Katalogzahlen.
G-1/G0 und spätere Produktabnahmen werden durch diese Modellprüfung nicht freigegeben.
