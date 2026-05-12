# Database Lineage And Version Matrix

## Why this file exists

This repository is cross-database.

That means directory names, version labels, and sibling-module relationships must be explicit.

The machine-readable source of truth is [`docs/database_catalog.json`](database_catalog.json).
This Markdown file is the human-readable overview.

Family-level onboarding lives under [`docs/onboarding/families`](onboarding/families/README.md).

## Current family map

```text
MIMIC-IV family
|- MIMIC-IV-3.1
`- MIMIC-IV-ECHO-1.0

AmsterdamUMCdb family
`- AmsterdamUMCdb-1.0.2

SICdb family
`- SICdb-1.0.8

NWICU family
`- NWICU-0.1.0

eICU-CRD family
`- eICU-CRD-2.0

Zigong family
`- Zigong-1.1
```

Interpretation rule:

- `MIMIC-IV-ECHO-1.0` is a sibling module, not a semantic child of `MIMIC-IV-3.1`
- version mapping is decided by the catalog and onboarding docs, not by whichever folder happens to be nearby
- public Layer 1 skeletons show the expected source staging layout, while actual patient-level execution remains in local work

## Current support matrix

| Database ID | Family | Role | Version | Public Layer 1 status | Public scripts | Special semantics contract | Public Layer 5 status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `MIMIC-IV-3.1` | `MIMIC-IV` | core database | `3.1` | skeleton and Layer 1 scripts published | unpack, convert, note fallback, public workflow | [`MIMICIV_SourcePackageAndModuleBoundary_Contract.md`](../Framework_Guideline/MIMICIV_SourcePackageAndModuleBoundary_Contract.md); local Layer 4 opening registry built pending owner review | broad public-card coverage from reviewed-approved local assets |
| `MIMIC-IV-ECHO-1.0` | `MIMIC-IV` | sibling module | `1.0` | skeleton and Layer 1 scripts published | ECHO unpack, ECHO convert, public workflow | local Layer 4 opening registry built pending owner review; public ECHO-specific policy not yet published | no reviewed-approved retained-variable family published yet |
| `AmsterdamUMCdb-1.0.2` | `AmsterdamUMCdb` | core database | `1.0.2` | skeleton and Layer 1 scripts published | convert, registry validation, public workflow | [`AmsterdamUMCdb_TimeSemantics_Contract.md`](../Framework_Guideline/AmsterdamUMCdb_TimeSemantics_Contract.md) | pilot reviewed-approved assets exist and public cards are already available for shared variables |
| `SICdb-1.0.8` | `SICdb` | core database | `1.0.8` | skeleton published; local Layer 2 opening and Stage C.2 complete | public workflow only for now | local Layer 4 opening registry built pending owner review; public opening policy not yet published | no reviewed-approved SICdb retained-variable assets yet |
| `NWICU-0.1.0` | `NWICU` | core database | `0.1.0` | skeleton published; local Layer 2 opening and Stage C.2 complete | public workflow only for now | local Layer 4 opening registry built pending owner review; public opening policy not yet published | no reviewed-approved NWICU retained-variable assets yet |
| `eICU-CRD-2.0` | `eICU-CRD` | core database | `2.0` | skeleton published; local Layer 2 opening and Stage C.2 complete | public workflow only for now | local Layer 4 opening registry built pending owner review; public opening policy not yet published | no reviewed-approved eICU-CRD retained-variable assets yet |
| `Zigong-1.1` | `Zigong` | core database | `1.1` | skeleton published; local Layer 2 opening and Stage C.2 complete | public workflow only for now | local Layer 4 opening registry built pending owner review; public opening policy not yet published | no reviewed-approved Zigong retained-variable assets yet |

## Current interpretation notes

### MIMIC-IV-3.1

- current public Layer 1 covers `core`, `ed`, and `note` staging expectations
- current public Layer 5 coverage is the most mature in this repository
- public variable cards already expose a GitHub-safe summary for reviewed-approved variables
- public interpretation must keep source-package provenance explicit, especially when note staging uses the fallback proxy path rather than an official raw note delivery
- local Layer 4 opening registry was built on 2026-05-09 and remains pending owner review

### MIMIC-IV-ECHO-1.0

