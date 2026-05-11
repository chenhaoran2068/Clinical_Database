# Class-2 First MVP Selection

Last updated: 2026-04-24

## Why this note exists

The temporary next-stage execution plan says Phase 1 should do three things before any class-2 implementation starts:

1. define class 2 formally
2. choose the first class-2 dual-database MVP variable
3. write the acceptance criteria before execution begins

This note closes those Phase-1 selection tasks.

## Class-2 interpretation used here

Class 2 is:

- `baseline_summary_window_numeric`

Meaning:

- one retained numeric row per anchor-qualified target entity
- not raw event-level output
- baseline, first-day, window-summary, or duration semantics are part of the variable identity
- anchor/window/aggregation/no-source-row rules must be locked before implementation

## Candidate comparison

| candidate | current public database coverage | class-2 fit | execution complexity | first dual-database MVP suitability | interpretation |
| --- | --- | --- | --- | --- | --- |
| `std_icu_los_days` | `MIMIC-IV-3.1`, `AmsterdamUMCdb-1.0.2` | strong | low to medium | highest | clear one-row-per-stay numeric duration summary with explicit anchor semantics in both databases |
| `std_weight_admission_baseline` | `MIMIC-IV-3.1` only | strong | medium | not first | good baseline-snapshot example, but it does not currently give the required early Amsterdam proof |
| `std_first_day_urine_output_summary` | `MIMIC-IV-3.1` only | medium to strong | medium to high | not first | good window-summary example, but its null semantics and official-compatibility nuances are heavier than needed for the opening dual-database proof |
| `std_sofa_first_day` | `MIMIC-IV-3.1` only | ambiguous | high | not first | score-composite semantics are likely to pull this toward class 8 rather than making it the best first class-2 MVP |

## Selection verdict

The first class-2 dual-database MVP variable should be:

- `std_icu_los_days`

## Why `std_icu_los_days` wins

`std_icu_los_days` is the best first class-2 MVP because it satisfies all of the opening constraints at once:

- already publicly approved in both `MIMIC-IV-3.1` and `AmsterdamUMCdb-1.0.2`
- truly one-row-per-stay numeric output rather than a raw event stream
- depends on explicit anchor and duration logic, so it really exercises class-2 semantics
- simpler than first-day urine-output summaries or score-family summaries
- likely to expose class-2 build-rule fields without immediately forcing a score/composite framework

It is also a useful stress test for a key class-2 distinction:

- class 2 is not only "event streams aggregated later"
- it also includes duration summaries whose truth comes from explicit interval boundaries

## Why the other candidates wait

`std_weight_admission_baseline` waits because:

- it is still a very good class-2 candidate
- but it does not currently provide the required opening Amsterdam proof

`std_first_day_urine_output_summary` waits because:

- it is valuable
- but it introduces official-style NULL behavior, first-day window nuances, and supportive-therapy semantics too early for the opening class-2 proof

`std_sofa_first_day` waits because:

- its first-day shape looks class-2-like
- but its score-composite nature risks mixing class-2 and class-8 governance in the very first trial

## Class-2 first MVP acceptance criteria

The first class-2 MVP will count as complete only when all of the following are true.

### Phase-1 pre-implementation criteria

- the class-2 contract exists
- the class-2 skeleton exists
- the first candidate variable is explicitly selected
- the candidate's acceptance criteria are written before implementation

### Variable-spec criteria

The `variable_spec.json` for `std_icu_los_days` must explicitly lock:

- `summary_subclass = duration_summary`
- `target_entity_grain = ICU stay`
- `anchor_family = ICU admission anchor`
- the duration meaning itself rather than a generic "stay summary"
- no-source-row behavior
- whether window bounds or anchor timestamps are required in retained output context

### Mapping-spec criteria

Both `MIMIC-IV-3.1` and `AmsterdamUMCdb-1.0.2` mapping specs must explicitly lock:

- primary source tables or approved upstream assets
- source locator mode
- anchor and interval fields
- target grain
- duration calculation translation
- validation expectations

### Execution criteria

The first class-2 MVP must add a governed `execution.py` that is class-2 aware rather than pretending the class-1 runner already covers summaries.

### Runtime criteria

Both databases must have:

- first execute-mode runtime evidence
- rerun reproducibility evidence
- passing runtime validation
- passing reproducibility validation

### Review criteria

The first class-2 approval review must explicitly judge:

- semantic fit to class 2
- official-source alignment
- public research plausibility
- whether class 2 stays broad enough after a duration-summary opening example

## Interpretation rule after selection

This selection does not mean every class-2 variable should look like ICU LOS.

It means:

- `std_icu_los_days` is the safest and cleanest first dual-database proof
- after that proof, the class should next absorb a more classic baseline/window example such as `std_weight_admission_baseline`

## Current status after selection

This selection note has now been executed.

`std_icu_los_days` has been instantiated as the first class-2 governed MVP with:

- public `variable_spec.json`
- reviewed class-2 mapping specs for `MIMIC-IV-3.1` and `AmsterdamUMCdb-1.0.2`
- the first class-2 governed execution runner
- execute-mode runtime evidence on both databases
- rerun reproducibility evidence on both databases

## Natural next step

The first natural next step after this first class-2 closure was:

1. begin Phase 3 for class 2
2. add the next more classical baseline/window example, with `std_weight_admission_baseline` as the leading candidate
3. then grow a small `MIMIC-IV-3.1` class-2 batch before broader Amsterdam backfill

Current update:

- `std_weight_admission_baseline` has now been instantiated as a governed `MIMIC-IV-3.1` baseline-snapshot example
- Amsterdam remains excluded from that approval because the local Amsterdam candidate is still `built_pending_user_review` and has now been reviewed as not suitable for same-name approval under the current hospital-admission event-baseline contract
- the Amsterdam grouped/proxy candidate has now been split into the separate `std_weight_icu_baseline_grouped_proxy` identity and approved as an Amsterdam-only governed class-2 variable
- `std_first_day_urine_output_summary` has now been instantiated as the first governed `window_summary` example and approved on `MIMIC-IV-3.1` with official first-day urine-output reference matching
- Amsterdam `std_first_day_urine_output_summary` has now also been approved as a same-name implementation after summary-specific mapping, execution, validation, and rerun evidence were built from the approved Amsterdam `std_icu_urine_output_event` stream
- the next class-2 step should therefore continue controlled `MIMIC-IV-3.1` batch expansion rather than re-litigating the already closed Amsterdam first-day urine-output summary approval

Current closure note:

- `CLASS2_CURRENT_APPROVAL_CLOSURE.md` now records the bounded current-stage Class 2 approval
- `CLASS2_TOTAL_CLOSURE_REVIEW_AND_MIMIC_EXPANSION_DECISION.md` now records the total closure review and the next MIMIC-IV-3.1 expansion decision
