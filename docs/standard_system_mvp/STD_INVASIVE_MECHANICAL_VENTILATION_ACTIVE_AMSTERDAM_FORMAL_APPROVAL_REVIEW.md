# std_invasive_mechanical_ventilation_active Amsterdam Formal Approval Review

Review date: 2026-05-02

Status: reviewed_approved

Database: `AmsterdamUMCdb-1.0.2`

Standard variable: `std_invasive_mechanical_ventilation_active`

## Decision

AmsterdamUMCdb is approved for the same-name `std_invasive_mechanical_ventilation_active` asset as a positive-only binary state episode variable.

The approved source boundary is deliberately narrow:

- retain only `processitems` itemid `9328`, label `Beademen`
- emit only true positive episodes
- do not union noninvasive ventilation, CPAP, oxygen delivery, tracheostomy status, ventilator-free days, or broad respiratory-support rows into this same-name asset

## Source Boundary

The candidate source audit found `18,471` raw `9328 / Beademen` interval rows across `15,950` Amsterdam admission identifiers.

The final approved output retains `18,259` rows across `15,879` stay-equivalent identifiers and `14,763` patient identifiers.

The output joins `admissions_core` by `admissionid` to populate `subject_id` from `patientid`. The raw Amsterdam `admissionid` is retained as the ICU/MC stay-equivalent `stay_id`.

## Adjacent-State Rules

The following adjacent process sources are excluded from the same-name invasive ventilation asset:

- `10740 / Beademen non-invasief`: explicit noninvasive ventilation boundary source
- `9671 / CPAP`: CPAP or adjacent noninvasive support boundary source

The following evidence is retained as context or flag evidence only:

- `9325 / Weanen`: retained as a weaning-overlap flag when the `9328` invasive ventilation interval is otherwise accepted
- CPAP/BIPAP mode or device context in listitem evidence: retained as context flags, not source expansion
- oxygen or airway context: retained as context flags, not source expansion
- tracheostomy-like or airway context: retained as context flags, not source expansion

The manual policy excludes `205` same-name boundary-risk rows, withholds `6` possible transition rows, and excludes `1` invalid negative-duration source row.

## Output Summary

- output rows: `18,259`
- unique `subject_id`: `14,763`
- unique `stay_id`: `15,879`
- retained clean rows: `18,061`
- retained rows with weaning flag: `198`
- short episodes less than or equal to 60 minutes: `285`
- prolonged episodes greater than or equal to 7 days: `2,465`
- duration minutes p50: `832`
- duration minutes p95: `23,013.2`
- duration minutes max: `248,286`

Amsterdam location distribution:

- `IC`: `15,486`
- `IC&MC`: `2,393`
- `MC`: `310`
- `MC&IC`: `70`

## Governed Evidence

Approved mapping spec:

- `docs/standard_system_mvp/std_invasive_mechanical_ventilation_active/mapping_spec_amsterdamumcdb_1_0_2.json`

Formal local implementation:

- `Methods/Clinical_Database/local_work/Layer 5/AmsterdamUMCdb-1.0.2/std_invasive_mechanical_ventilation_active/extract_code/Extract_Code_std_invasive_mechanical_ventilation_active.py`

Formal output:

- `Methods/Clinical_Database/local_work/Layer 3/AmsterdamUMCdb-1.0.2/treatment_state/std_invasive_mechanical_ventilation_active/std_invasive_mechanical_ventilation_active_long.parquet`

Governed runtime evidence:

- `docs/standard_system_mvp/std_invasive_mechanical_ventilation_active/runtime/amsterdamumcdb_1_0_2_first_real_execution/`
- `docs/standard_system_mvp/std_invasive_mechanical_ventilation_active/runtime/amsterdamumcdb_1_0_2_rerun_repro_check/`

Rerun reproducibility:

- `overall_status=pass`
- baseline process batch: `20260501T154335Z_AmsterdamUMCdb-1.0.2_std_invasive_mechanical_ventilation_active`
- rerun process batch: `20260501T154342Z_AmsterdamUMCdb-1.0.2_std_invasive_mechanical_ventilation_active`
- invariant primary output hash: `d26cc54173afbedafff7757f583df6d118500784e33019fccfa41801217be60c`

## What Is Not Approved Here

This review does not approve any of the following variables or concepts:

- `std_noninvasive_ventilation_active`
- `std_high_flow_nasal_cannula_active`
- `std_supplemental_oxygen_active`
- `std_tracheostomy_status_active`
- respiratory-support-free days
- broad respiratory support active

Those concepts should remain separate Class 3 candidates in the respiratory-support family.

## Conclusion

`processitems` itemid `9328 / Beademen` is narrow enough to serve as the approved Amsterdam same-name source for invasive mechanical ventilation active when governed by the documented adjacent-state exclusions and context flags.

The Amsterdam asset is now approved as a second database implementation of `std_invasive_mechanical_ventilation_active`, alongside the existing `MIMIC-IV-3.1` implementation.
