# Current-Stage Completion Standard

Last updated: 2026-04-23

## Why this note exists

`Clinical_Database` now has enough real structure, real local assets, and real public governance that "what counts as done for the current stage" should no longer be left to memory.

This note defines that stage-exit standard.

It answers two different questions:

1. what the current stage must achieve before it can be called complete
2. whether the repository and workspace baseline currently satisfy that standard

This note does not define the final end-state of the project.

For the longer transition into a stricter machine-readable, executable, validated standard system, use [`docs/STANDARD_SYSTEM_MATURITY_ROADMAP.md`](STANDARD_SYSTEM_MATURITY_ROADMAP.md).

## What "current stage" means

The current stage is not the full standard-system phase yet.

It is the stage in which the project must successfully establish:

- a stable local-work architecture
- a coherent GitHub-safe public method repository
- a real local baseline of reviewed-approved standard-variable assets
- explicit cross-database governance for the most important semantics already encountered
- a clear and documented handoff into the next stage

In short:

This is the "method-repository foundation plus local standardization baseline" stage.

## Current-stage completion goals

The current stage is complete only if all of the following are true:

1. local architecture and workspace roles are clear enough that raw, local-work, public, shared, and archive materials are not conceptually mixed
2. the public repository is live, legible, GitHub-safe, and self-checking
3. the local standardization line has real reviewed-approved assets, not only plans and discovery notes
4. the most important database-specific semantic traps already encountered have been formally documented and cleaned enough to support current approved assets
5. the public repository clearly explains what it does and does not contain
6. the boundary between "current stage complete" and "next stage begins" is explicit

## Detailed completion checklist

### Workstream 1: Local architecture stabilization

#### Goal

Make the local workspace structure stable enough that ongoing work no longer depends on path ambiguity or mixed directory semantics.

#### Required outcomes

- `Methods/Clinical_Database/local_work` is the canonical local work surface for Layer 1-5 execution
- public repository material is separated from local restricted or patient-level outputs
- shared vs method-specific vs local-production script placement rules are explicitly documented
- data-retention and migration rules have already been clarified enough to prevent current-stage confusion

#### Review standard

This workstream is complete when:

- the main local-work root is no longer conceptually ambiguous
- public-safe material and local-only material are clearly separated
- the current directory interpretation can be explained without relying on oral memory

### Workstream 2: Public method-repository foundation

#### Goal

Make the public repository a coherent, publishable, reusable GitHub-safe method surface.

#### Required outcomes

- the GitHub repository exists and is published
- `README.md` and `docs/GETTING_STARTED.md` define the repository scope clearly
- database lineage/version/onboarding surfaces exist
- public workflow entrypoints exist
- release-safe manifest and public inventory exist
- public repository checks and CI smoke surfaces exist

#### Review standard

This workstream is complete when:

- a new reader can understand what the repository is for
- a new reader can identify supported databases and entrypoints
- the repository can check its own public surface automatically
- the repository does not publish restricted raw/local-only data by mistake

### Workstream 3: Real local standardization baseline

#### Goal

Show that the project has already moved beyond planning and contains real retained-variable assets.

#### Required outcomes

- at least one active core database has a substantial `reviewed_approved` Layer 5 baseline
- at least one additional database has a real pilot reviewed-approved baseline
- reviewed-approved status is tracked through a formal local index rather than memory alone
- current-stage claims are supported by actual assets rather than only framework language

#### Review standard

This workstream is complete when:

- reviewed-approved assets exist in meaningful quantity for at least one database
- the secondary database baseline is real enough to prove cross-database standardization is not hypothetical
- approval status can be checked from a formal index

### Workstream 4: Semantics and governance baseline

#### Goal

Lock down the most important semantics already required by the currently approved assets.

#### Required outcomes

- identifier normalization rules are explicit
- major time-semantics rules are explicit where needed
- current approved public cards do not contradict the local approved semantics
- at least one known semantic drift class has already been audited and cleaned

#### Review standard

This workstream is complete when:

- key semantic contracts exist for the databases already in active use
- approved assets are not relying on unresolved identity/grain ambiguity
- important cleaned fixes are documented rather than silently absorbed

### Workstream 5: Public/local boundary discipline

#### Goal

Make sure the repository ecosystem does not confuse method publication with restricted local execution evidence.

