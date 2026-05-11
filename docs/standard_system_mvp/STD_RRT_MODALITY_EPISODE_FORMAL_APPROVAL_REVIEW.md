# std_rrt_modality_episode Formal Approval Review

Last updated: 2026-05-02

## Approval Verdict

Formal decision:

- `std_rrt_modality_episode` is approved as a Class 5 `episode_interval_bridge` variable.
- The approved database is `MIMIC-IV-3.1`.
- The approved interpretation is positive exact RRT modality episodes with governed labels and parent links.

Blocking-findings judgment:

- no blocking semantic finding remains
- no blocking mapping finding remains
- no blocking runtime-evidence finding remains
- no blocking reproducibility finding remains

This approval is bounded to the `MIMIC-IV-3.1` implementation described in this note.

## Why This Is Not Class 3

`std_rrt_modality_episode` is not a simple active flag.

It retains:

- positive interval timing
- `std_rrt_modality_episode = true`
- exact modality label in `std_rrt_exact_modality`
- family label in `std_rrt_family_class`
- parent links back to broader any-RRT and family episodes

That makes it an episode/modality bridge layer. It is therefore governed under the new Class 5 `episode_interval_bridge` skeleton rather than the Class 3 `binary_state_episode` skeleton.

## What This Approves

This review approves:

- public `variable_spec.json`
- public `mapping_spec_mimic_iv_3_1.json`
- governed `execution.py`
- first execute-mode runtime evidence
- rerun reproducibility evidence
- the first concrete governed Class 5 example

The approved exact modality label domain is:

- `CRRT`
- `CVVH`
- `CVVHD`
- `CVVHDF`
- `SCUF`
- `IHD`
- `Peritoneal`

Absence of a retained child row means no retained positive exact-modality episode under this source-label rule. It does not prove absence of umbrella RRT support, because unresolved active dialysis evidence can remain in `std_rrt_active` without being forced into a child label.

## Source And Boundary

The approved MIMIC source foundation uses:

- `source_supplied_derived.rrt`
- `source_supplied_derived.crrt`
- `icu.procedureevents`
- trusted `subject_id` / `hadm_id` / `stay_id` mapping

The mapping locks:

- typed official RRT modality points
- CRRT mode context points with exact modality labels
- approved exact dialysis procedure intervals
- exact labels `CRRT`, `CVVH`, `CVVHD`, `CVVHDF`, `SCUF`, `IHD`, and `Peritoneal`
- parent link rule `largest_positive_overlap_to_parent_support_episode`

The mapping explicitly excludes same-name approval for:

- umbrella any-RRT active state
- CRRT-family active state
- non-CRRT RRT active state
- RRT fluid-removal events
- first-day summaries or episode clips
- RRT-free-day outcomes
- AKI/KDIGO stage truth
- renal SOFA helper truth

## Internal Result Summary

The local reviewed-approved result reports:

- row count: `56,004`
- unique `stay_id`: `5,819`
- support duration minutes min / p50 / p90 / p95 / p99 / max: `1 / 240 / 1,103 / 1,811 / 4,144 / 29,618`
- episodes per stay min / p50 / p90 / p95 / p99 / max: `1 / 3 / 25 / 40 / 84 / 283`
- short episodes `<=60m`: `9,577`
- prolonged episodes `>=7d`: `75`
- support starts before ICU intime: `100`
- support ends after ICU outtime: `867`
- missing family parent link count among opening-family eligible rows: `0`

Exact modality mix:

- `CRRT`: `22,425`
- `CVVH`: `552`
- `CVVHD`: `668`
- `CVVHDF`: `24,517`
- `IHD`: `7,098`
- `Peritoneal`: `736`
- `SCUF`: `8`

## Governed Runtime Evidence

First execute-mode runtime evidence:

- runtime directory: `docs/standard_system_mvp/std_rrt_modality_episode/runtime/mimic_iv_3_1_first_real_execution/`
- process batch: `20260502T114546Z_MIMIC-IV-3.1_std_rrt_modality_episode`
- validation status: `pass`
- output row count: `56,004`

Rerun reproducibility evidence:

- runtime directory: `docs/standard_system_mvp/std_rrt_modality_episode/runtime/mimic_iv_3_1_rerun_repro_check/`
- process batch: `20260502T114848Z_MIMIC-IV-3.1_std_rrt_modality_episode`
- reproducibility status: `pass`

## Approval Conclusion

`std_rrt_modality_episode` is approved for `MIMIC-IV-3.1` as the first governed Class 5 episode-interval bridge variable.

It is the exact-modality child layer below `std_rrt_active`, not an umbrella active-state or family active-state replacement.
