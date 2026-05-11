# std_rrt_active Formal Approval Review

Last updated: 2026-05-02

## Approval Verdict

Formal decision:

- `std_rrt_active` is approved as a Class 3 `binary_state_episode` variable.
- The approved database is `MIMIC-IV-3.1`.
- The approved interpretation is positive-only any renal replacement therapy active episodes.

Blocking-findings judgment:

- no blocking semantic finding remains
- no blocking mapping finding remains
- no blocking runtime-evidence finding remains
- no blocking reproducibility finding remains

This approval is bounded to the `MIMIC-IV-3.1` implementation described in this note.

AmsterdamUMCdb same-name approval is handled in the later separate review `STD_RRT_ACTIVE_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`.

## What This Approves

This review approves:

- public `variable_spec.json`
- public `mapping_spec_mimic_iv_3_1.json`
- governed `execution.py`
- first execute-mode runtime evidence
- rerun reproducibility evidence
- an RRT-support expansion of the Class 3 `binary_state_episode` class

The approved meaning is:

- one retained row per positive any-RRT active episode
- ICU-stay anchored
- retained value `std_rrt_active = true`
- explicit `support_starttime`
- explicit `support_endtime`
- explicit `support_duration_minutes`
- no false rows emitted

Absence of a retained row means:

- no retained positive RRT episode under the approved source-evidence rule

Absence of a retained row does not mean:

- universal proof of no RRT
- universal proof of no AKI
- universal proof that all possible renal-support evidence was absent
- approval of a negative-state grid

## Source And Boundary

The approved MIMIC source foundation uses:

- `Methods/Clinical_Database/local_work/Layer 2/MIMIC-IV-3.1/reviewed_unsplit/source_supplied_derived/rrt.parquet`
- `Methods/Clinical_Database/local_work/Layer 2/MIMIC-IV-3.1/reviewed_unsplit/source_supplied_derived/crrt.parquet`
- `Methods/Clinical_Database/local_work/Layer 2/MIMIC-IV-3.1/reviewed_unsplit/icu_procedureevents.parquet`
- `Methods/Clinical_Database/local_work/Layer 3/MIMIC-IV-3.1/id_mapping/std_id_map_subject_hadm_stay/std_id_map_subject_hadm_stay_long.parquet`

The mapping locks:

- official broad RRT active evidence
- official CRRT system-active context evidence
- approved dialysis procedure intervals
- conservative unresolved active dialysis evidence for umbrella any-RRT truth
- target grain: one retained positive support episode row
- merge rule: merge overlapping or exactly contiguous approved any-RRT intervals within stay

The mapping explicitly excludes same-name approval for:

- `std_crrt_family_active`
- `std_non_crrt_rrt_active`
- `std_rrt_modality_episode`
- `std_rrt_fluid_removal_event`
- first-day RRT summaries or episode clips
- RRT-free-day outcomes
- AKI/KDIGO stage truth
- renal SOFA helper truth

## Internal Result Summary

The local reviewed-approved result reports:

- row count: `13,919`
- unique `stay_id`: `5,899`
- support duration minutes min / p50 / p90 / p95 / p99 / max: `120 / 480 / 6,050 / 8,919 / 16,606 / 44,966`
- episodes per stay min / p50 / p90 / p95 / p99 / max: `1 / 1 / 5 / 7 / 13 / 65`
- short episodes `<=60m`: `0`
- prolonged episodes `>=7d`: `538`
- support starts before ICU intime: `106`
- support ends after ICU outtime: `873`

Interpretation:

- the result is a positive episode table, not a stay-level yes/no summary
- multiple episodes per stay are expected when positive gaps separate retained support intervals
- unresolved active dialysis evidence is retained for umbrella any-RRT support truth but should not be used as exact modality truth
- modality-specific analyses should use the separate modality/family assets

## Governed Runtime Evidence

First execute-mode runtime evidence:

- runtime directory: `docs/standard_system_mvp/std_rrt_active/runtime/mimic_iv_3_1_first_real_execution/`
- process batch: `20260502T101955Z_MIMIC-IV-3.1_std_rrt_active`
- validation status: `pass`
- output row count: `13,919`

Rerun reproducibility evidence:

- runtime directory: `docs/standard_system_mvp/std_rrt_active/runtime/mimic_iv_3_1_rerun_repro_check/`
- process batch: `20260502T102259Z_MIMIC-IV-3.1_std_rrt_active`
- reproducibility status: `pass`

The rerun reproduces stable output artifacts and stable build-summary fields while allowing run-scoped process-batch identifiers and build logs to differ.

## What This Does Not Approve

This review does not approve:

- AmsterdamUMCdb same-name mapping under this MIMIC-specific decision
- CRRT-only support active
- non-CRRT support active
- exact RRT modality episodes
- RRT fluid-removal events
- first-day RRT summaries
- RRT-free-day outcomes
- AKI/KDIGO staging
- renal SOFA phenotype helpers

Those require separate variable identities, mapping specs, runtime evidence, and review.

## Approval Conclusion

`std_rrt_active` is approved for `MIMIC-IV-3.1` as a governed Class 3 positive-only binary-state episode variable.

This extends the Class 3 active-state skeleton from respiratory support and vasopressor support into renal replacement therapy while preserving the boundary between umbrella active-state truth and exact modality, device-parameter, fluid-removal, summary, outcome, and phenotype layers.
