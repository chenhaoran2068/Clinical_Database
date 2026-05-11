# std_rrt_fluid_removal_event Feasibility Review

Review date: 2026-05-02

Status: historical_feasibility_review__mimic_and_amsterdam_now_governed_approved

Standard variable: `std_rrt_fluid_removal_event`

Candidate class: Class 4 treatment / device / input-output event stream

## Decision

`std_rrt_fluid_removal_event` should be handled as a Class 4 event-stream variable, not as another Class 3 active flag and not as a Class 5 modality episode.

MIMIC-IV already has a reviewed local event-stream asset that is strong enough to be the first governed Class 4 promotion candidate once the public Class 4 contract is opened.

AmsterdamUMCdb later completed the bounded candidate path and formal parent-gap review. It is now approved under a source-event-primary rule using explicit fluid-removal volume rows, while still excluding rate settings, cumulative machine counters, access lines, active flags, modality episodes, urine output, and total output.

## Target Event Contract

The opening same-name event stream should retain source-faithful fluid-removal records with enough context for downstream balance bridges without pretending to be whole-body fluid balance.

Minimum fields:

- `subject_id` or database-native patient identifier
- `hadm_id` when available
- `stay_id` or database-native ICU admission identifier
- `charttime` or source-relative event time
- `fluid_removed_value`
- `unit`
- `standard_unit`
- `fluid_removed_value_ml` when deterministic conversion is possible
- `source_modality_context`
- `source_itemid_set`
- `source_item_label_set`
- `source_unit_set`
- `bridge_role_class`
- `parent_support_episode_id` when a governed parent episode can be linked
- `source_parent_support_std_variable_id`
- caution flags for negative values, extreme values, parent-link absence, duplicate same-time candidates, and counter-derived values

The first governed version should keep event timestamps source-faithful. Back-shifting retrospective dialysis charting to earlier hours, smoothing end-of-session totals, and differencing machine counters are downstream modeling choices unless separately governed.

## MIMIC-IV Source Audit

Local reviewed asset:

- `Methods/Clinical_Database/local_work/Layer 5/MIMIC-IV-3.1/std_rrt_fluid_removal_event/`
- status: `reviewed_approved`
- row count: `702,910`
- unique ICU stays: `4,418`
- default bridge rows: `338,554`
- context-only rows: `364,356`
- default bridge eligible volume: `130,066,286.79 ml`

Approved local inputs:

- parent umbrella RRT: `std_rrt_active`
- CRRT parameter event stream: `std_crrt_device_parameter_event`
- non-CRRT active state: `std_non_crrt_rrt_active`

Retained source rows:

| Source item | Source label | Unit | Current role | Interpretation |
| --- | --- | --- | --- | --- |
| `224191` | `Hourly Patient Fluid Removal` | `mL` | default bridge | machine-side hourly patient removal volume |
| `226499` | `Hemodialysis Output` | `mL` | default bridge | intermittent hemodialysis output, often session-scale/end-charted |
| `226457` | `Ultrafiltrate Output` | `mL` | context only | specialized ultrafiltrate output context, not default total-removal truth |
| `225806` | `Volume In (PD)` | `mL` | context only | peritoneal dialysis input context |
| `225807` | `Volume Out (PD)` | `mL` | context only | peritoneal dialysis output context |

MIMIC unit and semantics:

- retained default bridge values are stored as `mL`
- `224191` is an hourly charted volume, not an `mL/hr` rate setting
- `226499` is a session-scale output volume, not a continuous hourly rate
- the local reviewed asset does not treat the default bridge as complete whole-body fluid balance
- `Ultrafiltrate Output` and peritoneal dialysis rows are intentionally retained as context-only in the opening version

Local quality counts:

- `machine_hourly_patient_removal_volume`: `335,247` rows
- `hemodialysis_output_volume`: `3,307` rows
- `ultrafiltrate_output_volume_context`: `361,231` rows
- `peritoneal_dialysis_volume_in_context`: `1,669` rows
- `peritoneal_dialysis_volume_out_context`: `1,456` rows
- negative-value caution rows: `1,240`
- extreme-value caution rows: `1,306`

MIMIC conclusion:

MIMIC is suitable for first governed Class 4 promotion after a Class 4 event-stream contract is opened. The governed version should initially preserve the local reviewed default/context split rather than expanding the numerator.

## AmsterdamUMCdb Source Audit

Reviewed Amsterdam source surface:

- numeric events: `Methods/Clinical_Database/local_work/Layer 2/AmsterdamUMCdb-1.0.2/reviewed_unsplit/numericitems_event.parquet`
- process intervals: `Methods/Clinical_Database/local_work/Layer 2/AmsterdamUMCdb-1.0.2/reviewed_unsplit/processitems_interval.parquet`
- item dictionary: `Methods/Clinical_Database/local_work/Layer 2/AmsterdamUMCdb-1.0.2/reviewed_unsplit/amsterdam_item_dictionary_legacy.parquet`

Process intervals already used for RRT parent context:

