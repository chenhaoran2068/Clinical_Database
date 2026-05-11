# Amsterdam Hospital-Admission Bridge Feasibility Review

Review date: `2026-05-02`

## Formal Verdict

Amsterdam hospital-admission bridge status:

- verdict: `not_proven_under_current_opening_layer`
- practical decision: do not approve Amsterdam same-name `std_hospital_los_days`
- practical decision: do not approve Amsterdam same-name `std_days_to_next_hospital_admission`
- practical decision: do not map raw Amsterdam `admissionid` to canonical `hadm_id`

This is not a rejection of Amsterdam critical-care timing evidence.

It means the current Amsterdam opening layer proves ICU/MCU or ICU-semantic stay-equivalent boundaries, not true hospital-admission encounter boundaries.

## Bridge Question

The bridge would need to prove all of the following:

- a hospital-admission encounter identifier equivalent to canonical `hadm_id`
- a hospital admission start boundary
- a hospital discharge boundary
- an explicit relationship between one or more ICU/MCU local admissions and the hospital encounter
- a rule preventing multiple ICU/MCU stays inside one hospital admission from becoming duplicate hospital-level rows
- enough source scope to interpret future admissions as next hospital admissions rather than next ICU/MCU admissions

The current evidence does not satisfy those requirements.

## Evidence Reviewed

Public standard-system evidence:

- `docs/standard_system_mvp/STD_HOSPITAL_LOS_DAYS_AMSTERDAM_CANDIDATE_REVIEW.md`
- `docs/standard_system_mvp/STD_DAYS_TO_NEXT_HOSPITAL_ADMISSION_FORMAL_APPROVAL_REVIEW.md`
- `Framework_Guideline/ID_Normalization_Contract.md`
- `Framework_Guideline/AmsterdamUMCdb_TimeSemantics_Contract.md`

Local Amsterdam evidence:

- `Methods/Clinical_Database/local_work/Layer 2/AmsterdamUMCdb-1.0.2/reviewed_unsplit/admissions_core.parquet`
- `Methods/Clinical_Database/local_work/Layer 2/AmsterdamUMCdb-1.0.2/time_anchor/SCHEMA.md`
- `Methods/Clinical_Database/local_work/Layer 2/AmsterdamUMCdb-1.0.2/time_anchor/CRITICAL_TIME_SEMANTICS_CONTRACT.md`
- `Methods/Clinical_Database/local_work/Layer 5/AmsterdamUMCdb-1.0.2/2026-04-22_amsterdam_admissionid_to_stayid_consistency_audit.md`
- `Methods/Clinical_Database/local_work/Layer 5/AmsterdamUMCdb-1.0.2/std_icu_los_days/std_icu_los_days_opening_review_20260425.md`
- `Methods/Clinical_Database/local_work/Layer 5/AmsterdamUMCdb-1.0.2/std_icu_los_days/query_summary/std_icu_los_days_source_audit_summary.json`
- `Methods/Clinical_Database/local_work/Layer 5/AmsterdamUMCdb-1.0.2/hospital_admission_bridge_feasibility_audit/query_summary/amsterdam_hospital_admission_bridge_feasibility_summary.json`

## Data-Level Findings

The current `admissions_core` source has:

- rows: `23106`
- unique `patientid`: `20109`
- unique `admissionid`: `23106`
- patients with multiple `admissionid`: `2320`
- maximum `admissionid` rows per patient: `8`

Location distribution:

| location | rows |
| --- | ---: |
| `IC` | `16454` |
| `MC` | `4720` |
| `IC&MC` | `1848` |
| `MC&IC` | `84` |

Interpretation:

- the row universe is explicitly critical-care-unit scoped
- the source distinguishes ICU and MCU movement/scope, not hospital-wide encounter boundaries
- the already approved Amsterdam `std_icu_los_days` correctly uses `IC`, `IC&MC`, and `MC&IC` as ICU-semantic same-name scope and excludes `MC`-only rows from that same-name ICU denominator

## Time-Boundary Findings

Current time semantics are:

- `admittedat` is the source ICU-admission offset on the longitudinal source timeline
- `dischargedat` is the corresponding raw offset timing field
- `lengthofstay` is a source-supplied summary field, not the precise timing truth

Observed checks:

