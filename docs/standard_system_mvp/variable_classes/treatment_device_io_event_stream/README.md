# Variable Class Skeleton: Treatment Device IO Event Stream

Last updated: 2026-05-02

## What This Class Is

`treatment_device_io_event_stream` is the opening Class 4 skeleton for source-faithful event rows from treatment, device, medication, and intake-output sources.

It is used when a retained row means:

- a source-recorded event exists
- the event has a timestamp
- the event has a numeric or amount-like value
- the event has a source unit
- source context is necessary to interpret the value
- parent treatment/support episode links may be useful but do not replace event evidence

The first representative is:

- `std_rrt_fluid_removal_event`

## What This Class Is Not

This class is not:

- a simple physiologic/laboratory numeric measurement class
- a binary active-state episode class
- an exact modality episode class
- a baseline or window-summary class
- a diagnosis/admin flag class
- a support-free-day outcome class
- a phenotype or score class

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

- event-stream concept
- target entity grain
- event time rule
- value and unit meaning
- source-context role
- parent-link policy
- default versus context-only event roles when needed
- downstream aggregation boundary
- no-row interpretation

## Opening Approval Boundary

The opening Class 4 MVP approves only the class shape and the concrete variable that receives its own mapping, runtime evidence, rerun gate, and formal review.