- current public Layer 1 support is ready
- the module already exists as a local-work peer of MIMIC-IV, not a hidden subfolder
- retained-variable standardization has not yet started in the public repository
- local Layer 4 opening registry was built on 2026-05-09 and remains pending owner review

### AmsterdamUMCdb-1.0.2

- public Layer 1 conversion is available
- public interpretation must honor relative-time semantics and cross-admission overlap warnings
- current Layer 5 state is a pilot-approved subset, not full database completion

### SICdb-1.0.8

- local Layer 1 raw-original staging has begun from the SICdb 1.0.8 CSV delivery
- public Layer 1 skeleton is intentionally data-free and documents where restricted CSV files belong
- ID and time interpretation are provisional until Layer 2 opening review confirms `CaseID`, `PatientID`, offset fields, and dictionary joins
- no SICdb variable should be treated as reviewed-approved until a database-specific mapping and review packet exists
- local Layer 2 opening, Stage C cleaning, Stage C.1 adjudication, Stage C.2 semantic guardrails, and Layer 4 opening registry build completed on 2026-05-09; public export remains data-free

### NWICU-0.1.0

- local Layer 1 raw-original staging has begun from the NWICU delivery in source folder `NWICU-0.1.0`
- the formal database ID follows the official/source version `0.1.0`
- public Layer 1 skeleton is intentionally data-free and documents where restricted CSV/TXT files belong
- ID and time interpretation are provisional until Layer 2 opening review confirms `subject_id`, `hadm_id`, `stay_id`, timestamp fields, mortality fields, and dictionary joins
- no NWICU variable should be treated as reviewed-approved until a database-specific mapping and review packet exists
- local Layer 2 opening, Stage C cleaning, Stage C.1 adjudication, Stage C.2 semantic guardrails, and Layer 4 opening registry build completed on 2026-05-09; public export remains data-free

### eICU-CRD-2.0

- local Layer 1 raw-original staging has begun from the official eICU Collaborative Research Database 2.0 delivery
- public Layer 1 skeleton is intentionally data-free and documents where restricted CSV/TXT files belong
- ID and time interpretation are provisional until Layer 2 opening review confirms `patientunitstayid`, `patienthealthsystemstayid`, `uniquepid`, `hospitalid`, `wardid`, offset-time fields, mortality fields, and source-supplied APACHE surfaces
- no eICU-CRD variable should be treated as reviewed-approved until a database-specific mapping and review packet exists
- historical owner eICU workspaces are reference-only and should not be copied into the production or public method roots
- local Layer 2 opening, Stage C cleaning, Stage C.1 adjudication, Stage C.2 semantic guardrails, and Layer 4 opening registry build completed on 2026-05-09; public export remains data-free

### Zigong-1.1

- local Layer 1 raw-original staging has begun from the official Zigong 1.1 CSV delivery
- public Layer 1 skeleton is intentionally data-free and documents where restricted CSV files belong
- ID and time interpretation are provisional until Layer 2 opening review confirms `PATIENT_ID`, `INP_NO`, hour-offset fields, outcome fields, and dictionary usage
- no Zigong variable should be treated as reviewed-approved until a database-specific mapping and review packet exists
- `LICENSE.txt` and `SHA256SUMS.txt` are retained in local Layer 1 `raw_original`; the retained license matches its manifest hash, while the upstream `DataTables.zip` package hash cannot be verified from the currently staged unzipped CSV files
- local Layer 2 opening, Stage C cleaning, Stage C.1 adjudication, Stage C.2 semantic guardrails, and Layer 4 opening registry build completed on 2026-05-09; public export remains data-free

## How this matrix should be used

- use it first when deciding whether a new data source should be added as a new family, a new version, or a sibling module
- use the linked onboarding playbook before staging any official delivery into local work
- use the public workflow entrypoints only after confirming the database ID and module relationship here

## Related files

- [`docs/database_catalog.json`](database_catalog.json)
- [`docs/onboarding/README.md`](onboarding/README.md)
- [`docs/onboarding/families/README.md`](onboarding/families/README.md)
- [`docs/GETTING_STARTED.md`](GETTING_STARTED.md)
- [`Framework_Guideline/Database_Critical_Semantics_Contract.md`](../Framework_Guideline/Database_Critical_Semantics_Contract.md)
