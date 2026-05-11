# std_non_crrt_rrt_active Amsterdam Formal Approval Review

Review date: 2026-05-02

Status: reviewed_approved_with_source_coverage_note

Database: `AmsterdamUMCdb-1.0.2`

Standard variable: `std_non_crrt_rrt_active`

## Decision

AmsterdamUMCdb is approved for the same-name `std_non_crrt_rrt_active` asset as a positive-only Class 3 binary-state episode variable under a source-bounded hemodialysis opening mapping.

The approved source boundary is:

- retain `processitems` itemid `16363 / Hemodialyse`
- require non-null positive `start`, `stop`, and `duration`
- require `stop > start`
- merge overlapping or exactly contiguous retained Hemodialyse intervals within the same local admission
- emit only true positive non-CRRT RRT support episodes

The raw Amsterdam `admissionid` is retained as the ICU/MC stay-equivalent `stay_id`, with `subject_id` populated from `admissions_core.patientid`.

## Source Coverage Note

This approval is narrow and source-bounded.

Amsterdam opening evidence supports `Hemodialyse` active intervals. It does not prove complete non-CRRT coverage for peritoneal dialysis:

- `16352 / Peritoneaal catheter` is access-catheter evidence, not active dialysis interval evidence.
- numeric `Peritoneaaldialyse` rows are volume/event evidence, not governed active-state intervals.

Therefore, this is an approved same-name mapping for non-CRRT active support under current Amsterdam processitems evidence, with the peritoneal active-interval gap explicitly documented.

## Source Boundary

The source audit found `58` approved Hemodialyse source intervals. All approved intervals passed timing validity checks.

After interval union, the approved output retains:

- output rows: `57`
- unique `subject_id`: `43`
- unique `stay_id`: `46`

The following adjacent evidence is explicitly excluded from this same-name output:

- `12465 / CVVH`: sibling CRRT-family active interval
- `9161 / Dialyselijn Femoralis`: dialysis access line, `1,090` rows
- `9162 / Dialyselijn Jugularis`: dialysis access line, `520` rows
- `9163 / Dialyselijn Subclavia`: dialysis access line, `304` rows
- `16352 / Peritoneaal catheter`: peritoneal access catheter, `24` rows
- `18718 / Plasmaferese`: plasma exchange, `23` rows
- Hemodialyse, CVVH, and Peritoneaaldialyse fluid-removal or device measurements

This approval is for non-CRRT RRT active support under the retained Hemodialyse interval rule only. It does not approve umbrella any-RRT active state, CRRT-family active state, exact modality truth, access-line status, fluid-removal events, first-day summaries, AKI/KDIGO stage, or renal SOFA phenotype truth.

## Output Summary

- output rows: `57`
- unique `subject_id`: `43`
- unique `stay_id`: `46`
- short episodes less than or equal to 60 minutes: `0`
- prolonged episodes greater than or equal to 7 days: `1`
- duration minutes min / p50 / p90 / p95 / p99 / max: `75 / 230 / 888.2 / 2,798.8 / 9,274.48 / 13,344`

## Governed Evidence

Approved mapping spec:

- `docs/standard_system_mvp/std_non_crrt_rrt_active/mapping_spec_amsterdamumcdb_1_0_2.json`

Formal local implementation:

- `Methods/Clinical_Database/local_work/Layer 5/AmsterdamUMCdb-1.0.2/std_non_crrt_rrt_active/extract_code/Extract_Code_std_non_crrt_rrt_active.py`

Formal output:

- `Methods/Clinical_Database/local_work/Layer 3/AmsterdamUMCdb-1.0.2/treatment_state/std_non_crrt_rrt_active/std_non_crrt_rrt_active_long.parquet`

Governed runtime evidence:

- `docs/standard_system_mvp/std_non_crrt_rrt_active/runtime/amsterdamumcdb_1_0_2_first_real_execution/`
- `docs/standard_system_mvp/std_non_crrt_rrt_active/runtime/amsterdamumcdb_1_0_2_rerun_repro_check/`

Rerun reproducibility:

- `overall_status=pass`
- baseline process batch: `20260502T112847Z_AmsterdamUMCdb-1.0.2_std_non_crrt_rrt_active`
- rerun process batch: `20260502T112900Z_AmsterdamUMCdb-1.0.2_std_non_crrt_rrt_active`

## Conclusion

Amsterdam `processitems` rows for `Hemodialyse` are narrow enough to serve as reviewed-approved same-name source evidence for `std_non_crrt_rrt_active`, provided the hemodialysis-only source coverage note and adjacent-source exclusions remain locked.
