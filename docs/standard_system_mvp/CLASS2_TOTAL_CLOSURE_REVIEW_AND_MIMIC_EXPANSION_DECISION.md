# Class-2 Total Closure Review And MIMIC-IV Expansion Decision

Last updated: 2026-04-28

## Formal Verdict

Class 2, `baseline_summary_window_numeric`, passes the current total closure review.

The decision is:

- keep Class 2 approved as a bounded current-stage governed class
- continue MIMIC-IV-3.1 Class 2 expansion
- mark `std_weight_icu_baseline` as the first completed post-closure MIMIC-IV-3.1 Class 2 expansion
- mark `std_hospital_los_days` as the second completed post-closure MIMIC-IV-3.1 Class 2 expansion
- mark `std_bmi_admission_baseline` as the third completed post-closure MIMIC-IV-3.1 Class 2 expansion
- mark `std_bmi_icu_baseline` as the fourth completed post-closure MIMIC-IV-3.1 Class 2 expansion
- do not move directly to Class 3 before recording this expansion decision
- do not claim full Class 2 industrialization yet

This means the class is strong enough to expand, not that every Class 2 variable is already complete.

## What Was Reviewed

This review covers the public and local-evidence-facing Class 2 closure after Amsterdam `std_first_day_urine_output_summary` was promoted from candidate to same-name approved status.

Reviewed public surfaces:

- `Framework_Guideline/StandardVariableClass_BaselineSummaryWindowNumeric_Contract.md`
- `docs/standard_system_mvp/variable_classes/baseline_summary_window_numeric/README.md`
- `docs/standard_system_mvp/CLASS2_FIRST_MVP_SELECTION.md`
- `docs/standard_system_mvp/CLASS2_CURRENT_APPROVAL_CLOSURE.md`
- `docs/standard_system_mvp/STD_ICU_LOS_DAYS_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/STD_HOSPITAL_LOS_DAYS_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/STD_HOSPITAL_LOS_DAYS_AMSTERDAM_CANDIDATE_REVIEW.md`
- `docs/standard_system_mvp/STD_WEIGHT_ADMISSION_BASELINE_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/STD_WEIGHT_ICU_BASELINE_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/STD_WEIGHT_ADMISSION_BASELINE_AMSTERDAM_CANDIDATE_REVIEW.md`
- `docs/standard_system_mvp/STD_WEIGHT_ICU_BASELINE_GROUPED_PROXY_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/STD_FIRST_DAY_URINE_OUTPUT_SUMMARY_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/STD_FIRST_DAY_URINE_OUTPUT_SUMMARY_AMSTERDAM_CANDIDATE_REVIEW.md`
- `docs/standard_system_mvp/STD_FIRST_DAY_URINE_OUTPUT_SUMMARY_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/STD_BMI_ADMISSION_BASELINE_CANDIDATE_REVIEW.md`
- `docs/standard_system_mvp/STD_BMI_ICU_BASELINE_CANDIDATE_REVIEW.md`
- `docs/standard_system_mvp/STD_BMI_ADMISSION_BASELINE_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/STD_BMI_ICU_BASELINE_FORMAL_APPROVAL_REVIEW.md`
- current Class 2 variable specs, mapping specs, execution entrypoints, runtime manifests, validation reports, reproducibility reports, and public variable cards

Reviewed public-source alignment:

- MIMIC-IV v3.1 official database scope and ICU/hospital module semantics
- MIMIC-IV ICU stay count and hospital admission count
- MIMIC official first-day urine-output SQL concept surface
- MIMIC ICU weight item-code context
- AmsterdamUMCdb ICU/MCU admission scope
- Amsterdam `admissionid`, `lengthofstay`, `weightgroup`, and `numericitems` semantics
- public plausibility references for ICU LOS, body weight, and first-day urine output

## Current Class-2 Shape

Class 2 is not a database name and not a variable family name.

Class 2 means:

- one retained numeric row per anchor-qualified target entity
- baseline, first-day, duration, or window-summary semantics are part of the variable identity
- the output is not a raw event stream
- anchor, window, selection, aggregation, and no-source-row behavior must be locked before approval
- formal output requires governed execution and runtime evidence

Current approved subclasses:

| Subclass | Representative assets | Current closure state |
| --- | --- | --- |
| `duration_summary` | `std_icu_los_days`, `std_hospital_los_days`, `std_days_to_next_hospital_admission`, `std_days_to_next_icu_admission`, `std_days_to_next_icu_mcu_admission` | dual-database ICU-duration and ICU-next-admission closure, MIMIC hospital-duration and next-hospital-admission closure, plus Amsterdam split ICU/MCU next-admission closure |
| `baseline_snapshot` | `std_weight_admission_baseline`, `std_weight_icu_baseline`, `std_bmi_admission_baseline`, `std_bmi_icu_baseline`, `std_weight_icu_baseline_grouped_proxy` | exact MIMIC admission baseline, exact MIMIC ICU baseline, derived MIMIC BMI baselines, plus intentionally separate Amsterdam grouped/proxy baseline |
| `window_summary` | `std_first_day_urine_output_summary` | dual-database governed closure on MIMIC-IV-3.1 and AmsterdamUMCdb-1.0.2 |

