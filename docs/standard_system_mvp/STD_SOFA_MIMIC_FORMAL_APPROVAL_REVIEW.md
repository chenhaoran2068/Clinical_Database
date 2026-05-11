# std_sofa MIMIC Formal Approval Review

Review date: 2026-05-02

Status: reviewed_approved_mimic_governed_class8_mvp

Database: `MIMIC-IV-3.1`

Standard variable: `std_sofa`

Variable class: `score_phenotype_composite_derived`

## Decision

MIMIC-IV-3.1 is approved for governed same-name `std_sofa`.

The approved meaning is a source-supplied hourly SOFA rolling 24-hour score time series. The retained primary value is `std_sofa_total_24hours` in `score_points`, with same-row component trace context retained.

This approval does not approve raw lab/vital/treatment events, Sepsis-3 onset, AKI/KDIGO phenotype truth, mortality prediction, or score recalculation from scratch under this same variable identity.

## Governed Artifacts

Public governed files:

- `docs/standard_system_mvp/std_sofa/variable_spec.json`
- `docs/standard_system_mvp/std_sofa/mapping_spec_mimic_iv_3_1.json`
- `docs/standard_system_mvp/std_sofa/execution.py`
- `Framework_Guideline/StandardVariableClass_ScorePhenotypeCompositeDerived_Contract.md`

Runtime evidence:

- first execution: `docs/standard_system_mvp/std_sofa/runtime/mimic_iv_3_1_first_real_execution/`
- rerun: `docs/standard_system_mvp/std_sofa/runtime/mimic_iv_3_1_rerun_repro_check/`
- reproducibility report: `docs/standard_system_mvp/std_sofa/runtime/mimic_iv_3_1_rerun_repro_check/reproducibility_report.json`

Runtime process batches:

- first execution: `20260502T140404Z_MIMIC-IV-3.1_std_sofa`
- rerun: `20260502T140817Z_MIMIC-IV-3.1_std_sofa`

Reproducibility status: `pass`.

## Approved Source Scope

Approved MIMIC source:

- source table: `source_supplied_derived.sofa`
- supporting table: `icu.icustays`
- official SQL reference: `References/MIMIC/2026-03-20_snapshot_v2/raw/mimic_code/mimic-iv/concepts/score/sofa.sql`
- source value field: `sofa_24hours`
- source time fields: `hr`, `starttime`, `endtime`
- target grain: one retained score row per `stay_id` and `score_hour_index`

Approved retained context:

- current-hour organ components
- rolling 24-hour organ components
- score hour index
- score hour start/end
- rolling effective score window start/end/hours

## Output Summary

First governed execution output:

- total retained rows: `8,219,121`
- unique ICU stays: `94,437`
- primary score range in current reviewed local asset: `0` to `23`
- canonical approved score range: `0` to `24` score points

Known window profile from the reviewed local evidence package:

- partial windows under 24 hours: `2,031,859`
- full 24-hour windows: `6,187,262`

## Exclusion Boundary

This approval excludes:

- recomputing SOFA from raw labs/vitals/treatments as if it were the same mapping
- changing the source hour grid into exact ICU boundary truth
- interpreting no retained row as SOFA zero
- treating current-hour component scores and rolling 24-hour component scores as interchangeable
- promoting SOFA into Sepsis-3 onset or another phenotype without a separate governed phenotype rule

## Approval Rationale

The mapping is narrow enough for Class 8 because it locks the source-supplied composite score, time basis, primary score value, component trace, output grain, and no-row interpretation. It gives Class 8 a representative governed pattern for scores and composite derived assets without mixing in raw source event extraction.

## Bottom Line

MIMIC-IV-3.1 is the first governed approved database mapping for Class 8 through `std_sofa`. Future Class 8 work should proceed into a separate governed phenotype or score, such as SAPSII/OASIS/AKI/Sepsis-3, with its own component and onset rules.
