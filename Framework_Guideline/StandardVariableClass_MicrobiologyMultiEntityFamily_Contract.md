# Standard Variable Class Contract: Microbiology Multi-Entity Family

Last updated: 2026-05-03

## Purpose

This contract defines Class 9 for microbiology assets whose meaning depends on a hierarchy of related entities rather than a single flat result row.

Microbiology needs a separate class because a source row can represent a specimen-test event, an organism branch, or an antibiotic-susceptibility leaf. Flattening those levels into one ordinary lab result can lose parent-child meaning, overcount organisms, or turn susceptibility rows into false culture positives.

## Applicability

This class applies when a variable:

- is part of a microbiology laboratory-result hierarchy
- has a governed entity role such as test event, organism branch, or susceptibility leaf
- retains parent-child keys across hierarchy levels
- preserves raw specimen, organism, antibiotic, interpretation, quantity, and comment text where relevant
- cannot be represented safely as a continuous numeric lab, ordinal urinalysis result, diagnosis code, or score phenotype

Typical examples:

- `std_microbiology_test_event`
- `std_microbiology_organism_isolate`
- `std_microbiology_antibiotic_susceptibility`

## Non-Applicability

Do not use this class for:

- ordinary numeric labs
- ordinal urinalysis or sediment result events
- diagnosis code events
- treatment antibiotic administration or prescription events
- suspected-infection or Sepsis-3 phenotype outputs
- organism ontology harmonization without retained source hierarchy

## Minimum Variable-Spec Rule

The `variable_spec.json` should lock:

- `variable_id`
- microbiology family role
- entity grain
- source hierarchy rule
- parent-child rule
- raw text retention rule
- no-row interpretation
- same-name boundary against orders, antibiotics, infection phenotype, and ontology-derived concepts

## Minimum Mapping-Spec Rule

The `mapping_spec_<database>.json` should lock:

- source table and source package
- source entity key fields
- source grain and target grain
- family role translation
- hierarchy translation
- parent-child translation
- raw text retention translation
- validation expectations

## Runtime-Evidence Rule

This class inherits:

- `Framework_Guideline/StandardSystem_RuntimeEvidence_Contract.md`

Formal governed runs should emit validation, manifest, and rerun reproducibility evidence.

## Current Public Skeleton

The public reusable skeleton lives under:

- `docs/standard_system_mvp/variable_classes/microbiology_multi_entity_family/`

The opening governed family is:

- `docs/standard_system_mvp/std_microbiology_test_event/`
- `docs/standard_system_mvp/std_microbiology_organism_isolate/`
- `docs/standard_system_mvp/std_microbiology_antibiotic_susceptibility/`
