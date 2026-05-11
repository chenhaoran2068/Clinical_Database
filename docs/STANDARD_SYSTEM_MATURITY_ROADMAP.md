# Standard-System Maturity Roadmap

Last updated: 2026-04-23

## Why this note exists

`Clinical_Database` already works as a human-readable, reviewable, traceable public method repository.

That is a real achievement, but it is not yet the same thing as a full standard system.

The next transition is:

- from human-readable to machine-readable
- from review-guided to executable
- from documented to verifiable
- from name-based to stable-ID-based
- from strong records to strong reproducibility
- from descriptive governance to enforceable standard execution

This note formalizes that transition.

It does not replace the contracts in `Framework_Guideline/`.
It explains how the existing method repository can grow into a stricter cross-database semantic standard layer.

For the formal definition of what counts as "current stage complete" before this next transition begins, use [`docs/CURRENT_STAGE_COMPLETION_STANDARD.md`](CURRENT_STAGE_COMPLETION_STANDARD.md).

## Current baseline already achieved

The project already has:

- a public GitHub-safe method repository
- explicit Layer 1 / Layer 4 / Layer 5 contracts
- database-family and database-version onboarding surfaces
- public workflow entrypoints and repository checks
- local reviewed-approved retained-variable assets
- public standard-variable cards for approved variables
- local knowledge packages, review notes, manifests, and audit trails

So the starting point is not "from zero".

The accurate current description is:

- strong human-readable method framework
- early public governance layer
- partial local reproducibility evidence
- not yet a full machine-executable standard system

## Final target posture

The final target is not "another OMOP" and not "another FHIR server model".

The target is a stricter layer above raw databases and before downstream analysis:

- cross-database semantic standard layer
- standard-variable identity and version layer
- executable build-contract layer
- structured mapping and risk layer
- auditable and reproducible evidence layer
- automatic validation and admission gate
- standard execution layer

In short:

The project should let a user say "this is the same standard variable across databases" and then prove:

- what it means
- how it is represented
- how it is built
- how each database maps to it
- what risks apply
- how to rerun and verify it

## Six-layer maturity table

| Layer | Current state | Target state | Main gaps | Next action |
| --- | --- | --- | --- | --- |
| 1. Standard variable dictionary | `std_xxx` naming, concept direction, public cards, cross-database intent already exist | Stable `variable_id`, explicit `variable_version`, immutable semantic core, explicit source-value-class boundary, structured definition, explicit external-alignment model | identity still leans on names; immutable semantic core is not yet locked; source-value-class boundaries are not yet explicit; definition is mostly prose; external alignment is not systematic | publish identity/version contract, define immutable semantic core and value-origin boundary, and create a pilot registry with `mapping_type` |
| 2. Standard representation rules | unit/type/grain/precision awareness exists in reviews and cards | machine-readable representation schema that can reject invalid metadata through type/unit/range validation | no shared executable schema; no automatic validator; metadata is not yet rejectable on failure | publish representation schema and rejecting validator; backfill pilot variables |
| 3. Standard build rules | multi-source, multi-time-point, multi-candidate logic is already discussed in reviews | executable build spec fully structured into `time_window`, `selection`, `aggregation`, and `tie_break`, with no natural-language dependency in the executable layer | build logic is still mainly narrative; ambiguous prose can still leak into implementation | define rule taxonomy and create a reference executable spec for a pilot batch |
| 4. Database mapping rules | source tables/fields are often explained in local packages and shared extract code | structured mapping spec with source package, table, column, joins, filters, explicit source-to-target grain conversion, transformation rule, and identifier normalization notes | mapping is clearer than before, but not yet a formal mapping contract; grain conversion is not always explicit | define mapping schema with mandatory grain fields and backfill reviewed-approved pilot variables |
| 5. Risk and exception model | database-specific caveats and semantic warnings already exist in prose and contracts | structured risk fields plus prose explanation, with severity and executable action semantics such as `block`, `warn`, or `allow` | risks are not yet machine-consumable; publication logic cannot yet act on risk automatically | define structured risk schema and block unresolved high-severity or `block` action issues in publication flow |
| 6. Reproducible evidence chain | knowledge packages, manifests, review notes, public cards, and audits already exist | hard-linked chain `variable_spec -> mapping_spec -> execution_code -> output_dataset -> validation_report -> review_record`, with rerun verification and object signatures | evidence is strong, but lineage is not yet fully bound and rerun checks are not institutionalized | define reproducibility manifest and verification gate for approved variables |

## Hidden system layer: Execution Layer

The six layers above define what the standard system means.

They still need a running layer that executes those meanings.

That hidden but necessary layer is the `Execution Layer`.

Its minimum job is:

- read variable spec
- read database mapping spec
- apply build rules
- run execution code
- run validation
- emit output plus reproducibility manifest

All formal outputs must be produced through this governed execution path.

Outputs produced through ad hoc SQL, side scripts, or ungoverned notebooks may still exist for exploration, but they do not count as formal standard-variable outputs.

