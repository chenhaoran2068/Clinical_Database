# std_weight_admission_baseline Formal Approval Review

Last updated: 2026-04-25

## Approval Verdict

Formal decision:

- `std_weight_admission_baseline` is approved as a governed `MIMIC-IV-3.1` class-2 variable under the current `baseline_summary_window_numeric` approval standard

Blocking-findings judgment:

- no blocking MIMIC semantic finding remains
- no blocking MIMIC runtime-evidence finding remains
- no blocking MIMIC public-card publication issue remains

Scope boundary:

- this is a `MIMIC-IV-3.1` governed approval
- this is not yet a dual-database approval
- `AmsterdamUMCdb-1.0.2` has a local candidate asset, but its manifest status remains `built_pending_user_review`; it is therefore excluded from this approval

## Scope

This review covers:

- `docs/standard_system_mvp/std_weight_admission_baseline/variable_spec.json`
- `docs/standard_system_mvp/std_weight_admission_baseline/mapping_spec_mimic_iv_3_1.json`
- `docs/standard_system_mvp/std_weight_admission_baseline/execution.py`
- current governed runtime evidence on `MIMIC-IV-3.1`
- `docs/std_variable_cards/std_weight_admission_baseline.md`
- local reviewed-approved MIMIC Layer 5 evidence for `std_weight_admission_baseline`

## Current Approved Meaning

The approved current meaning is:

- one retained numeric baseline-snapshot row per hospital admission encounter when an eligible source row exists
- admission-start baseline body weight
- canonical unit: `kg`
- current storage/display rule: `round(2)`
- baseline window: `admittime` to `min(dischtime, admittime + 1440 minutes)`
- not a raw weight event stream
- not generic patient-level stable weight
- not ICU-start baseline weight
- not discharge or follow-up weight

Current no-source-row behavior:

- encounters without an eligible cleaned weight event are absent from the retained output rather than retained as null rows
- coverage is audited separately

## Current MIMIC-IV-3.1 Implementation Reviewed

Current approved implementation:

- upstream source asset: `std_weight_event`
- anchor source: `hosp.admissions.admittime`
- discharge clip: `hosp.admissions.dischtime`
- eligible rows: `cleaning_status = kept`, direct `hadm_id`, non-null measurement time, and approved source family
- source priority after closest-to-anchor selection:
  - `admission_weight_kg`
  - `admission_weight_lbs`
  - `daily_weight_kg`
- retained target key: `hadm_id`
- retained provenance key: `selected_stay_id`

Current retained output summary:

- `total_rows = 69,312`
- `unique_subject_id = 54,701`
- `unique_hadm_id = 69,312`
- duplicate `hadm_id` rows: `0`
- required retained fields: `0` nulls
- all-admissions coverage: `69,312 / 546,028 = 0.126939`
- ICU-admissions coverage: `69,312 / 85,242 = 0.81312`
- selected `admission_weight_kg` rows: `68,048`
- selected `admission_weight_lbs` rows: `268`
- selected `daily_weight_kg` rows: `996`

Current retained distribution:

- minimum: `20.0 kg`
- p25: `65.1 kg`
- p50: `77.8 kg`
- p75: `92.7 kg`
- p99: `155.0 kg`
- maximum: `500.0 kg`

Current baseline-offset distribution:

- minimum: `0 minutes`
- p25: `1 minute`
- p50: `1 minute`
- p75: `135 minutes`
- p99: `1357 minutes`
- maximum: `1440 minutes`

Current governed runtime status:

- first execute-mode runtime validator: `pass`
- rerun execute-mode runtime validator: `pass`
- rerun reproducibility gate: `pass`

Stable rerun evidence:

- `primary_output_asset` signature is invariant across reruns
- `preview_csv` signature is invariant across reruns
- stable build-summary fields match across reruns
- process-batch IDs differ as expected between first run and rerun

## Official-Source Alignment Review

Current official-alignment judgment: acceptable for MIMIC.

The current MIMIC mapping is not arbitrary because:

- the active official source release is `MIMIC-IV v3.1`
- the approved source-code family is explicitly limited to ICU `chartevents` weight items
- the local official `icu_d_items` source identifies:
  - `224639`: `Daily Weight`, `kg`, `Numeric`
  - `226512`: `Admission Weight (Kg)`, `kg`, `Numeric`
  - `226531`: `Admission Weight (lbs.)`, `Numeric`
