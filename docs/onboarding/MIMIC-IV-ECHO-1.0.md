# MIMIC-IV-ECHO-1.0 Onboarding

## Scope

- database ID: `MIMIC-IV-ECHO-1.0`
- family: `MIMIC-IV`
- module role: sibling module
- version: `1.0`

## Expected official source packages

- official MIMIC-IV-ECHO v1.0 delivery files or archives containing:
  - `echo-record-list.csv`
  - `echo-study-list.csv`
  - `structured-measurement.csv.gz`

## Layer 1 target layout

Local target root:

- `Methods/Clinical_Database/local_work/Layer 1/MIMIC-IV-ECHO-1.0/`

This is a sibling local-work path outside the public repository.

Expected buckets:

- `raw_original`
- `raw_unpacked`
- `source_supplied_derived`
- `local_converted_parquet`
- `docs_manifest`

Canonical unpacked root:

- `raw_unpacked/ECHO-1.0/`

`local_converted_parquet` stores locally regenerated parquet copies of the canonical ECHO source tables.

## First public commands

```powershell
python scripts/public_workflow.py status
python scripts/public_workflow.py build-layer1 --database-id MIMIC-IV-ECHO-1.0 --action unpack --layer1-root "..\..\Methods\Clinical_Database\local_work\Layer 1\MIMIC-IV-ECHO-1.0"
python scripts/public_workflow.py build-layer1 --database-id MIMIC-IV-ECHO-1.0 --action convert --layer1-root "..\..\Methods\Clinical_Database\local_work\Layer 1\MIMIC-IV-ECHO-1.0"
```

These relative examples assume the current shell is at the repository root.

## Public-safe artifacts already available

- Layer 1 skeleton in [`Data/Layer 1/MIMIC-IV-ECHO-1.0`](../../Data/Layer%201/MIMIC-IV-ECHO-1.0)
- ECHO Layer 1 unpack and convert scripts
- cross-database contracts that govern future `std_*` alignment
- local Layer 4 opening registry: `PolicyRegistry_MIMIC-IV-ECHO-1.0_opening.json`, built pending owner review

## Local-only execution surface

- staged official raw ECHO files
- local parquet copies
- any future Layer 2 to Layer 5 patient-level outputs
- future grouped reviews, knowledge packages, and evidence bundles

## Critical caveats

- `MIMIC-IV-ECHO-1.0` is not semantically owned by `MIMIC-IV-3.1`; treat it as a sibling module
- align ECHO with other MIMIC modules through `subject_id`, `study_id`, `measurement_id`, record lists, and explicit time-alignment notes rather than directory nesting
- retained-variable design has not started yet, so current public support stops at onboarding and Layer 1 reproducibility
