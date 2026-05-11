# std_rrt_fluid_removal_event Amsterdam Parent-Gap Audit Review

Review date: 2026-05-02

Status: approval_ready_with_parent_context_caution_not_yet_promoted

Database: `AmsterdamUMCdb-1.0.2`

Standard variable: `std_rrt_fluid_removal_event`

## Question

This review audits the `12,319` Amsterdam candidate rows with `parent_link_status = missing_expected_parent_episode_overlap` and decides whether source itemids `8805` and `8806` are narrow enough to enter a formal Amsterdam same-name approval path.

It does not itself promote the Amsterdam runtime from candidate to approved. A formal promotion still requires an approved mapping-spec revision, an approved extraction status, first execution, rerun, reproducibility evidence, and a formal approval review.

## Decision

`8805 / CVVH Onttrokken` and `8806 / Hemodialyse onttrekken` are narrow enough to enter formal Amsterdam same-name approval for `std_rrt_fluid_removal_event`, provided the approval rule is source-event-primary:

- inclusion is driven by explicit source-recorded fluid-removal volume rows with unit `ml`
- approved parent RRT episodes are retained as context and caution support
- parent overlap is not required as a hard inclusion gate
- missing parent overlap remains visible through `parent_link_status` and `parent_link_missing_caution_flag`

If future governance requires every Amsterdam row to overlap a same-modality Class 3 parent episode, then this candidate is not approval-ready. That stricter policy would reject many source-explicit rows because current parent episode coverage is incomplete, especially for hemodialysis.

The recommended policy is source-event-primary. The same-name variable is a Class 4 event stream, not a Class 3 active flag or Class 5 modality episode.

## Source Narrowness

Raw `numericitems_event` audit:

| Itemid | Label | Tag | Unit | Rows | Value-fluidout mismatch rows | Min | P50 | Max |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| `8805` | `CVVH Onttrokken` | blank | `ml` | `97,518` | `0` | `-228.0` | `110.0` | `4565.0` |
| `8805` | `CVVH Onttrokken` | `NUL` | `ml` | `865` | `0` | `-3.0` | `50.0` | `2124.0` |
| `8806` | `Hemodialyse onttrekken` | blank | `ml` | `310` | `0` | `0.0` | `1500.0` | `4500.0` |
| `8806` | `Hemodialyse onttrekken` | `NUL` | `ml` | `2` | `0` | `2000.0` | `2250.0` | `2500.0` |

Interpretation:

- both included itemids have explicit removal labels, deterministic `ml` unit, and `fluidout` equal to the source numeric value for all rows
- the labels are substantially narrower than excluded adjacent rows such as rate settings, cumulative counters, access-line rows, active flags, or modality episodes
- negative values are rare and should remain source caution rows rather than silently disappearing

## Parent-Link Gap Summary

Candidate output:

- total candidate rows: `98,695`
- rows linked to approved same-modality parent episodes: `86,376`
- rows without expected parent overlap: `12,319`
- total candidate volume: `15,466,790.0 ml`

Gap share by source item:

| Itemid | Label | Total rows | Gap rows | Gap share | Total volume ml | Gap volume ml | Gap volume share |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `8805` | `CVVH Onttrokken` | `98,383` | `12,046` | `12.2%` | `14,994,976.0` | `1,568,265.0` | `10.5%` |
| `8806` | `Hemodialyse onttrekken` | `312` | `273` | `87.5%` | `471,814.0` | `404,594.0` | `85.8%` |
| combined | included Amsterdam candidate rows | `98,695` | `12,319` | `12.5%` | `15,466,790.0` | `1,972,859.0` | `12.8%` |

Gap position classes:

| Itemid | Event context | Gap position class | Rows | Stays | Volume ml |
| --- | --- | --- | ---: | ---: | ---: |
| `8805` | `cvvh_removed_volume_candidate` | `after_last_parent` | `266` | `92` | `45,944.0` |
| `8805` | `cvvh_removed_volume_candidate` | `before_first_parent` | `2,028` | `67` | `213,482.0` |
| `8805` | `cvvh_removed_volume_candidate` | `between_parent_episodes` | `1,965` | `357` | `228,115.0` |
| `8805` | `cvvh_removed_volume_candidate` | `no_same_modality_parent_in_stay` | `7,787` | `87` | `1,080,724.0` |
| `8806` | `hemodialysis_removed_volume_candidate` | `after_last_parent` | `25` | `13` | `51,130.0` |
| `8806` | `hemodialysis_removed_volume_candidate` | `before_first_parent` | `43` | `11` | `72,900.0` |
| `8806` | `hemodialysis_removed_volume_candidate` | `between_parent_episodes` | `2` | `2` | `4,500.0` |
| `8806` | `hemodialysis_removed_volume_candidate` | `no_same_modality_parent_in_stay` | `203` | `132` | `276,064.0` |

## Gap Interpretation

The `12,319` gaps do not indicate that `8805` or `8806` are broad or contaminated. They indicate that the current parent active/episode layers do not fully cover all explicit fluid-removal source rows.

Evidence:

- gap rows still retain narrow labels: `CVVH Onttrokken` or `Hemodialyse onttrekken`
- gap rows still retain unit `ml`
- source `value` equals source `fluidout` for both itemids
- most missing same-modality rows do not overlap the broader `std_rrt_active` umbrella either: only `1 / 12,046` missing `8805` rows and `16 / 273` missing `8806` rows overlap umbrella RRT active intervals
- therefore umbrella active linkage cannot rescue the gap; the source event row itself must be treated as the primary evidence if Amsterdam is approved

The hemodialysis item has weak parent overlap (`39 / 312` linked). This is a parent-context weakness, not an item-label weakness. It should remain visible in approval documentation and in output flags.

## Approval Readiness Boundary

Approval-ready under this rule:

- include `8805 / CVVH Onttrokken`
- include `8806 / Hemodialyse onttrekken`
- require source unit `ml`
- require explicit event-level source row from `numericitems_event`
- retain raw value and `fluid_removal_value_ml`
- retain `parent_link_status`
- keep negative and extreme caution flags
- continue excluding rate settings, cumulative counters, access lines, active flags, modality episodes, urine output, and total output

Not approval-ready under this rule:

- using parent overlap as a hard inclusion gate
- using `std_rrt_active`, `std_crrt_family_active`, `std_non_crrt_rrt_active`, or `std_rrt_modality_episode` as the same-name event numerator
- importing `12091`, `12454`, `12463`, `14849`, `14851`, `20078`, or `20079` as source-faithful removal amount events without a separate derived/counter rule
- suppressing the `12,319` missing-parent rows without explicit documentation

## Formal Promotion Requirements

Before Amsterdam can be formally approved, perform a separate promotion pass:

1. Revise `mapping_spec_amsterdamumcdb_1_0_2.json` from candidate to approved source-event-primary mapping.
2. Revise the local Amsterdam extraction status from `not_approved_bounded_candidate` to an approved status.
3. Rename candidate event contexts to approved event contexts or explicitly document why the candidate names remain versioned.
4. Set an approved bridge role policy, likely `default_balance_bridge_include` for the explicit removal-volume rows, while retaining numeric eligibility and caution flags.
5. Rerun first execution and reproducibility for Amsterdam under the approved mapping.
6. Write a formal Amsterdam approval review that cites this parent-gap audit.

## Bottom Line

The parent-link gap is no longer a source-item narrowness blocker. It is a parent-context completeness caution.

Amsterdam `8805` and `8806` can enter formal same-name approval if the approved identity remains a Class 4 source-recorded fluid-removal event stream with parent context optional but visible. They cannot enter approval under a parent-required Class 3/5 policy.
