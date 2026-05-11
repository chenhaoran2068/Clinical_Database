# Event-Level Numeric Primary Source Skeleton

This is the first reusable standard-system MVP skeleton.

It is intentionally narrow.

It applies to variables that are:

- event-level
- numeric
- time-stamped
- drawn from one clear primary source family per database
- normalizable into a canonical unit/range/cleaning rule

## What this skeleton contains

- `template_variable_spec.json`
- `template_mapping_spec.json`
- `template_execution.py`

These files are not a claim that every future variable is already covered.

They are the first reusable pattern extracted from the governed `std_heart_rate` MVP.

## Current contract

Use this skeleton together with:

- `Framework_Guideline/StandardVariableClass_EventLevelNumericPrimarySource_Contract.md`
- `Framework_Guideline/StandardSystem_RuntimeEvidence_Contract.md`

## Current included and excluded examples

Good early fits:

- `std_heart_rate`
- `std_respiratory_rate`
- `std_temp`
- `std_sbp`
- `std_dbp`
- `std_map`
- `std_spo2`
- `std_glucose`
- `std_sodium`
- `std_potassium`

Not this class:

- `std_weight_admission_baseline`
- `std_icu_mortality`
- `std_vasopressor_support_active`
- `std_rrt_modality_episode`
- `std_bacteria_urine_sediment_result`
- `std_sofa2_first_day`
- `std_microbiology_organism_isolate`

## How to instantiate a new variable

1. Copy these three template files into `docs/standard_system_mvp/<variable_id>/`.
2. Replace placeholders in `template_variable_spec.json` and rename it to `variable_spec.json`.
3. Replace placeholders in `template_mapping_spec.json` and rename it to `mapping_spec_<database_slug>.json`.
4. Copy `template_execution.py` to `execution.py`.
5. Point `current_reference_implementation` and local evidence paths to the approved local variable assets.
6. Run `python scripts/public_workflow.py run-standard-mvp --variable-id <variable_id> --database-id <database_id> --validate-only`.
7. After the first governed real run, validate runtime evidence and then record rerun evidence.

## Short interpretation rule

This skeleton is for industrializing the first large batch of simple numeric observation variables.

It is not yet the final shape for summaries, flags, episodes, scores, or microbiology families.
