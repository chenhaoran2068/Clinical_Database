# Next-Stage Public Method Repository Checklist

Last updated: 2026-04-21

## Why this note exists

`Clinical_Database` is no longer just a loose collection of scripts and notes.

It is already growing into a public method repository for cross-database clinical data standardization.

The next stage is to make that public repository feel more like a reproducibility-oriented methods platform:

- not MIMIC-only
- not tied to one database family
- critical-care-first, but extensible to other clinical databases later

This note defines the next major build-out areas.

For the stricter transition from a human-readable method repository to a machine-readable, executable, validated standard system, use [`docs/STANDARD_SYSTEM_MATURITY_ROADMAP.md`](STANDARD_SYSTEM_MATURITY_ROADMAP.md).
This file stays focused on the public repository surface itself.

## Current public-repository baseline

The repository already has:

- framework contracts
- Layer 1 directory skeletons
- GitHub-safe Layer 1 / Layer 4 / Layer 5 scripts
- public standard-variable cards
- early cross-database public cards for approved shared variables

What it does not yet have is a full public "clone -> understand -> run -> verify" experience across multiple databases.

## Target posture

The target is a public repository that can serve as a cross-database counterpart to a MIMIC-style reproducibility repository, with these properties:

- method contracts are explicit
- database version handling is explicit
- standard variables are published consistently
- public scripts are reusable
- common validation can run automatically
- representative public-safe workflows show how the standardized assets are used

Initial public implementations for all five workstreams landed on 2026-04-21.

This file now tracks what exists and what should deepen next.

Second-wave public hardening also landed on 2026-04-21:

- release preparation entrypoint
- stronger repository checks and parser fixtures
- public database scaffold entrypoint
- finer generated public coverage exports
- additional governance/tutorial docs
- a more product-like public CLI surface

## Workstream 1: Database lineage and version matrix

### Goal

Publish a clear map of which databases, versions, and sibling-module relationships the repository currently knows about.

### Why this matters

The repository already contains MIMIC, ECHO, and Amsterdam materials.
Without one authoritative matrix, users can still misunderstand whether a source should be treated as a new family, a new version, or a sibling module.

### Minimum deliverables

- one public database catalog document
- one machine-readable version matrix or catalog
- explicit publication of `MIMIC-IV-3.1`, `MIMIC-IV-ECHO-1.0`, and `AmsterdamUMCdb-1.0.2`

### The matrix should answer

1. which database families and versions are currently supported
2. which modules are siblings rather than children
3. which public Layer 1 skeletons and scripts already exist
4. which special semantics contracts apply
5. which public Layer 5 coverage already exists

### Done criterion

A reader can answer "which databases and versions are currently supported, and to what public extent?" from one public file.

Current status:

- implemented in [`docs/DATABASE_LINEAGE_AND_VERSION_MATRIX.md`](DATABASE_LINEAGE_AND_VERSION_MATRIX.md)
- implemented in [`docs/database_catalog.json`](database_catalog.json)

## Workstream 2: Database onboarding playbooks

### Goal

Turn the current contracts and directory skeletons into practical database-level onboarding guides.

### Why this matters

Contracts define how things should look.
Playbooks define what someone should do first, second, and third when adding or rebuilding a database.

### Minimum deliverables

- one shared onboarding template
- one public onboarding playbook for `MIMIC-IV-3.1`
- one public onboarding playbook for `MIMIC-IV-ECHO-1.0`
- one public onboarding playbook for `AmsterdamUMCdb-1.0.2`

### Each onboarding playbook should answer

1. what official source package(s) are expected
2. where files go in Layer 1
3. which public scripts are the first entrypoints
4. what Layer 2 / Layer 4 / Layer 5 public expectations already exist
5. which parts are public-safe versus local-only
6. what current caveats or special semantics apply

### Done criterion

A new collaborator can read one playbook and understand the public-safe path from Layer 1 staging to downstream standardization for that database.

Current status:

- implemented in [`docs/onboarding/README.md`](onboarding/README.md)
- implemented in the three current database playbooks under [`docs/onboarding`](onboarding/README.md)

## Workstream 3: End-to-end public entrypoints

### Goal

Move from a toolbox of scripts toward a small set of recognizable workflow entrypoints.

### Why this matters

Right now the repository contains useful pieces, but users still need prior context to know which script to run first.

### Minimum deliverables

- one database-oriented build entrypoint
- one registry validation entrypoint
- one publication/export entrypoint
- one status or inventory entrypoint

### Desired public workflow shape

- `build database X`
- `validate policy registry`
- `export retained/public artifacts`
- `show current public repository status`

### First acceptable implementation

This does not need to start as a perfect CLI framework.
A small wrapper layer around existing public scripts is already enough if it makes the workflow obvious.

### Done criterion

A new user can identify the main public execution path without reading internal local-work notes.

Current status:

- implemented in [`scripts/public_workflow.py`](../scripts/public_workflow.py)
- extended with `prepare-release` and `scaffold-public-database`

## Workstream 4: Public testing and CI

### Goal

Make the public repository automatically check its own health.

### Why this matters

A mature reproducibility repository should not depend only on manual memory and manual inspection.

### Minimum deliverables

- schema checks for public critical files
- script compile/import checks
- at least one tiny public-safe fixture or smoke-run input
- one CI smoke workflow

### Good first checks

- verify public Python scripts compile
- verify key contracts and template files exist
- verify the database catalog still validates
- verify the public workflow entrypoints still start

### Done criterion

A normal public change to the repository triggers automatic sanity checks before drift accumulates.

Current status:

- implemented in [`scripts/check_public_repository.py`](../scripts/check_public_repository.py)
- implemented in [`.github/workflows/public-smoke.yml`](../.github/workflows/public-smoke.yml)
- now also checks release-governance sync, generated public exports, and public-card fixtures

## Workstream 5: Representative tutorials and analysis layer

### Goal

Show how the standardized outputs are meant to be used.

### Why this matters

The repository is already strong on contracts and standardization mechanics.
It is still weaker on public-safe examples that demonstrate how these standardized assets support actual critical-care research workflows.

### Minimum deliverables

- one tutorial for reading a standard-variable public card back into the local asset model
- one tutorial for a minimal variable-level validation workflow
- one tutorial for a cross-database comparison workflow

### Good first tutorial topics

- how to interpret `std_heart_rate` across MIMIC and Amsterdam
- how to read a public card together with its local Layer 5 knowledge package
- how to compare one standard variable across approved databases without violating local-only boundaries

### Done criterion

An external reader can understand not only what the standards are, but how they are meant to be used in practice.

## Recommended build order

The suggested order is:

1. publish the database lineage/version matrix
2. add onboarding playbooks for the currently active databases
3. add clearer public workflow entrypoints
4. add public tests and CI smoke checks
5. add representative tutorials

This order keeps the repository legible first, runnable second, and teachable third.

## Immediate next-step candidates

The most natural immediate next public tasks are:

- deepen the database matrix when new families or versions are added
- expand onboarding playbooks when new databases enter Layer 1
- deepen the public scaffold and release workflow as more database families arrive
- strengthen CI with more fixtures and smoke-test scenarios
- add more tutorials after each new reviewed-approved variable family

## Interpretation rule

This checklist is a build-order note, not a frozen contract.

The contracts in `Framework_Guideline/` remain the governing rules.
This file only states what the next public-repository construction layer should be.
