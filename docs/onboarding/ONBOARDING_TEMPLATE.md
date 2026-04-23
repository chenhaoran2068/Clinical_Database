# Database Onboarding Template

## Scope

- database ID:
- family:
- module role:
- version:

## Expected official source packages

- list the official package names or delivery forms

## Layer 1 target layout

- state explicitly that the local target root is a sibling local-work path outside the public repository
- where `raw_original` should be populated
- where `raw_unpacked` should be populated
- whether there is a canonical subfolder under `raw_unpacked`
- what `local_converted_parquet` is expected to contain

## First public commands

```powershell
python scripts/public_workflow.py status
python scripts/public_workflow.py build-layer1 ...
```

- state whether the example commands assume the current shell is at the repository root

## Public-safe artifacts already available

- Layer 1 skeleton
- contracts
- validators
- public variable cards

## Local-only execution surface

- local parquet copies
- Layer 2 to Layer 5 patient-level outputs
- local knowledge packages
- local previews and build logs

## Critical caveats

- list the critical semantics that a new collaborator must not miss
