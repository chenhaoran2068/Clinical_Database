# Amsterdam Next ICU/MCU Admission Duration Candidate Review

Review date: `2026-05-02`

## Formal Verdict

Amsterdam hospital-level next-admission work remains blocked.

Amsterdam ICU/MCU local-admission timing is feasible under the current opening layer, but it has two different possible identities:

- existing same-name candidate: `std_days_to_next_icu_admission`
- split new-identity candidate: `std_days_to_next_icu_mcu_admission`

The identity rule is:

- if the retained denominator and future search are restricted to ICU-semantic rows, use the existing `std_days_to_next_icu_admission` candidate route
- if MC-only rows are retained, do not publish under `std_days_to_next_icu_admission`; open a separate ICU/MCU identity such as `std_days_to_next_icu_mcu_admission`

This review is a feasibility and naming-boundary review only.

It does not approve a governed Amsterdam runtime yet.

## Why This Review Exists

The prior Amsterdam hospital-admission bridge review found that the current Amsterdam opening layer does not prove hospital admission/discharge boundaries.

That blocks Amsterdam same-name approval for:

- `std_hospital_los_days`
- `std_days_to_next_hospital_admission`

It does not block local critical-care admission timing.

Amsterdam already exposes enough ICU/MCU local-admission structure to ask a narrower question:

- for the same `patientid`, after the current ICU/MCU local admission has ended, when is the next later ICU/MCU local admission observed?

## Evidence Reviewed

Public evidence:

- `docs/standard_system_mvp/AMSTERDAM_HOSPITAL_ADMISSION_BRIDGE_FEASIBILITY_REVIEW.md`
- `docs/std_variable_cards/std_days_to_next_icu_admission.md`
- `docs/standard_system_mvp/STD_ICU_LOS_DAYS_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/std_icu_los_days/mapping_spec_amsterdamumcdb_1_0_2.json`
- `Framework_Guideline/ID_Normalization_Contract.md`
- `Framework_Guideline/AmsterdamUMCdb_TimeSemantics_Contract.md`

Local evidence:

- `Methods/Clinical_Database/local_work/Layer 2/AmsterdamUMCdb-1.0.2/reviewed_unsplit/admissions_core.parquet`
- `Methods/Clinical_Database/local_work/Layer 2/AmsterdamUMCdb-1.0.2/time_anchor/SCHEMA.md`
- `Methods/Clinical_Database/local_work/Layer 2/AmsterdamUMCdb-1.0.2/time_anchor/CRITICAL_TIME_SEMANTICS_CONTRACT.md`
- `Methods/Clinical_Database/local_work/Layer 5/AmsterdamUMCdb-1.0.2/next_icu_mcu_admission_duration_candidate_audit/query_summary/amsterdam_next_icu_mcu_admission_duration_candidate_summary.json`

## Source Structure

The source audit uses `admissions_core.parquet`.

Current source shape:

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

- `patientid` supports same-patient sequencing
- `admissionid` is the local ICU/MCU stay-equivalent row key
- `admissioncount`, `admittedat`, and `dischargedat` support local admission order and duration timing
- these fields still do not prove hospital admission/discharge encounters

## Time Rule

The candidate duration should not use the immediate next row blindly.

The immediate same-patient sequence has:

- paired current-to-next local rows: `2997`
- negative immediate gaps: `29`
- zero immediate gaps: `9`
- positive immediate gaps: `2959`

Therefore the governed duration rule must be:

- current anchor: current local admission `dischargedat`
- future event: first later eligible local admission whose `admittedat` is strictly after current `dischargedat`
- retained value: `(next admittedat - current dischargedat) / 86400000`, in days
- nonpositive immediate overlap or same-boundary artifacts must not become retained duration values

## Candidate Scope Results

### Existing Same-Name ICU Candidate

Candidate identity:

- `std_days_to_next_icu_admission`

Allowed Amsterdam scope:

- current rows: `location in (IC, IC&MC, MC&IC)`
- future rows: `location in (IC, IC&MC, MC&IC)`
- MC-only rows excluded

Audit result:

- retained candidate rows: `18386`
- observed next ICU-semantic local admission rows: `1860`
- no later ICU-semantic local admission observed rows: `16526`
- minimum observed gap days: `0.0006944444444444445`
- median observed gap days: `9.28888888888889`
- p95 observed gap days: `1609.6217361111103`
- maximum observed gap days: `4187.0875`
- negative or zero retained gaps after strict rule: `0`

