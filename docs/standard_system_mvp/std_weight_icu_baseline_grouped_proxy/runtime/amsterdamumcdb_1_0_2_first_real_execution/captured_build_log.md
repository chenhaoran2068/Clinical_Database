# Build Log: std_weight_icu_baseline_grouped_proxy

- process_batch_id: `20260425T054059Z_AmsterdamUMCdb-1.0.2_std_weight_icu_baseline_grouped_proxy`
- built_at_utc: `2026-04-25T05:41:06Z`
- database_id: `AmsterdamUMCdb-1.0.2`
- asset_status: `reviewed_approved`
- primary_source_table: `admissions_core.weightgroup`
- context_fallback_table: `listitems_event:itemid_10697`
- event_fallback_asset: `std_weight_event:+/-360min`
- output_asset: `Methods/Clinical_Database/local_work/Layer 3/AmsterdamUMCdb-1.0.2/anthropometrics/std_weight_icu_baseline_grouped_proxy/std_weight_icu_baseline_grouped_proxy_long.parquet`
- total_rows: `23106`
- nonnull_baseline_rows: `22206`
- unresolved_rows: `900`
- admissions_weightgroup_proxy_rows: `22160`
- event_fallback_rows: `46`
- p50_std_weight_kg_baseline: `74.50`
- listitems_weightsource_fallback_rows: `770`
- weightsource_discordance_rows: `611`

## Semantic Caution

- Amsterdam `admissionid` is ICU/MC encounter scoped, not a verified hospital admission anchor.
- This asset therefore remains an Amsterdam local encounter-admission baseline build candidate and should not be silently equated with the MIMIC hospital-admission baseline contract.
- `admissions_core.weightgroup` is the primary value source; `std_weight_event` only repairs missing grouped rows inside a strict near-admission window.
- Open boundary groups `59-` and `110+` are retained as boundary proxies rather than expanded hidden midpoints.