The target interface is intentionally simple:

- `run(variable_id, database_id, variable_version)`

Without this layer, the six layers remain a strong static structure.

With this layer, they become an actual standard system.

## Ordered build plan

The recommended order is:

1. stabilize identity and version semantics
2. formalize representation schema
3. formalize build-rule schema
4. formalize mapping schema
5. formalize risk schema
6. formalize reproducibility and validation gates
7. formalize the execution layer around the six structured specs

This order matters because later layers depend on earlier ones.

For example:

- executable mapping is weaker without stable variable identity
- reproducibility is weaker without executable build rules
- validation is weaker without structured representation and risk fields

## Workstream 1: Standard variable dictionary foundation

### Goal

Separate standard-variable identity from display name.

### Required deliverables

- one global identity/version contract
- one machine-readable variable-registry schema
- one pilot registry artifact for the first approved variable batch
- one explicit immutable-semantic-core rule
- one explicit source-value-class rule defining whether a variable accepts:
  - raw measured values only
  - derived values only
  - aggregated values only
  - a governed mixed mode
- explicit `mapping_type` support:
  - `exact`
  - `broader`
  - `narrower`
  - `derived`
  - `none`
- explicit external-reference fields for relevant standards such as `LOINC`, `SNOMED CT`, and `ICD`
- one external-terminology policy stating that standards such as `SNOMED CT` and `LOINC` act as semantic anchors when applicable, not as the primary identity skeleton of the system

### Review standard

This workstream is only complete when:

- a variable can be renamed without losing identity
- the immutable semantic core is explicit and cannot drift through versioning
- the variable explicitly states whether raw measured values, derived values, aggregated values, or a governed mixed mode are allowed
- every pilot variable has a stable `variable_id`
- every pilot variable has an explicit version rule
- every pilot variable states whether external mapping is exact, approximate, derived, or unavailable
- external terminology references help anchor meaning when appropriate, but derived or mixed variables are not forced into false one-to-one mappings

Version may evolve:

- representation
- build rules
- mapping

Version may not silently change:

- semantic intent
- category-level variable identity

If the semantic core changes, that is a new variable, not a new version.

If the allowed source-value class changes in a way that changes the semantic meaning of the variable, that is also a new variable rather than a silent version bump.

### First execution scope

Use a small mixed pilot batch:

- one simple observation variable
- one cross-database outcome variable
- one derived or scored variable

That pilot batch is enough to expose ID/version edge cases before broad backfill.

## Workstream 2: Standard representation schema

### Goal

Make variable representation machine-readable and automatically checkable.

### Required deliverables

- one representation contract
- one schema covering at least:
  - `unit`
  - `value_type`
  - `storage_precision`
  - `display_precision`
  - `hard_valid_range`
  - `plausible_clinical_range`
  - `semantic_grain`
  - `identifier_roles`
  - null/missingness semantics
- one validator script
- one pilot backfill set
- one explicit canonical-unit normalization rule stating that all accepted inputs must normalize to the canonical unit or fail validation

### Review standard

This workstream is only complete when:

- invalid metadata is rejected rather than merely described
- type, unit, and range failures can all produce explicit validation failure
- inputs that cannot be normalized into the canonical unit are rejected rather than silently mixed
- the schema can reject malformed representation metadata
- precision is split into storage and display layers
- valid-range semantics distinguish hard-invalid from clinically implausible
- the same representation rules can be checked without reading prose

### First execution scope

Backfill the same pilot variables selected in Workstream 1 so identity and representation stay aligned.

## Workstream 3: Executable build-rule specification

### Goal

Turn review-language build logic into executable specifications.

### Required deliverables

- one controlled vocabulary for build rules
- structured fields for:
  - selection rule
  - time window
  - aggregation rule
  - tie-break rule
  - source-priority rule
- one reference runner or translator layer
- one pilot equivalence test showing the spec reproduces the approved interpretation

### Review standard

This workstream is only complete when:

- two independent readers would derive the same executable logic from the same spec
- the pilot executable spec reproduces the approved interpretation on frozen input
- ambiguous wording such as "nearest" or "best" is replaced by explicit rule values
- the executable rule layer does not depend on free-form natural language

The executable rule block should converge toward a shape like:

- `time_window`
- `selection`
- `aggregation`
- `tie_break`

### First execution scope

Start with variables whose logic is understandable but nontrivial:

- one event-style observation
- one baseline-style variable
- one follow-up or outcome variable

## Workstream 4: Database mapping specification

### Goal

Replace explanatory mapping notes with formal mapping specifications.

### Required deliverables

- one mapping schema
- structured fields for:
  - source package
  - source table
  - source code system
  - source codes
  - source column
  - join path
  - filter condition
  - source grain
  - target grain
  - grain conversion rule
  - transformation rule
  - identifier normalization notes
- one pilot set of mapping specs tied to approved variables

### Review standard

This workstream is only complete when:

