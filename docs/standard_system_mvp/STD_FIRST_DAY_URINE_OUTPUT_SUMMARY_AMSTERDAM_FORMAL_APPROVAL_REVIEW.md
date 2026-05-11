# Amsterdam `std_first_day_urine_output_summary` Formal Approval Review

Review date: `2026-04-25`

## Formal Decision

- status: `reviewed_approved`
- approved database: `AmsterdamUMCdb-1.0.2`
- same-name variable: `std_first_day_urine_output_summary`
- variable class: `baseline_summary_window_numeric`
- summary subclass: `window_summary`
- governed mapping spec: `docs/standard_system_mvp/std_first_day_urine_output_summary/mapping_spec_amsterdamumcdb_1_0_2.json`
- governed execution entrypoint: `docs/standard_system_mvp/std_first_day_urine_output_summary/execution.py`
- upstream dependency: approved Amsterdam `std_icu_urine_output_event`

## Approved Meaning

Amsterdam `std_first_day_urine_output_summary` is approved as a same-name implementation of the shared first-day ICU urine-output summary contract.

It means:

- one retained row per ICU-semantic Amsterdam stay-equivalent admission
- target locations are `IC`, `IC&MC`, and `MC&IC`
- `MC`-only admissions are excluded from this same-name ICU summary
- the first-day window starts at Amsterdam `admittedat`
- the nominal first-day window ends at `admittedat + 24h`
- the numerator sums approved upstream `std_icu_urine_output_event.urine_output_ml` rows in that window
- stays without approved first-day urine values remain `NULL`, not zero-filled
- partial-window context is retained as flags rather than changing the numerator

It does not mean:

- raw Amsterdam `numericitems` should be rescanned for this summary
- MC-only admissions are included
- missing first-day urine output is zero
- urine-output rate, intake-output balance, or oliguria phenotype has been approved
- nephrostomy or ureteral-splint components are hidden; they remain flagged through upstream event provenance

## Local Build Evidence

The local reviewed-approved build produced:

- row_count: `18386`
- unique_subject_id: `16518`
- unique_stay_id: `18386`
- all Amsterdam admissions: `23106`
- ICU-semantic target rows: `18386`
- excluded MC-only rows: `4720`
- stays with first-day urine rows: `18115`
- stays without first-day urine rows: `271`
- first-day source urine-output rows: `286025`
- first-day approved value rows: `286024`
- first-day source excluded outlier rows: `1`
- first-day source component rows: `287005`
- complete 24h rows: `11074`
- partial-window rows: `7312`
- total first-day urine output: `33246351.0 mL`
- median first-day urine output: `1670.0 mL`
- p25 / p75 first-day urine output: `1115.0 / 2350.0 mL`
- max first-day urine output: `14150.0 mL`
- hard-range violation rows: `0`
- plausible-high prompt rows: `0`

## Governed Runtime Evidence

Public-safe runtime evidence exists for both the first real governed execution and the rerun reproducibility check:

- `docs/standard_system_mvp/std_first_day_urine_output_summary/runtime/amsterdamumcdb_1_0_2_first_real_execution/validation_report.json`
- `docs/standard_system_mvp/std_first_day_urine_output_summary/runtime/amsterdamumcdb_1_0_2_first_real_execution/manifest.json`
- `docs/standard_system_mvp/std_first_day_urine_output_summary/runtime/amsterdamumcdb_1_0_2_rerun_repro_check/validation_report.json`
- `docs/standard_system_mvp/std_first_day_urine_output_summary/runtime/amsterdamumcdb_1_0_2_rerun_repro_check/manifest.json`
- `docs/standard_system_mvp/std_first_day_urine_output_summary/runtime/amsterdamumcdb_1_0_2_rerun_repro_check/reproducibility_report.json`

Runtime validation status:

- first real execution: `pass`
- rerun execution: `pass`
- reproducibility report: `pass`

## Approval-Sensitive Checks

This approval depends on the following checks:

- duplicate stay rows: `0`
- missing target identifiers: `0`
- negative summary values: `0`
- hard-range violation rows: `0`
- NULL value rows with approved source value flag: `0`
- no-source-row behavior retained as `NULL`
- MC-only admissions excluded from same-name ICU scope
- upstream event-layer source routes remain represented through component flags

## Official And Public Alignment Interpretation

The approval is consistent with public Amsterdam source context because:

- AmsterdamUMCdb contains ICU and MCU admission records
- legacy `admissions.admissionid` is the local admission identifier for ICU/MCU admission records
- legacy `numericitems` contains urine-output item families in `mL`
- the upstream Amsterdam urine-output event layer already passed itemid, unit, unitid, value/fluidout, timestamp, dictionary-count, and route-component review

The strongest same-name support is not raw dictionary presence alone.

The strongest support is the completed chain:

- approved upstream Amsterdam event layer
- explicit ICU-semantic denominator
- summary-specific mapping spec
- governed execute-mode runtime evidence
- rerun reproducibility report
- public card regenerated as a cross-database approved variable

## Final Judgment

Amsterdam `std_first_day_urine_output_summary` is approved as a same-name `window_summary` implementation.

The approval is bounded to ICU-semantic Amsterdam admissions and does not approve an all-MCU summary, zero-filled missingness, urine-output rate, intake-output balance, or oliguria phenotype.