- `admissioncount = 1` rows: `20109`
- `admissioncount = 1` rows with `admittedat = 0`: `20109`
- `admissioncount > 1` rows: `2997`
- `admissioncount > 1` rows with positive `admittedat`: `2997`
- raw-offset LOS negative rows: `0`
- raw-offset LOS zero rows: `3`
- median raw-offset LOS: `25.6` hours
- p75 raw-offset LOS: `88.17916666666667` hours
- median absolute difference between raw-offset LOS and `lengthofstay`: `0.29999999999999716` hours

Interpretation:

- these fields are usable for ICU/MCU local admission timing
- they do not prove a hospital admission start time or hospital discharge time
- `admittedat` and `dischargedat` should not be renamed into hospital-admission boundaries just because they are admission/discharge-like words

## Identifier Findings

The current ID normalization contract maps Amsterdam:

- raw `patientid` to canonical `subject_id`
- raw `admissionid` to canonical `stay_id`

It explicitly does not map raw `admissionid` to canonical `hadm_id`.

That matters because:

- `std_hospital_los_days` requires hospital-admission encounter grain
- `std_days_to_next_hospital_admission` requires hospital-admission encounter grain plus future hospital-admission search
- the current Amsterdam row key is already governed as ICU/MCU stay-equivalent

## Naive Next-Admission Sequence Check

Sorting Amsterdam `admissionid` rows by `patientid`, `admittedat`, and `admissionid` gives a next-local-admission sequence:

- rows with a later Amsterdam `admissionid` for the same patient: `2997`
- rows without a later Amsterdam `admissionid` for the same patient: `20109`
- median next-gap days among observed later local admissions: `12.1125`
- p95 next-gap days among observed later local admissions: `1585.3408333333332`
- negative next-gap rows under naive sequencing: `29`
- zero-gap rows under naive sequencing: `9`

Interpretation:

- this can be source evidence for a possible future ICU/MCU next-local-admission variable
- it is not evidence for `std_days_to_next_hospital_admission`
- future-hospitalization semantics cannot be inferred from a future ICU/MCU local admission sequence

## Bridge Criteria Matrix

| Required bridge element | Current evidence | Decision |
| --- | --- | --- |
| hospital-admission encounter identifier equivalent to `hadm_id` | no published hospital-level key; `admissionid` is governed as `stay_id` | fail |
| hospital admission start boundary | no separate hospital-admission start field in current opening layer | fail |
| hospital discharge boundary | no separate hospital-discharge field in current opening layer | fail |
| ICU/MCU-to-hospital encounter link | no bridge table or grouping key currently governed | fail |
| duplicate prevention for multiple ICU/MCU stays inside one hospital encounter | cannot be defined without hospital encounter key | fail |
| next hospital admission search | only next Amsterdam ICU/MCU local admission sequence is available | fail |

## Consequences

`std_hospital_los_days`:

- remains approved for `MIMIC-IV-3.1` only
- Amsterdam same-name approval remains blocked
- current Amsterdam duration evidence should remain under ICU/stay-duration identities

`std_days_to_next_hospital_admission`:

- remains approved for `MIMIC-IV-3.1` only
- no Amsterdam mapping spec should be generated under this same-name identity
- no Amsterdam governed runtime evidence should be generated under this same-name identity

Amsterdam future work:

- if a hospital encounter bridge exists outside the current opening layer, it must be reviewed as a separate prerequisite
- if only ICU/MCU future local admission timing is needed, open a separate candidate such as a next ICU/MCU admission duration rather than forcing `std_days_to_next_hospital_admission`
- do not create canonical `hadm_id` for Amsterdam by convenience

Follow-up route:

- `AMSTERDAM_NEXT_ICU_MCU_ADMISSION_DURATION_CANDIDATE_REVIEW.md` records that Amsterdam can support next local critical-care admission timing under an ICU/MCU route
- MC-inclusive timing now uses the approved split identity `std_days_to_next_icu_mcu_admission`
- `STD_DAYS_TO_NEXT_ICU_MCU_ADMISSION_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md` records the governed approval for that split route
- ICU-semantic-only timing can be reviewed separately as a possible Amsterdam mapping for existing `std_days_to_next_icu_admission`

## Final Decision

The Amsterdam hospital-admission bridge is not proven under the current evidence.

Therefore:

- Amsterdam is not eligible for same-name `std_hospital_los_days`
- Amsterdam is not eligible for same-name `std_days_to_next_hospital_admission`
- raw `admissionid` remains a local ICU/MCU stay-equivalent key under the current public standard-system surface
