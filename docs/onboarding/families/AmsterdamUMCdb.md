# AmsterdamUMCdb Family Playbook

## Family identity

- family ID: `AmsterdamUMCdb`
- display name: `AmsterdamUMCdb family`
- current public members:
  - `AmsterdamUMCdb-1.0.2`

## Why this family doc exists

Right now the public repository only contains one AmsterdamUMCdb version.

Even so, it is still useful to define the family-level rule now, before additional versions or companion modules appear.

The most important family-level fact is that AmsterdamUMCdb has critical relative-time semantics that must remain explicit whenever a new version is added.

## Current member map

```text
AmsterdamUMCdb family
`- AmsterdamUMCdb-1.0.2
   |- current public Layer 1 conversion is published
   |- current public Layer 4 path centers on opening-policy semantics
   `- current public Layer 5 state is a pilot-reviewed subset
```

## Family-level rules

1. New AmsterdamUMCdb releases should be added as new versioned `database_id` rows under the same family rather than replacing `AmsterdamUMCdb-1.0.2`.
2. Database-level time semantics must stay explicit and version-scoped; do not assume that one Amsterdam release automatically inherits all timing assumptions from another without review.
3. Layer 1 staging may stay structurally similar across versions, but Layer 2 onward must always re-check opening contracts and time-anchor assumptions.
4. Per-version epidemiology comparisons should be documented in the local audit trail before cross-version analytic claims are treated as interchangeable.
5. If a future Amsterdam companion module appears, decide explicitly whether it is a sibling module or merely an alternate delivery of the same version.

## Current public-safe assets

- family and version matrix:
  - [`docs/DATABASE_LINEAGE_AND_VERSION_MATRIX.md`](../../DATABASE_LINEAGE_AND_VERSION_MATRIX.md)
- machine-readable catalog:
  - [`docs/database_catalog.json`](../../database_catalog.json)
- per-database onboarding:
  - [`../AmsterdamUMCdb-1.0.2.md`](../AmsterdamUMCdb-1.0.2.md)
- critical semantics contract:
  - [`Framework_Guideline/AmsterdamUMCdb_TimeSemantics_Contract.md`](../../../Framework_Guideline/AmsterdamUMCdb_TimeSemantics_Contract.md)

## What should happen when a new family member is added

1. add the new member to [`docs/database_catalog.json`](../../database_catalog.json)
2. decide whether it is a new version row or a sibling module
3. create the per-database onboarding playbook
4. review whether the time-semantics contract needs a new version-scoped companion note
5. revise this family playbook if the family-level governance rule changed
