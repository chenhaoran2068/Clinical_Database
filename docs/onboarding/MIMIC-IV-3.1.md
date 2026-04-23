# MIMIC-IV-3.1 Onboarding

## Scope

- database ID: `MIMIC-IV-3.1`
- family: `MIMIC-IV`
- module role: core database
- version: `3.1`

## Expected official source packages

- `mimic-iv-3.1.zip`
- `mimic-iv-ed-2.2.zip`
- optionally `mimic-iv-note-2.2.zip` when the official note package is available

## Layer 1 target layout

Local target root:

- `Methods/Clinical_Database/local_work/Layer 1/MIMIC-IV-3.1/`

This is a sibling local-work path outside the public repository.

Expected buckets:

- `raw_original`
- `raw_unpacked`
- `source_supplied_derived`
- `local_converted_parquet`
- `docs_manifest`

Expected unpacked module layout:

- `raw_unpacked/core/...`
- `raw_unpacked/ed/...`
- `raw_unpacked/note/...`

`local_converted_parquet` stores regenerated parquet copies for local execution speed only.

## Canonical ID mapping

Follow [`Framework_Guideline/ID_Normalization_Contract.md`](../../Framework_Guideline/ID_Normalization_Contract.md).

Current mapping for `MIMIC-IV-3.1`:

| Canonical ID | Raw source name | Semantic meaning | Current rule |
| --- | --- | --- | --- |
| `subject_id` | `subject_id` | patient identifier | direct reuse |
| `hadm_id` | `hadm_id` | hospital admission identifier | direct reuse |
| `stay_id` | `stay_id` | ICU stay identifier | direct reuse |

MIMIC is the simple case where raw naming already matches the current cross-database canonical ID vocabulary.

## First public commands

```powershell
python scripts/public_workflow.py status
python scripts/public_workflow.py build-layer1 --database-id MIMIC-IV-3.1 --action unpack --layer1-root "..\..\Methods\Clinical_Database\local_work\Layer 1\MIMIC-IV-3.1"
python scripts/public_workflow.py build-layer1 --database-id MIMIC-IV-3.1 --action convert --layer1-root "..\..\Methods\Clinical_Database\local_work\Layer 1\MIMIC-IV-3.1" --modules hosp icu ed note
```

These relative examples assume the current shell is at the repository root.

## Public-safe artifacts already available

- Layer 1 skeleton in [`Data/Layer 1/MIMIC-IV-3.1`](../../Data/Layer%201/MIMIC-IV-3.1)
- general contracts under [`Framework_Guideline`](../../Framework_Guideline)
- MIMIC source-package boundary contract in [`Framework_Guideline/MIMICIV_SourcePackageAndModuleBoundary_Contract.md`](../../Framework_Guideline/MIMICIV_SourcePackageAndModuleBoundary_Contract.md)
- Layer 4 registry validator
- broad public std-variable card coverage in [`docs/std_variable_cards`](../std_variable_cards)

## Local-only execution surface

- staged official raw source files
- local parquet copies
- Layer 2 to Layer 5 patient-level outputs
- reviewed knowledge packages and local evidence bundles

## Critical caveats

- `MIMIC-IV-3.1` and `MIMIC-IV-ECHO-1.0` are related family members, but they are not the same source-package scope
- note delivery may be absent; if so, the public fallback path reconstructs a local note proxy from existing parquet, but that is still a fallback rather than a fresh official download
- `chartevents` and `labevents` are large enough that the current public conversion logic may split outputs for stable local execution
- downstream variable work is standardized through global `std_*` semantics, not through raw MIMIC table names
