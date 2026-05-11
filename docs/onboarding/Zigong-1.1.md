# Zigong-1.1 Onboarding

## Database Identity

- `database_id`: `Zigong-1.1`
- family: `Zigong`
- role: `core_database`
- declared version: `1.1`
- current local stage: Layer 2 opening, Stage C cleaning, Stage C.1 adjudication, Stage C.2 semantic guardrails, and Layer 4 opening registry build complete locally; no reviewed-approved variables yet

## Local Layer 1 Layout

Restricted raw files belong under:

- `Methods/Clinical_Database/local_work/Layer 1/Zigong-1.1/raw_original`

The public skeleton is:

- `Data/Layer 1/Zigong-1.1`

Expected Layer 1 buckets:

- `raw_original`
- `raw_unpacked`
- `source_supplied_derived`
- `local_converted_parquet`
- `docs_manifest`

## Current Source Delivery

The current local intake used the official Zigong 1.1 CSV delivery placed in `Data_Raw/Zigong-1.1`.

Observed source files:

- `datDictionary.csv`
- `dtBaseline.csv`
- `dtDrugs.csv`
- `dtICD.csv`
- `dtLab.csv`
- `dtNursingChart.csv`
- `dtOutCome.csv`
- `dtTransfer.csv`
- `LICENSE.txt`
- `SHA256SUMS.txt`

`LICENSE.txt` and `SHA256SUMS.txt` were added after the first intake pass and are now retained in local Layer 1 `raw_original`.

The checksum manifest references the upstream `DataTables.zip` package and `LICENSE.txt`; it does not provide per-CSV checksums for the unzipped CSV files staged locally.

The retained `LICENSE.txt` matches the SHA256 value listed in `SHA256SUMS.txt`. `DataTables.zip` is not present in the Layer 1 raw-original directory, so that package-level checksum cannot be verified against the staged files.

## Opening Rules

- Do not publish raw CSV files or local converted parquet.
- Treat `PATIENT_ID`, `INP_NO`, source time fields, outcome fields, and the leading unnamed row-index column under the active local Stage C.2 semantic guardrails.
- Decode `datDictionary.csv` before mapping any raw column to a standard variable.
- Convert large event tables to local parquet before repeated extraction.
- Normalize `dtNursingChart.csv` carefully; it is a wide source table containing multiple clinical domains.

## Layer 2 Status

Zigong Layer 2 opening, Stage C cleaning, Stage C.1 problem adjudication, Stage C.2 semantic guardrail policy, and Layer 4 opening registry build have been completed locally. Public materials remain data-free; raw CSV files and local parquet/index assets stay outside the public repository.

Layer 4 local status:

- `PolicyRegistry_Zigong-1.1_opening.json`: built pending owner review
- `Layer4_SourceRegistry_Zigong-1.1.xlsx`: built locally

Current guardrails:

- use `dtBaseline.INP_NO` as the current baseline encounter/cohort anchor
- do not use `dtNursingChart` as a complete ICU-stay denominator
- use matched nursing rows only as event evidence with explicit linkage flags
- exclude unmatched nursing `INP_NO` rows from standard variables until owner/source clarification
- keep source timing fields raw until table-specific unit/anchor bridge policy is approved

Useful rerun checks:

1. Rerun raw CSV conversion into `local_converted_parquet` if the source delivery changes.
2. Rerun the Layer 2 opening inventory if row counts, key uniqueness, or join checks need confirmation.
3. Decode `datDictionary.csv` against every source table when a variable needs dictionary-backed interpretation.
4. Review the Stage C.2 semantic guardrail policy before selecting first candidate variables.
5. Select first candidate variables only after the relevant guardrail is satisfied.
