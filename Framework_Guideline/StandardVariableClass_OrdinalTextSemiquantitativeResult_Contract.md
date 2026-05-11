# Standard Variable Class Contract: Ordinal Text Semiquantitative Result

Last updated: 2026-05-02

## Purpose

This contract defines Class 6 for laboratory or assessment results whose retained value is categorical, ordinal, text-normalized, or semiquantitative rather than continuous numeric.

This class exists because values such as `negative`, `trace`, `1+`, `small`, `moderate`, `large`, `few`, or `many` should not be forced into ordinary numeric measurement semantics.

## Applicability

This class applies when a variable:

- retains a source-recorded event or result row
- has a finite governed result domain
- may normalize raw text, source flags, or semiquantitative numeric ladders
- keeps raw source result provenance
- is not a continuous numeric lab/vital event
- is not a binary active state, treatment episode, demographic/admin variable, or composite phenotype

Typical examples:

- `std_nitrite_urinalysis_result`
- `std_protein_urinalysis_result`
- urine sediment bacteria or cast results

## Non-Applicability

Do not use this class for:

- continuous numeric labs
- device or medication event streams
- treatment active states
- diagnosis code events
- demographic or identifier maps
- score or phenotype outputs

## Minimum Variable-Spec Rule

The `variable_spec.json` should lock:

- `variable_id`
- semantic intent and result grain
- `value_family`
- `source_value_class = source_recorded_ordinal_text_result`
- target entity grain
- result domain rule
- raw result retention rule
- normalization rule
- no-row interpretation

## Minimum Mapping-Spec Rule

The `mapping_spec_<database>.json` should lock:

- database id
- source table and source item/code list
- source result field
- source grain and target grain
- normalization translation
- raw result retention translation
- validation expectations

## Runtime-Evidence Rule

This class inherits:

- `Framework_Guideline/StandardSystem_RuntimeEvidence_Contract.md`

Formal governed runs should emit validation, manifest, and rerun reproducibility evidence.

## Current Public Skeleton

The public reusable skeleton lives under:

- `docs/standard_system_mvp/variable_classes/ordinal_text_semiquantitative_result/`

The first concrete governed example is:

- `docs/standard_system_mvp/std_nitrite_urinalysis_result/`
