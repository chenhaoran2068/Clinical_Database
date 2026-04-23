# Release-Safe Manifest Release Governance Contract

This contract defines the release-governance layer for `docs/release_safe_manifest.json`.

The manifest is not only a snapshot of current public files.
It is also the machine-readable release-facing descriptor for the public method repository.

## Why this contract exists

A file inventory alone answers:

- what is here now

It does not fully answer:

- which public release line this snapshot belongs to
- whether the snapshot is a stable release or a working-tree draft
- where the human-readable release history lives
- how future releases should record changes

This contract fills that gap.

## Core rule

`docs/release_safe_manifest.json` should carry an explicit release-governance block.

That block should make release identity, release status, and changelog linkage machine-readable.

## Minimum required release-governance fields

The release-governance block should include at least:

- `release_contract_version`
- `release_series_id`
- `release_version`
- `release_tag`
- `release_label`
- `release_status`
- `release_date`
- `changelog_path`
- `current_changelog_entry_heading`
- `release_notes_path`
- `versioning_rule`
- `release_update_rule`
- `release_notes_rule`
- `release_gate_rule`

## Status rule

The release-governance block should explicitly state what kind of snapshot the manifest describes.

Recommended statuses include:

- `working_tree_snapshot`
- `pre_release`
- `stable_release`
- `deprecated_release_line`

## Changelog interface rule

The repository should maintain a public changelog file for release-facing history.

Current public path:

- `docs/RELEASE_CHANGELOG.md`

The manifest should point to that changelog and identify the current matching entry heading.

The manifest should also point to the current release note under:

- `docs/releases/`

## Update rule

Whenever the public repository crosses a release boundary, the following should be updated in the same change set:

1. `docs/release_safe_manifest.json`
2. `docs/PUBLIC_INVENTORY.md`
3. `docs/RELEASE_CHANGELOG.md`
4. current generated public exports under `docs/public_exports/`
5. current release note under `docs/releases/`

This rule keeps machine-readable release identity and human-readable release history from drifting apart.

## Scope rule

The release-safe manifest may only describe GitHub-safe public artifacts.

It must not be repurposed to list:

- restricted raw data
- local parquet copies
- patient-level Layer 2 to Layer 5 outputs
- non-public local execution evidence

## Relationship to the public inventory

- `docs/release_safe_manifest.json` is the machine-readable release-facing source of truth
- `docs/PUBLIC_INVENTORY.md` is the human-readable inventory summary derived from the same public state

They should stay consistent, but they do not serve the same audience.

## Relationship to future release automation

The contract does not require a full tag-and-publish platform.

It does require that the repository expose the release-governance surface in a way that public workflow tooling can consume, such as:

- `prepare-release`
- repository checks that validate changelog and release-note linkage
- generated public exports that stay consistent with the manifest
