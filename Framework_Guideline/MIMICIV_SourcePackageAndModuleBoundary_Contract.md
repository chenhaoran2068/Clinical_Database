# MIMIC-IV Source Package And Module Boundary Contract

This contract records the highest-risk public semantics trap currently associated with `MIMIC-IV-3.1`.

The trap is not only a file-layout issue.
It is a provenance and scope issue.

## Core rule

- `MIMIC-IV-3.1` should be interpreted as the core database line staged from its own official source packages under the current Layer 1 conventions.
- `MIMIC-IV-ECHO-1.0` is a sibling module in the same family, not a semantic child of `MIMIC-IV-3.1`.
- a locally reconstructed note proxy is operationally usable for local ETL continuity, but it is not equivalent to an officially staged raw note delivery.

## Safe default interpretation

- treat `core`, `icu`, `ed`, and officially staged `note` material as the intended `MIMIC-IV-3.1` source-package scope
- keep ECHO material staged and governed as `MIMIC-IV-ECHO-1.0`
- if note work proceeds through the fallback path, keep that fact explicit in local provenance and do not silently upgrade it into an "official raw note" claim

## Prohibited interpretation

Do not assume any of the following by default:

- that ECHO files can be treated as part of `MIMIC-IV-3.1` simply because they are in the same family
- that a reconstructed note `csv.gz` proxy is equivalent to the official PhysioNet raw note package
- that a downstream retained-variable line built without official note delivery has the same source-package provenance as one built from officially staged note files

## Why this note exists

MIMIC already has broad retained-variable coverage in local work and public variable-card publication.

At that stage, unwritten memory about package boundaries becomes unsafe.

The main opening semantic trap is:

- confusing family relationship with package equivalence
- and confusing a local continuity fallback with official raw provenance

## Default implementation pattern

When writing public or local MIMIC-facing build notes:

1. name the database member explicitly as `MIMIC-IV-3.1` or `MIMIC-IV-ECHO-1.0`
2. state whether note input is an official staged delivery or a reconstructed fallback proxy
3. keep package provenance claims separate from downstream retained-variable approval claims

## Downstream consequence if violated

If this rule is ignored, the repository can silently overstate:

- source completeness
- raw-package provenance
- module equivalence
- cross-module comparability

That would weaken both reproducibility and later cross-database review.
