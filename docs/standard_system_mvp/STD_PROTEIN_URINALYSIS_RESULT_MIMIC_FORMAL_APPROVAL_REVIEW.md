# std_protein_urinalysis_result MIMIC Formal Approval Review

Review date: 2026-05-02

Status: reviewed_approved_mimic_governed_class6_lateral_expansion

Database: `MIMIC-IV-3.1`

Standard variable: `std_protein_urinalysis_result`

Variable class: `ordinal_text_semiquantitative_result`

## Decision

MIMIC-IV-3.1 is approved for governed same-name `std_protein_urinalysis_result`.

The approved meaning is a source-recorded urinalysis protein ordinal result event. The retained result domain is `negative`, `trace`, `mild_positive`, `moderate_positive`, `marked_positive`, and `severe_positive`, with raw source provenance and best-available admission/stay linkage retained.

This approval does not approve quantitative urine protein, total protein urine, protein/creatinine ratio, kidney phenotype, diagnosis code truth, or absence-of-row-as-negative logic under this same variable identity.

## Governed Artifacts

Public governed files:

- `docs/standard_system_mvp/std_protein_urinalysis_result/variable_spec.json`
- `docs/standard_system_mvp/std_protein_urinalysis_result/mapping_spec_mimic_iv_3_1.json`
- `docs/standard_system_mvp/std_protein_urinalysis_result/execution.py`
- `Framework_Guideline/StandardVariableClass_OrdinalTextSemiquantitativeResult_Contract.md`

Runtime evidence:

- first execution: `docs/standard_system_mvp/std_protein_urinalysis_result/runtime/mimic_iv_3_1_first_real_execution/`
- rerun: `docs/standard_system_mvp/std_protein_urinalysis_result/runtime/mimic_iv_3_1_rerun_repro_check/`
- reproducibility report: `docs/standard_system_mvp/std_protein_urinalysis_result/runtime/mimic_iv_3_1_rerun_repro_check/reproducibility_report.json`

Runtime process batches:

- first execution: `20260502T144940Z_MIMIC-IV-3.1_std_protein_urinalysis_result`
- rerun: `20260502T144953Z_MIMIC-IV-3.1_std_protein_urinalysis_result`

Reproducibility status: `pass`.

## Approved Source Scope

Approved MIMIC source:

- source table: `hosp.labevents`
- supporting source: `hosp.d_labitems` plus retained id maps
- approved source itemids: `51492`, `51992`
- source result field: `value`
- source time field: `charttime`
- source unit in retained rows: `mg/dL`

Approved normalization retains the semiquantitative dipstick ladder rather than converting it to a continuous numeric measurement.

## Output Summary

First governed execution output:

- total retained rows: `380,346`
- unique subjects: `139,077`
- unique hospital admissions: `99,160`
- unique ICU stays: `20,998`
- source abnormal true rows: `129,033`
- artifact numeric variant rows excluded: `1`
- placeholder rows excluded: `464,846`

Retained result distribution:

| Result | Rows |
| --- | ---: |
| `mild_positive` | `166,099` |
| `negative` | `81,205` |
| `moderate_positive` | `56,884` |
| `trace` | `54,296` |
| `marked_positive` | `18,421` |
| `severe_positive` | `3,441` |

Stay-link status:

| Link status | Rows |
| --- | ---: |
| `insufficient_linkage_info` | `236,909` |
| `hospital_only_no_icu_overlap` | `110,616` |
| `inferred_unique_stay` | `32,819` |
| `ambiguous_multi_stay` | `2` |

The 803 exact event-key duplicate rows are retained source events that collide on an analysis-level key; source-row provenance remains available through raw labevent identifiers.

## Exclusion Boundary

This approval excludes:

- treating missing retained rows as negative protein
- converting this ordinal dipstick result into a continuous mg/dL lab measurement
- merging with `std_total_protein_urine`
- merging with protein/creatinine ratio
- using the result directly as kidney disease, AKI, CKD, or nephrotic phenotype truth

## Approval Rationale

The mapping is a clean Class 6 lateral expansion because it keeps finite ordinal-result semantics, raw source provenance, source-item scope, event time, and no-row interpretation explicit. It also verifies that the protein urinalysis line remains separate from quantitative protein assets.

## Bottom Line

MIMIC-IV-3.1 is approved for `std_protein_urinalysis_result` as a second governed Class 6 urinalysis ordinal result after nitrite. The next Class 6 work can continue to leukocytes or urine sediment results using the same bounded ordinal-result pattern.
