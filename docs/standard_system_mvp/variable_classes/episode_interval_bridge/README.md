# Variable Class Skeleton: Episode Interval Bridge

Last updated: 2026-05-02

## What This Class Is

`episode_interval_bridge` is the opening Class 5 skeleton for positive interval rows that retain a categorical episode label or bridge back to a parent support episode.

It is used when a retained row means:

- an episode exists
- the episode has a start time
- the episode has an end time
- the episode has a governed label such as an exact modality or agent
- parent-link fields may be needed to connect it to broader support-state variables

The first representative is:

- `std_rrt_modality_episode`
- `std_vasopressor_support_agent_episode`

## What This Class Is Not

This class is not:

- a simple binary active-state class
- a numeric event measurement class
- a numeric baseline or window-summary class
- a medication dose event class
- a device parameter event class
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

- episode concept
- target entity grain
- retained label meaning
- retained label domain
- source-label inclusion rule
- interval start and end semantics
- parent-link rule when applicable
- no-row interpretation

## Opening Approval Boundary

The opening Class 5 MVP approves only the class shape and the concrete variable that receives its own mapping, runtime evidence, rerun gate, and formal review.
