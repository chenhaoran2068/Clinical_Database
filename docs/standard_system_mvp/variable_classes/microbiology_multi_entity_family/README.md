# Variable Class Skeleton: Microbiology Multi-Entity Family

Last updated: 2026-05-03

## What This Class Is

`microbiology_multi_entity_family` is Class 9. It covers microbiology assets where parent-child hierarchy is part of the variable meaning.

The opening governed family is:

- `std_microbiology_test_event`
- `std_microbiology_organism_isolate`
- `std_microbiology_antibiotic_susceptibility`

## Required Semantic Locks

A variable in this class should explicitly lock:

- microbiology entity role
- entity grain
- source hierarchy
- parent-child key rule
- raw text retention
- no-row interpretation
- exclusions from order-entry, antibiotic treatment, phenotype, and ontology-derived assets

## Minimum Files

Each governed variable in this class should provide:

- `variable_spec.json`
- `mapping_spec_<database>.json`
- `execution.py`
- first execution runtime evidence
- rerun reproducibility evidence
- a formal approval review

## Family Rule

The opening MIMIC implementation builds the three microbiology entities from one source table and one shared local builder. Even when one entity is executed, the sibling assets can be refreshed by the shared builder. Formal approval is still recorded separately per retained entity because each has a different target grain.
