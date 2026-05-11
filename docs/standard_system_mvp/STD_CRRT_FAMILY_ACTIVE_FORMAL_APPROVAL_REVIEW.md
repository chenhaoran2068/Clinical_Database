# std_crrt_family_active Formal Approval Review

Last updated: 2026-05-02

## Approval Verdict

Formal decision:

- `std_crrt_family_active` is approved as a Class 3 `binary_state_episode` variable.
- The approved database is `MIMIC-IV-3.1`.
- The approved interpretation is positive-only CRRT-family renal replacement therapy active episodes.

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
- the CRRT-family child layer below `std_rrt_active`

The approved meaning is:

- one retained row per positive CRRT-family active episode
- ICU-stay anchored
- retained value `std_crrt_family_active = true`
- explicit `support_starttime`
- explicit `support_endtime`
- explicit `support_duration_minutes`
- no false rows emitted

Absence of a retained row means no retained positive CRRT-family episode under the approved source-evidence rule. It does not mean no RRT, no AKI, or no exact modality evidence.

## Source And Boundary

The approved MIMIC source foundation uses:

- `source_supplied_derived.rrt`
- `source_supplied_derived.crrt`
- `icu.procedureevents`
- trusted `subject_id` / `hadm_id` / `stay_id` mapping

The mapping locks:

- generic CRRT active evidence
- CVVH, CVVHD, and CVVHDF exact continuous modality evidence
- official CRRT system-active context points
- approved CRRT-family dialysis procedure intervals
- reviewed CRRT-family ambiguous evidence

The mapping explicitly excludes same-name approval for:

- umbrella any-RRT active state
- non-CRRT RRT active state
- exact RRT modality episode detail
- RRT fluid-removal events
- first-day summaries or episode clips
- RRT-free-day outcomes
- AKI/KDIGO stage truth
- renal SOFA helper truth

Opening MIMIC v1 keeps SCUF visible in `std_rrt_modality_episode` but does not automatically promote isolated SCUF into this family parent.

## Internal Result Summary

The local reviewed-approved result reports:

- row count: `6,346`
- unique `stay_id`: `2,938`
- support duration minutes min / p50 / p90 / p95 / p99 / max: `1 / 2,610 / 8,674 / 11,547 / 19,103 / 44,966`
- episodes per stay min / p50 / p90 / p95 / p99 / max: `1 / 1 / 4 / 6 / 11 / 27`
- short episodes `<=60m`: `4`
- prolonged episodes `>=7d`: `458`
- support starts before ICU intime: `53`
- support ends after ICU outtime: `145`

## Governed Runtime Evidence

First execute-mode runtime evidence:

- runtime directory: `docs/standard_system_mvp/std_crrt_family_active/runtime/mimic_iv_3_1_first_real_execution/`
- process batch: `20260502T113331Z_MIMIC-IV-3.1_std_crrt_family_active`
- validation status: `pass`
- output row count: `6,346`

Rerun reproducibility evidence:

- runtime directory: `docs/standard_system_mvp/std_crrt_family_active/runtime/mimic_iv_3_1_rerun_repro_check/`
- process batch: `20260502T113634Z_MIMIC-IV-3.1_std_crrt_family_active`
- reproducibility status: `pass`

## Approval Conclusion

`std_crrt_family_active` is approved for `MIMIC-IV-3.1` as a governed Class 3 positive-only binary-state episode variable.

It is a child family layer below `std_rrt_active`, not a replacement for umbrella any-RRT active state or exact modality analysis.
