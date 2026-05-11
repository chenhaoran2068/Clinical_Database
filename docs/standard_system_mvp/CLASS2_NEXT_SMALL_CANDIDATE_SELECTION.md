# Class-2 Next Small Candidate Selection

Last updated: 2026-05-02

## Purpose

This note records the next small Class 2 candidate after the completed BMI governed promotion.

The goal is not to increase the variable count quickly.

The goal is to test whether Class 2 can safely expand beyond already closed baseline, LOS, BMI, and first-day urine-output examples without accidentally pulling in Class 5, Class 7, or Class 8 semantics.

## Selection Verdict

Selected next small candidate:

- `std_days_to_next_hospital_admission`

Selected opening database:

- `MIMIC-IV-3.1`

Candidate Class 2 interpretation:

- subclass: `duration_summary`
- subtype under review: observed follow-up duration summary
- target grain: one retained row per hospital admission encounter
- anchor: hospital discharge time
- retained value: elapsed days from current discharge to the first later different hospitalization in the captured MIMIC source

## Why This Candidate

`std_days_to_next_hospital_admission` is the best next small Class 2 candidate because it is simple enough to govern now but still adds a real boundary test.

It is simple because:

- the current local asset is already `reviewed_approved`
- the source basis is narrow: `hosp_admissions`
- the target grain is clear: one row per `hadm_id`
- the anchor is clear: `dischtime`
- the output is numeric in days
- the local Layer 5 package already contains query summaries, source audit, preview, manifest, and build log

It extends Class 2 because:

- previous duration examples were mostly within-encounter durations such as ICU LOS and hospital LOS
- this candidate is a post-discharge observed future-duration summary
- it forces the class to state no-future-event semantics explicitly
- it tests whether Class 2 can include some follow-up numeric summaries when the main difficulty remains anchor, search rule, duration rule, and null behavior

## Local Evidence Snapshot

Existing local MIMIC asset:

- `Methods/Clinical_Database/local_work/Layer 5/MIMIC-IV-3.1/std_days_to_next_hospital_admission/asset_manifest.md`

Existing Layer 3 output:

- `Methods/Clinical_Database/local_work/Layer 3/MIMIC-IV-3.1/outcomes/std_days_to_next_hospital_admission/std_days_to_next_hospital_admission_long.parquet`

Current local asset summary:

- total rows: `546,028`
- unique `hadm_id`: `546,028`
- observed next-hospital-admission rows: `321,561`
- no later hospitalization observed rows: `224,467`
- minimum observed days: `0.001`
- median observed days: `85.111`
- p95 observed days: `1774.269`
- maximum observed days: `5340.54`

Current source-audit snapshot:

- source table: `hosp_admissions`
- search rule: first later different hospitalization with `admittime > current dischtime`
- rows with missing discharge time: `0`
- self-match rows prevented: `175`
- immediate nonpositive next-row artifacts skipped or audited: `2,131`
- observed 30-day readmission rate among all admissions in the paired local build context: about `19.699%`

## Boundary Rules To Lock Before Approval

The candidate should be approved only if the governed MVP spec locks these rules:

- target grain is hospital admission encounter, not ICU stay and not patient
- anchor is `dischtime`, not `admittime`, ICU `intime`, or ICU `outtime`
- eligible next admission must be a later different hospitalization
- next `admittime` must be strictly after current `dischtime`
- same-time, overlapping, self-match, or nonpositive-gap artifacts must not become the retained next admission
- a retained null value means no later different hospitalization is observed in the captured MIMIC source, not proven absence of all future care
- the asset is a duration summary, not a binary readmission flag

## Alternatives Considered

### `std_days_to_next_icu_admission`

This is a close sibling and remains a good later candidate.

It is deferred because it is slightly less small:

- it is stay-level rather than hospital-admission-level
- it has a status column because null values can mean no next ICU admission or unresolved missing current outtime
- it should probably follow the hospital-admission version after the post-discharge duration rule is locked once

### `std_height`

This is useful and already cross-database approved locally.

It is deferred because it would test a different boundary:

