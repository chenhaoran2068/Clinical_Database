# eICU-CRD-2.0 Onboarding

## Database Identity

- `database_id`: `eICU-CRD-2.0`
- family: `eICU-CRD`
- role: `core_database`
- declared version: `2.0`
- current local stage: Layer 2 opening, Stage C cleaning, Stage C.1 adjudication, Stage C.2 semantic guardrails, and Layer 4 opening registry build complete locally; no reviewed-approved variables yet

## Local Layer 1 Layout

Restricted raw files belong under:

- `Methods/Clinical_Database/local_work/Layer 1/eICU-CRD-2.0/raw_original`

The public skeleton is:

- `Data/Layer 1/eICU-CRD-2.0`

Expected Layer 1 buckets:

- `raw_original`
- `raw_unpacked`
- `source_supplied_derived`
- `local_converted_parquet`
- `docs_manifest`

## Current Source Delivery

The current local intake used the official eICU Collaborative Research Database 2.0 delivery placed in `Data_Raw/eICU-CRD-2.0`.

Observed source files include:

- patient and site core: `patient.csv`, `hospital.csv`
- diagnoses/history: `admissionDx.csv`, `diagnosis.csv`, `pastHistory.csv`, `allergy.csv`
- APACHE source-supplied surfaces: `apacheApsVar.csv`, `apachePredVar.csv`, `apachePatientResult.csv`
- medications and treatment: `admissionDrug.csv`, `medication.csv`, `infusionDrug.csv`, `treatment.csv`
- vitals and charting: `vitalPeriodic.csv`, `vitalAperiodic.csv`, `nurseCharting.csv`, `nurseAssessment.csv`, `nurseCare.csv`
- respiratory: `respiratoryCare.csv`, `respiratoryCharting.csv`
- laboratory and microbiology: `lab.csv`, `customLab.csv`, `microLab.csv`
- care plan and notes: `carePlanGeneral.csv`, `carePlanGoal.csv`, `carePlanCareProvider.csv`, `carePlanEOL.csv`, `carePlanInfectiousDisease.csv`, `note.csv`
- source documentation files: `LICENSE.txt`, `SHA256SUMS.txt`

## Opening Rules

- Do not publish raw CSV/TXT files or local converted parquet.
- Treat `patientunitstayid`, `patienthealthsystemstayid`, `uniquepid`, `hospitalid`, `wardid`, offset fields, and mortality/discharge fields under the active local Stage C.2 semantic guardrails.
- Do not treat source-supplied APACHE files as approved standard scores without a dedicated score review.
- Convert large event streams to local parquet before repeated extraction.
- Remember that `SHA256SUMS.txt` references original gzipped delivery filenames, while the current local raw-original files are uncompressed.
- Historical owner eICU workspaces are reference-only; do not copy prior personal processing artifacts into production.

## Layer 2 Status

eICU Layer 2 opening, Stage C cleaning, Stage C.1 problem adjudication, Stage C.2 semantic guardrail policy, and Layer 4 opening registry build have been completed locally. Public materials remain data-free; raw CSV/TXT files and local parquet/index assets stay outside the public repository.

Layer 4 local status:

- `PolicyRegistry_eICU-CRD-2.0_opening.json`: built pending owner review
- `Layer4_SourceRegistry_eICU-CRD-2.0.xlsx`: built locally

Current guardrails:

- use `patientunitstayid` as the ICU-unit stay key
- treat `patienthealthsystemstayid` as hospital-system grouping and `uniquepid` as patient identity
- treat clinical offsets as source minute offsets and lock the anchor before first-24h windows
- convert APACHE `-1` and invalid negative values to missing/flagged values before numeric use
- do not treat source APACHE tables as approved standardized scores without variable-specific review

Useful rerun checks:

1. Rerun raw CSV conversion into `local_converted_parquet` if the source delivery changes.
2. Rerun the Layer 2 opening inventory if row counts, key uniqueness, or join checks need confirmation.
3. Review the Stage C.2 semantic guardrail policy before selecting first candidate variables.
4. Select first candidate variables only after the relevant guardrail is satisfied.
