# std_rrt_modality_episode Amsterdam Formal Approval Review

Review date: 2026-05-02

Status: reviewed_approved

Database: `AmsterdamUMCdb-1.0.2`

Standard variable: `std_rrt_modality_episode`

## Decision

AmsterdamUMCdb is approved for the same-name `std_rrt_modality_episode` asset as a Class 5 `episode_interval_bridge` variable.

The approved source boundary is:

- retain `processitems` itemid `12465 / CVVH` as exact modality label `CVVH`
- retain `processitems` itemid `16363 / Hemodialyse` as exact modality label `IHD`
- require non-null positive `start`, `stop`, and `duration`
- require `stop > start`
- merge overlapping or exactly contiguous intervals only within the same local admission and exact modality label
- link each child modality episode to the largest positive-overlap any-RRT parent and family parent

The raw Amsterdam `admissionid` is retained as the ICU/MC stay-equivalent `stay_id`, with `subject_id` populated from `admissions_core.patientid`.

## Source Boundary

The source audit found `5,413` approved source intervals:

- `12465 / CVVH`: `5,355`
- `16363 / Hemodialyse`: `58`

All `5,413` approved source intervals passed timing validity checks.

After exact-modality interval union, the approved output retains:

- output rows: `5,313`
- unique `subject_id`: `1,027`
- unique `stay_id`: `1,098`
- exact modality `CVVH`: `5,256`
- exact modality `IHD`: `57`
- family class `crrt_family`: `5,256`
- family class `non_crrt_rrt`: `57`
- missing any-RRT parent links: `0`
- missing family parent links: `0`

The following adjacent evidence is explicitly excluded from this same-name output:

- dialysis access-line rows
- peritoneal catheter rows
- plasma exchange rows
- CVVH orders and labs
- MFT/device-mode rows
- CVVH, Hemodialyse, and Peritoneaaldialyse fluid-removal or device measurements

This approval is for exact RRT modality episode truth for `CVVH` and `IHD` under Amsterdam processitems interval evidence. It does not approve umbrella active-state truth, family active-state truth, fluid-removal measurement, order truth, device parameter truth, or renal phenotype truth.

## Output Summary

- output rows: `5,313`
- unique `subject_id`: `1,027`
- unique `stay_id`: `1,098`
- short episodes less than or equal to 60 minutes: `183`
- prolonged episodes greater than or equal to 7 days: `4`
- duration minutes min / p50 / p90 / p95 / p99 / max: `4 / 1,482 / 4,320 / 4,483 / 6,734.72 / 13,344`

## Governed Evidence

Approved mapping spec:

- `docs/standard_system_mvp/std_rrt_modality_episode/mapping_spec_amsterdamumcdb_1_0_2.json`

Formal local implementation:

- `Methods/Clinical_Database/local_work/Layer 5/AmsterdamUMCdb-1.0.2/std_rrt_modality_episode/extract_code/Extract_Code_std_rrt_modality_episode.py`

Formal output:

- `Methods/Clinical_Database/local_work/Layer 3/AmsterdamUMCdb-1.0.2/treatment_state/std_rrt_modality_episode/std_rrt_modality_episode_long.parquet`

Governed runtime evidence:

- `docs/standard_system_mvp/std_rrt_modality_episode/runtime/amsterdamumcdb_1_0_2_first_real_execution/`
- `docs/standard_system_mvp/std_rrt_modality_episode/runtime/amsterdamumcdb_1_0_2_rerun_repro_check/`

Rerun reproducibility:

- `overall_status=pass`
- baseline process batch: `20260502T112847Z_AmsterdamUMCdb-1.0.2_std_rrt_modality_episode`
- rerun process batch: `20260502T112900Z_AmsterdamUMCdb-1.0.2_std_rrt_modality_episode`

## Conclusion

Amsterdam `processitems` rows for `CVVH` and `Hemodialyse` are narrow enough to serve as reviewed-approved same-name source evidence for `std_rrt_modality_episode` with exact labels `CVVH` and `IHD`, provided the documented parent-link and adjacent-source exclusions remain locked.