## Current Approved Assets

| Variable | Database coverage | Subclass | Approval meaning |
| --- | --- | --- | --- |
| `std_icu_los_days` | `MIMIC-IV-3.1`, `AmsterdamUMCdb-1.0.2` | `duration_summary` | ICU stay or ICU-semantic stay-equivalent duration in days |
| `std_hospital_los_days` | `MIMIC-IV-3.1` | `duration_summary` | hospital-admission encounter duration in days |
| `std_days_to_next_hospital_admission` | `MIMIC-IV-3.1` | `duration_summary` | hospital-admission encounter post-discharge observed next-admission duration in days |
| `std_days_to_next_icu_admission` | `MIMIC-IV-3.1`, `AmsterdamUMCdb-1.0.2` | `duration_summary` | ICU-only post-discharge observed next-ICU-admission duration in days |
| `std_days_to_next_icu_mcu_admission` | `AmsterdamUMCdb-1.0.2` | `duration_summary` | Amsterdam ICU/MCU local-admission post-discharge observed next-local-admission duration in days |
| `std_weight_admission_baseline` | `MIMIC-IV-3.1` | `baseline_snapshot` | exact cleaned body-weight event selected inside a hospital-admission baseline window |
| `std_weight_icu_baseline` | `MIMIC-IV-3.1` | `baseline_snapshot` | exact cleaned body-weight event selected inside an ICU-admission baseline window |
| `std_bmi_admission_baseline` | `MIMIC-IV-3.1` | `baseline_snapshot` derived numeric | hospital-admission baseline BMI derived from approved admission-baseline weight and approved height |
| `std_bmi_icu_baseline` | `MIMIC-IV-3.1` | `baseline_snapshot` derived numeric | ICU-stay baseline BMI derived from approved ICU-baseline weight and approved height |
| `std_weight_icu_baseline_grouped_proxy` | `AmsterdamUMCdb-1.0.2` | `baseline_snapshot` with grouped/proxy representation | ICU/MCU local-admission grouped/proxy baseline body-weight row |
| `std_first_day_urine_output_summary` | `MIMIC-IV-3.1`, `AmsterdamUMCdb-1.0.2` | `window_summary` | first-day ICU urine-output total in mL with NULL-preserving no-source behavior |

## LOS Duration Relationship

The current Class 2 duration-summary relationship is:

- `std_icu_los_days` is the first governed Class 2 representative and the first dual-database proof.
- `std_hospital_los_days` is a later sibling duration-summary variable, not the next replacement for `std_icu_los_days`.
- `std_icu_los_days` uses ICU stay or ICU-semantic stay-equivalent grain.
- `std_hospital_los_days` uses hospital-admission encounter grain.
- Amsterdam has already passed same-name review for `std_icu_los_days`.
- Amsterdam has already failed same-name review for `std_hospital_los_days` under the current public evidence because no separate hospital-admission encounter layer is currently proven.
- A future Amsterdam hospital-level admission/discharge bridge may reopen `std_hospital_los_days`; otherwise Amsterdam ICU/MCU duration variants must remain under ICU/stay-duration identities or be split into a distinct variable.
- The later `AMSTERDAM_NEXT_ICU_MCU_ADMISSION_DURATION_CANDIDATE_REVIEW.md` applies the same rule to next-admission duration: ICU-semantic timing can support Amsterdam same-name `std_days_to_next_icu_admission`, while MC-inclusive timing needs a split identity.
- That MC-inclusive split route has now been approved as Amsterdam-only `std_days_to_next_icu_mcu_admission`, preserving the difference between hospital-level next admission, ICU-only next admission, and ICU/MCU local-admission timing.
- The ICU-semantic same-name route has now also been approved as Amsterdam `std_days_to_next_icu_admission`, preserving the same boundary by excluding MC-only rows from the same-name output.

## Machine Evidence Review

The current Class 2 closure is acceptable because the approved assets have:

- public `variable_spec.json`
- public database-specific `mapping_spec_*.json`
- governed `execution.py`
- execute-mode `validation_report.json`
- execute-mode `manifest.json`
- rerun `reproducibility_report.json`
- public card publication
- formal approval review notes
- release-safe manifest coverage

The review also confirmed that the Amsterdam `std_first_day_urine_output_summary` promotion required and received its own summary-specific governed runtime evidence.

