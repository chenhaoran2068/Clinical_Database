# Class-1 First-Batch Approval Summary

Last updated: 2026-04-24

## Why this note exists

This note records the first formal content-level approval closure for the current public standard-system MVP class:

- `event_level_numeric_primary_source`

The repository already contains a broader technical MVP surface, but this note is narrower.
It marks which variables have now been reviewed in the team's current approval style and can be treated as the first approved class-1 content batch.

## Scope

This approval summary covers the following `MIMIC-IV-3.1` variables:

- `std_glucose`
- `std_respiratory_rate`
- `std_sodium`
- `std_potassium`
- `std_creatinine`
- `std_spo2`
- `std_temp`
- `std_sbp`
- `std_dbp`
- `std_map`

This note does not merge `std_heart_rate` into the same content-approval batch.

Reason:

- `std_heart_rate` remains the prototype predecessor and technical closure example for the class skeleton
- the current round's formal sequential content review and approval closure was completed on the 10 variables listed above

## Approval standard used in this round

A variable is considered approved in this note only when all of the following are true:

- `variable_spec.json` and reviewed mapping spec exist in public form
- governed `execution.py` exists
- first execute-mode runtime evidence passes validation
- rerun reproducibility evidence passes
- public card is publication-safe and explains the current semantic boundary clearly enough
- official-source alignment is acceptable
- public research plausibility is acceptable

In short:

- machine-readable lock present
- governed execution present
- runtime evidence present
- rerun evidence present
- public interpretation reviewed

## Batch status

Formal status:

- approved as the first reviewed class-1 content batch on `MIMIC-IV-3.1`

Current interpretation:

- this is the first reviewed-approved batch for the class
- it is strong enough to serve as the repository's first real class-1 approval baseline
- it is not yet the same thing as full approval for every class-1 variable in the repository

## Approved variables

| variable_id | family | total_rows | kept_rows | central distribution check | key approval interpretation |
| --- | --- | --- | --- | --- | --- |
| `std_glucose` | chemistry | `3,621,278` | `3,621,055` | `p50=110.0`, `p99=356.0` | official chemistry route and public plausibility both acceptable |
| `std_respiratory_rate` | vital sign | `8,636,655` | `8,636,179` | `p50=19.0`, `p99=37.0` | direct ICU respiratory-rate stream approved; current scope is intentionally narrower than every respiratory-rate-related family in MIMIC |
| `std_sodium` | chemistry | `4,110,683` | `4,110,676` | `p50=139.0`, `p99=149.0` | official chemistry route and public plausibility both acceptable |
| `std_potassium` | chemistry | `4,147,219` | `4,147,189` | `p50=4.1`, `p99=6.1` | official chemistry route and public plausibility both acceptable |
| `std_creatinine` | chemistry | `4,317,389` | `4,316,838` | `p50=0.9`, `p99=7.7` | official chemistry route and public plausibility both acceptable |
| `std_spo2` | oxygen saturation | `8,567,015` | `8,566,275` | `p50=97.0`, `p99=100.0` | direct ICU SpO2 stream approved; SaO2 and ED oxygen-saturation families remain intentionally separate |
| `std_temp` | temperature | `2,446,467` | `2,444,580` | `kept_p50=36.9`, `kept_p99=39.0` | current ordinary ICU body-temperature stream approved with explicit source-family normalization |
| `std_sbp` | blood pressure | `17,383,591` | `17,383,376` | `p50=117.0`, `p99=180.0` | official BP item family accepted; invasive/noninvasive/combined are governed representations, not averaging |
| `std_dbp` | blood pressure | `17,380,746` | `17,379,333` | `p50=61.0`, `p99=107.0` | official BP item family accepted; invasive/noninvasive/combined are governed representations, not averaging |
| `std_map` | blood pressure | `17,589,912` | `17,578,420` | `p50=77.0`, `p99=125.0` | approved as direct-first MAP with explicit same-time SBP/DBP fallback only when direct MAP is absent |

## Runtime and rerun closure

For all 10 variables above:

- first execute-mode runtime evidence passes
- rerun reproducibility report passes
- governed public runtime directories remain validator-clean

For `std_map`, the current explicit fallback remains limited and reviewable:

- `origin__direct = 17,382,175`
- `origin__derived_same_time_sbp_dbp = 207,737`
- derived share is approximately `1.18%`

That means the current `std_map` approval is not based on broad silent derivation.
It is based on:

- direct MAP as the default
- small governed fallback coverage
- explicit public warning that `measurement_origin` should be used when direct-only analysis is required

## Official-source alignment summary

Current official-alignment judgment for this batch:

- chemistry variables are aligned with the official MIMIC chemistry source families and remain compatible with MIT-LCP chemistry concept logic
- respiratory rate is aligned with the official direct ICU respiratory-rate item family currently chosen for the first retained build
- SpO2 is aligned with the direct ICU SpO2 item family currently chosen for the first retained build
- blood-pressure variables use the same official MIMIC BP item families that appear in the MIT-LCP vital-sign concept surface

Important blood-pressure interpretation rule:

- `std_sbp` and `std_dbp` are same-family-with-stronger-governance versions of the official MIMIC BP concept surface
- `std_map` is not a literal copy of MIT-LCP `mbp`
- `std_map` is approved here as a stricter governed variable:
  - direct MAP preferred
  - same-time SBP/DBP fallback only when direct MAP is absent

## Public research plausibility summary

Current plausibility judgment:

- chemistry distributions are compatible with common ICU laboratory ranges reported in public MIMIC studies
- respiratory rate, SpO2, and temperature distributions remain clinically plausible for ICU event streams
- blood-pressure medians remain in the same broad range as public MIMIC cohort tables
- `std_map` is slightly more governance-heavy than many public summary tables, but its final distribution remains clinically plausible and its derivation share remains limited

This means the current approval is not claiming that every future cohort will match these exact medians.
It is claiming that the current retained variables do not show obvious distributional failure relative to official-source semantics and public-study expectations.

## Public-card interpretation rule

After the current review round, the public cards for this batch should be read as follows:

- the card states the current approved semantic boundary
- the card is not a substitute for the full local Layer 5 evidence package
- if the card explicitly says the source scope is narrow, that narrowness is part of the approved meaning, not a temporary omission

Examples:

- `std_respiratory_rate` currently means the approved ordinary ICU respiratory-rate stream, not every respiratory-rate-related field family in MIMIC
- `std_spo2` currently means the approved direct ICU SpO2 stream, not all oxygen-saturation families
- `std_map` currently means direct-first MAP with explicit derived fallback, not silently mixed MAP semantics

## Boundary of this approval note

This note does not claim:

- that every class-1 variable in the repository is already content-reviewed and batch-approved
- that `std_heart_rate` has been merged into this exact approval closure
- that later databases already inherit this approval automatically

This note does claim:

- the first large `MIMIC-IV-3.1` reviewed class-1 content batch is now formally closed
- the approval baseline now extends across chemistry, vital signs, oxygen saturation, temperature, and blood-pressure-family examples

## Practical meaning

After this note, the repository can legitimately say:

- the class skeleton exists
- the class has multiple governed runtime closures
- the first real reviewed content batch for the class is now approved

That is a stronger claim than "we have a prototype".

It means:

- the class has begun to function as a governed approval system rather than only a technical demo

## Natural next step

The most natural next step is not to reopen these 10 variables.

The next step is to choose one of these two directions:

1. formally review and close `std_heart_rate` into the same content-approval style, then write a broader class-1 closure note
2. keep the current approved batch fixed and move to the next class-family rollout

