# Class 9 Microbiology Multi-Entity Family Rollout

Last updated: 2026-05-03

## Completion Meaning

In this repository, "Class 9 completed" means the microbiology multi-entity class is no longer only a conceptual bucket. It now has:

- a public Class 9 contract
- a reusable public MVP skeleton
- three concrete governed variable directories for the opening family
- `variable_spec.json`
- MIMIC mapping specs
- `execution.py`
- first execution runtime evidence
- rerun reproducibility evidence
- formal approval reviews for the parent, branch, and leaf entities

It does not mean every microbiology organism, ontology, antibiotic summary, infection phenotype, or every future database mapping has already been approved.

## Opening Governed Family

| Entity layer | Standard variable | Grain | MIMIC status | Runtime status |
| --- | --- | --- | --- | --- |
| Parent test event | `std_microbiology_test_event` | one specimen-test event | approved | first/rerun/repro pass |
| Organism branch | `std_microbiology_organism_isolate` | one specimen-test-organism branch | approved | first/rerun/repro pass |
| Susceptibility leaf | `std_microbiology_antibiotic_susceptibility` | one specimen-test-organism-antibiotic susceptibility row | approved | first/rerun/repro pass |

## Governed Artifacts

Class contract and skeleton:

- `Framework_Guideline/StandardVariableClass_MicrobiologyMultiEntityFamily_Contract.md`
- `docs/standard_system_mvp/variable_classes/microbiology_multi_entity_family/README.md`

Governed variable directories:

- `docs/standard_system_mvp/std_microbiology_test_event/`
- `docs/standard_system_mvp/std_microbiology_organism_isolate/`
- `docs/standard_system_mvp/std_microbiology_antibiotic_susceptibility/`

Formal reviews:

- `docs/standard_system_mvp/STD_MICROBIOLOGY_TEST_EVENT_MIMIC_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/STD_MICROBIOLOGY_ORGANISM_ISOLATE_MIMIC_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/STD_MICROBIOLOGY_ANTIBIOTIC_SUSCEPTIBILITY_MIMIC_FORMAL_APPROVAL_REVIEW.md`

## Runtime Evidence

| Variable | First process batch | Rerun process batch | Repro |
| --- | --- | --- | --- |
| `std_microbiology_test_event` | `20260502T154552Z_MIMIC-IV-3.1_std_microbiology_test_event` | `20260502T154803Z_MIMIC-IV-3.1_std_microbiology_test_event` | pass |
| `std_microbiology_organism_isolate` | `20260502T155017Z_MIMIC-IV-3.1_std_microbiology_organism_isolate` | `20260502T155225Z_MIMIC-IV-3.1_std_microbiology_organism_isolate` | pass |
| `std_microbiology_antibiotic_susceptibility` | `20260502T155441Z_MIMIC-IV-3.1_std_microbiology_antibiotic_susceptibility` | `20260502T155650Z_MIMIC-IV-3.1_std_microbiology_antibiotic_susceptibility` | pass |

## Content Integrity Closure

Post-execution direct parquet review found:

- parent test event rows: `1,562,787`
- organism branch rows: `306,613`
- susceptibility leaf rows: `1,314,671`
- duplicate parent event ids: `0`
- duplicate organism branch ids: `0`
- duplicate susceptibility source microevent ids: `0`
- organism rows missing parent event: `0`
- susceptibility rows missing parent event: `0`
- susceptibility rows missing parent organism branch: `0`
- parent organism-child flag alignment: `253,594` vs `253,594`
- parent susceptibility-child flag alignment: `117,722` vs `117,722`
- organism susceptibility-child count alignment: `139,153` vs `139,153`

## Boundary Rules

Class 9 is not Class 6, because the key problem is not only a finite text or ordinal value. The key problem is a hierarchy of test events, organism branches, and susceptibility leaves.

Class 9 is not Class 8, because the opening assets are not phenotype or score outputs. They are source-faithful microbiology entities with parent-child keys.

Do not collapse the opening family into one flat table unless a separate downstream analysis table is explicitly governed. The approved opening family keeps:

- parent `std_microbiology_test_event`
- child `std_microbiology_organism_isolate`
- leaf `std_microbiology_antibiotic_susceptibility`

## Near-Term Expansion Candidates

Possible Class 9 next steps:

- organism ontology harmonization as a separate derived/harmonized table
- blood-culture specific bacteremia candidate, after source hierarchy and contamination rules are proven
- infection phenotype links, but only under a Class 8 phenotype contract
- antibiotic exposure linkage, but only through Class 4 treatment event streams or a governed bridge
- Amsterdam microbiology feasibility review, only after its source hierarchy can prove equivalent parent/branch/leaf semantics

## Bottom Line

Class 9 is now formally open and approved on MIMIC-IV-3.1 for the opening microbiology parent/branch/leaf family. Future databases must prove their microbiology source hierarchy before using the same names.
