# Variable Class Skeleton: Score Phenotype Composite Derived

Last updated: 2026-05-02

## What This Class Is

`score_phenotype_composite_derived` is Class 8. It covers score streams, score summaries, phenotype onsets, and other multi-component derived constructs.

The first representative is:

- `std_sofa`

Approved lateral expansions include:

- `std_oasis`

## Required Semantic Locks

A variable in this class should explicitly lock:

- score or phenotype identity
- target entity grain
- time basis
- component trace
- primary value rule
- no-row interpretation

## Minimum Files

Each governed variable in this class should provide:

- `variable_spec.json`
- `mapping_spec_<database>.json`
- `execution.py`
- first execution runtime evidence
- rerun reproducibility evidence
