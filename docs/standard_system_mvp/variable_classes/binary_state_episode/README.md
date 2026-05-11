# Variable Class Skeleton: Binary State Episode

Last updated: 2026-04-28

## What This Class Is

`binary_state_episode` is the first governed class for positive binary active-state variables.

It is used when a retained row means:

- the state is active
- the state has a start time
- the state has an end time
- the state is anchored to an entity such as an ICU stay

The first representative is:

- `std_invasive_mechanical_ventilation_active`

## What This Class Is Not

This class is not:

- a numeric event measurement class
- a numeric baseline or window-summary class
- a medication dose event class
- a device parameter event class
- an ordinal/text result class
- a diagnosis/admin flag class
- a support-free-day outcome class

## Minimum Files For A Governed Variable

Each governed variable in this class should provide:

- `variable_spec.json`
- `mapping_spec_<database>.json`
- `execution.py`
- `runtime/<database>_first_real_execution/validation_report.json`
- `runtime/<database>_first_real_execution/manifest.json`
- `runtime/<database>_rerun_repro_check/validation_report.json`
- `runtime/<database>_rerun_repro_check/manifest.json`
- `runtime/<database>_rerun_repro_check/reproducibility_report.json`

## Required Semantic Locks

A variable in this class should explicitly lock:

- active-state concept
- retained positive value domain
- target entity grain
- source status inclusion rule
- source status exclusion rule
- interval start and end semantics
- no-row interpretation

## Opening Approval Boundary

The opening Class 3 MVP approves only the class shape and first concrete example.

It does not automatically approve every `*_active` variable.

Adjacent respiratory-support variables should still receive their own mapping and review before approval.
