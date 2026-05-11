# std_rrt_fluid_removal_event Amsterdam Formal Approval Review

Review date: 2026-05-02

Status: reviewed_approved_amsterdam_governed_class4_same_name_mapping

Database: `AmsterdamUMCdb-1.0.2`

Standard variable: `std_rrt_fluid_removal_event`

Variable class: `treatment_device_io_event_stream`

## Decision

AmsterdamUMCdb is approved for same-name `std_rrt_fluid_removal_event`.

The approved Amsterdam meaning is a source-recorded RRT fluid-removal event stream built from explicit `numericitems_event` removed-volume rows. The approval is source-event-primary: parent RRT support episodes are retained as context and caution evidence, but parent overlap is not a hard inclusion gate.

This approval does not approve rate settings, cumulative counters, dialysis access-line rows, RRT active flags, exact modality episodes, urine output, total ICU output, or hourly balance smoothing under the same variable identity.

## Governed Artifacts

Public governed files:

- `docs/standard_system_mvp/std_rrt_fluid_removal_event/variable_spec.json`
- `docs/standard_system_mvp/std_rrt_fluid_removal_event/mapping_spec_amsterdamumcdb_1_0_2.json`
- `docs/standard_system_mvp/std_rrt_fluid_removal_event/execution.py`
- `docs/standard_system_mvp/STD_RRT_FLUID_REMOVAL_EVENT_AMSTERDAM_PARENT_GAP_AUDIT_REVIEW.md`

Runtime evidence:

- first execution: `docs/standard_system_mvp/std_rrt_fluid_removal_event/runtime/amsterdamumcdb_1_0_2_first_real_execution/`
- rerun: `docs/standard_system_mvp/std_rrt_fluid_removal_event/runtime/amsterdamumcdb_1_0_2_rerun_repro_check/`
- reproducibility report: `docs/standard_system_mvp/std_rrt_fluid_removal_event/runtime/amsterdamumcdb_1_0_2_rerun_repro_check/reproducibility_report.json`

Runtime process batches:

- first execution: `20260502T131504Z_AmsterdamUMCdb-1.0.2_std_rrt_fluid_removal_event`
- rerun: `20260502T131511Z_AmsterdamUMCdb-1.0.2_std_rrt_fluid_removal_event`

Reproducibility status: `pass`.

## Approved Source Scope

Approved Amsterdam source rows:

| Source itemid | Source label | Unit | Approved role |
| --- | --- | --- | --- |
| `8805` | `CVVH Onttrokken` | `ml` | default bridge source-event evidence |
| `8806` | `Hemodialyse onttrekken` | `ml` | default bridge source-event evidence |

Approved event contexts:

| Event context | Rows | Stays | Volume ml |
| --- | ---: | ---: | ---: |
| `cvvh_removed_volume` | `98,383` | `941` | `14,994,976.0` |
| `hemodialysis_removed_volume` | `312` | `164` | `471,814.0` |

Total approved output:

- row count: `98,695`
- unique subjects: `937`
- unique stays: `1,019`
- total approved fluid-removed volume: `15,466,790.0 ml`
- bridge role: `default_balance_bridge_include`
- current status: `reviewed_approved`

## Parent Context

Parent-link status:

| Parent-link status | Rows |
| --- | ---: |
| `linked_to_approved_parent_episode` | `86,376` |
| `missing_expected_parent_episode_overlap` | `12,319` |

The `12,319` missing-parent rows were separately audited. The audit concluded that the gaps reflect parent active/episode coverage incompleteness, not source-item semantic contamination.

Approval interpretation:

- parent overlap is retained when available
- parent absence remains visible through `parent_link_status` and `parent_link_missing_caution_flag`
- missing parent overlap is not used to discard explicit source-recorded removal events

## Quality Cautions

Retained caution counts:

- negative-value caution rows: `6`
- extreme-value caution rows: `6`
- event-before-admission-anchor caution rows: `1`
- event-after-discharge caution rows: `1`

The negative and extreme rows are retained with caution flags instead of being silently dropped.

## Exclusion Boundary

This approval excludes:

- `8808 / Peritoneaaldialyse`
- `12091 / CVVH-Vochtverlies stand`
- `12454 / Vochtverlies ingesteld`
- `12463 / Onttrekken`
- `14849 / MFT_Ultrafiltratie (ingesteld)`
- `14851 / MFT_UF Totaal (ingesteld)`
- `20078 / MFT_Filtraatvolume_huidig`
- `20079 / MFT_Filtraatvolume_totaal`
- dialysis access-line rows
- peritoneal catheter rows
- RRT active flags
- exact RRT modality episodes
- urine output, total output, and fluid-balance summaries

Rate settings and cumulative/current machine counters require a separate governed derived rule before they can contribute to any downstream bridge.

## Approval Rationale

Amsterdam `8805` and `8806` are explicit source-recorded removed-volume rows in `ml`. Source `value` equals source `fluidout`, the labels are narrow, and the adjacent RRT/device/IO surface was reviewed enough to keep rate, counter, active-state, access-line, and modality-episode concepts outside this same-name variable.

The asset is approved because it preserves Class 4 event-stream semantics while keeping the parent-link weakness visible.

## Bottom Line

AmsterdamUMCdb is now a governed approved database mapping for `std_rrt_fluid_removal_event`, alongside MIMIC-IV-3.1. The next Amsterdam work should not reopen this same-name event approval; it should either build downstream bridge transformations or start a separate governed derivative for counter/rate device streams.
