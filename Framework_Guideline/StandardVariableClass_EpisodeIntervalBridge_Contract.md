# Standard Variable Class Contract: Episode Interval Bridge

Last updated: 2026-05-02

## Purpose

This contract defines the opening Class 5 skeleton for interval variables that retain a positive episode row plus a categorical episode label or parent-link bridge.

This class exists because exact modality episodes are not ordinary binary active flags. A row can still mean an episode is present, but the retained information of interest is the episode label, linkage, or interval bridge rather than only `true`.

## Applicability

This class applies when a variable is all of the following:

- interval-based
- anchored to a target entity such as ICU stay
- carries explicit start and end timing
- carries a categorical episode label, modality label, or parent-link bridge
- has a reviewed source-label inclusion rule
- is not a dose event, device-parameter event, numeric summary, or phenotype

Typical examples:

- `std_rrt_modality_episode`
- `std_vasopressor_support_agent_episode`
- future modality, agent, or bridge interval assets under RRT, respiratory support, ECMO, or multi-agent treatment families

## Non-Applicability

Do not force this class onto variables that are primarily:

- binary active-state outputs without a retained categorical episode label
- continuous numeric event measurements
- baseline, summary, duration, or window outputs
- medication dose event streams
- device parameter event streams
- ordinal or text laboratory results
- diagnosis, demographic, or administrative flags
- composite scores or phenotypes

Those are other classes or later class contracts.

## Opening Interpretation Rule

For the opening MVP, this class is positive-only.

That means:

- a retained row means the labeled episode exists during the recorded interval
- the label field must be retained and governed
- absence of a row means no retained positive labeled episode under the approved source rule
- absence of a row does not prove no parent support state, no treatment, or no uncaptured modality evidence

## Minimum Variable-Spec Rule

The `variable_spec.json` for this class should lock at minimum:

- `variable_id`
- `variable_version`
- categorical episode semantic intent
- `semantic_grain`
- `value_family = categorical_episode`
- `source_value_class` in `positive_modality_episode`, `positive_agent_episode`, or `positive_interval_bridge`
- target entity grain
- anchor family
- label meaning and retained label domain
- start/end interval requirements
- parent-link rule if the variable bridges to a broader parent state
- same-name inclusion and exclusion rule

## Minimum Mapping-Spec Rule

The `mapping_spec_<database>.json` for this class should lock at minimum:

- concrete `database_id`
- concrete source table or source family
- concrete source status or label field
- non-empty retained source-label list
- source grain and target grain
- episode start/end source fields
- label normalization rule
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

- `docs/standard_system_mvp/variable_classes/episode_interval_bridge/`

The first concrete governed example is:

- `docs/standard_system_mvp/std_rrt_modality_episode/`