- the public MIMIC FHIR code-system surface also exposes the same item-code family for `chartevents` `d_items`

Interpretation:

- `226512` is the dominant direct admission-weight source
- `226531` is acceptable only because the upstream `std_weight_event` asset already normalizes source values to kilograms
- `224639` is retained only as a lower-priority fallback after closest-to-admission timing and source-priority rules

This preserves the intended baseline semantics while preventing the source-code list from drifting silently.

## Public Research Plausibility Review

Current plausibility judgment: acceptable.

The governed MIMIC output has:

- p25 / p50 / p75 = `65.1 / 77.8 / 92.7 kg`

A public MIMIC-IV cohort table reports a very similar weight distribution in its training/testing cohorts, around:

- training p25 / median / p75 = `65.1 / 77.8 / 92.6 kg`
- testing p25 / median / p75 = `66.0 / 78.5 / 93.3 kg`

This does not prove every retained row is clinically correct, but it strongly argues against:

- hidden pounds-vs-kilograms inversion
- accidental first-day average instead of baseline snapshot
- a broad source-table mismatch
- a severe adult/pediatric population mix-up

## Amsterdam Boundary Review

Current Amsterdam judgment: reviewed and not approved into this public same-name governed MVP.

Reason:

- the Amsterdam local candidate manifest says `current_status = built_pending_user_review`
- the Amsterdam candidate uses `admissions_core.weightgroup` mapped into kilogram proxy values as its primary source
- Amsterdam `admissionid` is ICU/MC local encounter scoped, not a verified hospital-admission anchor equivalent
- the separate Amsterdam candidate review concludes that the asset is useful but should not be promoted into this same variable under the current hospital-admission baseline contract

Therefore:

- it may become useful later
- it is not included as an approved `mapping_spec_amsterdamumcdb_1_0_2.json` in this closure
- it should be handled through a later proxy/binned-variable decision or a stricter Amsterdam continuous-event baseline rebuild before any same-name cross-database approval

Detailed decision:

- `docs/standard_system_mvp/STD_WEIGHT_ADMISSION_BASELINE_AMSTERDAM_CANDIDATE_REVIEW.md`

## Public-Card Review

Current judgment:

- the public card is publication-safe
- the public card correctly states that current approval is `MIMIC-IV-3.1` only
- the public card preserves the key warning that admission baseline weight is not generic patient-level weight
- the public card preserves the key warning that MIMIC coverage is limited by direct linked source availability

## Final Approval Decision

`std_weight_admission_baseline` now satisfies the current approval bar for a MIMIC-only class-2 governed MVP:

- machine-readable variable lock present
- reviewed MIMIC mapping spec present
- governed `execution.py` present
- execute-mode runtime evidence present on `MIMIC-IV-3.1`
- rerun reproducibility evidence present on `MIMIC-IV-3.1`
- public interpretation acceptable
- official-source alignment acceptable
- public research plausibility acceptable
- Amsterdam boundary explicitly excluded until review

Formal conclusion:

- approve `std_weight_admission_baseline` as the first governed class-2 `MIMIC-IV-3.1` baseline-snapshot example after the `std_icu_los_days` dual-database duration-summary closure

## Boundary Of This Approval

This note does not claim:

- that the Amsterdam local candidate is approved
- that every future baseline variable can omit null target rows
- that all weight sources in MIMIC are exhausted
- that this variable should be used as a subject-level stable body weight

This note does claim:

- the current public `std_weight_admission_baseline` MIMIC governed MVP surface is formally content-approved
- the repository now has a classic baseline-snapshot example for class 2, not only a duration-summary example
- the Class 2 rollout can now continue into additional MIMIC baseline/window variables with the same approval bar

## Source Pointers

Public official/source references used in this review:

- MIMIC-IV v3.1 official dataset page: <https://physionet.org/content/mimiciv/3.1/>
- MIMIC FHIR `chartevents` `d_items` code-system surface: <https://mimic.mit.edu/fhir/CodeSystem-mimic-chartevents-d-items.html>
- LOINC body-weight concept anchor `29463-7`: <https://loinc.org/29463-7/>
- public MIMIC-IV cohort table with comparable weight distribution: <https://bmcmedinformdecismak.biomedcentral.com/articles/10.1186/s12911-024-02807-6/tables/1>
