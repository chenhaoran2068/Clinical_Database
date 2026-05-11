# std_microbiology_organism_isolate MIMIC Formal Approval Review

Review date: 2026-05-03

Status: reviewed_approved_mimic_governed_class9_opening_family

Database: `MIMIC-IV-3.1`

Standard variable: `std_microbiology_organism_isolate`

Variable class: `microbiology_multi_entity_family`

## Decision

MIMIC-IV-3.1 is approved for governed same-name `std_microbiology_organism_isolate`.

The approved meaning is an organism branch under a retained microbiology parent specimen-test event. The retained row preserves raw organism label, isolate number, branch role, positivity-analysis helper class, quantity/comment text, and parent-child linkage to both the parent test event and downstream susceptibility leaves.

This approval does not approve parent microbiology test events, antibiotic susceptibility leaves, organism ontology harmonization, infection phenotype truth, positive-culture-only flags, or no-row-as-no-organism logic under this same variable identity.

## Governed Artifacts

Public governed files:

- `docs/standard_system_mvp/std_microbiology_organism_isolate/variable_spec.json`
- `docs/standard_system_mvp/std_microbiology_organism_isolate/mapping_spec_mimic_iv_3_1.json`
- `docs/standard_system_mvp/std_microbiology_organism_isolate/execution.py`
- `Framework_Guideline/StandardVariableClass_MicrobiologyMultiEntityFamily_Contract.md`

Runtime evidence:

- first execution: `docs/standard_system_mvp/std_microbiology_organism_isolate/runtime/mimic_iv_3_1_first_real_execution/`
- rerun: `docs/standard_system_mvp/std_microbiology_organism_isolate/runtime/mimic_iv_3_1_rerun_repro_check/`
- reproducibility report: `docs/standard_system_mvp/std_microbiology_organism_isolate/runtime/mimic_iv_3_1_rerun_repro_check/reproducibility_report.json`

Runtime process batches:

- first execution: `20260502T155017Z_MIMIC-IV-3.1_std_microbiology_organism_isolate`
- rerun: `20260502T155225Z_MIMIC-IV-3.1_std_microbiology_organism_isolate`

Reproducibility status: `pass`.

## Approved Source Scope

Approved MIMIC source:

- source table: `hosp.microbiologyevents`
- source package: `reviewed_unsplit_hosp_microbiologyevents`
- source entity keys: `micro_specimen_id`, `test_seq`, `org_itemid`, `isolate_num`, `org_name`
- target grain: one retained organism branch row per `microbiology_organism_branch_id`

Opening approved test classes:

- `blood_culture`
- `urine_culture`
- `respiratory_culture`
- `wound_culture`
- `body_fluid_culture`
- `fungal_culture`
- `acid_fast_culture`

## Output Summary

First governed execution output:

- source opening-scope rows: `2,791,324`
- retained organism branch rows: `306,613`
- unique subjects: `89,352`
- non-null unique hospital admissions: `51,516`
- null `hadm_id` rows retained as subject-only evidence: `180,039`
- rows with susceptibility child: `139,153`
- rows with quantity text: `27`
- rows with comment text: `49,019`
- maximum susceptibility rows under one organism branch: `23`

Opening test class distribution:

| Test class | Rows |
| --- | ---: |
| `urine_culture` | `127,455` |
| `blood_culture` | `76,757` |
| `wound_culture` | `40,589` |
| `respiratory_culture` | `35,099` |
| `body_fluid_culture` | `17,056` |
| `fungal_culture` | `8,073` |
| `acid_fast_culture` | `1,584` |

Organism positivity-analysis distribution:

| Class | Rows |
| --- | ---: |
| `count_as_positive_isolate` | `262,045` |
| `exclude_cancelled_placeholder` | `37,140` |
| `exclude_flora_or_mixed_summary` | `7,428` |

## Integrity Review

Post-execution content review found:

- duplicate `microbiology_organism_branch_id` rows: `0`
- organism rows missing parent `microbiology_test_event_id`: `0`
- susceptibility rows missing parent `microbiology_organism_branch_id`: `0`
- organism rows with susceptibility child by child table: `139,153`
- organism rows with `susceptibility_row_count > 0`: `139,153`

## Exclusion Boundary

This approval excludes:

- treating every retained organism branch as a true infection
- treating summary flora or mixed flora as a counted positive isolate without using `organism_positive_analysis_class`
- treating no retained organism row as negative culture
- converting raw organism names to an ontology concept table under the same variable identity
- merging susceptibility interpretation into the organism branch grain

## Approval Rationale

The mapping is narrow enough for Class 9 because it locks organism-branch grain, parent test-event linkage, raw organism text retention, explicit branch-role and positivity helper classes, and downstream susceptibility child counts. It also proves deterministic first/rerun governed execution and zero parent-link gaps.

## Bottom Line

MIMIC-IV-3.1 is approved for `std_microbiology_organism_isolate` as the organism-branch layer of the opening Class 9 microbiology multi-entity family.