It was not inferred merely from the upstream event-layer approval.

## Full Interpretation

### `std_icu_los_days`

Meaning:

- duration summary
- one row per ICU stay or ICU-semantic stay-equivalent admission
- canonical unit is days
- not hospital LOS
- not event-level data

Current role:

- proves Class 2 can include interval-derived duration summaries
- gives the first clean dual-database Class 2 proof

### `std_hospital_los_days`

Meaning:

- duration summary
- MIMIC-only current same-name approval
- one row per hospital admission encounter
- canonical unit is days
- computed from `hosp_admissions.admittime` to `hosp_admissions.dischtime`
- not ICU LOS
- not Amsterdam ICU/MC local admission duration under the current opening surface
- negative-duration source edge cases are retained and flagged rather than silently removed

Current role:

- proves Class 2 can distinguish ICU-stay duration from hospital-admission duration
- completes the second controlled post-total-review MIMIC-IV-3.1 Class 2 expansion
- provides a duration-summary example at `hadm_id` grain
- now has an Amsterdam candidate boundary review confirming that same-name Amsterdam approval must wait for a true hospital-admission encounter layer

### `std_weight_admission_baseline`

Meaning:

- baseline snapshot
- MIMIC-only current same-name approval
- one exact cleaned weight event selected inside an admission-baseline window
- hospital-admission anchored
- not an ICU-start baseline
- not a subject-level stable weight

Current role:

- proves Class 2 can include exact baseline snapshots
- also exposes why Amsterdam grouped/proxy weight cannot silently reuse the same variable identity

### `std_weight_icu_baseline`

Meaning:

- baseline snapshot
- MIMIC-only current same-name approval
- one exact cleaned weight event selected inside an ICU-baseline window
- ICU-admission anchored
- not hospital-admission anchored
- not generic patient-level stable weight
- not an Amsterdam grouped/proxy weight

Current role:

- proves the current Class 2 baseline-snapshot contract can distinguish hospital-admission and ICU-admission anchors
- provides the first completed post-total-review MIMIC-IV-3.1 Class 2 expansion

### `std_weight_icu_baseline_grouped_proxy`

Meaning:

- Amsterdam-only grouped/proxy baseline snapshot
- useful ICU/MCU body-size baseline
- not exact continuous measured weight
- not same-name equivalent to `std_weight_admission_baseline`

Current role:

- proves the governance can split a useful local variable instead of forcing a false harmonization

### `std_first_day_urine_output_summary`

Meaning:

- window summary
- first 24 hours from ICU admission or ICU-semantic admission anchor
- canonical unit is mL
- no qualifying source row remains `NULL`
- not zero-filled missingness
- not urine-output rate
- not intake-output balance
- not oliguria phenotype

Current role:

- proves Class 2 can handle more difficult window-summary semantics
- now gives dual-database coverage after Amsterdam was built from the approved upstream event layer

## Findings

### Blocking findings

No blocking finding remains for the current Class 2 closure.

### Non-blocking findings

Two non-blocking issues were tracked during the next MIMIC expansion:

- `CLASS2_FIRST_MVP_SELECTION.md` contained an older end-state note saying Amsterdam `std_first_day_urine_output_summary` should still be attempted later; it should now be updated to say that this attempt has been completed and approved.
- `std_bmi_admission_baseline` and `std_bmi_icu_baseline` previously showed `########` in the latest review date field; this has now been repaired, both assets passed candidate review, and both have now completed governed Class 2 promotion.

## Expansion Decision

Decision: continue MIMIC-IV-3.1 Class 2 expansion now.

Reason:

- Class 2 has passed all current closure requirements.
- The class has representatives for all intended subclasses.
- The runtime and reproducibility gate has already handled both single-database and dual-database examples.
- MIMIC-IV-3.1 has multiple reviewed-approved local Class 2-style assets that can be promoted one at a time without inventing a new class.

This expansion should still be small and ordered.

It should not attempt to convert every possible summary variable in one pass.

## MIMIC-IV-3.1 Next Batch

### Batch 2A: current controlled expansion

The current MIMIC-IV-3.1 Class 2 governed MVP expansion state is:

| Priority | Candidate | Subclass | Current state | Approval gate |
| --- | --- | --- | --- | --- |
| 1 | `std_weight_icu_baseline` | `baseline_snapshot` | completed and approved as the first post-closure MIMIC expansion | ICU anchor, selection window, source priority, clipping boundaries, and no-source behavior are locked with execute/rerun evidence |
| 2 | `std_hospital_los_days` | `duration_summary` | completed and approved as the second post-closure MIMIC expansion | admission anchor, discharge boundary, encounter grain, negative-duration validity status, and audit-only ICU subset comparison are locked with execute/rerun evidence |
| 3 | `std_bmi_admission_baseline` | `baseline_snapshot` derived numeric | completed and approved as the third post-closure MIMIC expansion | upstream admission-baseline weight, upstream height, formula, missing-height behavior, outlier flagging, and rerun evidence are locked |
| 4 | `std_bmi_icu_baseline` | `baseline_snapshot` derived numeric | completed and approved as the fourth post-closure MIMIC expansion | upstream ICU-baseline weight, upstream height, formula, missing-height behavior, outlier flagging, and rerun evidence are locked |

