# NWICU-0.1.0 Onboarding

## Database Identity

- `database_id`: `NWICU-0.1.0`
- family: `NWICU`
- role: `core_database`
- official/source version: `0.1.0`
- local source holding folder label: `NWICU-0.1.0`
- current local stage: Layer 2 opening, Stage C cleaning, Stage C.1 adjudication, Stage C.2 semantic guardrails, and Layer 4 opening registry build complete locally; no reviewed-approved variables yet

## Local Layer 1 Layout

Restricted raw files belong under:

- `Methods/Clinical_Database/local_work/Layer 1/NWICU-0.1.0/raw_original`

The public skeleton is:

- `Data/Layer 1/NWICU-0.1.0`

Expected Layer 1 buckets:

- `raw_original`
- `raw_unpacked`
- `source_supplied_derived`
- `local_converted_parquet`
- `docs_manifest`

## Current Source Delivery

The current local intake used the NWICU delivery placed in `Data_Raw/NWICU-0.1.0`, with official/source version `0.1.0`.

Observed source files:

- `admissions.csv`
- `chartevents.csv`
- `diagnoses_icd.csv`
- `d_icd_diagnoses.csv`
- `d_items.csv`
- `d_labitems.csv`
- `emar.csv`
- `icustays.csv`
- `labevents.csv`
- `LICENSE.txt`
- `patients.csv`
- `prescriptions.csv`
- `procedureevents.csv`
- `SHA256SUMS.txt`

## Opening Rules

- Do not publish raw CSV/TXT files or local converted parquet.
- Treat `subject_id`, `hadm_id`, `stay_id`, timestamp fields, mortality fields, and dictionaries under the active local Stage C.2 semantic guardrails.
- Do not map variables directly from raw field names without checking `d_items.csv`, `d_labitems.csv`, and `d_icd_diagnoses.csv`.
- Convert large event streams to local parquet before repeated extraction.
- Remember that `SHA256SUMS.txt` references original gzipped delivery paths, while the current local raw-original files are uncompressed.

## Layer 2 Status

NWICU Layer 2 opening, Stage C cleaning, Stage C.1 problem adjudication, Stage C.2 semantic guardrail policy, and Layer 4 opening registry build have been completed locally. Public materials remain data-free; raw CSV/TXT files and local parquet/index assets stay outside the public repository.

Layer 4 local status:

- `PolicyRegistry_NWICU-0.1.0_opening.json`: built pending owner review
- `Layer4_SourceRegistry_NWICU-0.1.0.xlsx`: built locally

Current guardrails:

- use `stay_id` as ICU-stay key, `hadm_id` as hospital-admission key, and `subject_id` as patient key
- use MIMIC-like absolute timestamps only after joining to approved admission/ICU anchors
- keep the `labevents = 1,048,575` source-delivery warning attached to high-stakes lab completeness analyses
- do not claim current CSV-only delivery fully verifies compressed-source completeness

Useful rerun/opening checks:

1. Rerun raw CSV conversion into `local_converted_parquet` if the source delivery changes.
2. Rerun the Layer 2 opening inventory if row counts, key uniqueness, or join checks need confirmation.
3. Review the Stage C.2 semantic guardrail policy before selecting first candidate variables.
4. Select a small first candidate batch only after the relevant guardrail is satisfied.
