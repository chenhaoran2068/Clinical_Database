# Class-1 Current Approval Closure

Last updated: 2026-05-04

Status: technical working closure; owner approval deferred for the latest Amsterdam Batch2 recommendation set

## Why This Note Exists

This note records the current governed closure state for the first reusable standard-variable class:

- `event_level_numeric_primary_source`

Owner approval update: on 2026-05-04 the project owner deferred approval and shifted the execution strategy to Class 1-9 build-first, approval-later. This note should therefore treat the Amsterdam Batch2 recommendation subset as technical review recommendations pending owner approval, not final owner approval.

It supersedes the older 2026-04-24 current-closure note, but it does not erase the historical first-batch record.

Historical and supporting records:

- `docs/standard_system_mvp/VARIABLE_REVIEW_REPORTING_STANDARD.md`
- `docs/standard_system_mvp/CLASS1_FIRST_BATCH_APPROVAL_SUMMARY.md`
- `docs/standard_system_mvp/AMSTERDAM_CLASS1_BATCH1_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/AMSTERDAM_CLASS1_BATCH2_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/STD_ICU_URINE_OUTPUT_EVENT_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`
- `Framework_Guideline/StandardVariableClass_EventLevelNumericPrimarySource_Contract.md`

## Approval Standard

A Class-1 database asset is treated as approved only when the current evidence supports all of the following:

- variable identity remains event-level, numeric, and time-stamped
- the source mapping is narrow enough to preserve the same variable meaning
- governed `execution.py` runtime evidence exists where the variable has entered the standard-system MVP path
- first execution validation and rerun reproducibility pass
- local distribution is plausible and outlier behavior is explicit
- already processed database assets are not contradicted
- official source/dictionary alignment is acceptable
- public clinical or epidemiologic plausibility checks do not reveal a source-scale or source-identity failure
- the public card does not overclaim current database coverage

Older MIMIC-approved public-card assets may predate the current Amsterdam mapping-status fields. They remain part of the approved public baseline when their public card and local reviewed-approved evidence already support that status, but new Amsterdam same-name promotions should use explicit mapping-status and runtime-evidence closure.

Post-review reporting must follow `VARIABLE_REVIEW_REPORTING_STANDARD.md`: every reviewed variable needs a per-variable report covering its distribution, cross-database comparison, official source alignment, clinical or literature plausibility, risks, and final decision. A batch count alone is not a sufficient review report.

## Current Governed Class-1 Surface

Current `MIMIC-IV-3.1` governed MVP Class-1 baseline:

1. `std_heart_rate`
2. `std_glucose`
3. `std_respiratory_rate`
4. `std_sodium`
5. `std_potassium`
6. `std_creatinine`
7. `std_spo2`
8. `std_temp`
9. `std_sbp`
10. `std_dbp`
11. `std_map`

Current `AmsterdamUMCdb-1.0.2` governed Class-1 working surface:

Previously governed approved/opening baseline:

1. `std_heart_rate`
2. `std_map`
3. `std_sbp`
4. `std_dbp`
5. `std_respiratory_rate`
6. `std_spo2`
7. `std_temp`
8. `std_glucose`
9. `std_sodium`
10. `std_potassium`
11. `std_chloride`
12. `std_creatinine`
13. `std_lactate_bg`
14. `std_paco2`
15. `std_pao2`
16. `std_bicarbonate_bg`
17. `std_bun`
18. `std_hemoglobin`
19. `std_hematocrit`
20. `std_platelet_count`
21. `std_wbc_count`
22. `std_icu_urine_output_event`

Technical review recommendations pending owner approval:

1. `std_oxygen_partial_pressure_bg_allspecimen`
2. `std_carbon_dioxide_partial_pressure_bg_allspecimen`
3. `std_oxygen_saturation_bg_allspecimen`
4. `std_total_bilirubin`
5. `std_albumin`
6. `std_inr`
7. `std_aptt`

## Amsterdam Review Blocks

| block | variables | review status | interpretation |
| --- | --- | --- | --- |
| Amsterdam heart-rate prototype | `std_heart_rate` | reviewed_approved | Cross-database Class-1 prototype remains accepted for Amsterdam and MIMIC. |
| Amsterdam Batch1 numeric spine | 20 variables from BP, vitals, routine chemistry, blood-gas arterial gases, CBC, and BUN families | reviewed_approved | Formal review approved direct Amsterdam source boundaries, unit conversions, runtime evidence, and reproducibility. |
| Amsterdam urine-output event | `std_icu_urine_output_event` | reviewed_approved | Event-level urine-output stream approved as Class-1; summary variables and non-urine outputs remain excluded. |
| Amsterdam Batch2 recommendation subset | 7 variables from all-specimen blood gas, bilirubin/albumin, INR, and APTT | technical_review_recommend_approve | Formal technical review recommends same-name approval after distribution, official-source, MIMIC, and literature checks; owner approval is deferred. |
| Amsterdam Batch2 held subset | `std_oxygen_saturation_bg_arterial_specimen`, `std_pt` | not_approved_keep_candidate | Both remain candidates and must not be counted as Amsterdam reviewed-approved assets. |

## Held Class-1 Candidates

| variable_id | current status | hold reason |
| --- | --- | --- |
| `std_oxygen_saturation_bg_arterial_specimen` | `built_pending_user_review` | Amsterdam does not currently provide a universal structured arterial-specimen flag for the retained rows. The candidate differs from the all-specimen oxygen-saturation asset by only 71 rows, so arterial certainty would be overclaimed. |
| `std_pt` | `built_pending_user_review` | The Amsterdam source dictionary says seconds, but the actual distribution is INR-like rather than PT-seconds-like. This violates same-name identity against the approved MIMIC PT seconds asset. |

## Current Closure Interpretation

The approved Class-1 surface is now broad enough to support ongoing Class-1 use across:

- vital signs
- blood pressure
- routine chemistry
- CBC-style blood counts
- blood-gas measurements
- coagulation lab measurements
- event-level urine-output volume

This is a meaningful Class-1 closure for currently approved assets.

It is not a claim that every possible Class-1 variable has been reviewed, and it is not a claim that the two held Amsterdam candidates are approved.

## Review Rule Coverage

The current approved/recommendation surface satisfies the review rules as follows:

- local distributions are recorded in each formal review and runtime manifest
- already processed database assets are compared where same-name MIMIC anchors exist
- Amsterdam official dictionary/item evidence is recorded for source inclusion and exclusion
- unit conversions are explicitly governed in mapping specs and execution outputs
- top-level public cards are refreshed to avoid claiming unapproved Amsterdam coverage for held mappings
- external clinical plausibility is documented in the Batch1, Batch2, and urine-output formal reviews

The two held candidates are examples of the same rules working correctly:

- `std_oxygen_saturation_bg_arterial_specimen` fails the source-certainty rule
- `std_pt` fails the cross-database source-scale identity rule

## Practical Meaning

The repository can now treat Class 1 as an active governed approval system rather than a prototype.

Approved Class-1 variables can be used as inputs for later class work when their public card and local Layer 5 evidence support the intended database and semantic boundary.

Class 1 should not be marked fully exhausted until the two held Amsterdam candidates are either:

- resolved and approved with stronger evidence, or
- formally split/reclassified so they no longer block the same-name Class-1 queue.

## Natural Next Step

Resolve the two held Amsterdam Class-1 candidates before declaring the Amsterdam same-name Class-1 campaign fully closed:

1. `std_oxygen_saturation_bg_arterial_specimen`
2. `std_pt`

If those remain unresolved, they should be carried as explicit hold items while the team proceeds to the next approved variable class.
