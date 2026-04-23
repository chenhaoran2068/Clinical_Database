# Database Family New-Version Admission Contract

This contract defines how a new database version or sibling module is allowed to enter the public method repository.

It exists because "same family" does not mean "safe to drop into the old folder and treat as inherited."

## Why this contract exists

The repository now has explicit database families such as:

- `MIMIC-IV`
- `AmsterdamUMCdb`

Within a family, future additions can take different forms:

- a new core version
- a sibling module
- a companion delivery that looks related but should not become a new member

Without a formal admission contract, future additions could silently break:

- directory semantics
- version clarity
- family boundaries
- downstream reproducibility

## Core rule

Every new family member must enter through an explicit admission decision.

No new version or sibling module should be admitted by directory convenience alone.

## Definitions

### Family

A named group of related databases or modules that share a long-term governance layer, such as `MIMIC-IV`.

### Core version row

A versioned database member that represents a primary database line within the family, such as `MIMIC-IV-3.1`.

### Sibling module

A related but semantically independent family member that must not be treated as a child of the nearest core-version directory, such as `MIMIC-IV-ECHO-1.0`.

### Companion delivery

A source package or documentation delivery that may belong to an existing database member without deserving a new `database_id`.

### Deprecated family member

A version or module that remains recorded for lineage and reproducibility but is no longer the preferred active build target.

## Admission rules

### Rule 1: New core versions require a new `database_id`

If the incoming asset is a new version of an existing core database line, it must be admitted as a new `database_id` row.

It must not overwrite an existing row such as:

- replacing `MIMIC-IV-3.1` in place
- silently reusing an older Layer 1 skeleton
- silently changing an existing catalog row's version string

### Rule 2: Sibling modules require explicit sibling status

If the incoming asset is a sibling module rather than a new core version, the repository must explicitly mark it as a sibling module.

It must receive:

- its own `database_id`
- its own onboarding playbook
- its own Layer 1 root or explicit staging rule
- its own public-support status fields

It must not be semantically governed only by being placed under another database's directory.

### Rule 3: New admissions require a minimum public packet

Before a new family member is considered formally admitted into the public method repository, the following public-safe packet should exist:

1. updated `docs/database_catalog.json`
2. updated database lineage matrix
3. family-playbook update when family interpretation changes
4. per-database onboarding playbook
5. Layer 1 skeleton or an explicit published reason why none exists yet
6. public script entrypoint list or explicit published absence
7. public support-status fields for Layer 1, Layer 4, and Layer 5

Operational note:

- the repository may use a public scaffold helper to generate this packet
- scaffolding does not equal approval
- the family/database rows still require explicit review

### Rule 4: Inheritance is limited

A new family member may inherit:

- global contracts
- shared naming philosophy
- shared public workflow entrypoints when applicable

It may not automatically inherit:

- database-specific critical semantics
- prior version assumptions about timing, identifiers, or source packaging
- retained-variable approval status
- claims of equivalence with older versions

### Rule 5: Critical semantics must be reconsidered

For each newly admitted family member, the team should explicitly decide whether:

- an existing database-specific critical semantics contract still applies
- a new database-specific contract is required
- no database-specific contract is yet needed because the member has not entered retained-variable work

### Rule 6: Coexistence and deprecation must remain explicit

Older family members should remain visible in the catalog until an explicit deprecation or retirement decision is published.

A new admission must not erase the lineage of earlier members.

If a member becomes deprecated, the public repository should mark that status explicitly in catalog or release-facing metadata rather than silently removing the row.

## Machine-readable expectations

At minimum, a newly admitted family member should be reflected in:

- `docs/database_catalog.json`
- `docs/DATABASE_LINEAGE_AND_VERSION_MATRIX.md`
- `docs/onboarding/...`
- or in scaffold draft outputs that are about to be reviewed into those locations

Family-level governance should remain visible in:

- `docs/onboarding/families/...`

## Approval expectation

The admission decision should be explicit before broad downstream retained-variable scaling begins for the new family member.

This does not mean the member must already have mature Layer 5 coverage.

It means the repository must already know what the member is.

## Relationship to other contracts

- `CrossDatabase_Variable_Harmonization_Contract.md` governs same-name standard-variable behavior
- `Database_Critical_Semantics_Contract.md` governs database-specific semantic traps
- this contract governs how new family members are admitted into the repository structure itself
