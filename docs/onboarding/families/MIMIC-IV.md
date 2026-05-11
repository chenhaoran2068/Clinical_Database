# MIMIC-IV Family Playbook

## Family identity

- family ID: `MIMIC-IV`
- display name: `MIMIC-IV family`
- current public members:
  - `MIMIC-IV-3.1`
  - `MIMIC-IV-ECHO-1.0`

## Why this family doc exists

`MIMIC-IV` is already more than one thing in practice.

Even in the current public repository, the family includes:

- a core database line used for `hosp`, `icu`, `ed`, and `note` staging
- a stand-alone ECHO module that should not be semantically absorbed into the core-version folder name

Without a family-level rulebook, future versions such as `MIMIC-IV-2.2` or future sibling modules would be too easy to stage in a way that looks convenient locally but is semantically wrong.

## Current member map

```text
MIMIC-IV family
|- MIMIC-IV-3.1
|  |- current public Layer 1 covers core/hosp, icu, ed, note staging expectations
|  |- local Layer 4 opening registry built pending owner review
|  `- current public Layer 5 coverage is the most mature in the repository
`- MIMIC-IV-ECHO-1.0
   |- sibling module
   |- separate Layer 1 root
   |- local Layer 4 opening registry built pending owner review
   `- retained-variable design has not started yet
```

## Family-level rules

1. Core-version rows and sibling-module rows are not interchangeable.
2. `MIMIC-IV-ECHO-1.0` must remain a sibling module, not a semantic child of `MIMIC-IV-3.1`.
3. New core versions such as `MIMIC-IV-2.2` or later should be added as new `database_id` entries under the same family, not by overwriting `MIMIC-IV-3.1`.
4. Cross-module alignment should be based on explicit identifiers and timing notes such as `subject_id`, `study_id`, `measurement_id`, record-list references, and documented time-alignment behavior, not on directory nesting.
5. Family-level semantics should be documented once here, while per-database staging details belong in the individual onboarding playbooks.

## Current public-safe assets

- family and version matrix:
  - [`docs/DATABASE_LINEAGE_AND_VERSION_MATRIX.md`](../../DATABASE_LINEAGE_AND_VERSION_MATRIX.md)
- machine-readable catalog:
  - [`docs/database_catalog.json`](../../database_catalog.json)
- per-database onboarding:
  - [`../MIMIC-IV-3.1.md`](../MIMIC-IV-3.1.md)
  - [`../MIMIC-IV-ECHO-1.0.md`](../MIMIC-IV-ECHO-1.0.md)
- public workflow:
  - [`scripts/public_workflow.py`](../../../scripts/public_workflow.py)

## What should happen when a new family member is added

1. add the new member to [`docs/database_catalog.json`](../../database_catalog.json)
2. decide whether it is a new core-version row or a sibling-module row
3. add a per-database onboarding playbook
4. add or revise the public Layer 1 skeleton and any needed public scripts
5. revise this family playbook if the family interpretation rule changed
