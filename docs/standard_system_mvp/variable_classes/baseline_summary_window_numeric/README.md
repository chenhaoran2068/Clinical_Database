# Baseline Summary Window Numeric Skeleton

This is the second reusable standard-system MVP skeleton.

It is still intentionally narrow.

It applies to variables that are:

- numeric at the retained output layer
- one row per anchor-qualified target entity
- semantically baseline, first-day, window-summary, or duration outputs
- dependent on explicit anchor/window/aggregation rules

## Current summary subclasses

Current intended summary subclasses inside this class are:

- `baseline_snapshot`
- `window_summary`
- `duration_summary`

That subclass lock is important because a duration summary should not pretend to be the same thing as a baseline snapshot.

## What this skeleton contains

- `template_variable_spec.json`
- `template_mapping_spec.json`
- `template_execution.py`

The execution entrypoint template is now available because the first class-2 governed MVP runner surface has been frozen through `std_icu_los_days` and then reused for baseline and window-summary examples.

## Current contract

Use this skeleton together with:

- `Framework_Guideline/StandardVariableClass_BaselineSummaryWindowNumeric_Contract.md`
- `Framework_Guideline/StandardSystem_RuntimeEvidence_Contract.md`

## Good early fits

- `std_icu_los_days`
- `std_hospital_los_days`
- `std_weight_admission_baseline`
- `std_weight_icu_baseline`
- `std_bmi_admission_baseline`
- `std_bmi_icu_baseline`
- `std_weight_icu_baseline_grouped_proxy`
- `std_first_day_urine_output_summary`

Use caution with:

- `std_sofa_first_day`

It looks like a first-day numeric summary, but its score-composite semantics may ultimately need class-8 governance rather than class-2 governance.

## Not this class

- `std_heart_rate`
- `std_glucose`
- `std_spo2`
- `std_vasopressor_support_active`
- `std_rrt_modality_episode`
- `std_microbiology_organism_isolate`

## How to instantiate a new variable

1. Copy these two template files into `docs/standard_system_mvp/<variable_id>/`.
2. Replace placeholders in `template_variable_spec.json` and rename it to `variable_spec.json`.
3. Replace placeholders in `template_mapping_spec.json` and rename it to `mapping_spec_<database_slug>.json`.
4. Copy `template_execution.py` to `execution.py`.
5. Lock the summary subclass, anchor family, window rules, selection rule, aggregation rule, and no-source-row action before using the class runner.

## Short interpretation rule

This skeleton exists so that the next phase can define class-2 variables without smearing together:

- raw events
- baselines
- first-day summaries
- duration summaries

The opening class-2 execution pattern now exists through `std_icu_los_days`.

The first MIMIC hospital-admission duration-summary expansion now exists through:

- `std_hospital_los_days`

This variable proves that Class 2 can keep ICU-stay duration and hospital-admission duration as separate same-class but different-identity variables.

The first more classical MIMIC baseline-snapshot expansion now exists through:

- `std_weight_admission_baseline`
- `std_weight_icu_baseline`

The first MIMIC derived baseline-snapshot BMI pair now exists through:

- `std_bmi_admission_baseline`
- `std_bmi_icu_baseline`

These variables prove that Class 2 can include derived baseline snapshots when upstream dependencies, formula, missingness behavior, outlier-flag behavior, governed execution, and rerun evidence are locked explicitly.

The first Amsterdam grouped/proxy ICU-baseline weight split-variable now exists through:

- `std_weight_icu_baseline_grouped_proxy`

This variable is class-2-compatible, but it is intentionally not same-name equivalent to exact continuous admission-baseline weight variables.

The first MIMIC first-day window-summary example now exists through:

- `std_first_day_urine_output_summary`

This variable proves the `window_summary` subclass under official-style NULL behavior and official MIMIC first-day urine-output compatibility.

It is still not a claim that every future class-2 variable is already automatically covered without further review.
