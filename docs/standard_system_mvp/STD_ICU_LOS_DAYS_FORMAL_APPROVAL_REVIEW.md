# std_icu_los_days Formal Approval Review

Last updated: 2026-04-25

## Approval Verdict

Formal decision:

- `std_icu_los_days` is approved as the first governed class-2 variable under the current `baseline_summary_window_numeric` approval standard

Blocking-findings judgment:

- no blocking semantic finding remains
- no blocking runtime-evidence finding remains
- no blocking public-card publication issue remains

Governance outcome completed during this review:

- the first class-2 public `variable_spec.json` is now locked for `std_icu_los_days`
- reviewed mapping specs now exist for both `MIMIC-IV-3.1` and `AmsterdamUMCdb-1.0.2`
- the first governed class-2 `execution.py` now exists and has closed on both databases with execute-mode runtime evidence and rerun reproducibility evidence

## Scope

This review covers:

- `docs/standard_system_mvp/std_icu_los_days/variable_spec.json`
- `docs/standard_system_mvp/std_icu_los_days/mapping_spec_mimic_iv_3_1.json`
- `docs/standard_system_mvp/std_icu_los_days/mapping_spec_amsterdamumcdb_1_0_2.json`
- `docs/standard_system_mvp/std_icu_los_days/execution.py`
- current governed runtime evidence on `MIMIC-IV-3.1`
- current governed runtime evidence on `AmsterdamUMCdb-1.0.2`
- `docs/std_variable_cards/std_icu_los_days.md`

## Current Approved Meaning

The approved current meaning is:

- one retained numeric duration row per ICU stay or ICU-semantic stay-equivalent row
- full ICU-stay interval duration in days
- ICU admission anchor family
- not a raw event stream
- not hospital length of stay
- not a first-day or partial-window summary

Canonical representation:

- canonical unit: `days`
- current storage/display rule: `round(3)`
- current class-2 summary subclass: `duration_summary`

## Current Database Implementations Reviewed

### MIMIC-IV-3.1

Current approved implementation:

- primary source table: `icu.icustays`
- current retained primary duration field: `icu_icustays.los`
- audit-only rounded reference field: `icustay_detail.los_icu`
- retained output summary:
  - `total_rows = 94,458`
  - `observed_rows = 94,444`
  - `missing_outtime_rows = 14`
  - `p50 = 1.966 days`
  - `p99 = 26.439 days`
  - `max = 226.403 days`
- current governed runtime status:
  - first execute-mode runtime validator: `pass`
  - rerun reproducibility gate: `pass`

Current interpretation boundary:

- this is the direct ICU-stay duration summary for `stay_id`
- the current same-name approval keeps `icu_icustays.los` as primary and does not silently switch the retained source to rounded `icustay_detail.los_icu`

### AmsterdamUMCdb-1.0.2

Current approved implementation:

- primary source table: `admissions_core`
- current retained primary duration rule: raw `admittedat` / `dischargedat` offsets converted to days
- audit-only reported summary field: `lengthofstay`
- approved same-name scope: `location in (IC, IC&MC, MC&IC)`
- retained output summary:
  - `total_rows = 18,386`
  - `observed_rows = 18,386`
  - `zero_duration_rows = 3`
  - `p50 = 1.244 days`
  - `p99 = 52.706 days`
  - `max = 237.366 days`
- current governed runtime status:
  - first execute-mode runtime validator: `pass`
  - rerun reproducibility gate: `pass`

Current interpretation boundary:

- raw `admissionid` is treated as the Amsterdam ICU-semantic stay-equivalent identifier and normalized to `stay_id`
- `MC`-only admissions remain outside this same-name ICU LOS contract
- the retained primary duration stays anchored to raw offsets rather than the reported `lengthofstay` summary field

## Official-Source Alignment Review

Current official-alignment judgment: acceptable.

### MIMIC-IV-3.1

The current MIMIC implementation aligns with the official source surface because:

- `MIMIC-IV` `v3.1` is the active official dataset release on PhysioNet
- the official MIT-LCP `icustay_detail.sql` code path derives `los_icu` from `icu_outtime - icu_intime` and rounds it, which is consistent with treating full-precision ICU-stay duration as the primary concept and the rounded derived table as reference support

