# std_tracheostomy_status_active Amsterdam Formal Approval Review

Review date: 2026-05-02

Status: reviewed_approved

Database: `AmsterdamUMCdb-1.0.2`

Standard variable: `std_tracheostomy_status_active`

## Decision

AmsterdamUMCdb is approved for the same-name `std_tracheostomy_status_active` asset as a positive-only binary state episode variable.

The approved source boundary is:

- retain `processitems` itemid `12635`, label `Tracheostoma`
- emit only true positive episodes
- do not union invasive ventilation, NIV/CPAP, HFNC, oxygen-only delivery, tracheostomy-care orders, or broad respiratory-support rows into this same-name asset

## Source Boundary

The source audit found:

- `12635 / Tracheostoma`: `1,940` valid source rows
- invalid timing rows: `0`

The final approved output retains:

- output rows: `1,940`
- unique `subject_id`: `1,081`
- unique `stay_id`: `1,275`

The output joins `admissions_core` by `admissionid` to populate `subject_id` from `patientid`. The raw Amsterdam `admissionid` is retained as the ICU/MC stay-equivalent `stay_id`.

## Adjacent-State Rules

The following adjacent sources are excluded from this same-name tracheostomy-status output:

- `9328 / Beademen`: invasive mechanical ventilation
- `10740 / Beademen non-invasief`: noninvasive ventilation
- `9671 / CPAP`: CPAP / NIV-family support
- oxygen administration device values
- legacy no-longer-used tracheostomy process codes `9171`, `9176`, `9177`, and `10618`
- tracheostomy-care procedure orders such as cannula care or cleaning

This asset tracks tracheostomy status. It is not auto-equated to invasive mechanical ventilation.

## Output Summary

- output rows: `1,940`
- unique `subject_id`: `1,081`
- unique `stay_id`: `1,275`
- short episodes less than or equal to 60 minutes: `12`
- prolonged episodes greater than or equal to 7 days: `929`
- duration minutes p50: `9,836`
- duration minutes p90: `33,211.6`
- duration minutes p95: `46,196.7`
- duration minutes max: `292,926`
- episodes per stay p50 / p90 / p99 / max: `1 / 3 / 5 / 7`

Amsterdam location distribution:

- `IC`: `1,070`
- `IC&MC`: `781`
- `MC`: `77`
- `MC&IC`: `12`

## Governed Evidence

Approved mapping spec:

- `docs/standard_system_mvp/std_tracheostomy_status_active/mapping_spec_amsterdamumcdb_1_0_2.json`

Formal local implementation:

- `Methods/Clinical_Database/local_work/Layer 5/AmsterdamUMCdb-1.0.2/std_tracheostomy_status_active/extract_code/Extract_Code_std_tracheostomy_status_active.py`

Formal output:

- `Methods/Clinical_Database/local_work/Layer 3/AmsterdamUMCdb-1.0.2/treatment_state/std_tracheostomy_status_active/std_tracheostomy_status_active_long.parquet`

Governed runtime evidence:

- `docs/standard_system_mvp/std_tracheostomy_status_active/runtime/amsterdamumcdb_1_0_2_first_real_execution/`
- `docs/standard_system_mvp/std_tracheostomy_status_active/runtime/amsterdamumcdb_1_0_2_rerun_repro_check/`

Rerun reproducibility:

- `overall_status=pass`
- baseline process batch: `20260502T080348Z_AmsterdamUMCdb-1.0.2_std_tracheostomy_status_active`
- rerun process batch: `20260502T080350Z_AmsterdamUMCdb-1.0.2_std_tracheostomy_status_active`

## What Is Not Approved Here

This review does not approve any of the following variables or concepts:

- `std_invasive_mechanical_ventilation_active`
- `std_noninvasive_ventilation_active`
- `std_high_flow_nasal_cannula_active`
- `std_supplemental_oxygen_active`
- respiratory-support-free days
- broad respiratory support active

## Conclusion

Amsterdam `processitems` itemid `12635 / Tracheostoma` is narrow enough to serve as the approved same-name source for `std_tracheostomy_status_active` when kept separate from ventilation, NIV/CPAP, oxygen-device, and tracheostomy-care evidence.