### Batch 2B: BMI derived-baseline promotion

The BMI metadata blocker has now been repaired, and the governed promotion has now been completed.

These BMI variables are now governed-approved for `MIMIC-IV-3.1`:

| Candidate | Subclass | Current state | Approval evidence |
| --- | --- | --- | --- |
| `std_bmi_admission_baseline` | `baseline_snapshot` derived numeric | completed and approved | public spec, MIMIC mapping, governed execution, runtime evidence, rerun evidence, reproducibility report, and formal approval review |
| `std_bmi_icu_baseline` | `baseline_snapshot` derived numeric | completed and approved | public spec, MIMIC mapping, governed execution, runtime evidence, rerun evidence, reproducibility report, and formal approval review |

### Later, higher-complexity candidates

These should not be the immediate next expansion:

| Candidate family | Reason to defer |
| --- | --- |
| `std_first_day_intake_output_balance_summary` | depends on both intake and output semantics; higher risk of sign and component mixing |
| RRT/CRRT first-day summaries | episode and treatment-family boundaries may pull toward Class 4 or Class 5 governance |
| `std_sofa_first_day` and score summaries | score/composite semantics likely belong to Class 8 rather than plain Class 2 |
| free-day outcomes | trial-style follow-up and competing-risk logic may need a distinct outcome/follow-up class |

## Expansion Acceptance Criteria

Each new MIMIC-IV-3.1 Class 2 promotion must include:

- `variable_spec.json`
- `mapping_spec_mimic_iv_3_1.json`
- `execution.py`
- first real runtime `validation_report.json`
- first real runtime `manifest.json`
- rerun runtime `validation_report.json`
- rerun runtime `manifest.json`
- rerun `reproducibility_report.json`
- public card refresh
- formal approval review note
- release-safe manifest and inventory update

Each promotion must also explicitly state:

- target grain
- anchor family
- window or duration rule
- selection rule
- aggregation rule
- tie-break rule
- no-source-row behavior
- hard range and plausible range
- upstream dependency if derived
- whether same-name cross-database expansion is allowed now or deferred

## Do-Not-Do Rules

Do not:

- treat BMI as a simple raw measurement; it is derived from height and weight
- silently reuse Amsterdam grouped/proxy body-size evidence as exact MIMIC-style baseline weight
- treat first-day urine-output total as urine-output rate or zero-filled missing output
- force score/composite variables into Class 2 before Class 8 governance is decided
- start a broad 400-variable conversion before the next two MIMIC Class 2 examples pass the same runtime/rerun gate

## Final Decision

Class 2 passes current total closure review.

The next execution path is approved:

1. promote MIMIC-IV-3.1 `std_weight_icu_baseline`
2. promote MIMIC-IV-3.1 `std_hospital_los_days`
3. repair BMI public metadata and perform candidate review
4. promote `std_bmi_admission_baseline` and `std_bmi_icu_baseline` only through the full governed MVP hard chain

This is the controlled route from current Class 2 proof to broader MIMIC-IV-3.1 Class 2 expansion.

Current execution update:

- `std_weight_icu_baseline` has completed step 1 with public spec, MIMIC mapping spec, governed execution, runtime evidence, rerun reproducibility evidence, public card refresh, and formal approval review
- `std_hospital_los_days` has completed step 2 with public spec, MIMIC mapping spec, governed execution, runtime evidence, rerun reproducibility evidence, public card refresh, and formal approval review
- Amsterdam has been reviewed and intentionally not promoted to same-name `std_hospital_los_days`; its current duration evidence remains in ICU/stay-duration semantics
- BMI metadata repair, candidate review, governed promotion, runtime evidence, rerun reproducibility evidence, public card refresh, and formal approval review have completed for `std_bmi_admission_baseline` and `std_bmi_icu_baseline`
- the Amsterdam split ICU/MCU route has now been executed and approved as `std_days_to_next_icu_mcu_admission`; ICU-only Amsterdam mapping is handled as a separate same-name `std_days_to_next_icu_admission` decision
- that separate ICU-only Amsterdam mapping decision has now completed as same-name `std_days_to_next_icu_admission`, with governed execution, runtime evidence, rerun reproducibility evidence, public card refresh, and formal approval review