That means the present `std_icu_los_days` MIMIC mapping is not an arbitrary private interpretation.

It is acceptable relative to the current official dataset and official code surface.

### AmsterdamUMCdb-1.0.2

The current Amsterdam implementation aligns with the official source surface because:

- the official AmsterdamUMCdb repository describes the legacy `admissions` table as admissions data for patients admitted to the ICU or MCU
- the official AmsterdamUMCdb paper reports `18,386` ICU admissions and an ICU-subgroup median LOS of about `1.25` days, which matches the ICU-semantic scope retained by the current asset

The current approved source-choice difference is also explicit:

- the official paper's descriptive ICU LOS summary is reproduced by reported `lengthofstay / 24`
- the retained standardized asset intentionally uses raw `admittedat` / `dischargedat` offsets as timing truth

That is an approved source-choice difference, not an unexplained mismatch.

## Public Research Plausibility Review

Current plausibility judgment: acceptable.

For `MIMIC-IV-3.1`:

- the current governed retained distribution has `p50 = 1.966 days`
- public MIMIC ICU literature commonly reports ICU LOS medians around the low single-digit day range
- one public MIMIC-IV ED-to-ICU cohort paper reports a median ICU LOS of `1.80` days, which is close enough to argue against an obvious unit or anchor mistake

For `AmsterdamUMCdb-1.0.2`:

- the current governed retained distribution has `p50 = 1.244 days`
- the official AmsterdamUMCdb ICU subgroup paper summary reports a median ICU LOS of `1.25` days

For cross-database interpretation:

- `MIMIC-IV-3.1` current `p50 = 1.966`
- `AmsterdamUMCdb-1.0.2` current `p50 = 1.244`

Those medians are not identical, which is expected because the databases represent different clinical populations and ICU mixes.

What matters here is:

- both are clearly in the same unit family
- both have plausible ICU-scale durations
- neither distribution suggests a hidden hours-versus-days error or a hospital-LOS-versus-ICU-LOS mix-up

## Public-Card Review

Current judgment:

- the public card is publication-safe
- the public card keeps the stay-level interpretation boundary
- the public card keeps the Amsterdam primary-source caution
- the public card keeps the MIMIC primary-field caution

Clarification:

- the per-database `latest_review_date` shown on the current public card should still be read as the underlying database-asset review date
- this document is the later class-2 governed content-approval note for the public standard-system MVP surface

## Final Approval Decision

`std_icu_los_days` now satisfies the current approval bar for the first class-2 governed MVP:

- machine-readable variable lock present
- reviewed mapping specs present for both databases
- governed `execution.py` present
- execute-mode runtime evidence present on both databases
- rerun reproducibility evidence present on both databases
- public interpretation acceptable
- official-source alignment acceptable
- public research plausibility acceptable

Formal conclusion:

- approve `std_icu_los_days` as the first closed class-2 governed MVP

## Boundary Of This Approval

This note does not claim:

- that every future class-2 variable should use the same structure as ICU LOS
- that all baseline or first-day summary variables can skip class-specific review because this duration-summary example passed
- that all future databases automatically inherit approval

This note does claim:

- the current public `std_icu_los_days` governed MVP surface is formally content-approved
- the repository now has one real dual-database closure for class 2
- the class-2 runner surface is now concrete enough to support the next batch of class-2 variables

## Source Pointers

Public official/source references used in this review:

- MIMIC-IV v3.1 official dataset page: <https://physionet.org/content/mimiciv/3.1/>
- MIT-LCP `icustay_detail.sql` official code surface: <https://raw.githubusercontent.com/MIT-LCP/mimic-code/main/mimic-iv/concepts_postgres/demographics/icustay_detail.sql>
- AmsterdamUMCdb official repository README: <https://github.com/AmsterdamUMC/AmsterdamUMCdb>
- AmsterdamUMCdb official paper: <https://pmc.ncbi.nlm.nih.gov/articles/PMC8132908/>
- public MIMIC-IV cohort paper with ICU LOS around 1.80 days in the analyzed cohort: <https://pmc.ncbi.nlm.nih.gov/articles/PMC11973772/>
