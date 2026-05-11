# Standard Variable Class Contract: Score Phenotype Composite Derived

Last updated: 2026-05-02

## Purpose

This contract defines Class 8 for scores, phenotypes, and composite derived variables.

This class exists because these variables are governed by multi-component rules, time windows, component trace, and phenotype definitions rather than by a single source field.

## Applicability

This class applies when a variable:

- is a clinical score, phenotype, onset definition, or composite derived construct
- uses multiple component inputs or an official source-supplied composite table
- needs component trace, time-window semantics, or derivation-rule documentation
- is not merely a source event, active flag, interval episode, demographic field, or ordinal text result

Typical examples:

- `std_sofa`
- `std_sofa_first_day`
- `std_aki_kdigo`
- `std_sepsis3_onset_*`
- `std_oasis`
- `std_sapsii`

## Non-Applicability

Do not use this class for:

- source numeric lab/vital events
- baseline/window numeric summaries
- treatment active flags
- treatment/device/IO source events
- administrative or demographic source fields
- microbiology multi-entity families

## Minimum Variable-Spec Rule

The `variable_spec.json` should lock:

- score or phenotype identity
- target entity grain
- time basis rule
- component trace rule
- primary score or phenotype value rule
- no-row interpretation
- same-name cross-database boundary

## Minimum Mapping-Spec Rule

The `mapping_spec_<database>.json` should lock:

- source table or derived source package
- source value field
- source grain and target grain
- time basis translation
- score value translation
- component trace translation
- validation expectations

## Runtime-Evidence Rule

This class inherits:

- `Framework_Guideline/StandardSystem_RuntimeEvidence_Contract.md`

## Current Public Skeleton

The public reusable skeleton lives under:

- `docs/standard_system_mvp/variable_classes/score_phenotype_composite_derived/`

The first concrete governed example is:

- `docs/standard_system_mvp/std_sofa/`
