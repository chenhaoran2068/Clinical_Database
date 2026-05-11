# std_crrt_family_active Amsterdam Formal Approval Review

Review date: 2026-05-02

Status: reviewed_approved

Database: `AmsterdamUMCdb-1.0.2`

Standard variable: `std_crrt_family_active`

## Decision

AmsterdamUMCdb is approved for the same-name `std_crrt_family_active` asset as a positive-only Class 3 binary-state episode variable.

The approved source boundary is:

- retain `processitems` itemid `12465 / CVVH`
- require non-null positive `start`, `stop`, and `duration`
- require `stop > start`
- merge overlapping or exactly contiguous retained CVVH intervals within the same local admission
- emit only true positive CRRT-family support episodes

The raw Amsterdam `admissionid` is retained as the ICU/MC stay-equivalent `stay_id`, with `subject_id` populated from `admissions_core.patientid`.

## Source Boundary

The source audit found `5,355` approved CVVH source intervals. All approved intervals passed timing validity checks.

After interval union, the approved output retains:

- output rows: `5,256`
- unique `subject_id`: `1,005`
- unique `stay_id`: `1,065`

The following adjacent evidence is explicitly excluded from this same-name output:

- `16363 / Hemodialyse`: sibling non-CRRT active interval
- `9161 / Dialyselijn Femoralis`: dialysis access line, `1,090` rows
- `9162 / Dialyselijn Jugularis`: dialysis access line, `520` rows
- `9163 / Dialyselijn Subclavia`: dialysis access line, `304` rows
- `16352 / Peritoneaal catheter`: peritoneal access catheter, `24` rows
- `18718 / Plasmaferese`: plasma exchange, `23` rows
- CVVH orders, medication protocol rows, device parameters, MFT rows, and fluid-removal measurements

This approval is for CRRT-family active support only. It does not approve umbrella any-RRT active state, non-CRRT active state, exact modality truth, access-line status, fluid-removal events, first-day summaries, AKI/KDIGO stage, or renal SOFA phenotype truth.

## Output Summary

- output rows: `5,256`
- unique `subject_id`: `1,005`
- unique `stay_id`: `1,065`
- short episodes less than or equal to 60 minutes: `183`
- prolonged episodes greater than or equal to 7 days: `3`
- duration minutes min / p50 / p90 / p95 / p99 / max: `4 / 1,500 / 4,322 / 4,483.75 / 6,715.8 / 11,887`

## Governed Evidence

Approved mapping spec:

- `docs/standard_system_mvp/std_crrt_family_active/mapping_spec_amsterdamumcdb_1_0_2.json`

Formal local implementation:

- `Methods/Clinical_Database/local_work/Layer 5/AmsterdamUMCdb-1.0.2/std_crrt_family_active/extract_code/Extract_Code_std_crrt_family_active.py`

Formal output:

- `Methods/Clinical_Database/local_work/Layer 3/AmsterdamUMCdb-1.0.2/treatment_state/std_crrt_family_active/std_crrt_family_active_long.parquet`

Governed runtime evidence:

- `docs/standard_system_mvp/std_crrt_family_active/runtime/amsterdamumcdb_1_0_2_first_real_execution/`
- `docs/standard_system_mvp/std_crrt_family_active/runtime/amsterdamumcdb_1_0_2_rerun_repro_check/`

Rerun reproducibility:

- `overall_status=pass`
- baseline process batch: `20260502T112847Z_AmsterdamUMCdb-1.0.2_std_crrt_family_active`
- rerun process batch: `20260502T112900Z_AmsterdamUMCdb-1.0.2_std_crrt_family_active`

## Conclusion

Amsterdam `processitems` rows for `CVVH` are narrow enough to serve as reviewed-approved same-name source evidence for `std_crrt_family_active`, provided the documented sibling and adjacent-source exclusions remain locked.
