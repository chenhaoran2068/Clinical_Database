# `std_heart_rate` Cross-Database Walkthrough

## Goal

Show the public-safe way to compare one already standardized variable across two databases without collapsing back into raw-table thinking.

Current example:

- `MIMIC-IV-3.1`
- `AmsterdamUMCdb-1.0.2`
- variable: [`std_heart_rate`](../std_variable_cards/std_heart_rate.md)

## What is public versus local here

Public-safe inputs:

- [`docs/std_variable_cards/std_heart_rate.md`](../std_variable_cards/std_heart_rate.md)
- [`docs/DATABASE_LINEAGE_AND_VERSION_MATRIX.md`](../DATABASE_LINEAGE_AND_VERSION_MATRIX.md)
- [`Framework_Guideline/CrossDatabase_Variable_Harmonization_Contract.md`](../../Framework_Guideline/CrossDatabase_Variable_Harmonization_Contract.md)

Local-only evidence:

- `Methods/Clinical_Database/local_work/Layer 5/MIMIC-IV-3.1/std_heart_rate/`
- `Methods/Clinical_Database/local_work/Layer 5/AmsterdamUMCdb-1.0.2/std_heart_rate/`
- database-specific grouped reviews
- local previews, numeric summaries, and query checks

## Step 1: confirm the semantic target

Read the public card first.

That establishes the cross-database intent:

- same `std_variable_id`
- same standard meaning
- same standard unit
- same expected grain

Do not start by comparing raw source field names between databases.
Start by confirming that the repositories already claim they are the same standardized variable.

## Step 2: confirm that the database relationship is what you think it is

Check the current database matrix:

- [`MIMIC-IV-3.1`](../onboarding/MIMIC-IV-3.1.md)
- [`AmsterdamUMCdb-1.0.2`](../onboarding/AmsterdamUMCdb-1.0.2.md)

This avoids a common mistake:

- assuming directory proximity implies semantic compatibility

Instead, compatibility must come from:

- the public card
- the harmonization contract
- the reviewed local evidence

## Step 3: inspect the local knowledge packages separately

Public cards answer:

- what the variable is
- how it should be interpreted globally

Local knowledge packages answer:

- how each database produced that variable
- which source tables and columns were used
- which database-specific caveats were approved
- which review evidence supports the retention rule

For `std_heart_rate`, the correct cross-database workflow is:

1. read the public card once
2. read the MIMIC local evidence package
3. read the Amsterdam local evidence package
4. compare conclusions at the standardized layer, not at the raw naming layer

## Step 4: run local numeric checks only after the semantics are fixed

Typical local commands look like:

```powershell
python scripts/layer5/export_layer3_filtered_preview.py ...
python scripts/layer5/summarize_layer3_numeric_asset.py ...
```

These are local-only because they touch patient-level assets.

The public repository should teach the workflow shape, not publish the local patient-level outputs.

## Step 5: make the research-facing comparison

Once both local assets are individually approved, the comparison question becomes:

- are the two retained assets close enough in semantics, unit, and grain to support the intended joint analysis?

That is a standardized-variable question.
It is not a question about whether one database originally used a different raw table name or device feed.

## Recommended habit

Use this order every time:

1. public card
2. matrix and onboarding
3. local knowledge package
4. local distribution review
5. cross-database analytic decision
