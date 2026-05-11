# Variable Class Skeleton: Ordinal Text Semiquantitative Result

Last updated: 2026-05-02

## What This Class Is

`ordinal_text_semiquantitative_result` is Class 6. It covers result events where the retained value is a governed categorical or ordinal result rather than a continuous numeric measurement.

The first representative is:

- `std_nitrite_urinalysis_result`

Approved lateral expansions include:

- `std_protein_urinalysis_result`

## Required Semantic Locks

A variable in this class should explicitly lock:

- result concept
- target entity grain
- source item/code inclusion
- retained result domain
- normalization rule
- raw result retention
- no-row interpretation

## Minimum Files

Each governed variable in this class should provide:

- `variable_spec.json`
- `mapping_spec_<database>.json`
- `execution.py`
- first execution runtime evidence
- rerun reproducibility evidence
