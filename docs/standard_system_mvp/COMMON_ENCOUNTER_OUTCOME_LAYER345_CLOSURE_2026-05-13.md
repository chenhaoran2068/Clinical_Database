# Common Encounter/Outcome Layer 3/4/5 Closure

Date: 2026-05-13

This public-safe note records that the local common encounter/outcome block has passed a Layer 3/4/5 closure audit.

No patient-level data are included here.

## Closed Scope

The local closure audit covered:

- ICU admission and discharge boundary evidence
- hospital discharge boundary evidence
- ICU mortality
- hospital mortality where supported
- post-ICU-admission 28d, 30d, 90d, and 365d mortality
- `std_allcause_death_time_after_icu_admission`

## Closure Result

The local audit found:

- no missing materialized Layer 3 assets
- no Layer 3 row-count mismatch against the Layer 5 MasterIndex
- no missing Layer 4/5 knowledge-package path
- no fixed-horizon policy-status mismatch
- no all-cause death-time policy-status mismatch

## Current Cross-Database Caveats

- eICU-CRD-2.0 does not support post-discharge fixed-horizon mortality under the current source surface.
- SICdb-1.0.8 supports short fixed horizons, but ICU-admission-anchored 365d mortality is blocked because source observation is not guaranteed through ICU+365 days.
- NWICU-0.1.0 fixed-horizon mortality and death-time evidence are approved only as restricted partial evidence because out-of-hospital mortality is not collected.
- AmsterdamUMCdb-1.0.2 fixed-horizon mortality uses owner-confirmed linked vital-status semantics; public field documentation does not itself define a universal fixed censoring horizon.
- `std_allcause_death_time_after_icu_admission` is an evidence bundle for event-time analysis planning, not a binary endpoint by itself.

## Local Production Record

The full local closure report is:

- `Methods/Clinical_Database/local_work/Layer 5/Global/common_encounter_outcomes/2026-05-13_common_encounter_outcome_layer345_closure_audit.md`
