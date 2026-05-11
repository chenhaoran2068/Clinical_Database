# std_rrt_active Amsterdam Formal Approval Review

Review date: 2026-05-02

Status: reviewed_approved

Database: `AmsterdamUMCdb-1.0.2`

Standard variable: `std_rrt_active`

## Decision

AmsterdamUMCdb is approved for the same-name `std_rrt_active` asset as a positive-only Class 3 binary-state episode variable.

The approved source boundary is:

- retain `processitems` itemid `12465 / CVVH`
- retain `processitems` itemid `16363 / Hemodialyse`
- require non-null positive `start`, `stop`, and `duration`
- require `stop > start`
- merge overlapping or exactly contiguous approved intervals within the same local admission
- emit only true positive RRT support episodes

The raw Amsterdam `admissionid` is retained as the ICU/MC stay-equivalent `stay_id`, with `subject_id` populated from `admissions_core.patientid`.

## Source Boundary

The source audit found `5,413` approved processitems source intervals:

- `12465 / CVVH`: `5,355`
- `16363 / Hemodialyse`: `58`

All `5,413` approved source intervals passed timing validity checks.

After interval union, the approved output retains:

- output rows: `5,313`
- unique `subject_id`: `1,027`
- unique `stay_id`: `1,098`

## Adjacent-State Rules

The following adjacent evidence is explicitly excluded from this same-name output:

- `9161 / Dialyselijn Femoralis`: dialysis access line, `1,090` rows
- `9162 / Dialyselijn Jugularis`: dialysis access line, `520` rows
- `9163 / Dialyselijn Subclavia`: dialysis access line, `304` rows
- `18718 / Plasmaferese`: plasma exchange, `23` rows
- `procedureorderitems` CVVH orders such as start, stop, reset, filter change, and lab collection
- `drugitems` CVVH protocol medication or fluid rows
- `numericitems` CVVH device settings, pressures, MFT parameters, and fluid-removal measurements
- `listitems` MFT_Behandeling device-mode rows and RedenStakenCVVH stop-reason rows

This approval is for umbrella any-RRT active state only. It does not approve access-line presence, exact modality truth, CRRT-only active state, non-CRRT-only active state, device parameter events, fluid-removal events, AKI/KDIGO stage, or renal SOFA phenotype truth.

## Output Summary

- output rows: `5,313`
- unique `subject_id`: `1,027`
- unique `stay_id`: `1,098`
- short episodes less than or equal to 60 minutes: `183`
- prolonged episodes greater than or equal to 7 days: `4`
- duration minutes min / p50 / p90 / p95 / p99 / max: `4 / 1,482 / 4,320 / 4,483 / 6,734.72 / 13,344`
- episodes per stay p50 / p90 / p99 / max: `3 / 11.3 / 28.03 / 92`
- CRRT-containing output episodes: `5,256`
- hemodialysis-containing output episodes: `57`

Amsterdam location distribution:

- `IC`: `4,616`
- `IC&MC`: `579`
- `MC`: `54`
- `MC&IC`: `64`

## Governed Evidence

Approved mapping spec:

- `docs/standard_system_mvp/std_rrt_active/mapping_spec_amsterdamumcdb_1_0_2.json`

Formal local implementation:

- `Methods/Clinical_Database/local_work/Layer 5/AmsterdamUMCdb-1.0.2/std_rrt_active/extract_code/Extract_Code_std_rrt_active.py`

Formal output:

- `Methods/Clinical_Database/local_work/Layer 3/AmsterdamUMCdb-1.0.2/treatment_state/std_rrt_active/std_rrt_active_long.parquet`

Governed runtime evidence:

- `docs/standard_system_mvp/std_rrt_active/runtime/amsterdamumcdb_1_0_2_first_real_execution/`
- `docs/standard_system_mvp/std_rrt_active/runtime/amsterdamumcdb_1_0_2_rerun_repro_check/`

Rerun reproducibility:

- `overall_status=pass`
- baseline process batch: `20260502T101351Z_AmsterdamUMCdb-1.0.2_std_rrt_active`
- rerun process batch: `20260502T101359Z_AmsterdamUMCdb-1.0.2_std_rrt_active`

## What Is Not Approved Here

This review does not approve any of the following variables or concepts:

- `std_crrt_family_active`
- `std_non_crrt_rrt_active`
- `std_rrt_modality_episode`
- `std_rrt_fluid_removal_event`
- first-day RRT summary variables
- RRT-free-day outcome variables
- AKI/KDIGO staging
- renal SOFA phenotype helpers
- access-line status variables
- plasma exchange active state

## Conclusion

Amsterdam processitems rows for `CVVH` and `Hemodialyse` are narrow enough to serve as the reviewed-approved same-name source for `std_rrt_active`, provided the documented exclusions and overlap-union rule remain locked.
