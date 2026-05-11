# Standard Variable Class Contract: Diagnosis Admin Demographic ID Map

Last updated: 2026-05-02

## Purpose

This contract defines Class 7 for diagnosis, administrative, demographic, and identifier-map variables.

This class exists because these variables are not ordinary clinical measurements. Their main burden is source authority, entity grain, identifier scope, and normalization of administrative or demographic categories.

## Applicability

This class applies when a variable primarily represents:

- patient, encounter, or stay identifiers
- demographic categories
- administrative encounter attributes
- diagnosis code events or diagnosis-derived code layers

Typical examples:

- `std_sex`
- `std_age`
- `std_race`
- `std_id_map_subject_hadm`
- `std_id_map_subject_hadm_stay`
- ICD diagnosis event layers

## Non-Applicability

Do not use this class for:

- numeric vitals/labs
- treatment active states or episodes
- device/IO event streams
- ordinal laboratory result text
- composite scores or phenotypes

## Minimum Variable-Spec Rule

The `variable_spec.json` should lock:

- `variable_id`
- target entity grain
- identifier scope rule
- source authority rule
- normalization rule
- retained value domain when applicable
- no-row interpretation

## Minimum Mapping-Spec Rule

The `mapping_spec_<database>.json` should lock:

- source table
- source identifier and value fields
- source grain and target grain
- identifier translation
- value normalization translation
- validation expectations

## Runtime-Evidence Rule

This class inherits:

- `Framework_Guideline/StandardSystem_RuntimeEvidence_Contract.md`

## Current Public Skeleton

The public reusable skeleton lives under:

- `docs/standard_system_mvp/variable_classes/diagnosis_admin_demographic_id_map/`

The first concrete governed example is:

- `docs/standard_system_mvp/std_sex/`
