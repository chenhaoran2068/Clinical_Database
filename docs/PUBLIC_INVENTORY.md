# Public Inventory

## What this file is

This is the human-readable inventory of the current GitHub-safe public repository surface.
The machine-readable counterpart is [`docs/release_safe_manifest.json`](release_safe_manifest.json).

## Snapshot summary

- catalog version: `2026-04-21`
- family count: `2`
- database count: `3`
- public std-variable cards: `463`
- cross-database public cards: `7`
- total release-safe files listed in the manifest: `551`
- release version: `0.1.0-dev`
- release tag: `public-method-foundation-2026-04-21`
- release status: `working_tree_snapshot`

## Release governance

- release version: `0.1.0-dev`
- release tag: `public-method-foundation-2026-04-21`
- release label: `public-method-repository-foundation`
- release status: `working_tree_snapshot`
- release date: `2026-04-21`
- changelog: `docs/RELEASE_CHANGELOG.md`
- current changelog heading: `## 0.1.0-dev - 2026-04-21`
- release notes: `docs/releases/public-method-foundation-2026-04-21.md`

## Coverage by family

| family_id | display_name | current database_ids | family playbook | family union count | family shared count |
| --- | --- | --- | --- | --- | --- |
| `MIMIC-IV` | MIMIC-IV family | `MIMIC-IV-3.1`, `MIMIC-IV-ECHO-1.0` | `docs/onboarding/families/MIMIC-IV.md` | `463` | `0` |
| `AmsterdamUMCdb` | AmsterdamUMCdb family | `AmsterdamUMCdb-1.0.2` | `docs/onboarding/families/AmsterdamUMCdb.md` | `7` | `7` |

## Coverage by database/module

| database_id | family | role | version | layer1 | layer4 | layer5 | public cards | onboarding |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `MIMIC-IV-3.1` | `MIMIC-IV` | core_database | `3.1` | published_skeleton_and_public_scripts | contract_and_registry_validator_published | broad reviewed-approved local assets exist and public std-variable cards are published | `463` | `docs/onboarding/MIMIC-IV-3.1.md` |
| `MIMIC-IV-ECHO-1.0` | `MIMIC-IV` | sibling_module | `1.0` | published_skeleton_and_public_scripts | global contracts available; no ECHO-specific policy registry published yet | database-level local notes exist, but no reviewed-approved retained-variable family has been published yet | `0` | `docs/onboarding/MIMIC-IV-ECHO-1.0.md` |
| `AmsterdamUMCdb-1.0.2` | `AmsterdamUMCdb` | core_database | `1.0.2` | published_skeleton_and_public_scripts | database opening policy registry contract and validator path are published | pilot reviewed-approved local assets exist and public std-variable cards are published for shared variables | `7` | `docs/onboarding/AmsterdamUMCdb-1.0.2.md` |

## Public asset classes

| asset class | count | notes |
| --- | --- | --- |
| root files | `2` | repository-level public entry files |
| framework contracts | `11` | governing public contracts in `Framework_Guideline/` |
| core docs | `7` | matrix, inventory, review checklist, and other core public notes |
| release docs | `2` | changelog and release-process support docs |
| release note docs | `1` | one release note per public release tag |
| public export support files | `1` | README for generated public export artifacts |
| public export docs | `4` | generated repository status and variable-coverage exports |
| onboarding support files | `4` | README and templates for onboarding layers |
| family playbooks | `2` | family-level governance docs |
| database playbooks | `3` | per-database onboarding docs |
| tutorials | `6` | public-safe walkthroughs |
| GitHub workflows | `1` | public CI/smoke workflows |
| public scripts | `22` | GitHub-safe Python scripts under `scripts/` |
| Layer 1 skeleton files | `18` | committed public Layer 1 skeleton contents across supported databases |
| std-variable card support files | `1` | shared README for public cards |
| public std-variable cards | `463` | variable-level public documentation cards |
| test support files | `2` | public-safe fixtures and repository test notes |

## Key entrypoints

- `python scripts/public_workflow.py status`
- `python scripts/public_workflow.py status --family-id MIMIC-IV`
- `python scripts/public_workflow.py build-layer1 ...`
- `python scripts/public_workflow.py validate-registry ...`
- `python scripts/public_workflow.py check-public-repository`
- `python scripts/public_workflow.py prepare-release --dry-run`
- `python scripts/public_workflow.py scaffold-public-database --help`
- `python scripts/public_workflow.py export-public-artifacts --artifact release-safe-manifest`
- `python scripts/public_workflow.py export-public-artifacts --artifact public-inventory`
- `python scripts/public_workflow.py export-public-artifacts --artifact release-governance`
- `python scripts/public_workflow.py export-public-artifacts --artifact database-variable-coverage`
- `python scripts/public_workflow.py export-public-artifacts --artifact family-variable-coverage`
- `python scripts/public_workflow.py export-public-artifacts --artifact variable-coverage-summary`

## Full machine-readable inventory

For the complete file-level release-safe list, use [`docs/release_safe_manifest.json`](release_safe_manifest.json).

For public variable-coverage exports, use the generated files under [`docs/public_exports`](public_exports/README.md).
