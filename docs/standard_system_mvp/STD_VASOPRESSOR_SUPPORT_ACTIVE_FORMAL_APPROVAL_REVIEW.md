# std_vasopressor_support_active Formal Approval Review

Last updated: 2026-05-02

## Approval Verdict

Formal decision:

- `std_vasopressor_support_active` is approved as a Class 3 `binary_state_episode` variable.
- The approved database is `MIMIC-IV-3.1`.
- The approved interpretation is positive-only any vasopressor-capable support active episodes.

Blocking-findings judgment:

- no blocking semantic finding remains
- no blocking mapping finding remains
- no blocking runtime-evidence finding remains
- no blocking reproducibility finding remains

This approval is bounded to the `MIMIC-IV-3.1` implementation described in this note.

AmsterdamUMCdb same-name approval is recorded separately in `STD_VASOPRESSOR_SUPPORT_ACTIVE_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`.

## What This Approves

This review approves:

- public `variable_spec.json`
- public `mapping_spec_mimic_iv_3_1.json`
- governed `execution.py`
- first execute-mode runtime evidence
- rerun reproducibility evidence
- a vasopressor-support expansion of the Class 3 `binary_state_episode` class

The approved meaning is:

- one retained row per positive vasopressor-support active episode
- ICU-stay anchored
- retained value `std_vasopressor_support_active = true`
- explicit `support_starttime`
- explicit `support_endtime`
- explicit `support_duration_minutes`
- no false rows emitted

Absence of a retained row means:

- no retained positive vasopressor-support episode under the approved source-role rule

Absence of a retained row does not mean:

- universal proof of hemodynamic stability
- universal proof of no shock
- universal proof that all possible vasopressor evidence was absent
- approval of a negative-state grid

## Source And Boundary

The approved MIMIC source is the reviewed local upstream infusion foundation:

- `Methods/Clinical_Database/local_work/Layer 3/MIMIC-IV-3.1/medication/std_icu_vasoactive_medication_infusion_event/std_icu_vasoactive_medication_infusion_event_long.parquet`

The supporting stay anchor map is:

- `Methods/Clinical_Database/local_work/Layer 3/MIMIC-IV-3.1/id_mapping/std_id_map_subject_hadm_stay/std_id_map_subject_hadm_stay_long.parquet`

The mapping locks:

- source role field: `vasoactive_support_role_class`
- included role classes: `vasopressor`, `mixed_pressor_inotrope`
- required upstream eligibility: `vasoactive_rate_analysis_eligible = true`
- source start field: `source_vasoactive_course_starttime`
- source end field: `source_vasoactive_course_endtime`
- merge rule: merge overlapping or exactly contiguous eligible parent courses within stay
- target grain: one retained positive support episode row

The mapping explicitly excludes:

- pure `inotrope`
- pure `inodilator`
- agent-specific support episode detail
- norepinephrine-equivalent dose
- septic-shock phenotype
- vasopressor-free days

## Internal Result Summary

The local reviewed-approved result reports:

- row count: `71,270`
- unique `subject_id`: `22,899`
- unique `hadm_id`: `25,575`
- unique `stay_id`: `26,886`
- episodes per stay p50 / p90 / p99 / max: `2 / 5 / 16 / 76`
- support duration minutes min / p50 / p90 / p99 / max: `1 / 330 / 2,549 / 9,391 / 62,128`
- mixed pressor/inotrope episodes: `2,717`
- mixed pressor/inotrope only episodes: `1,461`
- pure vasopressor episodes: `69,809`
- concurrent-agent episodes: `11,023`
- short episodes `<=15m`: `2,920`
- prolonged episodes `>=7d`: `601`
- nonpositive duration rows: `0`
- missing relative timing rows: `0`

Interpretation:

- the result is a positive episode table, not a stay-level yes/no summary
- multiple episodes per stay are expected when positive gaps separate parent courses
- mixed pressor/inotrope rows are retained by design but explicitly flagged
- septic-shock analyses must add phenotype-specific criteria downstream

## Governed Runtime Evidence

First execute-mode runtime evidence:

- runtime directory: `docs/standard_system_mvp/std_vasopressor_support_active/runtime/mimic_iv_3_1_first_real_execution/`
- process batch: `20260502T090104Z_MIMIC-IV-3.1_std_vasopressor_support_active`
- validation status: `pass`
- output row count: `71,270`

Rerun reproducibility evidence:

- runtime directory: `docs/standard_system_mvp/std_vasopressor_support_active/runtime/mimic_iv_3_1_rerun_repro_check/`
- process batch: `20260502T090418Z_MIMIC-IV-3.1_std_vasopressor_support_active`
- reproducibility status: `pass`

The rerun reproduces the stable output artifacts and stable build-summary fields while allowing run-scoped process-batch identifiers and build logs to differ.

## What This Does Not Approve

This review does not approve:

- `std_vasopressor_support_agent_episode`
- norepinephrine-equivalent dose variables
- septic-shock onset variables
- vasopressor-free-day outcome variables
- pure inotrope support active
- per-minute vasopressor grids

Those require separate variable identities, mapping specs, runtime evidence, and review.

## Approval Conclusion

`std_vasopressor_support_active` is approved for `MIMIC-IV-3.1` as a governed Class 3 positive-only binary-state episode variable.

This closes the first non-respiratory Class 3 treatment-support active-state example and shows that the Class 3 skeleton can extend from respiratory support to medication-derived support states without collapsing into agent-specific, dose, or phenotype semantics.
