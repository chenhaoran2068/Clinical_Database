# Layer5 Public Variable Card Contract

This contract defines how a standardized variable may expose a GitHub-safe public summary without copying the entire local Layer 5 evidence package into the public repository.

## Core split

The project should treat these as different layers with different purposes:

- local Layer 5 knowledge package = full execution evidence and review record
- GitHub public variable card = public stable metadata subset

They are related, but they are not the same artifact.

## Why the split exists

The full local Layer 5 knowledge package is designed to preserve:

- database-specific implementation detail
- audit evidence
- local build history
- approval history
- rerun and reprocessing assessment

The public repository should instead expose only the stable subset that helps people understand the standardized variable itself.

## What the GitHub public variable card should contain

The GitHub-safe public subset should focus on stable variable-level meaning.

At minimum, it should contain:

- `std_variable_id`
- standardized English name
- standardized Chinese name
- standardized Japanese name when available
- short standard definition
- semantic folder
- standard unit
- value type
- grain
- default display rule
- default relative-time interpretation when relevant
- global warnings or cautions
- cross-database equivalence note when relevant

## Parser-friendly structure rule

Public cards are now also part of the repository's machine-checked publication surface.

That means they should keep a stable high-level section structure.

Recommended required headings:

- `## Identity`
- `## Cross-Database Standard Definition`
- `## Approved Database Implementations`
- `## Cross-Database Status`
- `## Current Approved Database Assets`
- `## Publication Rule`

## What should remain local in Layer 5

The following should stay in the local Layer 5 knowledge package rather than being mirrored directly to GitHub:

- source tables
- source columns
- source itemids or concept codes
- database-specific exceptions
- local cleaning thresholds
- build logs
- grouped review history
- rerun assessment
- preview outputs
- query summaries
- local lineage paths that are mainly operational

## Publication filter rule

The public exporter should be conservative when local execution text is richer than the public-safe contract.

Preferred rule:

- publish stable semantic metadata directly
- publish only public-safe caution text
- suppress local-only execution detail rather than trying to paraphrase it automatically

In practice, if a note or caution line depends mainly on:

- raw source tables
- raw source columns or fields
- raw itemids or concept identifiers
- local status-field names
- local cleaning thresholds
- build or review artifacts

then that line should remain local and should not be mirrored into the GitHub public card.

Future refinement rule:

- if the project later needs richer public notes, add dedicated public-safe fields rather than reusing local execution prose unchanged

## Relationship to other contracts

This contract does not replace:

- `CrossDatabase_Variable_Harmonization_Contract.md`

That harmonization contract governs whether variables across databases are truly the same standardized variable.

This public-card contract governs what stable subset of a finalized variable may be exposed safely in the public repository.

## Sync rule

The project should avoid manual double maintenance whenever possible.

Preferred rule:

- generate GitHub public variable cards from local Layer 5 knowledge packages or other canonical local metadata

Avoid:

- hand-copying the same metadata into two independently edited places

The public card should be a derived publication artifact, not the execution-time source of truth.

## Placement

Recommended GitHub-safe placement:

- `docs/std_variable_cards/`

Recommended full local evidence placement:

- `Methods/Clinical_Database/local_work/Layer 5/<database>/<std_variable_id>/`

## Operational interpretation

If a field is mainly needed to understand the global standardized variable, it is a candidate for the public card.

If a field is mainly needed to prove, reproduce, audit, or debug one database-specific retained build, it should remain local.
