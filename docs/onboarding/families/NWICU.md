# NWICU Family Onboarding

NWICU is governed as a standalone ICU database family.

Current database IDs:

- `NWICU-0.1.0`

## Family Rules

- Treat each NWICU release as a versioned database ID.
- Preserve the distinction between the official/source version and any local source folder label.
- Do not inherit ID, time, or dictionary assumptions across versions without a fresh opening review.
- Keep restricted source files local; the public repository only carries skeletons, contracts, and documentation.
- Standard-variable work should start after Layer 2 confirms patient, admission, ICU stay, timestamp, mortality, and dictionary semantics.

## Opening Risks

- `subject_id` appears to be the patient-level anchor and must be checked for uniqueness and reuse semantics.
- `hadm_id` appears to be the hospital-admission anchor and must be checked against admissions, diagnoses, prescriptions, labs, and medication records.
- `stay_id` appears in ICU tables and must be checked as the ICU-stay anchor.
- Timestamp fields resemble MIMIC-style wall-clock fields but still require a deidentification/time-semantics review before first-24h or time-window variables are built.
- `d_items.csv`, `d_labitems.csv`, and `d_icd_diagnoses.csv` should be treated as source dictionaries, not optional labels.
- `SHA256SUMS.txt` documents the original gzipped delivery paths, while the current local files are uncompressed CSV/TXT.

## Current Status

`NWICU-0.1.0` has a local Layer 1 raw-original copy, Layer 2 opening outputs, Stage C source-access indexes, Stage C.1 problem adjudication, Stage C.2 semantic guardrails, and a Layer 4 opening registry built pending owner review. No reviewed-approved Layer 5 variables exist yet.

Public materials remain data-free; restricted raw CSV/TXT files and local parquet/index assets are not published.
