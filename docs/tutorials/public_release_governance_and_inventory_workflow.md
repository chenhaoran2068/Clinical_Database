# Public Release Governance And Inventory Workflow

## Why this tutorial exists

The public repository now has a release-facing layer.

That means we do not only care about "what files exist".

We also care about:

- which public release line the snapshot belongs to
- whether the snapshot is only a working-tree draft or a stable release
- whether machine-readable and human-readable release surfaces agree

## The main public release artifacts

- `docs/release_safe_manifest.json`
- `docs/PUBLIC_INVENTORY.md`
- `docs/RELEASE_CHANGELOG.md`
- `docs/releases/<release_tag>.md`
- `docs/public_exports/...`

## Machine vs human split

### Machine-facing

- `docs/release_safe_manifest.json`
- `docs/public_exports/repository_status.json`
- `docs/public_exports/database_variable_coverage.json`
- `docs/public_exports/family_variable_coverage.json`

### Human-facing

- `docs/PUBLIC_INVENTORY.md`
- `docs/public_exports/variable_coverage_summary.md`
- `docs/RELEASE_CHANGELOG.md`
- `docs/releases/<release_tag>.md`

## The standard workflow

### Step 1. Confirm the changelog entry

Make sure `docs/RELEASE_CHANGELOG.md` contains the intended current heading:

```text
## <release_version> - <YYYY-MM-DD>
```

### Step 2. Dry-run release preparation

```powershell
python scripts/public_workflow.py prepare-release --dry-run
```

This shows which generated public outputs will be refreshed.

### Step 3. If needed, prepare a new release entry

Example:

```powershell
python scripts/public_workflow.py prepare-release `
  --release-version 0.2.0-dev `
  --release-tag public-method-foundation-2026-05-01 `
  --release-label public-method-repository-second-wave `
  --release-status pre_release `
  --release-date 2026-05-01 `
  --summary-line "expanded public release governance and variable-coverage exports"
```

### Step 4. Run the repository health check

```powershell
python scripts/public_workflow.py check-public-repository
```

This validates:

- generated outputs
- release-governance sync
- changelog linkage
- public card structure
- fixture parsing

## What `prepare-release` actually updates

- `docs/release_safe_manifest.json`
- `docs/PUBLIC_INVENTORY.md`
- `docs/public_exports/repository_status.json`
- `docs/public_exports/database_variable_coverage.json`
- `docs/public_exports/family_variable_coverage.json`
- `docs/public_exports/variable_coverage_summary.md`
- the current release note recorded in the manifest

## Why this matters

Without this layer, a public repository slowly drifts into a state where:

- the changelog says one thing
- the manifest says another
- the inventory reflects a third moment in time
- nobody can tell what the current public release boundary really is

The release workflow exists to prevent that drift.
