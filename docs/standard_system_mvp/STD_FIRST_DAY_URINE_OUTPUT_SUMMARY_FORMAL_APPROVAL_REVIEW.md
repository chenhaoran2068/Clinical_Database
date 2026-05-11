# std_first_day_urine_output_summary Formal Approval Review

Last updated: 2026-04-25

## Approval Verdict

Formal decision:

- `std_first_day_urine_output_summary` is approved as the first governed Class-2 `window_summary` variable under the current `baseline_summary_window_numeric` approval standard

Blocking-findings judgment:

- no blocking MIMIC semantic finding remains
- no blocking MIMIC runtime-evidence finding remains
- no blocking public-card publication issue remains after public-card normalization

Scope boundary:

- this is a `MIMIC-IV-3.1` governed approval
- this is not yet a dual-database approval
- `AmsterdamUMCdb-1.0.2` has no approved same-name mapping under this first-day urine-output window contract yet

## Scope

This review covers:

- `docs/standard_system_mvp/std_first_day_urine_output_summary/variable_spec.json`
- `docs/standard_system_mvp/std_first_day_urine_output_summary/mapping_spec_mimic_iv_3_1.json`
- `docs/standard_system_mvp/std_first_day_urine_output_summary/execution.py`
- governed runtime evidence on `MIMIC-IV-3.1`
- `docs/std_variable_cards/std_first_day_urine_output_summary.md`
- local reviewed-approved MIMIC Layer 5 evidence for `std_first_day_urine_output_summary`

## Current Approved Meaning

The approved current meaning is:

- one retained row per ICU stay
- first-day ICU urine-output total in mL
- window start: ICU `intime`
- window end: ICU `intime + 24 hours`
- aggregation: sum qualifying approved ICU urine-output event rows inside the first-day window
- no-source-row behavior: retain the ICU stay row with `first_day_urine_output_ml = NULL`
- partial-window behavior: retain partial-window caution fields, but do not clip the official aggregation numerator by ICU outtime

This variable is:

- a Class-2 `window_summary`
- a stay-level summary
- official MIMIC first_day_urine_output-compatible

This variable is not:

- a raw urine-output event stream
- total intake-output balance
- urine-output rate normalized by weight or time
- a zero-filled missing-output variable
- an Amsterdam same-name approval

## Current MIMIC-IV-3.1 Implementation Reviewed

Current approved implementation:

- upstream source asset: `std_icu_urine_output_event`
- anchor source: `icu.icustays`
- official reference asset: source-supplied derived `first_day_urine_output`
- source event window: `charttime >= intime` and `charttime <= intime + 24 hours`
- target retained key: `stay_id`
- retained primary value field: `first_day_urine_output_ml`
- official profile class: `official_mimic_first_day_urine_output_sql_compatible_v1`

Current retained output summary:

- `row_count = 94,458`
- `stays_with_first_day_urine = 89,442`
- `stays_without_first_day_urine = 5,016`
- `complete_24h_rows = 74,829`
- `partial_window_rows = 19,629`
- `total_first_day_urine_output_ml = 152,814,080.4930113`
- `median_first_day_urine_output_ml = 1,475.0`

Official-reference comparison:

- `official_reference_row_count = 94,458`
- `official_reference_nonnull_rows = 89,442`
- `official_reference_total_first_day_urine_output_ml = 152,814,080.4930113`
- `official_compare_compared_rows = 94,458`
- `official_compare_exact_match_rows = 94,458`
- `official_compare_official_only_rows = 0`
- `official_compare_local_only_rows = 0`
- `official_compare_subject_mismatch_rows = 0`
- `official_compare_value_mismatch_rows = 0`

Current governed runtime status:

- static governed spec validation: `pass`
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

- `MIMIC-IV v3.1` is the active official dataset release used by the repository
- the MIMIC ICU module exposes `outputevents` as ICU output-event data and `icustays` as the ICU stay timing table
- the official MIMIC code surface has a `urine_output.sql` concept and a `first_day_urine_output.sql` concept
- the current local implementation exactly matches the source-supplied derived first-day urine-output reference asset on all `94,458` rows

The upstream urine-event source is also locked to the official urine item family:

