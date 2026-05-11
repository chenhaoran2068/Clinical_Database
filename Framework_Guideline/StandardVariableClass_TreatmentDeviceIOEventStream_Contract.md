# Standard Variable Class Contract: Treatment Device IO Event Stream

Last updated: 2026-05-02

## Purpose

This contract defines the opening Class 4 skeleton for event-stream variables that retain source-recorded treatment, device, or intake-output amount events with timestamp, value, unit, and source context.

This class exists because these variables are not simple physiologic measurements, binary active-state episodes, summary windows, or modality intervals. They are event records that often need treatment/device provenance and downstream aggregation rules.

## Applicability

This class applies when a variable is all of the following:

- event-level
- time-stamped
- numeric or amount-like
- tied to treatment, device, medication, input-output, or support-device operation
- carries source context needed to interpret the value
- may link to a parent treatment/support episode
- is not itself an active flag, exact modality episode, baseline summary, or phenotype

Typical examples:

- `std_rrt_fluid_removal_event`
- future medication input event streams
- future ventilator parameter event streams
- future ECMO device parameter event streams
- future ICU output-event streams

## Non-Applicability

Do not force this class onto variables that are primarily:

- ordinary physiologic or laboratory numeric measurements with one clear source family
- binary active-state episodes
- exact modality or categorical interval episodes
- baseline, summary, duration, or window outputs
- ordinal or text laboratory results
- diagnosis, demographic, or administrative flags
- composite scores or phenotypes

Those are other classes or later class contracts.

## Event-Stream Interpretation Rule

For the opening MVP, this class retains source-faithful event rows.

That means:

- a retained row is a source-recorded treatment/device/IO amount event
- event time must remain source-faithful unless a mapping-specific rule explicitly states otherwise
- value and unit must be retained or deterministically standardized
- source context must be retained because the same numeric value can mean dose, setting, output, counter, or target depending on source semantics
- downstream summaries, smoothing, counter differencing, or episode redistribution are separate governed transformations
- absence of a row means no retained event under the approved source rule, not absence of the treatment or device state

## Minimum Variable-Spec Rule

The `variable_spec.json` for this class should lock at minimum:

- `variable_id`
- `variable_version`
- event-stream semantic intent
- `semantic_grain`
- `value_family = numeric_event_with_context`
- `source_value_class = source_recorded_treatment_device_io_amount_event`
- target entity grain
- anchor family
- event time rule
- event value meaning
- unit rule
- context-role rule
- parent-link rule when applicable
- downstream aggregation boundary
- same-name inclusion and exclusion rule

## Minimum Mapping-Spec Rule

The `mapping_spec_<database>.json` for this class should lock at minimum:

- concrete `database_id`
- concrete source table or source-family expression
- concrete source itemids or source codes
- source event time field
- source value field
- source unit field
- source grain and target grain
- unit normalization rule
- context retention rule
- parent-link translation when applicable
- validation expectations

## Execution Rule

Formal outputs for this class should be produced through one governed execution entrypoint per variable directory.

That execution entrypoint should:

- read the public `variable_spec.json`
- read the public `mapping_spec_<database>.json`
- validate cross-file agreement before execution
- delegate to the current approved local implementation until a more spec-native runner replaces it

## Runtime-Evidence Rule

This class inherits the public runtime-evidence contract from:

- `Framework_Guideline/StandardSystem_RuntimeEvidence_Contract.md`

Formal governed runs should emit:

- `validation_report.json`
- `manifest.json`
- `reproducibility_report.json` when a rerun comparison is recorded

## Current Public Skeleton

The public reusable skeleton lives under:

- `docs/standard_system_mvp/variable_classes/treatment_device_io_event_stream/`

The first concrete governed example is:

- `docs/standard_system_mvp/std_rrt_fluid_removal_event/`
