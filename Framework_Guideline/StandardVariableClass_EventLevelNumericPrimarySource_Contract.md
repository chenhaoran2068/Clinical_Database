# Standard Variable Class Contract: Event-Level Numeric Primary Source

This contract defines the first reusable standard-variable class for the standard-system MVP.

## Applicability

This class applies when a variable is all of the following:

- event-level
- numeric
- time-stamped
- mapped from one clear primary source table/code family per database
- normalizable into one canonical unit/range/cleaning rule set

Typical examples:

- `std_heart_rate`
- `std_respiratory_rate`
- `std_temp`
- `std_sbp`
- `std_dbp`
- `std_map`
- `std_spo2`
- `std_glucose`

## Non-applicability

Do not force this class onto variables that are primarily:

- baseline or summary values
- scores, phenotypes, or multi-step derived constructs
- binary state flags such as `*_active`
- episode or interval outputs
- ordinal or text lab results
- diagnosis, demographic, or administrative variables
- microbiology multi-entity outputs

Those are later classes, not extensions of this one.

## Immutable semantic rule

Within this class, the variable's immutable semantic core must still stay fixed:

- the same `variable_id` must keep the same semantic intent
- a new summary meaning is a new variable, not a version bump
- a new derived meaning is a new variable, not a version bump

Example:

- event-level heart-rate observation = one variable
- average first-day heart rate = a different variable

## Minimum variable-spec rule

The `variable_spec.json` for this class should lock at minimum:

- `variable_id`
- `variable_version`
- event-level semantic intent
- `semantic_grain = time-stamped measurement event`
- `value_family = numeric_measurement`
- canonical unit
- timestamp requirement
- identifier roles
- cleaned canonical range

## Minimum mapping-spec rule

The `mapping_spec_<database>.json` for this class should lock at minimum:

- one concrete `database_id`
- one concrete primary source table
- one concrete source code system
- one non-empty source code list
- source grain and target grain
- identifier normalization notes
- canonical-unit normalization rule
- cleaned-range rule
- validation expectations

## Execution rule

Formal outputs for this class should be produced through one governed execution entrypoint per variable directory.

That execution entrypoint should:

- read the public `variable_spec.json`
- read the public `mapping_spec_<database>.json`
- validate cross-file agreement before execution
- delegate to the current approved local implementation until a more spec-native runner replaces it

## Runtime-evidence rule

This class inherits the public runtime-evidence contract from:

- `Framework_Guideline/StandardSystem_RuntimeEvidence_Contract.md`

So formal governed runs should emit:

- `validation_report.json`
- `manifest.json`
- `reproducibility_report.json` when a rerun comparison is recorded

## First-class rollout rule

This is the first reusable class, not the universal final schema.

Current interpretation:

- use this class to industrialize the first large batch of simple event-level numeric variables
- do not claim that it already covers every standard-variable family in the repository

## Current public skeleton

The public reusable skeleton currently lives under:

- `docs/standard_system_mvp/variable_classes/event_level_numeric_primary_source/`

The first concrete governed example is:

- `docs/standard_system_mvp/std_heart_rate/`
