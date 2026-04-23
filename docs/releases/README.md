# Release Notes

This folder stores one GitHub-safe public release note per published release tag or working-tree release snapshot.

Relationship to nearby files:

- `docs/RELEASE_CHANGELOG.md`
  - short running release history
- `docs/releases/<release_tag>.md`
  - one release-facing note for that specific release line
- `docs/release_safe_manifest.json`
  - machine-readable release governance and release-safe file inventory

Operational rule:

- the release note should match the `release_notes_path` recorded in `docs/release_safe_manifest.json`
- the release note should be regenerated during `prepare-release`
