# std_microbiology_antibiotic_susceptibility MIMIC Formal Approval Review

Review date: 2026-05-03

Status: reviewed_approved_mimic_governed_class9_opening_family

Database: `MIMIC-IV-3.1`

Standard variable: `std_microbiology_antibiotic_susceptibility`

Variable class: `microbiology_multi_entity_family`

## Decision

MIMIC-IV-3.1 is approved for governed same-name `std_microbiology_antibiotic_susceptibility`.

The approved meaning is an antibiotic susceptibility leaf row under an organism branch and parent microbiology test event. The retained row preserves raw antibiotic label, raw interpretation code, standardized interpretation helper class, dilution context, and parent-child linkage.

This approval does not approve antibiotic administration, prescription intent, medication exposure, parent culture events, organism isolate summaries, infection phenotype truth, antibiogram summaries, or no-row-as-susceptible/resistant logic under this same variable identity.

## Governed Artifacts

Public governed files:

- `docs/standard_system_mvp/std_microbiology_antibiotic_susceptibility/variable_spec.json`
- `docs/standard_system_mvp/std_microbiology_antibiotic_susceptibility/mapping_spec_mimic_iv_3_1.json`
- `docs/standard_system_mvp/std_microbiology_antibiotic_susceptibility/execution.py`
- `Framework_Guideline/StandardVariableClass_MicrobiologyMultiEntityFamily_Contract.md`

Runtime evidence:

- first execution: `docs/standard_system_mvp/std_microbiology_antibiotic_susceptibility/runtime/mimic_iv_3_1_first_real_execution/`
- rerun: `docs/standard_system_mvp/std_microbiology_antibiotic_susceptibility/runtime/mimic_iv_3_1_rerun_repro_check/`
- reproducibility report: `docs/standard_system_mvp/std_microbiology_antibiotic_susceptibility/runtime/mimic_iv_3_1_rerun_repro_check/reproducibility_report.json`

Runtime process batches:

- first execution: `20260502T155441Z_MIMIC-IV-3.1_std_microbiology_antibiotic_susceptibility`
- rerun: `20260502T155650Z_MIMIC-IV-3.1_std_microbiology_antibiotic_susceptibility`

Reproducibility status: `pass`.

## Approved Source Scope

Approved MIMIC source:

- source table: `hosp.microbiologyevents`
- source package: `reviewed_unsplit_hosp_microbiologyevents`
- source entity keys: `microevent_id`, `micro_specimen_id`, `test_seq`, `org_itemid`, `isolate_num`, `ab_itemid`
- target grain: one retained antibiotic susceptibility leaf row

Opening approved test classes:

- `blood_culture`
- `urine_culture`
- `respiratory_culture`
- `wound_culture`
- `body_fluid_culture`
- `fungal_culture`

## Output Summary

First governed execution output:

- source opening-scope rows: `2,791,324`
- retained susceptibility leaf rows: `1,314,671`
- unique subjects: `52,973`
- non-null unique hospital admissions: `33,109`
- null `hadm_id` rows retained as subject-only evidence: `838,045`
- S/I/R standard eligible rows: `1,314,419`
- resistance analysis eligible rows: `1,314,412`
- rows with dilution text: `1,284,277`
- rows with dilution value: `1,283,868`
- rows with comment text: `290,960`

Opening test class distribution:

| Test class | Rows |
| --- | ---: |
| `urine_culture` | `823,984` |
| `wound_culture` | `157,682` |
| `blood_culture` | `135,674` |
| `respiratory_culture` | `124,715` |
| `body_fluid_culture` | `72,253` |
| `fungal_culture` | `363` |

Interpretation class distribution:

| Interpretation class | Rows |
| --- | ---: |
| `susceptible` | `1,050,745` |
| `resistant` | `224,987` |
| `intermediate` | `38,687` |
| `susceptible_dose_dependent` | `203` |
| `other_rare_raw_code` | `49` |

## Integrity Review

Post-execution content review found:

- duplicate `source_microevent_id` rows: `0`
- susceptibility rows missing parent `microbiology_test_event_id`: `0`
- susceptibility rows missing parent `microbiology_organism_branch_id`: `0`
- resistance analysis eligible rows: `1,314,412`
- resistance analysis ineligible rows: `259`

## Exclusion Boundary

This approval excludes:

- treating susceptibility leaf rows as antibiotic administrations
- treating no retained susceptibility row as susceptible, resistant, no organism, or no culture
- collapsing S/I/R/D/rare raw codes into a binary result without a downstream analysis rule
- summarizing into an antibiogram under the same variable identity
- merging susceptibility rows into organism isolate or parent culture event grain

## Approval Rationale

The mapping is narrow enough for Class 9 because it locks susceptibility-leaf grain, parent organism and parent event linkage, raw antibiotic and interpretation retention, standardized interpretation helper classes, and explicit no-row interpretation. It also proves deterministic first/rerun governed execution and zero parent-link gaps.

## Bottom Line

MIMIC-IV-3.1 is approved for `std_microbiology_antibiotic_susceptibility` as the susceptibility-leaf layer of the opening Class 9 microbiology multi-entity family.
