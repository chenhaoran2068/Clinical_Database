# Variable Class Skeleton: Diagnosis Admin Demographic ID Map

Last updated: 2026-05-02

## What This Class Is

`diagnosis_admin_demographic_id_map` is Class 7. It covers demographic variables, administrative encounter variables, diagnosis code layers, and identifier maps.

The first representative is:

- `std_sex`

Approved lateral expansions include:

- `std_id_map_subject_hadm`

## Required Semantic Locks

A variable in this class should explicitly lock:

- entity grain
- source authority
- identifier scope
- retained value domain when applicable
- normalization rule
- no-row interpretation

## Minimum Files

Each governed variable in this class should provide:

- `variable_spec.json`
- `mapping_spec_<database>.json`
- `execution.py`
- first execution runtime evidence
- rerun reproducibility evidence
