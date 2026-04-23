# Public Exports

This folder stores generated GitHub-safe public export artifacts.

These files are derived from the current public repository state.

They are meant to serve two different audiences:

- machine-readable export consumers
- human reviewers who want a narrower view than the full release-safe manifest

Current generated files:

- `repository_status.json`
- `database_variable_coverage.json`
- `family_variable_coverage.json`
- `variable_coverage_summary.md`

Generation rule:

- update these files together with `docs/release_safe_manifest.json`
- update these files together with `docs/PUBLIC_INVENTORY.md`
- update these files together with `docs/RELEASE_CHANGELOG.md`
- update these files together with the current release note under `docs/releases/`

Recommended entrypoints:

```powershell
python scripts/public_workflow.py export-public-artifacts --artifact repository-status
python scripts/public_workflow.py export-public-artifacts --artifact database-variable-coverage
python scripts/public_workflow.py export-public-artifacts --artifact family-variable-coverage
python scripts/public_workflow.py export-public-artifacts --artifact variable-coverage-summary
python scripts/public_workflow.py prepare-release --dry-run
```
