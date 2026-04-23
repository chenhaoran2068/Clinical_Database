# Layer 5 Scripts

This folder is reserved for GitHub-safe retained-builder scripts.

Current opening rule:

- retained builders should load and validate the approved policy registry before applying database-specific cleaning logic
- scripts should avoid local hard-coded machine paths
- scripts should accept command-line arguments whenever practical
- patient-level outputs do not belong in this public repository
- GitHub-safe Layer 5 helpers may still run against user-staged local Layer 3 or Layer 5 assets, but any patient-level outputs they emit remain local-only

Current shared helper:

- `master_index_helper.py`
  - read rows from `std_variable_database_assets`
  - upsert one database-specific asset record
  - ensure the V2 database-instance sheet exists
- `check_local_id_semantics.py`
  - scan local Layer 5 knowledge packages for ID-normalization wording drift
  - currently includes an Amsterdam-focused guardrail for `admissionid -> stay_id` / stay-equivalent semantics
- `export_public_variable_card.py`
  - build a GitHub-safe public variable card from local Layer 5 metadata
  - keep source-table details and build logs in local knowledge packages
  - require an explicit `--database-id` when a variable already has multiple approved database assets
  - support `--cross-database` when one merged public card should summarize multiple approved database assets

Default write policy from `2026-04-19` onward:

- new generalized builders should default to writing database-specific asset registry rows into:
  - `std_variable_database_assets`
- they should not default to writing only:
  - `std_variable_catalog`
- `std_variable_catalog` remains a legacy-compatible variable directory and may still be updated only when explicit backward compatibility is needed

During the Amsterdam opening phase, local real-data helpers may temporarily live under:

- `Methods/Clinical_Database/local_work/Layer 5/<database>/shared_extract_code`

As retained builders mature and become GitHub-safe, they should be promoted into this folder.
