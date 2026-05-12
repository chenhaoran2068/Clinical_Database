# SICdb-1.0.8 Onboarding

## Database Identity

- `database_id`: `SICdb-1.0.8`
- family: `SICdb`
- role: `core_database`
- current local stage: Layer 2 opening, Stage C cleaning, Stage C.1 adjudication, Stage C.2 semantic guardrails, and Layer 4 opening registry build complete locally; no reviewed-approved variables yet

## Local Layer 1 Layout

Restricted raw files belong under:

- `Methods/Clinical_Database/local_work/Layer 1/SICdb-1.0.8/raw_original`

The public skeleton is:

- `Data/Layer 1/SICdb-1.0.8`

Expected Layer 1 buckets:

- `raw_original`
- `raw_unpacked`
- `source_supplied_derived`
- `local_converted_parquet`
- `docs_manifest`

## Current Source Delivery

The current local intake used the SICdb 1.0.8 CSV delivery.

Observed source files:

- `cases.csv`
- `d_references.csv`
- `data_float_h.csv`
- `data_range.csv`
- `data_ref.csv`
- `laboratory.csv`
- `medication.csv`
- `unitlog.csv`

## Opening Rules

- Do not publish raw CSVs or local converted parquet.
- Treat `CaseID`, `PatientID`, offsets, and dictionary fields under the active local Stage C.2 semantic guardrails.
- Do not map variables directly from raw field names without checking `d_references.csv`.
- Convert large event streams to local parquet before repeated extraction.

## Layer 2 Status

SICdb Layer 2 opening, Stage C cleaning, Stage C.1 problem adjudication, Stage C.2 semantic guardrail policy, and Layer 4 opening registry build have been completed locally. Public materials remain data-free; raw CSV files and local parquet/index assets stay outside the public repository.

Layer 4 local status:

- `PolicyRegistry_SICdb-1.0.8_opening.json`: built pending owner review
- `Layer4_SourceRegistry_SICdb-1.0.8.xlsx`: built locally

Current guardrails:

- use `cases.CaseID` as the trusted case anchor unless a future owner review accepts broader source populations
- restrict `data_ref` and `unitlog` variables to rows linkable to `cases.CaseID`
- keep `unitlog.LogState` as a raw source code surface unless a variable-specific policy defines a recode
- do not use offset-based first-day windows until the table-specific unit/anchor policy is written

Useful later checks:

1. Rerun raw CSV conversion into `local_converted_parquet` if the source delivery changes.
2. Rerun the Layer 2 opening inventory if row counts, key uniqueness, or join checks need confirmation.
3. Review the Stage C.2 semantic guardrail policy before selecting first candidate variables.
4. Select a small first candidate batch only after the relevant guardrail is satisfied.
