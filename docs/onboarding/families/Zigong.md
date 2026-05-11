# Zigong Family Onboarding

Zigong is governed as a standalone ICU database family.

Current database IDs:

- `Zigong-1.1`

## Family Rules

- Treat each Zigong release as a versioned database ID.
- Keep restricted source CSV files local; the public repository only carries skeletons, contracts, and documentation.
- Do not inherit identity, offset-time, outcome, dictionary, or wide-table assumptions across releases without a fresh opening review.
- Standard-variable work should start after Layer 2 confirms patient identity, inpatient encounter identity, offset-time semantics, outcome definitions, and data dictionary usage.

## Opening Risks

- `PATIENT_ID` appears to be the patient-level anchor and must be checked across baseline, drugs, ICD, outcomes, and transfers.
- `INP_NO` appears to be an inpatient encounter or hospital-admission anchor and must be checked across baseline, ICD, labs, nursing charting, and transfers.
- `datDictionary.csv` is central to interpreting the source tables and must be decoded before variable mapping.
- Some fields are documented as hour offsets from hospital admission, but other time fields require review before first-day or first-24h derivations.
- `dtNursingChart.csv` is a wide charting table and should be normalized carefully before repeated variable extraction.
- The leading unnamed column in the CSV files appears to be an exported row index, not a clinical identifier.

## Current Status

`Zigong-1.1` has a local Layer 1 raw-original copy, Layer 2 opening outputs, Stage C source-access indexes, Stage C.1 problem adjudication, Stage C.2 semantic guardrails, and a Layer 4 opening registry built pending owner review. No reviewed-approved Layer 5 variables exist yet.

The active local semantic guardrails prevent `dtNursingChart` from acting as a complete ICU-stay denominator until the unmatched `INP_NO` population is clarified.