- `226559`: Foley
- `226560`: Void
- `226561`: Condom Cath
- `226584`: Ileoconduit
- `226563`: Suprapubic
- `226564`: R Nephrostomy
- `226565`: L Nephrostomy
- `226567`: Straight Cath
- `226557`: R Ureteral Stent
- `226558`: L Ureteral Stent
- `227488`: GU Irrigant Volume In
- `227489`: GU Irrigant/Urine Volume Out

Interpretation:

- this variable correctly exercises the `window_summary` subclass
- the official first-day SQL compatibility is stronger than ordinary plausibility matching because the governed output exactly matches the official reference output
- the NULL behavior is part of the approved contract, not an unresolved missing-data accident

## Public Research Plausibility Review

Current plausibility judgment: acceptable.

The current retained output has:

- median first-day urine output: `1,475.0 mL`
- first-day observed urine rows in `89,442 / 94,458` ICU stays

This is plausible for adult ICU first-day urine-output summaries.

The strongest plausibility evidence is the exact match to the official MIMIC first-day urine-output reference asset.

Additional clinical interpretation:

- first-day urine output is often interpreted against oliguria thresholds and renal-support contexts
- this variable intentionally does not compute urine-output rate because rate logic requires additional body-weight and time-window decisions
- users needing KDIGO-style urine-output-rate logic should use or build a separate weight-aware derivative rather than overloading this total-output summary

## Public-Card Review

Current judgment:

- the public card is publication-safe
- the public card correctly states current approval is `MIMIC-IV-3.1` only
- the public card now uses `mL` as the public unit
- the public card avoids publishing a malformed localized Chinese name
- the public card preserves the key warnings:
  - NULL means no qualifying first-day urine row, not zero
  - the official numerator is not clipped by ICU outtime
  - urine-output-rate logic remains deferred

## Final Approval Decision

`std_first_day_urine_output_summary` now satisfies the current approval bar for a MIMIC-only Class-2 governed MVP:

- machine-readable variable lock present
- reviewed MIMIC mapping spec present
- governed `execution.py` present
- execute-mode runtime evidence present on `MIMIC-IV-3.1`
- rerun reproducibility evidence present on `MIMIC-IV-3.1`
- public interpretation acceptable
- official-source alignment acceptable
- public plausibility acceptable
- public card normalized for the governed class-2 closure

Formal conclusion:

- approve `std_first_day_urine_output_summary` as the first governed Class-2 `window_summary` example

## Boundary Of This Approval

This note does not claim:

- that Amsterdam has an approved same-name implementation
- that missing urine output should be interpreted as zero
- that first-day urine-output rate is approved here
- that all intake-output balance variables should use this same contract
- that all future first-day variables can skip separate review

This note does claim:

- the current public `std_first_day_urine_output_summary` MIMIC governed MVP surface is formally content-approved
- Class 2 now has an approved representative of all three current summary subclasses:
  - `duration_summary`
  - `baseline_snapshot`
  - `window_summary`

## Recommended Next Action

Recommended next class-2 action:

- update the current Class-2 closure surface so it records that `window_summary` is now represented
- then choose whether to continue a small MIMIC Class-2 batch or attempt a careful Amsterdam mapping review for this variable

Do not:

- force Amsterdam into same-name approval until its urine-output source semantics, ICU/MCU stay scope, time anchors, and NULL/zero behavior are explicitly reviewed

## Source Pointers

Public official/source references used in this review:

- MIMIC-IV v3.1 official dataset page: <https://physionet.org/content/mimiciv/3.1/>
- MIMIC-IV ICU module documentation: <https://lcp.mit.edu/mimic.mit.edu/docs/IV/modules/icu/>
- MIMIC official `first_day_urine_output.sql` concept: <https://raw.githubusercontent.com/MIT-LCP/mimic-code/main/mimic-iv/concepts_postgres/firstday/first_day_urine_output.sql>
- MIMIC official `urine_output.sql` concept: <https://raw.githubusercontent.com/MIT-LCP/mimic-code/main/mimic-iv/concepts_postgres/measurement/urine_output.sql>
- MIMIC FHIR `outputevents` item-code surface: <https://mimic.mit.edu/fhir/CodeSystem-mimic-outputevents-d-items.html>
