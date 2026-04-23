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
```

Interpretation rule:

- `MIMIC-IV-ECHO-1.0` is a sibling module, not a semantic child of `MIMIC-IV-3.1`
- version mapping is decided by the catalog and onboarding docs, not by whichever folder happens to be nearby
- public Layer 1 skeletons show the expected source staging layout, while actual patient-level execution remains in local work

## Current support matrix

| Database ID | Family | Role | Version | Public Layer 1 status | Public scripts | Special semantics contract | Public Layer 5 status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `MIMIC-IV-3.1` | `MIMIC-IV` | core database | `3.1` | skeleton and Layer 1 scripts published | unpack, convert, note fallback, public workflow | [`MIMICIV_SourcePackageAndModuleBoundary_Contract.md`](../Framework_Guideline/MIMICIV_SourcePackageAndModuleBoundary_Contract.md) | broad public-card coverage from reviewed-approved local assets |
| `MIMIC-IV-ECHO-1.0` | `MIMIC-IV` | sibling module | `1.0` | skeleton and Layer 1 scripts published | ECHO unpack, ECHO convert, public workflow | none beyond global contracts | no reviewed-approved retained-variable family published yet |
| `AmsterdamUMCdb-1.0.2` | `AmsterdamUMCdb` | core database | `1.0.2` | skeleton and Layer 1 scripts published | convert, registry validation, public workflow | [`AmsterdamUMCdb_TimeSemantics_Contract.md`](../Framework_Guideline/AmsterdamUMCdb_TimeSemantics_Contract.md) | pilot reviewed-approved assets exist and public cards are already available for shared variables |

## Current interpretation notes

### MIMIC-IV-3.1

- current public Layer 1 covers `core`, `ed`, and `note` staging expectations
- current public Layer 5 coverage is the most mature in this repository
- public variable cards already expose a GitHub-safe summary for reviewed-approved variables
- public interpretation must keep source-package provenance explicit, especially when note staging uses the fallback proxy path rather than an official raw note delivery

### MIMIC-IV-ECHO-1.0

- current public Layer 1 support is ready
- the module already exists as a local-work peer of MIMIC-IV, not a hidden subfolder
- retained-variable standardization has not yet started in the public repository

### AmsterdamUMCdb-1.0.2

- public Layer 1 conversion is available
- public interpretation must honor relative-time semantics and cross-admission overlap warnings
- current Layer 5 state is a pilot-approved subset, not full database completion

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
