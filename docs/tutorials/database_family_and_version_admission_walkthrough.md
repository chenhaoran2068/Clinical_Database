# Database Family And Version Admission Walkthrough

## Why this tutorial exists

The public repository is no longer single-database.

That means a new incoming source cannot be added by folder convenience alone.

We need to answer three questions first:

1. is this a new family
2. is this a new version of an existing family member
3. is this a sibling module that should stay semantically separate

## The governing files

Read these together:

- `Framework_Guideline/Database_Family_NewVersion_Admission_Contract.md`
- `docs/DATABASE_LINEAGE_AND_VERSION_MATRIX.md`
- `docs/database_catalog.json`
- `docs/onboarding/families/README.md`

## The current example

The repository currently models:

- `MIMIC-IV-3.1`
- `MIMIC-IV-ECHO-1.0`
- `AmsterdamUMCdb-1.0.2`

The key interpretation is:

- `MIMIC-IV-ECHO-1.0` is a sibling module inside the `MIMIC-IV` family
- it is not a semantic child of `MIMIC-IV-3.1`
- directory nesting is not the source of truth
- the catalog and contracts are the source of truth

## How to review a future incoming source

### Step 1. Decide the family relationship

Ask:

- does it belong to an existing family
- does it require a new family
- is it a core version or a sibling module

### Step 2. Decide whether a new `database_id` is required

Use a new `database_id` if the incoming source is:

- a new core version
- a sibling module
- a semantically distinct companion delivery that should be tracked independently

Do not reuse an existing `database_id` just because the names look similar.

### Step 3. Scaffold the public-safe minimum packet

Use:

```powershell
python scripts/public_workflow.py scaffold-public-database --database-id NEW-DB-1.0 --family-id NEW-FAMILY --version 1.0 --dry-run
```

That command does not auto-approve the new member.

By default it scaffolds:

- Layer 1 skeleton
- onboarding draft

Optional additions require explicit flags:

- add `--create-family-template-if-missing` to create a family-playbook draft when needed
- add `--emit-catalog-snippets-dir <dir>` to emit draft catalog JSON snippets for later review

Example with the optional packet enabled:

```powershell
python scripts/public_workflow.py scaffold-public-database `
  --database-id NEW-DB-1.0 `
  --family-id NEW-FAMILY `
  --version 1.0 `
  --create-family-template-if-missing `
  --emit-catalog-snippets-dir docs/tmp_catalog_snippets `
  --dry-run
```

### Step 4. Update the public lineage surface

Before broad downstream build work starts, update:

- `docs/database_catalog.json`
- `docs/DATABASE_LINEAGE_AND_VERSION_MATRIX.md`
- family onboarding docs when needed
- per-database onboarding docs

### Step 5. Re-check repository health

Run:

```powershell
python scripts/public_workflow.py check-public-repository
```

This ensures the new public surface is still internally consistent.

All command examples in this tutorial assume the current shell is at the repository root.

## Practical interpretation rule

The admission contract is not bureaucracy for its own sake.

It exists to stop these silent failure modes:

- accidentally overwriting an older version in place
- pretending a sibling module is equivalent to a core database line
- inheriting timing or identifier assumptions without review
- creating catalog drift between docs, skeletons, and public scripts

## What remains local-only

This tutorial is public-safe.

It does not cover:

- patient-level Layer 2 outputs
- local policy registry drafts
- retained-variable review evidence
- local Layer 5 asset packages
