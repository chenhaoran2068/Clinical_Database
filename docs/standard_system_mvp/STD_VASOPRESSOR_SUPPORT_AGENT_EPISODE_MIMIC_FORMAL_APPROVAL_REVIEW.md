# std_vasopressor_support_agent_episode MIMIC Formal Approval Review

Review date: 2026-05-02

Status: reviewed_approved_mimic_governed_class5_lateral_expansion

Database: `MIMIC-IV-3.1`

Standard variable: `std_vasopressor_support_agent_episode`

Variable class: `episode_interval_bridge`

## Decision

MIMIC-IV-3.1 is approved for governed same-name `std_vasopressor_support_agent_episode`.

The approved meaning is a positive child episode interval for a specific retained vasoactive agent, linked back to the broader parent `std_vasopressor_support_active` episode. This approval preserves agent identity, child interval timing, parent support linkage, and strict concurrency flags.

This approval does not approve raw infusion events, any-support parent timing, vasopressor dose burden, norepinephrine-equivalent dose, septic shock phenotype, mortality risk, or primary-agent selection under this same variable identity.

## Governed Artifacts

Public governed files:

- `docs/standard_system_mvp/std_vasopressor_support_agent_episode/variable_spec.json`
- `docs/standard_system_mvp/std_vasopressor_support_agent_episode/mapping_spec_mimic_iv_3_1.json`
- `docs/standard_system_mvp/std_vasopressor_support_agent_episode/execution.py`
- `Framework_Guideline/StandardVariableClass_EpisodeIntervalBridge_Contract.md`

Runtime evidence:

- first execution: `docs/standard_system_mvp/std_vasopressor_support_agent_episode/runtime/mimic_iv_3_1_first_real_execution/`
- rerun: `docs/standard_system_mvp/std_vasopressor_support_agent_episode/runtime/mimic_iv_3_1_rerun_repro_check/`
- reproducibility report: `docs/standard_system_mvp/std_vasopressor_support_agent_episode/runtime/mimic_iv_3_1_rerun_repro_check/reproducibility_report.json`

Runtime process batches:

- first execution: `20260502T144113Z_MIMIC-IV-3.1_std_vasopressor_support_agent_episode`
- rerun: `20260502T144523Z_MIMIC-IV-3.1_std_vasopressor_support_agent_episode`

Reproducibility status: `pass`.

## Approved Source Scope

Approved MIMIC source foundation:

- direct source asset: `std_icu_vasoactive_medication_infusion_event`
- parent support asset: `std_vasopressor_support_active`
- supporting stay map: `std_id_map_subject_hadm_stay`
- conceptual official interval reference: `mimic-iv/concepts/medication/vasoactive_agent.sql`

Approved retained agent labels:

- `dopamine`
- `epinephrine`
- `norepinephrine`
- `phenylephrine`
- `vasopressin`

Opening v1 includes `mixed_pressor_inotrope` rows by design, but keeps their role class visible.

## Output Summary

First governed execution output:

- retained agent episodes: `96,606`
- unique ICU stays: `26,886`
- unique parent support episodes: `71,270`
- strict concurrent-other-agent episodes: `35,786`
- short agent episodes <=15 minutes: `3,879`
- prolonged agent episodes >=7 days: `638`

Agent distribution from reviewed local evidence:

| Agent | Episodes |
| --- | ---: |
| `dopamine` | `2,961` |
| `epinephrine` | `5,173` |
| `norepinephrine` | `43,798` |
| `phenylephrine` | `34,521` |
| `vasopressin` | `10,153` |

## Boundary Checks

Approved semantics:

- one row per `stay_id + std_vasoactive_agent + continuous child support episode`
- merge only overlapping or exactly contiguous intervals within the same agent
- require exactly one parent `std_vasopressor_support_active` episode by containment
- compute strict concurrency by positive time overlap with a distinct retained agent episode

Excluded semantics:

- parent any-support active timing
- raw medication infusion segments
- dose-rate event streams
- norepinephrine-equivalent transformation
- vasopressor burden summary
- shock phenotype or sepsis phenotype
- selecting one agent as the primary agent for a parent support episode

## Approval Rationale

The mapping is narrow enough for Class 5 because it has explicit start/end interval semantics, a governed retained label domain, same-agent continuity rules, parent-link requirements, and explicit no-row interpretation. It also surfaced and fixed a stale local dependency path before governed execution, after which first/rerun output reproduced exactly.

## Bottom Line

MIMIC-IV-3.1 is approved for `std_vasopressor_support_agent_episode` as the Class 5 lateral expansion beyond RRT modality episodes. Future database mappings must prove both agent identity and parent-support episode linkage before using this same name.
