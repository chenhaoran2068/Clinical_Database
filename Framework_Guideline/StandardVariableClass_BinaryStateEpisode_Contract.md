# Standard Variable Class Contract: Binary State Episode

Last updated: 2026-04-28

## Purpose

This contract defines the third reusable standard-variable class for the standard-system MVP.

This class exists because binary active-state assets are not ordinary numeric event streams and are not numeric baseline/window summaries.

## Applicability

This class applies when a variable is all of the following:

- time-varying state or active flag
- binary in retained interpretation
- represented as one row per positive state episode or interval
- anchored to an explicit target entity such as ICU stay
- carries explicit start and end timing
- has a clearly approved source-status inclusion rule
- keeps the active-state meaning separate from dose, device parameters, and downstream free-day outcomes

Typical examples:

- `std_invasive_mechanical_ventilation_active`
- `std_noninvasive_ventilation_active`
- `std_high_flow_nasal_cannula_active`
- `std_supplemental_oxygen_active`
- `std_tracheostomy_status_active`

## Non-Applicability

Do not force this class onto variables that are primarily:

- continuous numeric event measurements
- numeric baseline, summary, duration, or window outputs
- medication dose event streams
- device parameter event streams
- input or output amount event streams
- multi-agent treatment episode families requiring agent-level provenance
- diagnosis, demographic, or administrative flags
- ordinal/text/semiquantitative laboratory results
- derived support-free-day outcomes
- composite scores or phenotypes

Those are other classes or later class contracts.

## Positive-Only Interpretation Rule

For the opening MVP, this class is positive-only.

That means:

- a retained row means the state is active during the recorded interval
- the retained value field should be `true` for all retained rows
- absence of a row means no retained positive state episode under the approved source rule
- absence of a row does not prove all possible support, treatment, or status evidence was absent

If a future database needs explicit negative rows, that should be a contract revision rather than a silent extension.

## Immutable Semantic Rule

Within this class, the variable's immutable semantic core must stay fixed.

The same `variable_id` must keep:

- the same active-state concept
- the same target state scope
- the same broad target entity grain
- the same same-name inclusion boundary

Examples:

- invasive mechanical ventilation active = one variable
- noninvasive ventilation active = a different variable
- any advanced respiratory support active = a different broader variable
- invasive mechanical ventilation free days = a different outcome variable

## Minimum Variable-Spec Rule

The `variable_spec.json` for this class should lock at minimum:

- `variable_id`
- `variable_version`
- active-state semantic intent
- `semantic_grain`
- `value_family = binary_state`
- `source_value_class = positive_state_episode`
- target entity grain
- anchor family
- start/end interval requirements
- retained value domain
- same-name inclusion and exclusion rule

## Minimum Mapping-Spec Rule

The `mapping_spec_<database>.json` for this class should lock at minimum:

- concrete `database_id`
- concrete source table
- concrete source status field
- non-empty included source-status code list
- source grain and target grain
- identifier normalization notes
- episode start/end source fields
- state-value normalization rule
- positive-only no-row interpretation
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

- `docs/standard_system_mvp/variable_classes/binary_state_episode/`

The first concrete governed example is:

- `docs/standard_system_mvp/std_invasive_mechanical_ventilation_active/`
