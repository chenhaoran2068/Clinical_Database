# std_non_crrt_rrt_active Formal Approval Review

Last updated: 2026-05-02

## Approval Verdict

Formal decision:

- `std_non_crrt_rrt_active` is approved as a Class 3 `binary_state_episode` variable.
- The approved database is `MIMIC-IV-3.1`.
- The approved interpretation is positive-only non-CRRT renal replacement therapy active episodes.

Blocking-findings judgment:

- no blocking semantic finding remains
- no blocking mapping finding remains
- no blocking runtime-evidence finding remains
- no blocking reproducibility finding remains

This approval is bounded to the `MIMIC-IV-3.1` implementation described in this note.

## What This Approves

This review approves:

- public `variable_spec.json`
- public `mapping_spec_mimic_iv_3_1.json`
- governed `execution.py`
- first execute-mode runtime evidence
- rerun reproducibility evidence
- the non-CRRT child layer below `std_rrt_active`

The approved meaning is:

- one retained row per positive non-CRRT RRT active episode
- ICU-stay anchored
- retained value `std_non_crrt_rrt_active = true`
- explicit `support_starttime`
- explicit `support_endtime`
- explicit `support_duration_minutes`
- no false rows emitted

Absence of a retained row means no retained positive non-CRRT RRT episode under the approved source-evidence rule. It does not mean no RRT, no CRRT, no AKI, or no exact modality evidence.

## Source And Boundary

The approved MIMIC source foundation uses:

- `source_supplied_derived.rrt`
- `icu.procedureevents`
- trusted `subject_id` / `hadm_id` / `stay_id` mapping

The mapping locks:

- IHD active evidence
- peritoneal dialysis active evidence
- approved IHD and peritoneal procedure intervals
- reviewed non-CRRT ambiguous evidence

The mapping explicitly excludes same-name approval for:

- umbrella any-RRT active state
- CRRT-family active state
- exact RRT modality episode detail
- RRT fluid-removal events
- first-day summaries or episode clips
- RRT-free-day outcomes
- AKI/KDIGO stage truth
- renal SOFA helper truth

Opening MIMIC v1 is IHD plus peritoneal dialysis for the non-CRRT parent. Hybrid or prolonged-intermittent modalities are not claimed as fully captured unless represented by the approved source labels.

## Internal Result Summary

The local reviewed-approved result reports:

- row count: `7,816`
- unique `stay_id`: `3,790`
- support duration minutes min / p50 / p90 / p95 / p99 / max: `240 / 308 / 1,440 / 3,019 / 8,316 / 29,618`
- episodes per stay min / p50 / p90 / p95 / p99 / max: `1 / 1 / 4 / 6 / 11 / 52`
- short episodes `<=60m`: `0`
- prolonged episodes `>=7d`: `55`
- support starts before ICU intime: `47`
- support ends after ICU outtime: `721`

## Governed Runtime Evidence

First execute-mode runtime evidence:

- runtime directory: `docs/standard_system_mvp/std_non_crrt_rrt_active/runtime/mimic_iv_3_1_first_real_execution/`
- process batch: `20260502T113938Z_MIMIC-IV-3.1_std_non_crrt_rrt_active`
- validation status: `pass`
- output row count: `7,816`

Rerun reproducibility evidence:

- runtime directory: `docs/standard_system_mvp/std_non_crrt_rrt_active/runtime/mimic_iv_3_1_rerun_repro_check/`
- process batch: `20260502T114242Z_MIMIC-IV-3.1_std_non_crrt_rrt_active`
- reproducibility status: `pass`

## Approval Conclusion

`std_non_crrt_rrt_active` is approved for `MIMIC-IV-3.1` as a governed Class 3 positive-only binary-state episode variable.

It is a child family layer below `std_rrt_active`, not a replacement for umbrella any-RRT active state or exact modality analysis.
