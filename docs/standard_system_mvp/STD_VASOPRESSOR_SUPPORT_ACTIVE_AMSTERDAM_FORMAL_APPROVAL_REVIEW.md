# std_vasopressor_support_active Amsterdam Formal Approval Review

Review date: 2026-05-02

Status: reviewed_approved

Database: `AmsterdamUMCdb-1.0.2`

Standard variable: `std_vasopressor_support_active`

## Decision

AmsterdamUMCdb is approved for the same-name `std_vasopressor_support_active` asset as a positive-only binary state episode variable.

The approved source boundary is:

- retain continuous `drugitems` syringe-pump rows with ordercategoryid `65`
- retain itemid `6818 / Adrenaline (Epinefrine)` as `vasopressor`
- retain itemid `7179 / Dopamine (Inotropin)` as `mixed_pressor_inotrope`
- retain itemid `7229 / Noradrenaline (Norepinefrine)` as `vasopressor`
- retain itemid `12467 / Terlipressine (Glypressin)` as `vasopressor`
- retain itemid `19929 / Fenylefrine` as `vasopressor`
- require non-null positive start/stop/duration, `iscontinuous = 1`, and `rate > 0`
- merge overlapping or exactly contiguous approved source intervals within the same local admission
- emit only true positive support episodes

## Source Boundary

The source audit found `295,488` Amsterdam candidate syringe-pump rows, of which `295,043` passed the validity filter and `445` were excluded as invalid source rows.

Valid source-row counts:

- `7229 / Noradrenaline (Norepinefrine)`: `261,266`
- `7179 / Dopamine (Inotropin)`: `31,417`
- `6818 / Adrenaline (Epinefrine)`: `2,076`
- `12467 / Terlipressine (Glypressin)`: `243`
- `19929 / Fenylefrine`: `41`

After interval union, the approved output retains:

- output rows: `23,885`
- unique `subject_id`: `12,394`
- unique `stay_id`: `13,487`

The output joins `admissions_core` by `admissionid` to populate `subject_id` from `patientid`. The raw Amsterdam `admissionid` is retained as the ICU/MC stay-equivalent `stay_id`.

## Adjacent-State Rules

The following adjacent or same-family evidence is excluded from this same-name output:

- `7178 / Dobutamine (Dobutrex)`: pure inotrope
- `9126 / Fenylefrine`: topical/non-IV phenylephrine evidence
- ordercategoryid `24` bolus or injection rows
- ordercategoryid `29` non-syringe-pump row
- ordercategoryid `69` topical/non-IV row
- `16962 / SEPSIS_VASOPRESSOREN`: screening or phenotype list evidence
- norepinephrine-equivalent dose
- septic-shock onset
- vasopressor-free days
- agent-specific vasopressor episode detail

The approved source scope is any vasopressor-capable support active state, not shock truth and not a dose or agent-specific exposure table.

## Output Summary

- output rows: `23,885`
- unique `subject_id`: `12,394`
- unique `stay_id`: `13,487`
- short episodes less than or equal to 15 minutes: `299`
- short episodes less than or equal to 60 minutes: `1,635`
- prolonged episodes greater than or equal to 7 days: `542`
- duration minutes min / p50 / p90 / p99 / max: `1 / 731 / 4,487.6 / 14,222.6 / 71,308`
- episodes per stay p50 / p90 / p99 / max: `1 / 3 / 10 / 38`
- mixed pressor/inotrope episodes: `7,671`
- mixed pressor/inotrope-only episodes: `5,800`
- pure vasopressor episodes: `18,085`

Amsterdam location distribution:

- `IC`: `19,176`
- `IC&MC`: `3,353`
- `MC`: `1,228`
- `MC&IC`: `128`

## Governed Evidence

Approved mapping spec:

- `docs/standard_system_mvp/std_vasopressor_support_active/mapping_spec_amsterdamumcdb_1_0_2.json`

Formal local implementation:

- `Methods/Clinical_Database/local_work/Layer 5/AmsterdamUMCdb-1.0.2/std_vasopressor_support_active/extract_code/Extract_Code_std_vasopressor_support_active.py`

Formal output:

- `Methods/Clinical_Database/local_work/Layer 3/AmsterdamUMCdb-1.0.2/treatment_state/std_vasopressor_support_active/std_vasopressor_support_active_long.parquet`

Governed runtime evidence:

- `docs/standard_system_mvp/std_vasopressor_support_active/runtime/amsterdamumcdb_1_0_2_first_real_execution/`
- `docs/standard_system_mvp/std_vasopressor_support_active/runtime/amsterdamumcdb_1_0_2_rerun_repro_check/`

Rerun reproducibility:

- `overall_status=pass`
- baseline process batch: `20260502T090715Z_AmsterdamUMCdb-1.0.2_std_vasopressor_support_active`
- rerun process batch: `20260502T090735Z_AmsterdamUMCdb-1.0.2_std_vasopressor_support_active`

## What Is Not Approved Here

This review does not approve any of the following variables or concepts:

- `std_vasopressor_support_agent_episode`
- norepinephrine-equivalent dose variables
- septic-shock onset variables
- vasopressor-free-day outcome variables
- pure inotrope support active
- per-minute vasopressor grids
- broad treatment-support composite states

## Conclusion

Amsterdam continuous syringe-pump `drugitems` rows for the approved vasopressor-capable itemids are narrow enough to serve as the reviewed-approved same-name source for `std_vasopressor_support_active` when governed by the documented exclusions and overlap-union rule.
