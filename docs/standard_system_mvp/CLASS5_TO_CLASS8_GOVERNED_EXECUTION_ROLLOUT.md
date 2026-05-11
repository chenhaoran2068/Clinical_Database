# Class 5-8 Governed Execution Rollout

Last updated: 2026-05-02

## Completion Meaning

In this repository, "Class 5-8 completed" means the class is no longer only a verbal category. It now has:

- a public class contract
- a reusable public MVP skeleton
- at least one concrete governed variable directory
- `variable_spec.json`
- database mapping spec
- `execution.py`
- first execution runtime evidence
- rerun reproducibility evidence
- a formal approval review for the representative governed variable

It does not mean every possible variable in that class has already been mapped for every database.

## Current Representative Closure

| Class | Class id | Representative governed variable | Database status | Runtime status |
| --- | --- | --- | --- | --- |
| Class 5 | `episode_interval_bridge` | `std_rrt_modality_episode` | MIMIC and Amsterdam approved | first/rerun/repro pass |
| Class 6 | `ordinal_text_semiquantitative_result` | `std_nitrite_urinalysis_result` | MIMIC approved | first/rerun/repro pass |
| Class 7 | `diagnosis_admin_demographic_id_map` | `std_sex` | MIMIC approved | first/rerun/repro pass |
| Class 8 | `score_phenotype_composite_derived` | `std_sofa` | MIMIC approved | first/rerun/repro pass |

## First Lateral Expansion Batch

The first post-representative lateral expansion batch is complete:

| Class | Approved lateral variable | Database status | Runtime status | Formal review |
| --- | --- | --- | --- | --- |
| Class 5 | `std_vasopressor_support_agent_episode` | MIMIC approved | first/rerun/repro pass | `docs/standard_system_mvp/STD_VASOPRESSOR_SUPPORT_AGENT_EPISODE_MIMIC_FORMAL_APPROVAL_REVIEW.md` |
| Class 6 | `std_protein_urinalysis_result` | MIMIC approved | first/rerun/repro pass | `docs/standard_system_mvp/STD_PROTEIN_URINALYSIS_RESULT_MIMIC_FORMAL_APPROVAL_REVIEW.md` |
| Class 7 | `std_id_map_subject_hadm` | MIMIC approved | first/rerun/repro pass | `docs/standard_system_mvp/STD_ID_MAP_SUBJECT_HADM_MIMIC_FORMAL_APPROVAL_REVIEW.md` |
| Class 8 | `std_oasis` | MIMIC approved | first/rerun/repro pass | `docs/standard_system_mvp/STD_OASIS_MIMIC_FORMAL_APPROVAL_REVIEW.md` |

## Class 5: Episode / Interval / Bridge

Purpose: start-stop intervals, modality episodes, bridge intervals, and follow-up intervals.

Representative already open:

- `std_rrt_modality_episode`

Approved lateral expansion:

- `std_vasopressor_support_agent_episode`

Approved evidence:

- MIMIC first: `20260502T114546Z_MIMIC-IV-3.1_std_rrt_modality_episode`
- MIMIC rerun: `20260502T114848Z_MIMIC-IV-3.1_std_rrt_modality_episode`
- Amsterdam first: `20260502T112847Z_AmsterdamUMCdb-1.0.2_std_rrt_modality_episode`
- Amsterdam rerun: `20260502T112900Z_AmsterdamUMCdb-1.0.2_std_rrt_modality_episode`

Near-term expansion candidates:

- RRT support family episode
- ICU/hospital follow-up bridge
- 28-day outcome bridge
- treatment-free-day bridge after the underlying support episode is approved

Do not use Class 5 for simple active flags or point/event streams. If the record is a single measurement event, use Class 1, 4, or 6 depending on value semantics.

## Class 6: Ordinal / Text / Semiquantitative Result

Purpose: source-recorded finite-domain categorical or ordinal results that should not be forced into continuous numeric variables.

Representative approved:

- `std_nitrite_urinalysis_result`

Approved lateral expansion:

- `std_protein_urinalysis_result`

Approved evidence:

- first execution: `20260502T140255Z_MIMIC-IV-3.1_std_nitrite_urinalysis_result`
- rerun: `20260502T140319Z_MIMIC-IV-3.1_std_nitrite_urinalysis_result`
- formal review: `docs/standard_system_mvp/STD_NITRITE_URINALYSIS_RESULT_MIMIC_FORMAL_APPROVAL_REVIEW.md`

Near-term expansion candidates:

- `std_leukocyte_esterase_urinalysis_result`
- urine sediment bacteria result
- urine sediment casts result
- other semiquantitative lab flags with governed result domains

Key boundary rule: absence of a retained result row is not a negative result unless a separate source-specific no-row-as-negative rule is formally approved.

## Class 7: Diagnosis / Admin / Demographic / ID Map

Purpose: patient/admin categories, diagnosis-code events, and stable identifier maps.

Representative approved:

- `std_sex`

Approved lateral expansion:

- `std_id_map_subject_hadm`

Approved evidence:

- first execution: `20260502T140341Z_MIMIC-IV-3.1_std_sex`
- rerun: `20260502T140347Z_MIMIC-IV-3.1_std_sex`
- formal review: `docs/standard_system_mvp/STD_SEX_MIMIC_FORMAL_APPROVAL_REVIEW.md`

Near-term expansion candidates:

- race/ethnicity demographic category, if source semantics are narrow enough
- ICD diagnosis code event
- subject-hadm-stay ID map
- discharge disposition
- admission type/source administrative category

Key boundary rule: Class 7 variables must lock the identifier grain first. Do not silently expand a patient-level asset to admission or stay grain.

## Class 8: Score / Phenotype / Composite Derived

Purpose: multi-rule scores, phenotypes, onset definitions, and composite derived outputs.

Representative approved:

- `std_sofa`

Approved lateral expansion:

- `std_oasis`

Approved evidence:

- first execution: `20260502T140404Z_MIMIC-IV-3.1_std_sofa`
- rerun: `20260502T140817Z_MIMIC-IV-3.1_std_sofa`
- formal review: `docs/standard_system_mvp/STD_SOFA_MIMIC_FORMAL_APPROVAL_REVIEW.md`

Near-term expansion candidates:

- SAPSII
- AKI KDIGO stage or onset
- Sepsis-3 onset
- respiratory failure phenotype

Key boundary rule: score and phenotype variables must retain component trace or rule provenance. They should not be treated as raw source-event extraction.

## Execution Order Going Forward

Recommended order after this rollout:

1. Expand only one class at a time with a small candidate.
2. Prefer MIMIC first when the local evidence is already reviewed.
3. Promote Amsterdam only when its source semantics match the same-name rule.
4. If a source does not support the same name, create a split identity rather than forcing equivalence.
5. For every approved representative, require first execution, rerun, reproducibility report, and formal approval review.

## Boundary With Class 9

Class 9, microbiology multi-entity family, is now separately opened in `docs/standard_system_mvp/CLASS9_MICROBIOLOGY_MULTI_ENTITY_FAMILY_ROLLOUT.md`.

Do not squeeze organism/isolate/susceptibility relations into Class 6 or Class 8. Class 9 keeps its own multi-entity contract because the approved grain moves across parent test event, organism branch, and antibiotic susceptibility leaf rows.