Observed next-location counts:

| next location | rows |
| --- | ---: |
| `IC` | `1522` |
| `IC&MC` | `325` |
| `MC&IC` | `13` |

Decision:

- this is the eligible route if the goal is to add Amsterdam to the existing public `std_days_to_next_icu_admission` identity
- it must remain ICU-semantic and must not retain MC-only rows

### Split ICU/MCU Candidate

Candidate identity:

- recommended new candidate: `std_days_to_next_icu_mcu_admission`

Allowed Amsterdam scope:

- current rows: `location in (IC, MC, IC&MC, MC&IC)`
- future rows: `location in (IC, MC, IC&MC, MC&IC)`

Audit result:

- retained candidate rows: `23106`
- observed next ICU/MCU local admission rows: `2967`
- no later ICU/MCU local admission observed rows: `20139`
- minimum observed gap days: `0.0006944444444444445`
- median observed gap days: `12.8375`
- p95 observed gap days: `1592.3065972222205`
- maximum observed gap days: `4531.061111111111`
- negative or zero retained gaps after strict rule: `0`

Observed next-location counts:

| next location | rows |
| --- | ---: |
| `IC` | `1752` |
| `MC` | `781` |
| `IC&MC` | `416` |
| `MC&IC` | `18` |

Decision:

- this is the preferred route if the analytic target is explicitly Amsterdam ICU/MCU local admission timing
- it should not be presented as `std_days_to_next_icu_admission`, because `MC` rows are a real retained part of the denominator and future search

## Death-Time Context

`dateofdeath` exists in `admissions_core`, but it should not be used as the primary ordering rule for this candidate.

The local audit found:

- source rows with missing `dateofdeath`: `15416`
- ICU/MCU inclusive no-next rows with `dateofdeath` at or after current discharge: `3974`
- ICU/MCU inclusive observed-next rows with `dateofdeath` before next `admittedat`: `31`

Interpretation:

- `dateofdeath` can support later censoring or context flags
- it is not a substitute for same-patient local admission sequencing
- any death-aware status policy needs a separate censoring contract before formal approval

## Naming Boundary Matrix

| Candidate route | Row scope | Same-name eligible? | Decision |
| --- | --- | --- | --- |
| `std_days_to_next_hospital_admission` | hospital admission encounter | no | blocked by absent hospital bridge |
| `std_days_to_next_icu_admission` | ICU-semantic Amsterdam rows only | yes | promoted after governed Amsterdam mapping review |
| `std_days_to_next_icu_mcu_admission` | all Amsterdam ICU/MCU rows including MC-only | new identity required | recommended if the project wants full Amsterdam local critical-care scope |

## Recommended Next Step

Because the current user-approved direction is Amsterdam ICU/MCU timing rather than a narrow ICU-only add-on, the recommended next governed MVP is:

- open `std_days_to_next_icu_mcu_admission` as a new Class 2 duration-summary candidate
- write `variable_spec.json`
- write `mapping_spec_amsterdamumcdb_1_0_2.json`
- create governed `execution.py`
- run first execution and rerun reproducibility
- write a formal approval review

The narrower `std_days_to_next_icu_admission` Amsterdam mapping was left as a separate same-name path in this candidate review and has since been promoted through governed approval.

## Final Decision

Amsterdam is feasible for next local critical-care admission duration.

It is not feasible for next hospital admission under current evidence.

The immediate next Amsterdam execution path should use the ICU/MCU identity split if MC-only rows are retained.

## Promotion Outcome

Status as of `2026-05-02`:

- the ICU/MCU split route has been promoted into governed Amsterdam approval as `std_days_to_next_icu_mcu_admission`
- governed variable directory: `docs/standard_system_mvp/std_days_to_next_icu_mcu_admission/`
- formal approval review: `docs/standard_system_mvp/STD_DAYS_TO_NEXT_ICU_MCU_ADMISSION_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`
- the narrower ICU-semantic same-name route has also now been promoted into governed Amsterdam approval as `std_days_to_next_icu_admission`
- same-name governed variable directory: `docs/standard_system_mvp/std_days_to_next_icu_admission/`
- same-name formal approval review: `docs/standard_system_mvp/STD_DAYS_TO_NEXT_ICU_ADMISSION_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`
- Amsterdam same-name `std_days_to_next_hospital_admission` remains blocked
- Amsterdam same-name `std_days_to_next_icu_admission` remains ICU-semantic only, not the MC-inclusive approved output
