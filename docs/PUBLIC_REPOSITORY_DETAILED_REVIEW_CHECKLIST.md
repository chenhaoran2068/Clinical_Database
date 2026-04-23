# Public Repository Detailed Review Checklist

Last updated: `2026-04-21`

## Why this file exists

This is the formal audit checklist for `Github/Clinical_Database`.

It is not the same as the local `Layer 1-5` cleanup checklist.

This file focuses on the GitHub-safe public method repository surface:

- public contracts
- onboarding docs
- public scripts and CLI
- release-governance outputs
- tutorials
- public variable cards
- CI and fixture coverage

## How to use this checklist

For each section, record:

- status: `pass`, `partial`, or `fail`
- reviewer
- review date
- blocking issues
- follow-up action

The goal is not only to ask "does the file exist".

The goal is to ask whether the public repository is internally consistent, legible, and governance-safe.

## Section 1. Repository identity

Check:

- `README.md` clearly states that this is a public method repository
- `README.md` clearly states what is not present
- `docs/GETTING_STARTED.md` gives a real onboarding path
- `docs/PUBLIC_INVENTORY.md` matches the current repository state

Questions:

- could a new collaborator understand the repository boundary without chat history
- is the public/local split clear

## Section 2. Family and version governance

Check:

- `docs/DATABASE_LINEAGE_AND_VERSION_MATRIX.md`
- `docs/database_catalog.json`
- `Framework_Guideline/Database_Family_NewVersion_Admission_Contract.md`

Questions:

- are all current public family members represented exactly once
- are sibling modules explicitly modeled as sibling modules
- would a future new version know how to enter cleanly

## Section 3. Onboarding surface

Check:

- `docs/onboarding/README.md`
- `docs/onboarding/families/*.md`
- `docs/onboarding/*.md`
- `docs/onboarding/ONBOARDING_TEMPLATE.md`
- `docs/onboarding/families/FAMILY_TEMPLATE.md`

Questions:

- does each current database have a playbook
- do family playbooks explain version and sibling-module rules
- does the template still match the current public method philosophy

## Section 4. Public CLI and scripts

Check:

- `scripts/public_workflow.py`
- `scripts/check_public_repository.py`
- `scripts/export_public_metadata.py`
- `scripts/prepare_public_release.py`
- `scripts/scaffold_public_database.py`
- `scripts/README.md`

Questions:

- are the main public actions obvious
- can a reviewer identify the correct first command
- are scripts still GitHub-safe and argument-driven
- are we duplicating local-only behavior into the public tree by mistake

## Section 5. Release governance

Check:

- `Framework_Guideline/ReleaseSafe_Manifest_ReleaseGovernance_Contract.md`
- `docs/release_safe_manifest.json`
- `docs/RELEASE_CHANGELOG.md`
- `docs/releases/README.md`
- current release note under `docs/releases/`

Questions:

- does the manifest point to the right changelog heading
- does the release note match the manifest release tag
- are release-safe outputs updated together rather than one by one

## Section 6. Public exports and inventory

Check:

- `docs/public_exports/README.md`
- `docs/public_exports/repository_status.json`
- `docs/public_exports/database_variable_coverage.json`
- `docs/public_exports/family_variable_coverage.json`
- `docs/public_exports/variable_coverage_summary.md`
- `docs/PUBLIC_INVENTORY.md`

Questions:

- do the machine-readable and human-readable views agree
- is coverage by database legible
- is coverage by family legible
- can a reviewer quickly tell which databases have public-card depth and which do not

## Section 7. Public variable-card layer

Check:

- `Framework_Guideline/Layer5_PublicVariableCard_Contract.md`
- `docs/std_variable_cards/README.md`
- current card set under `docs/std_variable_cards/`

Questions:

- do cards still follow the parser-friendly public structure
- do cards expose stable cross-database meaning rather than local execution details
- are approved database assets and publication rules still visible

## Section 8. Tutorials and representational clarity

Check:

- `docs/tutorials/README.md`
- all tutorial markdown files

Questions:

- do tutorials explain how to think with the repository, not only what files exist
- do tutorials cover family/version governance, variable-card interpretation, and release governance
- would an external researcher understand the method stack after reading them

## Section 9. Contracts and cross-contract coherence

Check:

- `Framework_Guideline/Layer1_Directory_Contract.md`
- `Framework_Guideline/CrossDatabase_Variable_Harmonization_Contract.md`
- `Framework_Guideline/Database_Critical_Semantics_Contract.md`
- `Framework_Guideline/PolicyRegistry_Contract.md`
- `Framework_Guideline/Script_Placement_Contract.md`

Questions:

- do the contracts still reflect the actual repository layout
- have new public scripts or exports silently created a new governance surface without a contract update
- do contracts contradict any generated outputs

## Section 10. Testing and CI

Check:

- `.github/workflows/public-smoke.yml`
- `tests/README.md`
- `tests/fixtures/public_cards/std_fixture_demo.md`

Questions:

- does CI cover compile, repository check, metadata export, release dry-run, and scaffold dry-run
- do fixtures still prove the parser contract instead of only passing on current production cards

## Section 11. Boundary with local work

Check:

- the public repo still does not contain restricted raw data
- the public repo still does not contain local parquet copies
- the public repo still does not contain patient-level Layer 2-5 outputs
- the current public docs still point clearly to `Methods/Clinical_Database/local_work` for local execution

Questions:

- are we keeping public-safe and local-only responsibilities distinct
- are local companion functions documented somewhere stable

## Section 12. Review output format

For each review cycle, produce:

1. one table of `pass / partial / fail` by section
2. one list of blocking issues
3. one list of non-blocking cleanup items
4. one summary of what is release-ready now

## Bottom line

The public repository should not be reviewed by impression.

It should be reviewed as a governed public methods surface with:

- explicit version lineage
- explicit onboarding
- explicit release governance
- explicit variable publication rules
- explicit CI and fixture coverage