#### Required outcomes

- public cards expose only the GitHub-safe stable subset
- local knowledge packages remain the full execution-evidence surface
- release-safe governance explicitly excludes raw data, parquet copies, and patient-level Layer 2-5 outputs
- local-only execution details are not leaking into public publication surfaces beyond safe summaries

#### Review standard

This workstream is complete when:

- the public repository boundary is explicit in writing
- the release-safe manifest and inventory reflect that boundary
- public materials are useful without disclosing restricted local execution surfaces

### Workstream 6: Next-stage handoff clarity

#### Goal

Make the end of the current stage and the start of the next stage unambiguous.

#### Required outcomes

- the final target of the project is documented
- the current phase is explicitly described as not yet the full standard system
- the next phase is explicitly defined as the first machine-readable, executable, validated MVP closure
- the recommended next action is clear enough that the project does not drift back into vague expansion

#### Review standard

This workstream is complete when:

- a collaborator can explain both "what is already done" and "what still belongs to the next stage"
- the next phase begins with one governed MVP variable rather than uncontrolled breadth expansion

## Phase-exit interpretation rule

The current stage should be called complete when:

- the method-repository foundation is complete
- the local standardization baseline is real
- current key semantics are governed
- the public/local boundary is coherent
- the next-stage handoff is explicit

The current stage does **not** require:

- a full machine-executable standard system
- stable variable IDs and executable schemas for every variable
- the execution layer MVP to already exist
- ECHO retained-variable families to already be completed

Those belong to the next stage.

## Execution result against this standard

### Workstream 1 result: Complete

Evidence:

- the canonical local execution surface has been moved under `Methods/Clinical_Database/local_work`
- the public repository is separated under `Github/Clinical_Database`
- script-placement governance has already been formalized
- data migration and retention governance has already been documented and reviewed

### Workstream 2 result: Complete

Evidence:

- the public repository has been published to GitHub
- repository entry surfaces, onboarding, matrix, public workflow, release governance, inventory, and checks all exist
- public repository checks currently pass

### Workstream 3 result: Complete

Evidence:

- `MIMIC-IV-3.1` has a substantial reviewed-approved retained-variable baseline
- `AmsterdamUMCdb-1.0.2` has a real pilot reviewed-approved baseline
- the local Layer 5 master index formally tracks review status

### Workstream 4 result: Complete for current-stage scope

Evidence:

- identifier normalization has been formalized publicly
- Amsterdam time semantics are formally documented
- Amsterdam `admissionid -> stay_id` consistency drift has already been audited and cleaned for the currently affected approved assets
- public-card wording has already been brought back into alignment for the cleaned cases

Interpretation:

- this does not mean all future semantics problems are solved
- it means the semantics required for the current approved baseline have crossed the minimum governance threshold for this stage

### Workstream 5 result: Complete

Evidence:

- the public repository explicitly states what it does and does not contain
- release-safe manifest and public inventory exist and are checked
- raw data, parquet copies, and patient-level Layer 2-5 outputs remain outside the public release surface

### Workstream 6 result: Complete

Evidence:

- the final target and the next-stage transition are now formally documented in [`docs/STANDARD_SYSTEM_MATURITY_ROADMAP.md`](STANDARD_SYSTEM_MATURITY_ROADMAP.md)
- the project now clearly distinguishes:
  - current stage = method-repository foundation plus local standardization baseline
  - next stage = first governed standard-system MVP closure

## Formal verdict

Under this standard, the **current stage is complete**.

That verdict means:

- the foundation stage has been successfully closed
- the repository/workspace baseline is coherent enough to stop re-litigating basic architecture
- the next work should now move to the first true standard-system MVP rather than continuing indefinite foundation expansion

## What remains intentionally outside this stage

The following are important, but they are **not blockers for current-stage completion**:

- ECHO retained-variable family buildout
- broad backfill of machine-readable schemas across all existing approved variables
- first `run(variable_id, database_id, variable_version)` execution path
- first non-bypassable single-variable MVP closure
- future database family/version expansion beyond the current published baseline

## Next action after stage completion

The next action is:

- choose one pilot variable
- define its governed specs
- run it through a single standard execution path
- validate it
- bind it into a reproducibility manifest

That step begins the next stage.
