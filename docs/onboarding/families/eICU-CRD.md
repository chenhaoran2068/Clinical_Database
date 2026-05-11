# eICU-CRD Family Onboarding

eICU-CRD is governed as a standalone ICU database family.

Current database IDs:

- `eICU-CRD-2.0`

## Family Rules

- Treat each eICU-CRD release as a versioned database ID.
- Keep restricted source CSV/TXT files local; the public repository only carries skeletons, contracts, and documentation.
- Do not inherit identity, offset-time, APACHE, or site/hospital assumptions across releases without a fresh opening review.
- Standard-variable work should start after Layer 2 confirms ICU-stay identity, health-system stay identity, patient identity, hospital/site fields, offset-time semantics, mortality fields, and high-volume event extraction strategy.

## Opening Risks

- `patientunitstayid` appears to be the primary ICU-stay anchor, but uniqueness and joins must be checked table by table.
- `patienthealthsystemstayid` and `uniquepid` require careful linkage review before any patient-level longitudinal variable is built.
- eICU uses offset-style time fields; first-day and first-24h windows must not be copied from timestamp-based databases without review.
- `hospitalid`, `wardid`, and hospital-level fields may support site context but must be handled as deidentified, site-safe metadata.
- `apacheApsVar.csv`, `apachePredVar.csv`, and `apachePatientResult.csv` are source-supplied APACHE-related surfaces and should not be conflated with reconstructed standard scores.
- `nurseCharting.csv`, `vitalPeriodic.csv`, `lab.csv`, `nurseAssessment.csv`, and `intakeOutput.csv` are large enough that parquet conversion or partitioning should precede repeated extraction.

## Current Status

`eICU-CRD-2.0` has a local Layer 1 raw-original copy, Layer 2 opening outputs, Stage C source-access indexes, Stage C.1 problem adjudication, Stage C.2 semantic guardrails, and a Layer 4 opening registry built pending owner review. No reviewed-approved Layer 5 variables exist yet.

The active local semantic guardrails lock `patientunitstayid` as the ICU-unit stay key and require APACHE sentinel/negative-value handling before any standardized score work.
