# SICdb Family Onboarding

SICdb is governed as a standalone ICU database family.

Current database IDs:

- `SICdb-1.0.8`

## Family Rules

- Treat each SICdb release as a versioned database ID.
- Do not inherit ID, time, or dictionary assumptions across versions without a fresh opening review.
- Keep the raw CSV delivery local; the public repository only carries skeletons, contracts, and documentation.
- Standard-variable work should start after Layer 2 confirms the case/stay identity, patient identity, offset-time semantics, and reference dictionary joins.

## Opening Risks

- `CaseID` appears to be the case/stay anchor but needs Layer 2 validation.
- `PatientID` appears in multiple tables and needs patient-level linkage review.
- Time fields appear to be offsets rather than wall-clock datetimes.
- `d_references.csv` is likely central to decoding coded values and item names.
- `data_float_h.csv` is large enough that parquet conversion or partitioning should precede repeated variable extraction.

## Current Status

`SICdb-1.0.8` has a local Layer 1 raw-original copy, Layer 2 opening outputs, Stage C source-access indexes, Stage C.1 problem adjudication, Stage C.2 semantic guardrails, and a Layer 4 opening registry built pending owner review. No reviewed-approved Layer 5 variables exist yet.

The active local semantic guardrails restrict downstream use to cases-linked rows unless a future owner review accepts broader source populations.