- `12465` / `CVVH`: governed `std_crrt_family_active`
- `16363` / `Hemodialyse`: governed source-bounded `std_non_crrt_rrt_active`
- `16352` / `Peritoneaal catheter`: access/catheter context, not active peritoneal dialysis treatment

Plausible volume-event candidates:

| Itemid | Label | Unit | Rows | Stays | Median value | Median gap | Current interpretation |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| `8805` | `CVVH Onttrokken` | `ml` | `98,383` | `941` | `110` | `60 min` | strongest Amsterdam CRRT fluid-removal volume candidate |
| `8806` | `Hemodialyse onttrekken` | `ml` | `312` | `164` | `1,500` | `2,430 min` | strongest Amsterdam hemodialysis removal volume candidate |
| `8808` | `Peritoneaaldialyse` | `ml` | `102` | `19` | `1,188.5` | `1,440 min` | RRT-adjacent but direction is not explicit enough for default removal |

Adjacent rows that should not be default same-name fluid-removal events:

| Itemid | Label | Unit | Rows | Reason |
| --- | --- | --- | ---: | --- |
| `12091` | `CVVH-Vochtverlies stand` | `ml` | `83,945` | machine/status reading; values can increase and decrease, so not a single source-faithful event amount |
| `12454` | `Vochtverlies ingesteld` | `ml/uur` | `69,427` | rate setting, not removed volume |
| `12463` | `Onttrekken` | `ml/uur` | `10,374` | order/setting rate, not removed volume |
| `14849` | `MFT_Ultrafiltratie (ingesteld)` | `ml/uur` | `1,948,560` | one-minute machine setting/rate stream |
| `14851` | `MFT_UF Totaal (ingesteld)` | `ml` | `1,796,778` | setting/target-style total, not actual fluid removed event |
| `20078` | `MFT_Filtraatvolume_huidig` | `l` | `1,664,478` | one-minute current machine counter; requires differencing and reset logic |
| `20079` | `MFT_Filtraatvolume_totaal` | `l` | `1,664,541` | one-minute cumulative/total machine counter; requires differencing and reset logic |

Amsterdam parent-overlap signal:

- `8805` rows overlapping `CVVH` process intervals: `86,337 / 98,383`
- `8806` rows overlapping `Hemodialyse` process intervals: `39 / 312`
- `8808` rows overlapping `Peritoneaal catheter` process intervals: `12 / 102`
- MFT/current-total filtrate counter rows overlap CVVH heavily, but their representation is counter/device-parameter evidence rather than source-faithful removed-volume events

Amsterdam unit and semantics:

- `8805`, `8806`, and `8808` are in `ml`
- `12454`, `12463`, and `14849` are in `ml/uur` and should remain rate-setting/device context
- `20078` and `20079` are in `l` and behave like one-minute machine counters; they are not directly equivalent to a single charted fluid-removal event
- `8805` is source-narrow enough to be a CRRT/CVVH removed-volume candidate
- `8806` is source-narrow enough to be a hemodialysis removed-volume candidate, but parent active overlap is incomplete and must be carried as a caution rather than hidden
- `8808` is too direction-ambiguous for default fluid-removal inclusion in opening governance

Amsterdam conclusion:

Amsterdam has now received same-name governed approval for `std_rrt_fluid_removal_event` after the bounded candidate execution and parent-gap audit. The approved route starts with `8805` and `8806`, retains parent-link flags, and keeps `8808`, `12091`, and MFT counter/rate rows outside the default event numerator.

## Exclusion Boundary

The same-name output must exclude:

- urine output
- total ICU output
- generic intake-output balance rows
- generic RRT active flags
- CRRT-family or non-CRRT-family active flags
- dialysis access-line rows
- peritoneal catheter rows unless separately proven as treatment events
- exact RRT modality episodes
- order/rate settings such as `ml/uur`
- cumulative machine counters unless a governed differencing/reset rule exists
- device pressures, flows, alarms, filter status, replacement-fluid settings, and anticoagulation settings
- plasma exchange unless a separate RRT/plasma-exchange boundary is approved

## Recommended Execution Order

1. Open the Class 4 `treatment_device_io_event_stream` public contract.
2. Promote MIMIC `std_rrt_fluid_removal_event` first, preserving the local reviewed source/default/context split.
3. Use that governed MIMIC build to lock the event-stream schema and validation gates.
4. Run a bounded Amsterdam candidate execution for `8805` and `8806` only.
5. Review Amsterdam parent-link absence, duplicate timestamps, negative values, and unit conversion before approval.
6. Consider a separate Amsterdam device-counter derivative later for `20078` and `20079`, but only with an explicit differencing and reset-detection rule.

## Bottom Line

This audit supported moving from Class 3 active-state work into a Class 4 event-stream variable. MIMIC and Amsterdam are now both governed approved mappings for `std_rrt_fluid_removal_event`; Amsterdam approval depends on the later parent-gap audit and formal approval review rather than on this initial feasibility review alone.
