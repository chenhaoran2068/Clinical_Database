# Minimal Variable Validation Workflow

## Goal

Show the smallest reasonable review loop for one standardized variable after a local asset has been built.

This tutorial stays public-safe by describing the workflow shape rather than publishing patient-level outputs.

## Step 1: lock the public definition

Start with the public card for the variable you care about.

Examples:

- [`std_heart_rate`](../std_variable_cards/std_heart_rate.md)
- [`std_map`](../std_variable_cards/std_map.md)
- [`std_glucose`](../std_variable_cards/std_glucose.md)

This locks:

- standard meaning
- unit
- grain
- value type

## Step 2: locate the matching local asset

The local retained asset should live under a database-specific Layer 5 path such as:

- `Methods/Clinical_Database/local_work/Layer 5/MIMIC-IV-3.1/std_heart_rate/`
- `Methods/Clinical_Database/local_work/Layer 5/AmsterdamUMCdb-1.0.2/std_heart_rate/`

Do not validate an unnamed local file in isolation.
Always validate it against a known `std_variable_id`.

## Step 3: generate a small local preview

Use the public-safe script interface as a reminder of the intended workflow, then run the local preview script against your local asset.

Typical command shape:

```powershell
python scripts/layer5/export_layer3_filtered_preview.py ...
```

The exact arguments stay local because they point to local retained assets.

## Step 4: summarize the numeric distribution

For numeric variables, the next local step is usually:

```powershell
python scripts/layer5/summarize_layer3_numeric_asset.py ...
```

This is where you look for:

- impossible values
- suspicious spikes
- missingness patterns
- unit-scale mistakes

## Step 5: compare against expectations

Expectation sources can include:

- the public variable card
- the grouped review package
- the database-specific onboarding caveats
- official database papers or epidemiology references in the local audit trail

## Step 6: decide the action

Typical outcomes are:

- keep the current retention rule
- tighten the cleaning rule
- add a caveat
- defer the asset until a contract decision is made

## Core idea

A good variable validation loop is not only "look at the distribution."

It is:

1. standard locked
2. local asset identified
3. preview generated
4. summary reviewed
5. decision recorded
