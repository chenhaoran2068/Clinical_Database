# std_noninvasive_ventilation_active Amsterdam Formal Approval Review

Review date: 2026-05-02

Status: reviewed_approved

Database: `AmsterdamUMCdb-1.0.2`

Standard variable: `std_noninvasive_ventilation_active`

## Decision

AmsterdamUMCdb is approved for the same-name `std_noninvasive_ventilation_active` asset as a positive-only binary state episode variable.

The approved source boundary is:

- retain `processitems` itemid `10740`, label `Beademen non-invasief`
- retain `processitems` itemid `9671`, label `CPAP`
- merge overlapping same-variable source intervals within the same stay
- emit only true positive episodes
- do not union invasive ventilation, HFNC, oxygen-only delivery, tracheostomy status, or broad respiratory-support rows into this same-name asset

## Source Boundary

The source audit found `4,736` valid Amsterdam NIV/CPAP interval rows:

- `9671 / CPAP`: `2,953`
- `10740 / Beademen non-invasief`: `1,783`

After merging overlapping same-variable intervals, the approved output retains:

- output rows: `4,566`
- unique `subject_id`: `1,309`
- unique `stay_id`: `1,414`

The output joins `admissions_core` by `admissionid` to populate `subject_id` from `patientid`. The raw Amsterdam `admissionid` is retained as the ICU/MC stay-equivalent `stay_id`.

## Adjacent-State Rules

The following adjacent sources are excluded from this same-name NIV output:

- `9328 / Beademen`: invasive mechanical ventilation
- HFNC: no approved Amsterdam source found
- `8189` oxygen administration device values: oxygen/device evidence, not NIV source
- `12635 / Tracheostoma`: tracheostomy status

The approved source scope is intentionally `NIV/CPAP`, not all oxygen delivery.

## Output Summary

- output rows: `4,566`
- unique `subject_id`: `1,309`
- unique `stay_id`: `1,414`
- short episodes less than or equal to 60 minutes: `2,145`
- prolonged episodes greater than or equal to 7 days: `8`
- duration minutes p50: `73`
- duration minutes p90: `1,015`
- duration minutes p95: `1,743`
- duration minutes max: `101,580`
- episodes per stay p50 / p90 / p99 / max: `1 / 6 / 31 / 149`

Amsterdam location distribution:

- `IC`: `1,531`
- `IC&MC`: `2,532`
- `MC`: `464`
- `MC&IC`: `39`

## Governed Evidence

Approved mapping spec:

- `docs/standard_system_mvp/std_noninvasive_ventilation_active/mapping_spec_amsterdamumcdb_1_0_2.json`

Formal local implementation:

- `Methods/Clinical_Database/local_work/Layer 5/AmsterdamUMCdb-1.0.2/std_noninvasive_ventilation_active/extract_code/Extract_Code_std_noninvasive_ventilation_active.py`

Formal output:

- `Methods/Clinical_Database/local_work/Layer 3/AmsterdamUMCdb-1.0.2/treatment_state/std_noninvasive_ventilation_active/std_noninvasive_ventilation_active_long.parquet`

Governed runtime evidence:

- `docs/standard_system_mvp/std_noninvasive_ventilation_active/runtime/amsterdamumcdb_1_0_2_first_real_execution/`
- `docs/standard_system_mvp/std_noninvasive_ventilation_active/runtime/amsterdamumcdb_1_0_2_rerun_repro_check/`

Rerun reproducibility:

- `overall_status=pass`
- baseline process batch: `20260502T080342Z_AmsterdamUMCdb-1.0.2_std_noninvasive_ventilation_active`
- rerun process batch: `20260502T080343Z_AmsterdamUMCdb-1.0.2_std_noninvasive_ventilation_active`

## What Is Not Approved Here

This review does not approve any of the following variables or concepts:

- `std_invasive_mechanical_ventilation_active`
- `std_high_flow_nasal_cannula_active`
- `std_supplemental_oxygen_active`
- `std_tracheostomy_status_active`
- respiratory-support-free days
- broad respiratory support active

## Conclusion

Amsterdam `processitems` itemids `10740 / Beademen non-invasief` and `9671 / CPAP` are narrow enough to serve as the approved same-name source for `std_noninvasive_ventilation_active` when governed by the documented adjacent-state exclusions and overlap-union rule.
