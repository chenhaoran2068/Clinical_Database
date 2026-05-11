# std_rrt_fluid_removal_event Amsterdam Bounded Candidate Review

Review date: 2026-05-02

Status: historical_candidate_review_superseded_by_formal_approval

Database: `AmsterdamUMCdb-1.0.2`

Standard variable: `std_rrt_fluid_removal_event`

## Decision

This historical candidate review has been superseded by formal Amsterdam approval.

The original bounded candidate execution proved the source boundary. Formal approval now lives in `docs/standard_system_mvp/STD_RRT_FLUID_REMOVAL_EVENT_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`.

## Governed Candidate Runtime

Candidate public files:

- `docs/standard_system_mvp/std_rrt_fluid_removal_event/mapping_spec_amsterdamumcdb_1_0_2.json`
- `docs/standard_system_mvp/std_rrt_fluid_removal_event/execution.py`

Historical candidate runtime evidence was replaced by active approved runtime evidence:

- first approved execution: `docs/standard_system_mvp/std_rrt_fluid_removal_event/runtime/amsterdamumcdb_1_0_2_first_real_execution/`
- approved rerun: `docs/standard_system_mvp/std_rrt_fluid_removal_event/runtime/amsterdamumcdb_1_0_2_rerun_repro_check/`
- reproducibility report: `docs/standard_system_mvp/std_rrt_fluid_removal_event/runtime/amsterdamumcdb_1_0_2_rerun_repro_check/reproducibility_report.json`

Runtime process batches:

- first candidate execution: `20260502T124906Z_AmsterdamUMCdb-1.0.2_std_rrt_fluid_removal_event`
- candidate rerun: `20260502T124919Z_AmsterdamUMCdb-1.0.2_std_rrt_fluid_removal_event`

Approved reproducibility status: `pass`.

## Bounded Candidate Scope

Candidate default source rows:

| Itemid | Label | Unit | Rows | Stays | Candidate interpretation |
| --- | --- | --- | ---: | ---: | --- |
| `8805` | `CVVH Onttrokken` | `ml` | `98,383` | `941` | strongest CRRT/CVVH fluid-removal volume candidate |
| `8806` | `Hemodialyse onttrekken` | `ml` | `312` | `164` | strongest hemodialysis fluid-removal volume candidate |

Candidate context or excluded rows:

| Itemid | Label | Unit | Rows | Candidate action |
| --- | --- | --- | ---: | --- |
| `8808` | `Peritoneaaldialyse` | `ml` | `102` | retain as adjacent context only unless direction and treatment-active parent are proven |
| `12091` | `CVVH-Vochtverlies stand` | `ml` | `83,945` | exclude from default event stream; behaves like a device/status reading |
| `12454` | `Vochtverlies ingesteld` | `ml/uur` | `69,427` | exclude; rate setting |
| `12463` | `Onttrekken` | `ml/uur` | `10,374` | exclude; order/setting rate |
| `14849` | `MFT_Ultrafiltratie (ingesteld)` | `ml/uur` | `1,948,560` | exclude; one-minute machine setting/rate stream |
| `14851` | `MFT_UF Totaal (ingesteld)` | `ml` | `1,796,778` | exclude; setting/target-style total |
| `20078` | `MFT_Filtraatvolume_huidig` | `l` | `1,664,478` | exclude from default same-name event stream; one-minute current machine counter requiring differencing/reset logic |
| `20079` | `MFT_Filtraatvolume_totaal` | `l` | `1,664,541` | exclude from default same-name event stream; one-minute cumulative counter requiring differencing/reset logic |

## Parent-Context Signal

Overlap with already governed Amsterdam RRT parent intervals:

- `8805` rows overlapping `12465 / CVVH`: `86,337 / 98,383`
- `8806` rows overlapping `16363 / Hemodialyse`: `39 / 312`
- `8808` rows overlapping `16352 / Peritoneaal catheter`: `12 / 102`

Interpretation:

- `8805` has strong CVVH parent support but still needs event execution and parent-link flags
- `8806` has a narrow label but weak overlap with current Hemodialyse process intervals, so missing-parent flags must be retained
- `8808` is not enough for default same-name fluid-removal approval because the label does not prove output direction and the parent evidence is catheter/access-oriented rather than treatment-active

## Candidate Execution Result

Bounded candidate output:

- row count: `98,695`
- unique subjects: `937`
- unique stays: `1,019`
- `8805 / CVVH Onttrokken`: `98,383` rows
- `8806 / Hemodialyse onttrekken`: `312` rows
- rows with expected approved parent link: `86,376`
- rows without expected parent overlap: `12,319`
- negative-value caution rows: `6`
- extreme-value caution rows: `6`
- event-before-admission-anchor caution rows: `1`
- event-after-discharge caution rows: `1`
- total candidate fluid-removed volume: `15,466,790.0 ml`

Candidate volume by source context:

| Candidate event context | Rows | Volume ml |
| --- | ---: | ---: |
| `cvvh_removed_volume_candidate` | `98,383` | `14,994,976.0` |
| `hemodialysis_removed_volume_candidate` | `312` | `471,814.0` |

Parent-link status:

| Parent-link status | Rows |
| --- | ---: |
| `linked_to_approved_parent_episode` | `86,376` |
| `missing_expected_parent_episode_overlap` | `12,319` |

## Required Candidate Output Shape

The bounded candidate should emit an event stream shaped like:

- `subject_id` or Amsterdam patient identifier when available
- `stay_id` or Amsterdam `admissionid`
- `charttime` or relative event minute
- `fluid_removed_value`
- `unit`
- `standard_unit`
- `fluid_removed_value_ml`
- `source_modality_context`
- `source_itemid`
- `source_item_label`
- `parent_support_episode_id` when linked
- `parent_link_status`
- `bridge_role_class`
- caution flags for negative values, parent-link absence, and excluded adjacent source families

## Explicit Non-Approval Boundary

This review does not approve:

- Amsterdam same-name `std_rrt_fluid_removal_event`
- `12091` as a default event source
- any `ml/uur` rate setting as a removed-volume event
- `20078` or `20079` counter rows as source-faithful event amounts
- peritoneal dialysis rows as default removal without direction proof
- access lines or peritoneal catheter rows as fluid-removal events
- RRT active flags or modality episodes as fluid-removal events

## Candidate Execution Gate

The completed Amsterdam candidate execution satisfies the bounded execution gate:

1. includes `8805` and `8806`
2. excludes rate settings and machine counters from the default event numerator
3. carries parent-link status instead of dropping missing-parent rows silently
4. retains source labels and units
5. writes a candidate review after execution before any formal approval decision

## Bottom Line

Amsterdam now has a reproducible bounded candidate execution, but not formal same-name approval. The key blocker is not execution mechanics; it is approval semantics, especially the `12,319` rows without expected parent overlap and the need to decide whether `8805/8806` can become default same-name event evidence without importing adjacent rate, counter, access-line, active-flag, or modality-episode semantics.

Follow-up parent-gap audit and approval:

- `docs/standard_system_mvp/STD_RRT_FLUID_REMOVAL_EVENT_AMSTERDAM_PARENT_GAP_AUDIT_REVIEW.md`
- `docs/standard_system_mvp/STD_RRT_FLUID_REMOVAL_EVENT_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`
- conclusion: `8805 / CVVH Onttrokken` and `8806 / Hemodialyse onttrekken` are narrow enough to enter formal Amsterdam same-name approval under a source-event-primary rule, with parent links retained as context/caution rather than as a hard inclusion gate
- current Amsterdam status is now `reviewed_approved`
