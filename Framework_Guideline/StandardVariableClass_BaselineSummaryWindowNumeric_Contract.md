# Standard Variable Class Contract: Baseline Summary Window Numeric

This contract defines the second reusable standard-variable class for the standard-system MVP.

## Applicability

This class applies when a variable is all of the following:

- numeric at the retained output layer
- one row per anchor-qualified target entity rather than one row per raw event
- semantically defined by baseline, first-day, window-summary, or duration logic
- dependent on an explicit anchor family, window rule, or interval boundary rule
- reproducible only when selection, aggregation, and no-source-row behavior are locked

Typical examples:

- `std_icu_los_days`
- `std_hospital_los_days`
- `std_weight_admission_baseline`
- `std_weight_icu_baseline_grouped_proxy`
- `std_first_day_urine_output_summary`

This class may also later host some first-day or follow-up numeric summaries, but only when the main difficulty is the summary/window contract itself.

## Non-applicability

Do not force this class onto variables that are primarily:

- raw event-level numeric observations
- binary support/state flags
- treatment/device event streams
- episode or interval tables whose primary output is start-stop structure rather than one retained numeric summary
- diagnosis, demographic, administrative, or identifier-linkage outputs
- multi-component scores or phenotypes whose main semantic burden is the composite score logic itself rather than the summary/window shape
- microbiology multi-entity outputs

## Immutable semantic rule

Within this class, the variable's immutable semantic core must still stay fixed.

For class 2, that immutable core includes not only the concept but also the summary semantics:

- `variable_id`
- semantic intent
- target entity grain
- summary subclass
- anchor family
- window label
- window start rule
- window end rule
- qualifying-row rule
- selection rule
- aggregation rule
- no-source-row action

If one of those meaning-defining fields changes, that is usually a new variable, not a version bump.

Examples:

- admission baseline weight vs discharge weight = different variables
- first-day urine-output total vs first-48-hour urine-output total = different variables
- ICU LOS vs hospital LOS = different variables
- first-day mean heart rate vs first-day maximum heart rate = different variables

## Recommended class-2 summary subclasses

The class should explicitly distinguish at least these summary subclasses:

- `baseline_snapshot`
- `window_summary`
- `duration_summary`

This avoids forcing all summary variables to pretend they are the same shape.

## Minimum variable-spec rule

The `variable_spec.json` for this class should lock at minimum:

- `variable_id`
- `variable_version`
- semantic intent and semantic definition
- `summary_subclass`
- `target_entity_grain`
- `anchor_family`
- `window_label`
- `window_start_rule`
- `window_end_rule`
- `qualifying_row_rule`
- `selection_rule`
- `aggregation_rule`
- `tie_break_rule`
- `no_source_row_action`
- `partial_window_action`
- canonical unit and value type
- identifier roles
- output-time-context requirements
- hard-valid and plausible ranges when meaningful

## Minimum mapping-spec rule

The `mapping_spec_<database>.json` for this class should lock at minimum:

- one concrete `database_id`
- one explicit `source_locator_mode`
- explicit source package/table or approved upstream source asset references
- local prepared input asset path or paths
- source grain and target grain
- anchor-field translation
- window translation
- selection translation
- aggregation translation
- no-source-row translation
- identifier normalization notes
- validation expectations

Unlike class 1, class 2 mappings may or may not be driven by raw source codes.

That difference must be explicit rather than implied.

## Build-rule rule

This class should not rely on prose such as:

- "use the baseline value"
- "use the first-day summary"
- "use the official window"

Instead it should make the following executable semantics explicit:

- how the anchor is defined
- how the window starts
- how the window ends
- which rows qualify
- how multiple qualifying rows are reduced
- how ties are broken
- what happens when no qualifying row exists
- what happens when the source window is partial

## Validation rule

This class should validate at minimum:

- one retained row per target entity/window key
- required anchor and context fields are present
- window bounds are internally coherent
- unit/type checks pass
- range checks pass when meaningful
- no-source-row behavior is explicitly checked rather than silently guessed
- duplicate retained rows fail

## Execution rule

Formal outputs for this class should eventually be produced through one governed execution entrypoint per variable directory.

That entrypoint should:

- read the public `variable_spec.json`
- read the public `mapping_spec_<database>.json`
- validate cross-file agreement before execution
- delegate to the current approved local implementation until a more spec-native runner replaces it

Important current interpretation:

- Phase 1 may define the class and templates before the first class-specific runner exists
- no variable should claim full class-2 execute-mode closure until that governed runner is actually frozen and used

## Runtime-evidence rule

This class inherits the public runtime-evidence contract from:

- `Framework_Guideline/StandardSystem_RuntimeEvidence_Contract.md`

For class 2, the runtime evidence should additionally make the summary/window semantics inspectable through locked specs and build-summary fields.

Preferred build-summary fields include:

- target row count
- null row count when relevant
- anchor family
- window label
- aggregation rule identifier

## Current public skeleton

The current reusable skeleton for this class lives under:

- `docs/standard_system_mvp/variable_classes/baseline_summary_window_numeric/`

## Current phase interpretation

This class is now formally defined, its first governed dual-database MVP has been executed through `std_icu_los_days`, its first governed MIMIC hospital-duration expansion has been executed through `std_hospital_los_days`, its first governed MIMIC exact baseline-snapshot expansion has been executed through `std_weight_admission_baseline`, and its first Amsterdam grouped/proxy ICU-baseline weight split-variable has been executed through `std_weight_icu_baseline_grouped_proxy`.

So the current status is:

- class contract defined
- public templates defined
- first candidate chosen
- first governed dual-database MVP closed through `std_icu_los_days`
- first governed MIMIC-only hospital-duration example closed through `std_hospital_los_days`
- first governed MIMIC-only baseline-snapshot example closed through `std_weight_admission_baseline`
- first governed Amsterdam-only grouped/proxy baseline-weight split-variable closed through `std_weight_icu_baseline_grouped_proxy`
- broader class-2 batch industrialization not yet claimed