- a third party can reconstruct the intended query path from the mapping spec
- a third party can tell exactly which raw source codes are in-scope for the variable in that database
- source grain and target grain are explicit
- grain conversion is explicit whenever source and target grains differ
- identifier remapping, such as raw-source IDs to `subject_id` / `hadm_id` / `stay_id`, is formal rather than implied

### First execution scope

Prefer variables with already-cleaned public semantics and known local reviewed-approved assets.

## Workstream 5: Structured risk and exception model

### Goal

Make database-specific caveats machine-visible without losing human-readable explanation.

### Required deliverables

- one structured risk schema
- required fields for:
  - `risk_type`
  - `severity`
  - `affected_scope`
  - `affected_databases`
  - `trigger_condition`
  - `required_action`
  - `publication_impact`
- one paired prose summary field for human interpretation
- one publication rule for unresolved high-severity risks

### Review standard

This workstream is only complete when:

- unresolved high-severity risks can be detected automatically
- publication logic can distinguish warning-only vs blocking issues
- the machine-readable risk block and the prose explanation do not contradict each other
- the system can act on explicit outcomes such as `block`, `warn`, or `allow`

### First execution scope

Start with already-known semantic problem families:

- identifier-grain ambiguity
- time-anchor ambiguity
- unit inconsistency
- derived-variable approximation risk

## Workstream 6: Reproducible evidence chain and validation gate

### Goal

Turn strong records into strong reproducibility.

### Required deliverables

- one lineage/reproducibility manifest schema
- one hard link model for:
  - `variable_spec`
  - approved `mapping_spec`
  - approved `build_spec`
  - `execution_code`
  - `input_dataset_signature`
  - `output_dataset`
  - `validation_report`
  - `review_record`
- one rerun-verification procedure
- one approval gate stating what must pass before a variable is called `reviewed_approved`

### Review standard

This workstream is only complete when:

- a frozen approved variable can be rerun and compared against an expected signature
- acceptable tolerance rules are explicit for nondeterministic or environment-sensitive cases
- the repository can show which code and which spec produced which approved asset
- every link in the evidence chain has a stable identity, version, or signature strong enough to detect silent drift
- validation failure blocks formal output acceptance or promotion

### First execution scope

Pilot on a very small approved set first.

Do not try to backfill every historical variable before the schema and gate design stabilizes.

## Suggested phase boundaries

### Phase A: Identity and representation foundation

Deliver:

- Workstream 1
- Workstream 2

Why first:

- later executable rules and validation gates will drift without stable identity and representation schemas

### Phase B: Executable construction layer

Deliver:

- Workstream 3
- Workstream 4

Why second:

- this is the transition from "understandable" to "rebuildable"

### Phase C: Governance and risk automation

Deliver:

- Workstream 5
- the first blocking publication rules

Why third:

- publication safety should run on structured metadata, not only prose review

### Phase D: Reproducibility gate

Deliver:

- Workstream 6
- the first rerun-verification loop

Why last:

- reproducibility gates are strongest after identity, representation, build, mapping, and risk layers are formalized

### Phase E: Execution-layer closure

Deliver:

- the first `run(variable_id, database_id, variable_version)` path
- one end-to-end standard-variable MVP

Why last:

- the execution layer should sit on top of stabilized specs rather than improvising around missing structure

## Minimal viable standard-system closure

To avoid overbuilding too early, the first true standard-system milestone should be one fully closed variable rather than many partial ones.

Minimum closure means one variable, one database, and one non-bypassable execution path.

The smallest acceptable MVP should include:

1. `variable_spec.json`
2. `mapping_spec_<database>.json`
3. `execution.py`
4. `validation_report.json`
5. `manifest.json`

For the first observation-style MVP such as `std_heart_rate`, `variable_spec.json` must explicitly state whether the variable accepts only raw measured values or also allows calculated, derived, or aggregated values.

For database mappings such as MIMIC, `mapping_spec_<database>.json` must explicitly lock the local source codes that count as that variable in that database.

The operational rule is:

- that variable should be generated only through the standard execution path, not by side SQL or ad hoc rebuilds outside the governed route
- validation failure should stop the result from being treated as a formal output

The first MVP validator should at minimum check:

- type validity
- canonical-unit validity
- numeric range validity
- duplicate-key behavior
- missing timestamp behavior

Once one variable reaches that level, the project has entered the standard-system phase in a real rather than descriptive sense.

## What should not be broken while upgrading

During this transition, keep these current strengths intact:

- existing reviewed-approved local assets
- existing public cards
- current GitHub-safe/public vs local-only boundary
- current database-family and version onboarding clarity
- current audit trail and grouped-review culture

The goal is not to throw away the current framework.

The goal is to lift it into a more formal standard system without losing the evidence discipline already built.

## Interpretation rule

This roadmap is not itself the final machine contract.

It is the formal transition plan from:

- a strong human-readable method repository

to:

- a stronger machine-readable, executable, validated standard system