- current grain is patient-level
- no explicit anchor/window is retained in the MIMIC asset
- Amsterdam uses grouped/proxy height semantics
- it may require a patient-level canonical/static numeric class decision rather than a straightforward Class 2 expansion

### `std_age`

This is intentionally not selected.

It is numeric, but its main governance burden is demographic/admin semantics and MIMIC elderly top-coding, so it is closer to Class 7 than to Class 2.

### `std_first_day_intake_output_balance_summary`

This remains deferred.

It is a real Class 2-style window summary, but it is not small:

- it mixes intake and output components
- sign conventions and component boundaries are high-risk
- it depends on approved hourly balance logic
- it should not be the immediate post-BMI expansion candidate

### Scores, free-day outcomes, and RRT/CRRT summaries

These remain deferred.

- `std_sofa_first_day` and related scores likely belong to Class 8 score/composite governance
- respiratory-support-free-day outcomes involve trial-style follow-up and competing-risk semantics
- RRT/CRRT summaries may pull in treatment episode or modality logic from Class 4 or Class 5

## Amsterdam Same-Name Position

Do not attempt Amsterdam same-name approval for this variable in the opening step.

Reason:

- the current Amsterdam opening surface uses ICU/MCU local admission identifiers
- a true hospital-admission encounter layer with hospital admission/discharge boundaries is not yet proven in the public governed layer
- this is the same boundary that kept Amsterdam out of `std_hospital_los_days`

Amsterdam can be revisited only after a hospital-level admission/discharge bridge is separately proven.

Post-bridge follow-up:

- `AMSTERDAM_HOSPITAL_ADMISSION_BRIDGE_FEASIBILITY_REVIEW.md` has now confirmed that the hospital-level bridge is not proven under the current opening layer
- `AMSTERDAM_NEXT_ICU_MCU_ADMISSION_DURATION_CANDIDATE_REVIEW.md` records the safer Amsterdam route as ICU/MCU local-admission timing rather than next hospital admission
- MC-inclusive Amsterdam timing has now been split and approved as `std_days_to_next_icu_mcu_admission`; it is not attached to this hospital-admission variable
- ICU-only Amsterdam timing has now also been approved as same-name `std_days_to_next_icu_admission`; it still does not change the hospital-admission variable boundary

## Approval Acceptance Criteria

The next governed promotion should produce:

- `docs/standard_system_mvp/std_days_to_next_hospital_admission/variable_spec.json`
- `docs/standard_system_mvp/std_days_to_next_hospital_admission/mapping_spec_mimic_iv_3_1.json`
- `docs/standard_system_mvp/std_days_to_next_hospital_admission/execution.py`
- first execute-mode runtime evidence on `MIMIC-IV-3.1`
- rerun runtime evidence on `MIMIC-IV-3.1`
- `reproducibility_report.json`
- refreshed public card
- formal approval review note
- release-safe manifest and inventory update

The formal review must explicitly decide whether this candidate remains inside Class 2 as a follow-up duration summary or whether follow-up/bridge semantics require a separate later class boundary.

## Final Decision

Proceed next with `std_days_to_next_hospital_admission` as the next small Class 2 candidate.

This candidate is the right size for the next step: small enough to govern safely, but different enough to test Class 2 beyond the already completed BMI and LOS examples.

## Promotion Outcome

Status as of `2026-05-02`:

- `std_days_to_next_hospital_admission` has now been promoted from selected candidate to governed MIMIC-IV-3.1 approval
- formal approval review: `docs/standard_system_mvp/STD_DAYS_TO_NEXT_HOSPITAL_ADMISSION_FORMAL_APPROVAL_REVIEW.md`
- governed variable directory: `docs/standard_system_mvp/std_days_to_next_hospital_admission/`
- Amsterdam remains not approved for same-name use until a true hospital-admission encounter bridge is proven
- Amsterdam ICU/MCU local-admission timing has now been handled separately through `std_days_to_next_icu_mcu_admission`
- Amsterdam ICU-only local-admission timing has now been handled separately through same-name `std_days_to_next_icu_admission`
