# std_heart_rate Formal Approval Review

Last updated: 2026-04-24

## Approval Verdict

Formal decision:

- `std_heart_rate` is approved under the current class-1 content-approval standard

Blocking-findings judgment:

- no blocking semantic finding remains
- no blocking runtime-evidence finding remains
- no blocking public-card publication issue remains

Governance repair completed during this review:

- the older `MIMIC-IV-3.1` pilot runtime evidence was refreshed into the same current runtime-evidence contract used by the later class-1 variables
- the current `MIMIC-IV-3.1` mapping note was tightened so `itemid 211` is treated as a legacy cross-version code note rather than an active `MIMIC-IV-3.1` candidate source
- the public `variable_spec.json` now explicitly carries the shared `event_level_numeric_primary_source` class lock so `std_heart_rate` no longer relies on wrapper-side backward compatibility

## Scope

This review covers:

- `docs/standard_system_mvp/std_heart_rate/variable_spec.json`
- `docs/standard_system_mvp/std_heart_rate/mapping_spec_mimic_iv_3_1.json`
- `docs/standard_system_mvp/std_heart_rate/mapping_spec_amsterdamumcdb_1_0_2.json`
- `docs/standard_system_mvp/std_heart_rate/execution.py`
- current governed runtime evidence on `MIMIC-IV-3.1`
- current governed runtime evidence on `AmsterdamUMCdb-1.0.2`
- `docs/std_variable_cards/std_heart_rate.md`

## Current Approved Meaning

The approved current meaning is:

- one row per time-stamped heart-rate measurement event
- raw measured numeric heart-rate values only
- not a baseline variable
- not a stay-level summary
- not a derived rhythm or score variable

Canonical representation:

- canonical unit: `bpm`
- current cleaned retained range: `[0, 250] bpm`
- current storage/display rule: integer-valued retained output

## Current Database Implementations Reviewed

### MIMIC-IV-3.1

Current approved implementation:

- primary source package/table: `icu.chartevents`
- current formal source code: `itemid 220045`
- current official local dictionary meaning: `Heart Rate`
- retained output summary:
  - `total_rows = 8,752,069`
  - `kept_rows = 8,752,005`
  - `excluded_outlier_rows = 64`
  - `p50 = 85.0`
  - `p99 = 136.0`
  - `unique_stay_id = 94,437`
- current governed runtime status:
  - first execute-mode runtime validator: `pass`
  - rerun reproducibility gate: `pass`

Current interpretation boundary:

- this is the direct charted ICU heart-rate stream currently locked to `220045`
- this approval does not silently widen `std_heart_rate` to every historical or cross-version heart-rate code family

### AmsterdamUMCdb-1.0.2

Current approved implementation:

- primary source table: `numericitems`
- current formal source code: `itemid 6640`
- current official local dictionary meaning: `Hartfrequentie / heart rate`
- source unit: `/min`, normalized to canonical `bpm`
- retained output summary:
  - `total_rows = 37,732,398`
  - `kept_rows = 37,732,286`
  - `excluded_outlier_rows = 112`
  - `raw_p50 = 86.0`
  - `raw_p99 = 135.0`
  - `unique_admissions = 23,105`
- current governed runtime status:
  - first execute-mode runtime validator: `pass`
  - rerun reproducibility gate: `pass`

Current interpretation boundary:

- raw `admissionid` is treated as the Amsterdam ICU-semantic stay-equivalent identifier and normalized to `stay_id`
- Amsterdam retained time should be interpreted as offset time, not public wall-clock datetime

## Official-Source Alignment Review

Current official-alignment judgment: acceptable.

### MIMIC-IV-3.1

The current MIMIC implementation aligns with both:

- the local reviewed `icu_d_items` dictionary row showing `220045 = Heart Rate`, `Routine Vital Signs`, `bpm`, `chartevents`, `Numeric`
- the current MIT-LCP `mimic-iv` `vitalsign.sql` concept surface, which defines `heart_rate` from `itemid IN (220045)` rather than widening the official `mimic-iv` concept here to `211`

That means the present `std_heart_rate` MIMIC mapping is not merely a private choice.
It is acceptable relative to the current official concept surface.

### AmsterdamUMCdb-1.0.2

The current Amsterdam implementation aligns with both:

- the local reviewed legacy dictionary row showing `6640 = Hartfrequentie / heart rate`, unit `/min`, table `numericitems`
- the official AmsterdamUMCdb repository description that legacy `numericitems` stores numerical measurements and observations within ICU/MCU admissions

That means the Amsterdam mapping is also semantically aligned with the official source surface.

## Public Research Plausibility Review

Current plausibility judgment: acceptable.

For `MIMIC-IV-3.1`:

- the current governed retained distribution has `p50 = 85.0 bpm`
- published MIMIC-IV ICU cohort tables report heart-rate medians in the low-to-mid `80s bpm`, for example `82.0` and `85.0` bpm in the linked public cohort table

For cross-database comparison:

- `MIMIC-IV-3.1` current `p50 = 85.0`
- `AmsterdamUMCdb-1.0.2` current `raw_p50 = 86.0`
- `MIMIC-IV-3.1` current `p99 = 136.0`
- `AmsterdamUMCdb-1.0.2` current `raw_p99 = 135.0`

So the two approved database implementations are closely aligned in their central and high-percentile ranges.
That does not prove universal equivalence for every future cohort, but it does argue against an obvious semantic or unit mismatch.

## Public-Card Review

Current judgment:

- the public card is publication-safe
- the public card keeps the event-level interpretation boundary
- the public card keeps the Amsterdam time-semantics caution

Clarification:

- the per-database `latest_review_date` shown on the current public card should still be read as the underlying database-asset review date
- this document is the later class-1 content-approval note that closes the broader current approval decision

## Final Approval Decision

`std_heart_rate` now satisfies the same approval bar used for the current class-1 reviewed variables:

- machine-readable variable lock present
- reviewed mapping specs present
- governed `execution.py` present
- execute-mode runtime evidence present
- rerun reproducibility evidence present
- public interpretation acceptable
- official-source alignment acceptable
- public research plausibility acceptable

Formal conclusion:

- approve `std_heart_rate` into the current broader class-1 approval closure

## Boundary Of This Approval

This note does not claim:

- that all future databases automatically inherit approval
- that baseline or summarized heart-rate variables should reuse the same `std_heart_rate` name
- that every future heart-rate-family implementation may ignore database-specific timing cautions

This note does claim:

- the current public `std_heart_rate` governed MVP surface is formally content-approved
- the variable is now strong enough to join the broader current class-1 closure note

## Source Pointers

Public official/source references used in this review:

- MIT-LCP `mimic-iv` `vitalsign.sql`: <https://raw.githubusercontent.com/MIT-LCP/mimic-code/main/mimic-iv/concepts_postgres/measurement/vitalsign.sql>
- AmsterdamUMCdb official repository README: <https://github.com/AmsterdamUMC/AmsterdamUMCdb>
- public MIMIC-IV cohort table with heart-rate medians in the low-to-mid 80s bpm: <https://pmc.ncbi.nlm.nih.gov/articles/PMC11701063/>
