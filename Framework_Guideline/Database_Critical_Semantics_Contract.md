# Database Critical Semantics Contract

This contract defines a project-wide rule for database-specific high-risk semantics.

Cross-database harmonization is global.
But each database still has its own silent failure modes.

Those database-specific traps must be written down explicitly rather than left as memory.

## Core rule

Each database that enters standardized retained-variable work should have at least one approved database-specific critical semantics contract covering its highest-risk semantic pitfall.

The exact topic does not need to be the same across databases.

## Why this is necessary

Global contracts answer questions like:

- when two variables may share one `std_variable_id`
- what unit and value type must stay stable
- how registry-driven ETL should behave

They do **not** automatically protect against database-specific semantic traps such as:

- time-offset illusions
- admission-grain confusion
- death-time vs administrative discharge confusion
- device setting vs observed state confusion
- note provenance or release-package caveats
- linkage-key assumptions that look safe but are not

These problems must be handled by database-specific contracts.

## Minimum expectation

Before broad retained-variable scaling for a new database, the project should identify and document:

1. the highest-risk semantic illusion or ambiguity
2. the authoritative interpretation
3. the default safe rule
4. the prohibited default interpretation
5. the downstream consequence if the rule is violated

## Recommended structure for a database-specific contract

Each database-specific critical semantics contract should ideally include:

- why the note exists
- the core rule
- the safe default interpretation
- the prohibited interpretation
- example formula or implementation pattern when relevant
- downstream implication for later builders and reviews

## Placement

GitHub-safe database-specific contracts should normally live in:

- `Framework_Guideline/<Database>_<Topic>_Contract.md`

Database-local execution evidence, audits, grouped review packages, and machine-readable policy registries should continue to live under local work such as:

- `Methods/Clinical_Database/local_work/Layer 4/<database>/`
- `Methods/Clinical_Database/local_work/Layer 5/<database>/`

## Approval rule

A database should not rely on unwritten tribal memory for its main semantic trap.

At least one critical semantics contract should be approved before large-scale retained-variable expansion for that database.

Additional contracts may be added later if more than one high-risk semantic area exists.

## Amsterdam example

`AmsterdamUMCdb_TimeSemantics_Contract.md` is the current example of a database-specific critical semantics contract.

Its topic is time semantics, because that is the highest-risk opening pitfall discovered for AmsterdamUMCdb.

## MIMIC example

`MIMICIV_SourcePackageAndModuleBoundary_Contract.md` is the current MIMIC example.

Its topic is source-package provenance and module boundary semantics, because the highest-risk public trap for the current MIMIC core line is to confuse:

- core-package scope with sibling-module scope
- or a local note fallback with official raw note delivery

Future databases may use different topics if their main risk is not time.
