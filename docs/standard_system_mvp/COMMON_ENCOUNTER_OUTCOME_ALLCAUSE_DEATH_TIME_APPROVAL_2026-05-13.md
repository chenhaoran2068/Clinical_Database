# Common Encounter Outcome All-Cause Death-Time Evidence Approval

Date: 2026-05-13

Scope:

- `std_allcause_death_time_after_icu_admission`
- MIMIC-IV-3.1
- AmsterdamUMCdb-1.0.2
- eICU-CRD-2.0
- SICdb-1.0.8
- NWICU-0.1.0

## Public Summary

`std_allcause_death_time_after_icu_admission` is a death-time evidence bundle expressed as continuous 24-hour days after ICU admission. It is intended for event-time review, custom horizon derivation, and survival-analysis planning.

It is not a standalone binary endpoint. Users must evaluate the companion source, precision, observation-status, censoring-status, and conflict fields before analysis.

## Approved Database Scope

| Database | Approval scope | Key limitation |
|---|---|---|
| MIMIC-IV-3.1 | Approved death-time evidence bundle | Use with MIMIC death follow-up/censoring semantics; unresolved severe conflicts remain missing. |
| AmsterdamUMCdb-1.0.2 | Approved under linked vital-status interpretation | Public documentation confirms `dateofdeath`, but fixed censoring horizon is owner-confirmed rather than explicitly documented as a universal public rule. |
| eICU-CRD-2.0 | Approved discharge-boundary death-time proxy only | No approved general post-discharge death follow-up in the current source surface. |
| SICdb-1.0.8 | Approved death-time bundle with 365-day censoring limitation | Short horizons are reviewable; ICU-anchored 365d is incomplete for rows with censoring before 365 days. |
| NWICU-0.1.0 | Approved restricted partial death-time evidence bundle | Out-of-hospital mortality is not collected; missing `patients.dod` is not complete all-cause survival. |

## NWICU-Specific Approval Boundary

NWICU is approved only as restricted partial recorded-death / in-system survival evidence.

Approved NWICU source logic:

1. Use exact same-hospital `admissions.deathtime` when safely interpretable.
2. Use patient-level recorded `patients.dod` when exact same-hospital death time is unavailable.
3. Correct supported date-only or near-boundary death conflicts to day 0 with retained conflict flags.
4. Use status-derived death-boundary proxies only when death status evidence supports them.
5. Treat later in-system hospital/ICU contact as survival/censoring evidence only for horizons it reaches.
6. Keep rows missing death and missing sufficient later in-system survival evidence as `NA`.

NWICU fixed-horizon interpretation remains restricted partial:

- 28d: 3,912 deaths / 10,061 non-deaths / 14,639 NA
- 30d: 3,969 deaths / 9,829 non-deaths / 14,814 NA
- 90d: 4,787 deaths / 6,424 non-deaths / 17,401 NA
- 365d: 5,632 deaths / 1,757 non-deaths / 21,223 NA

Researchers should not pool NWICU fixed-horizon mortality with complete all-cause mortality datasets without explicit missingness and selection-bias assessment.

## Research Use Rule

For every database, death status variables use:

- death = `1`
- alive / no death through the approved window = `0`
- unknown / blocked / insufficient evidence = `NA`

For death-time evidence bundles, the numeric time value must be interpreted together with:

- source field
- source precision
- observation status
- censoring status
- censoring time
- conflict flag
- precision caution
- completeness class

## Local Production Record

The complete local production approval record remains under:

- `Methods/Clinical_Database/local_work/Layer 5/Global/common_encounter_outcomes/2026-05-13_nwicu_std_allcause_death_time_after_icu_admission_owner_approval.md`
- `Methods/Clinical_Database/local_work/Layer 5/Global/common_encounter_outcomes/2026-05-13_std_allcause_death_time_after_icu_admission_bundle_review.md`
- `Methods/Clinical_Database/local_work/Layer 4/Global/2026-05-13_std_allcause_death_time_after_icu_admission_policy.md`
