# AmsterdamUMCdb-1.0.2 Onboarding

## Scope

- database ID: `AmsterdamUMCdb-1.0.2`
- family: `AmsterdamUMCdb`
- module role: core database
- version: `1.0.2`

## Expected official source packages

- official AmsterdamUMCdb deliveries obtained through the authorized access path
- unpacked source CSV tables staged under `raw_unpacked`

## Layer 1 target layout

Local target root:

- `Methods/Clinical_Database/local_work/Layer 1/AmsterdamUMCdb-1.0.2/`

This is a sibling local-work path outside the public repository.

Expected buckets:

- `raw_original`
- `raw_unpacked`
- `source_supplied_derived`
- `local_converted_parquet`
- `docs_manifest`

Amsterdam currently uses a public Layer 1 conversion path from `raw_unpacked` to `local_converted_parquet`.
There is no public unpack script yet because the common local operating assumption is that Amsterdam source tables are already staged in unpacked form.

## Canonical ID mapping

Follow [`Framework_Guideline/ID_Normalization_Contract.md`](../../Framework_Guideline/ID_Normalization_Contract.md).

Current mapping for `AmsterdamUMCdb-1.0.2`:

| Canonical ID | Raw source name | Semantic meaning | Current rule |
| --- | --- | --- | --- |
| `subject_id` | `patientid` | patient identifier | direct semantic mapping |
| `stay_id` | `admissionid` | ICU/MC admission record identifier | use as the local ICU-semantic stay-equivalent key |
| `hadm_id` | not yet published | hospital admission identifier | do not synthesize by default in the current public opening surface |

Current Amsterdam note:

- `admissionid` should not be published as canonical `hadm_id` just because the raw source column contains the word `admission`
- under the current approved ICU-standardization surface, `admissionid` is treated as the local `stay_id` equivalent for ICU-semantic rows
- `admissioncount` remains a source longitudinal sequence field, not a canonical encounter identifier

## First public commands

```powershell
python scripts/public_workflow.py status
python scripts/public_workflow.py build-layer1 --database-id AmsterdamUMCdb-1.0.2 --action convert --layer1-root "..\..\Methods\Clinical_Database\local_work\Layer 1\AmsterdamUMCdb-1.0.2"
python scripts/public_workflow.py validate-registry --registry "..\..\Methods\Clinical_Database\local_work\Layer 4\AmsterdamUMCdb-1.0.2\PolicyRegistry_AmsterdamUMCdb-1.0.2_opening.json"
```

These relative examples assume the current shell is at the repository root.

## Public-safe artifacts already available

- Layer 1 skeleton in [`Data/Layer 1/AmsterdamUMCdb-1.0.2`](../../Data/Layer%201/AmsterdamUMCdb-1.0.2)
- Amsterdam time-semantics contract
- Layer 4 registry validator
- public std-variable cards for shared variables that already reached reviewed-approved local status

## Local-only execution surface

- staged official raw AmsterdamUMCdb source files
- local parquet copies
- Layer 2 time-anchor outputs
- Layer 4 machine-readable registry files and local review logs
- Layer 5 patient-level retained assets and evidence packages

## Critical caveats

- `admittedat` and `dischargedat` are relative offsets on the source longitudinal timeline, not universal zero points
- negative times from later admissions cannot be blindly accepted as baseline because cross-admission overlap is real
- `measuredat-first` reflects retrospective physiological state
- `dischargedat` must not be defaulted to death time
- follow [`Framework_Guideline/AmsterdamUMCdb_TimeSemantics_Contract.md`](../../Framework_Guideline/AmsterdamUMCdb_TimeSemantics_Contract.md) before doing downstream retention work
