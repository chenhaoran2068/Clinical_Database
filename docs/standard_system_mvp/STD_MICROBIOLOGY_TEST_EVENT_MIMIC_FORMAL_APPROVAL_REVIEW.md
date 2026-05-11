# std_microbiology_test_event MIMIC Formal Approval Review

Review date: 2026-05-03

Status: reviewed_approved_mimic_governed_class9_opening_family

Database: `MIMIC-IV-3.1`

Standard variable: `std_microbiology_test_event`

Variable class: `microbiology_multi_entity_family`

## Decision

MIMIC-IV-3.1 is approved for governed same-name `std_microbiology_test_event`.

The approved meaning is a performed microbiology parent specimen-test event. The retained row is the parent event grain and carries specimen/test context, timing, raw comment and Gram-stain helper text, and child organism/susceptibility counts. Child organism and antibiotic susceptibility rows remain separate governed Class 9 entities.

This approval does not approve organism isolate rows, antibiotic susceptibility leaf rows, microbiology orders, antibiotic administration, organism ontology harmonization, suspected-infection phenotype, Sepsis-3 onset, or no-row-as-no-infection logic under this same variable identity.

## Governed Artifacts

Public governed files:

- `docs/standard_system_mvp/std_microbiology_test_event/variable_spec.json`
- `docs/standard_system_mvp/std_microbiology_test_event/mapping_spec_mimic_iv_3_1.json`
- `docs/standard_system_mvp/std_microbiology_test_event/execution.py`
- `Framework_Guideline/StandardVariableClass_MicrobiologyMultiEntityFamily_Contract.md`

Runtime evidence:

- first execution: `docs/standard_system_mvp/std_microbiology_test_event/runtime/mimic_iv_3_1_first_real_execution/`
- rerun: `docs/standard_system_mvp/std_microbiology_test_event/runtime/mimic_iv_3_1_rerun_repro_check/`
- reproducibility report: `docs/standard_system_mvp/std_microbiology_test_event/runtime/mimic_iv_3_1_rerun_repro_check/reproducibility_report.json`

Runtime process batches:

- first execution: `20260502T154552Z_MIMIC-IV-3.1_std_microbiology_test_event`
- rerun: `20260502T154803Z_MIMIC-IV-3.1_std_microbiology_test_event`

Reproducibility status: `pass`.

## Approved Source Scope

Approved MIMIC source:

- source table: `hosp.microbiologyevents`
- source package: `reviewed_unsplit_hosp_microbiologyevents`
- source entity keys: `micro_specimen_id`, `test_seq`
- target grain: one retained parent microbiology specimen-test event row

Opening approved test classes:

- `blood_culture`
- `urine_culture`
- `respiratory_culture`
- `wound_culture`
- `body_fluid_culture`
- `gram_stain`
- `fungal_culture`
- `acid_fast_culture`

## Output Summary

First governed execution output:

- source opening-scope rows: `2,791,324`
- retained parent events: `1,562,787`
- unique subjects: `198,590`
- non-null unique hospital admissions: `160,675`
- null `hadm_id` rows retained as subject-only evidence: `765,553`
- events with organism child: `253,594`
- events with positive isolate child: `213,534`
- events with susceptibility child: `117,722`
- timestamp rows: `1,483,447`
- date-only rows: `79,340`

Opening test class distribution:

| Test class | Rows |
| --- | ---: |
| `blood_culture` | `618,571` |
| `urine_culture` | `502,562` |
| `gram_stain` | `179,660` |
| `respiratory_culture` | `67,425` |
| `body_fluid_culture` | `61,686` |
| `fungal_culture` | `50,443` |
| `wound_culture` | `45,120` |
| `acid_fast_culture` | `37,320` |

Event positivity helper distribution:

| Positivity helper class | Rows |
| --- | ---: |
| `negative_denominator` | `950,279` |
| `positive_numerator` | `185,104` |
| `exclude_mixed_or_contaminated` | `179,595` |
| `manual_review_needed` | `93,539` |
| `exclude_quantity_text_only` | `79,647` |
| `exclude_placeholder_only` | `40,029` |
| `exclude_cancelled_or_invalid` | `20,047` |
| `exclude_commensal_or_normal_flora` | `14,547` |

## Integrity Review

Post-execution content review found:

- duplicate `microbiology_test_event_id` rows: `0`
- organism child rows missing parent test event: `0`
- susceptibility child rows missing parent test event: `0`
- event rows with organism child by child table: `253,594`
- event rows with `has_organism_child`: `253,594`
- event rows with susceptibility child by child table: `117,722`
- event rows with `has_susceptibility_child`: `117,722`

## Exclusion Boundary

This approval excludes:

- treating `has_organism_child` alone as definitive infection truth
- treating no retained event row as no infection, no order, or no antimicrobial exposure
- merging parent event rows with organism isolate rows
- merging parent event rows with antibiotic susceptibility rows
- flattening Gram-stain comments into organism identity without separate review
- converting quantity text into standardized colony-count numeric values

## Approval Rationale

The mapping is narrow enough for Class 9 because it locks the parent event grain, source entity keys, opening microbiology test classes, raw text retention, child-count context, and no-row interpretation. It also proves deterministic first/rerun governed execution with parent-child integrity across the opening MIMIC microbiology family.

## Bottom Line

MIMIC-IV-3.1 is approved for `std_microbiology_test_event` as the parent layer of the opening Class 9 microbiology multi-entity family.
