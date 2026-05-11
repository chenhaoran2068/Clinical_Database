# std_rrt_fluid_removal_event Formal Approval Review

Review date: 2026-05-02

Status: reviewed_approved_mimic_opening_governed_class4_mvp__amsterdam_approved_in_followup

Database: `MIMIC-IV-3.1`

Standard variable: `std_rrt_fluid_removal_event`

Variable class: `treatment_device_io_event_stream`

## Decision

`std_rrt_fluid_removal_event` is approved as the first governed Class 4 treatment/device/input-output event-stream MVP on `MIMIC-IV-3.1`.

The approved same-name meaning is a source-faithful RRT extracorporeal fluid-removal event stream with event time, value in `mL`, source context, bridge-role class, and parent support context where available.

This opening approval did not approve AmsterdamUMCdb at the time it was written. Amsterdam was later approved in `docs/standard_system_mvp/STD_RRT_FLUID_REMOVAL_EVENT_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`.

## Governed Artifacts

Public governed files:

- `docs/standard_system_mvp/variable_classes/treatment_device_io_event_stream/`
- `Framework_Guideline/StandardVariableClass_TreatmentDeviceIOEventStream_Contract.md`
- `docs/standard_system_mvp/std_rrt_fluid_removal_event/variable_spec.json`
- `docs/standard_system_mvp/std_rrt_fluid_removal_event/mapping_spec_mimic_iv_3_1.json`
- `docs/standard_system_mvp/std_rrt_fluid_removal_event/execution.py`

Runtime evidence:

- first execution: `docs/standard_system_mvp/std_rrt_fluid_removal_event/runtime/mimic_iv_3_1_first_real_execution/`
- rerun: `docs/standard_system_mvp/std_rrt_fluid_removal_event/runtime/mimic_iv_3_1_rerun_repro_check/`
- reproducibility report: `docs/standard_system_mvp/std_rrt_fluid_removal_event/runtime/mimic_iv_3_1_rerun_repro_check/reproducibility_report.json`

Runtime process batches:

- first execution: `20260502T125059Z_MIMIC-IV-3.1_std_rrt_fluid_removal_event`
- rerun: `20260502T125110Z_MIMIC-IV-3.1_std_rrt_fluid_removal_event`

The rerun reproducibility gate passed. The primary parquet and preview CSV signatures were invariant across reruns. Runtime build-summary comparison uses a small numeric tolerance for floating-point aggregates while retaining strict artifact signature checks.

## Source Scope

Approved MIMIC inputs:

- approved parent RRT umbrella: `std_rrt_active`
- approved CRRT parameter event stream: `std_crrt_device_parameter_event`
- approved non-CRRT support state: `std_non_crrt_rrt_active`
- selected ICU chartevents itemid split tables for hemodialysis and peritoneal dialysis context rows

Approved source rows:

| Source item | Source label | Unit | Approved role |
| --- | --- | --- | --- |
| `224191` | `Hourly Patient Fluid Removal` | `mL` | default bridge |
| `226499` | `Hemodialysis Output` | `mL` | default bridge |
| `226457` | `Ultrafiltrate Output` | `mL` | context only |
| `225806` | `Volume In (PD)` | `mL` | context only |
| `225807` | `Volume Out (PD)` | `mL` | context only |

## Output Validation

Approved output counts:

- row count: `702,910`
- unique ICU stays: `4,418`
- default bridge rows: `338,554`
- context-only rows: `364,356`
- negative-value caution rows: `1,240`
- extreme-value caution rows: `1,306`
- default bridge eligible volume: `130,066,286.79 ml`

Event-name counts:

| Standard event name | Rows |
| --- | ---: |
| `machine_hourly_patient_removal_volume` | `335,247` |
| `hemodialysis_output_volume` | `3,307` |
| `ultrafiltrate_output_volume_context` | `361,231` |
| `peritoneal_dialysis_volume_in_context` | `1,669` |
| `peritoneal_dialysis_volume_out_context` | `1,456` |

RRT family context:

- `crrt_family`: `696,478` rows
- `non_crrt_rrt`: `6,432` rows

## Boundary

Approved same-name inclusion:

- source-faithful RRT fluid-removal amount events
- standard unit `mL`
- default versus context-only bridge role
- source item and modality context
- parent support context where available

Excluded from this same-name approval:

- urine output
- total ICU output
- generic intake-output balance
- RRT active flags
- CRRT-family active flags
- non-CRRT active flags
- exact RRT modality episodes
- dialysis access-line status
- rate settings
- cumulative device counters
- hourly balance bridge rows
- first-day summaries
- AKI/KDIGO or renal SOFA phenotype truth

## Approval Rationale

The MIMIC source boundary is narrow, source items are explicit, units are deterministic, runtime evidence is governed, and rerun reproducibility passed.

The asset is approved because it preserves the necessary Class 4 event-stream semantics without pretending to be a Class 3 active flag, Class 5 exact modality episode, or Class 2 summary.

## Next Work

Amsterdam bounded candidate execution was later promoted after parent-link gap review. See `docs/standard_system_mvp/STD_RRT_FLUID_REMOVAL_EVENT_AMSTERDAM_PARENT_GAP_AUDIT_REVIEW.md` and `docs/standard_system_mvp/STD_RRT_FLUID_REMOVAL_EVENT_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`.
