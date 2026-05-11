# std_nitrite_urinalysis_result MIMIC Formal Approval Review

Review date: 2026-05-02

Status: reviewed_approved_mimic_governed_class6_mvp

Database: `MIMIC-IV-3.1`

Standard variable: `std_nitrite_urinalysis_result`

Variable class: `ordinal_text_semiquantitative_result`

## Decision

MIMIC-IV-3.1 is approved for governed same-name `std_nitrite_urinalysis_result`.

The approved meaning is a source-recorded urinalysis nitrite ordinal result event. The retained result domain is `negative` and `positive`, with raw source result provenance retained for audit.

This approval does not approve numeric urine chemistry, microbiology culture evidence, urinary tract infection phenotype truth, diagnosis code truth, or absence-of-row-as-negative logic under this same variable identity.

## Governed Artifacts

Public governed files:

- `docs/standard_system_mvp/std_nitrite_urinalysis_result/variable_spec.json`
- `docs/standard_system_mvp/std_nitrite_urinalysis_result/mapping_spec_mimic_iv_3_1.json`
- `docs/standard_system_mvp/std_nitrite_urinalysis_result/execution.py`
- `Framework_Guideline/StandardVariableClass_OrdinalTextSemiquantitativeResult_Contract.md`

Runtime evidence:

- first execution: `docs/standard_system_mvp/std_nitrite_urinalysis_result/runtime/mimic_iv_3_1_first_real_execution/`
- rerun: `docs/standard_system_mvp/std_nitrite_urinalysis_result/runtime/mimic_iv_3_1_rerun_repro_check/`
- reproducibility report: `docs/standard_system_mvp/std_nitrite_urinalysis_result/runtime/mimic_iv_3_1_rerun_repro_check/reproducibility_report.json`

Runtime process batches:

- first execution: `20260502T140255Z_MIMIC-IV-3.1_std_nitrite_urinalysis_result`
- rerun: `20260502T140319Z_MIMIC-IV-3.1_std_nitrite_urinalysis_result`

Reproducibility status: `pass`.

## Approved Source Scope

Approved MIMIC source:

- source table: `hosp.labevents`
- supporting source: `hosp.d_labitems` plus retained id maps
- approved source itemids: `51487`, `51987`
- source result field: `value`
- time field: `charttime`

Approved normalization:

| Retained result | Source forms |
| --- | --- |
| `negative` | approved negative text variants such as `NEG`, `NEGATIVE`, `N` |
| `positive` | approved positive text variants such as `POS`, `POSITIVE`, `P` |

Blank and non-interpretable placeholders are excluded rather than coerced into negative results.

## Output Summary

First governed execution output:

- total retained rows: `131,979`
- unique subjects: `66,796`
- unique hospital admissions: `31,080`
- unique ICU stays: `5,223`
- negative rows: `123,979`
- positive rows: `8,000`
- source abnormal true rows: `1,554`

Stay-link status:

| Link status | Rows |
| --- | ---: |
| `insufficient_linkage_info` | `91,488` |
| `hospital_only_no_icu_overlap` | `33,105` |
| `inferred_unique_stay` | `7,385` |
| `ambiguous_multi_stay` | `1` |

The 118 exact event-key duplicate rows are not duplicate source `labevent_id` rows; they are retained source events that collide on the analysis-level event key of subject/admission/stay/time/result and remain traceable by `source_labevent_id_raw`.

## Exclusion Boundary

This approval excludes:

- treating missing retained rows as negative nitrite
- urinary tract infection phenotype truth
- microbiology organism or susceptibility evidence
- diagnosis-code evidence
- continuous numeric urine chemistry
- collapsing hospital-only rows into ICU-stay rows without the retained linkage flag

## Approval Rationale

The mapping is narrow enough for Class 6 because it preserves a finite ordinal/text result domain, raw source result provenance, source item identity, event time, and best-available admission/stay linkage. It also keeps the no-row policy explicit.

## Bottom Line

MIMIC-IV-3.1 is the first governed approved database mapping for Class 6 through `std_nitrite_urinalysis_result`. The next Class 6 work should extend laterally to another urinalysis ordinal result, such as protein or sediment bacteria, rather than reclassifying this as numeric or phenotype truth.
