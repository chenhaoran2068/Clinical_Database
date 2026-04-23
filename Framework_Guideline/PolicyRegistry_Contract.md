# Policy Registry Contract

## Purpose

This contract defines how database-specific cleaning and filtering decisions are recorded in a machine-readable registry.

The registry exists so production ETL does not depend on runtime model interpretation.

The intended three-layer pattern is:

1. Human-reviewed contract text
2. Machine-readable policy registry
3. Deterministic builder code that reads the registry

## Why JSON

The default published registry format is JSON.

Reasons:

- readable by Python standard library without extra dependencies
- stable for version control
- easy to validate deterministically
- easy for builders to load in new environments

YAML may still be used for drafting, but published production registries should be JSON unless there is a strong reason not to.

## Placement

Recommended local registry placement:

- `Methods/Clinical_Database/local_work/Layer 4/<database>/PolicyRegistry_<database>_<scope>.json`

Recommended public method assets:

- `Framework_Guideline/PolicyRegistry_Contract.md`
- `scripts/layer4/validate_policy_registry.py`

## Execution Rule

Published ETL builders should not ask a model to interpret contracts at runtime.

Instead, builders should:

1. load the approved JSON registry
2. validate it
3. apply explicit rule blocks deterministically
4. emit classification fields and default-routing decisions

## Required Top-Level Keys

Every published registry should contain:

- `registry_metadata`
- `shared_defaults`
- `policies`

## Required `registry_metadata` Keys

- `registry_name`
- `registry_version`
- `database_name`
- `layer_scope`
- `registry_status`
- `contract_name`
- `contract_version`
- `execution_mode`
- `runtime_model_interpretation_allowed`
- `created_at`
- `source_review_artifacts`

## Required `shared_defaults` Keys

- `default_grain`
- `default_anchor_asset`
- `default_relative_time_formula`
- `default_boundary_truth_fields`
- `disallowed_default_boundary_fields`

Recommended shared fields:

- `default_observation_time_priority`
- `dischargedat_interpretation`
- `measuredat_interpretation`
- `notes`

## Required Per-Policy Keys

Each policy object in `policies` should contain:

- `policy_id`
- `policy_family`
- `policy_version`
- `status`
- `applies_to_assets`
- `intent`
- `trigger_conditions`
- `classification_outputs`
- `default_actions`
- `rule_blocks`
- `notes`

Recommended optional fields:

- `evidence`
- `clinical_category_itemids`
- `lookback_window_max_hours`
- `future_extension_fields`

## Policy Design Principles

- One policy family should cover one clear semantic problem.
- Policies should emit explicit fields instead of relying on hidden builder assumptions.
- Rules should prefer `exclude_from_default` over silent coercion when source semantics are uncertain.
- If a row is clinically useful but unsafe for default use, route it to a child or context path rather than deleting it.

## Recommended Status Values

- `draft`
- `built_pending_user_review`
- `reviewed_approved`
- `deprecated`

## Amsterdam Opening Example Families

Opening Amsterdam registries already need policy families like:

- later-admission negative-time stratification
- retrospective post-discharge scoring and administrative routing
- measuredat-first retrospective interpretation
- dischargedat is not death-time interpretation

## Validation

Published registries should be checked with:

```text
python scripts/layer4/validate_policy_registry.py --registry <path-to-json>
```

Validation is structural.
Clinical approval still comes from human grouped review.
