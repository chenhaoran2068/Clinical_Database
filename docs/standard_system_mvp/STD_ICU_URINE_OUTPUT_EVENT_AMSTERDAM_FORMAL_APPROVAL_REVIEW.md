# std_icu_urine_output_event Amsterdam Formal Approval Review

Last updated: 2026-04-25

## Review Verdict

Formal decision:

- approve `AmsterdamUMCdb-1.0.2` as a reviewed-approved implementation of `std_icu_urine_output_event`
- accept its public `mapping_spec_amsterdamumcdb_1_0_2.json`
- accept its governed execute-mode runtime evidence
- accept its rerun reproducibility evidence
- accept the cross-database public card update listing both `MIMIC-IV-3.1` and `AmsterdamUMCdb-1.0.2`

This approval is for the event-level urine-output stream only.

It does not approve:

- Amsterdam `std_first_day_urine_output_summary`
- urine-output rate
- intake-output balance
- all output events
- non-urine drains
- dialysis or CRRT removal
- silent broad inclusion of every Amsterdam `fluidout` row

## What Was Reviewed

Reviewed local Amsterdam evidence:

- `Methods/Clinical_Database/local_work/Layer 5/AmsterdamUMCdb-1.0.2/std_icu_urine_output_event/asset_manifest.md`
- `Methods/Clinical_Database/local_work/Layer 5/AmsterdamUMCdb-1.0.2/std_icu_urine_output_event/std_icu_urine_output_event_opening_review_20260425.md`
- `Methods/Clinical_Database/local_work/Layer 5/AmsterdamUMCdb-1.0.2/std_icu_urine_output_event/query_summary/std_icu_urine_output_event_source_audit_summary.json`
- `Methods/Clinical_Database/local_work/Layer 5/AmsterdamUMCdb-1.0.2/std_icu_urine_output_event/query_summary/std_icu_urine_output_event_quality_summary.json`
- `Methods/Clinical_Database/local_work/Layer 5/AmsterdamUMCdb-1.0.2/std_icu_urine_output_event/query_summary/std_icu_urine_output_event_approval_sensitive_source_rows.csv`
- `Methods/Clinical_Database/local_work/Layer 5/AmsterdamUMCdb-1.0.2/std_icu_urine_output_event/extract_code/Extract_Code_std_icu_urine_output_event.py`

Reviewed public governed evidence:

- `docs/standard_system_mvp/std_icu_urine_output_event/variable_spec.json`
- `docs/standard_system_mvp/std_icu_urine_output_event/mapping_spec_amsterdamumcdb_1_0_2.json`
- `docs/standard_system_mvp/std_icu_urine_output_event/execution.py`
- `docs/standard_system_mvp/std_icu_urine_output_event/runtime/amsterdamumcdb_1_0_2_first_real_execution/validation_report.json`
- `docs/standard_system_mvp/std_icu_urine_output_event/runtime/amsterdamumcdb_1_0_2_first_real_execution/manifest.json`
- `docs/standard_system_mvp/std_icu_urine_output_event/runtime/amsterdamumcdb_1_0_2_rerun_repro_check/validation_report.json`
- `docs/standard_system_mvp/std_icu_urine_output_event/runtime/amsterdamumcdb_1_0_2_rerun_repro_check/manifest.json`
- `docs/standard_system_mvp/std_icu_urine_output_event/runtime/amsterdamumcdb_1_0_2_rerun_repro_check/reproducibility_report.json`
- `docs/std_variable_cards/std_icu_urine_output_event.md`

Reviewed official/source context:

- AmsterdamUMCdb official repository scope
- AmsterdamUMCdb legacy `numericitems` source semantics
- AmsterdamUMCdb legacy dictionary urine-output item families
- MIMIC urine-output and first-day urine-output concepts as the cross-database boundary comparison

## Approved Source Boundary

Approved Amsterdam source itemids:

| itemid | source label | approved source meaning | route class | external anchor |
| --- | --- | --- | --- | --- |
| `8794` | `UrineCAD` | urine output from indwelling urinary catheter | `indwelling_urinary_catheter` | LOINC `9187-6` |
| `8796` | `UrineSupraPubis` | urine output from suprapubic catheter | `suprapubic_catheter` | LOINC `9187-6` |
| `8798` | `UrineSpontaan` | spontaneous urine output | `spontaneous_void` | LOINC `9197-5` |
| `8800` | `UrineIncontinentie` | urine output recorded under incontinence route | `incontinence` | LOINC `9187-6` |
| `8803` | `UrineUP` | urine output from urostomy | `urostomy` | LOINC `9187-6` |
| `10743` | `Nefrodrain li Uit` | urine output from left-sided nephrostomy | `left_nephrostomy` | LOINC `79549-2` |
| `10745` | `Nefrodrain re Uit` | urine output from right-sided nephrostomy | `right_nephrostomy` | LOINC `79549-2` |
| `19921` | `UrineSplint Li` | urine output from left-sided ureteral splint | `left_ureteral_splint` | LOINC `9187-6` |
| `19922` | `UrineSplint Re` | urine output from right-sided ureteral splint | `right_ureteral_splint` | LOINC `9187-6` |

Interpretation:

- these itemids are approved because the official dictionary and local hotset audit agree on urine-output semantics
- nephrostomy and ureteral-splint rows are included with explicit route/family flags rather than hidden inside a bladder-catheter-only concept
- the source-code lock is narrow by design and must not be replaced with a broad `fluidout` or `mL output` rule

## Same-Itemid Detail Audit

The source audit found:

- total hotset rows: `1,681,873`
- hotset row count matches manifest: `true`
- all included units are case-insensitive `mL`
- all included `unitid` values are `6`
- all included `islabresult` values are `0`
- all source rows have non-null `fluidout`
- all source rows have non-null `measuredat`
- all source rows have non-null `registeredat`
- `value` equals `fluidout` when both are present
- exact duplicate source rows: `0`
- audit problems: none

Interpretation:

- this specifically addresses the concern that equal `itemid` might hide important internal differences
- no structural fracture was detected across unit, dictionary count, lab flag, source value, timestamps, or duplicate behavior
- this does not mean every extreme numeric value is clinically valid; extreme values are handled by the cleaning rule below

## Build And Cleaning Summary

The reviewed-approved Amsterdam build reports:

- source component rows: `1,681,873`
- grouped event rows: `1,672,309`
- unique `subject_id`: `19,924`
- unique `stay_id`: `22,798`
- raw total urine output: `234,950,412.0 mL`
- cleaned approved total urine output: `226,262,072.0 mL`
- median approved event volume: `100.0 mL`
- p99 approved event volume: `500.0 mL`
- cleaned max single-event volume: `4,450.0 mL`
- raw max single-event volume: `6,352,410.0 mL`
- negative grouped event rows: `1`
- grouped event rows over `5,000 mL`: `4`
- hard-invalid excluded approved-value rows: `5`

Approved cleaning rule:

- retain the grouped raw value in `urine_output_ml_raw`
- set approved `urine_output_ml` to null when raw grouped value is `< 0` or `> 5,000 mL`
- set `cleaning_status = excluded_implausible_single_event_volume` for those rows
- keep those rows auditable rather than deleting them silently

Interpretation:

- the build is not pretending rare extreme values are normal
- it keeps source transparency and protects the approved standard value at the same time
- this is the right compromise for a first governed event-layer asset

## Runtime Evidence

First execute-mode runtime evidence:

- runtime directory: `docs/standard_system_mvp/std_icu_urine_output_event/runtime/amsterdamumcdb_1_0_2_first_real_execution/`
- process batch: `20260425T101123Z_AmsterdamUMCdb-1.0.2_std_icu_urine_output_event`
- validation status: `pass`
- subprocess return code: `0`
- primary output signature recorded: yes

Rerun reproducibility evidence:

- runtime directory: `docs/standard_system_mvp/std_icu_urine_output_event/runtime/amsterdamumcdb_1_0_2_rerun_repro_check/`
- process batch: `20260425T102006Z_AmsterdamUMCdb-1.0.2_std_icu_urine_output_event`
- reproducibility status: `pass`
- primary output asset is rerun-invariant by signature
- preview CSV is rerun-invariant by signature

Interpretation:

- this is not only a local script result
- the public governed runtime layer can show which spec, mapping, code path, output asset, validation report, and rerun report belong together
- the Amsterdam event layer can now serve as the upstream governed input for a later Amsterdam `std_first_day_urine_output_summary` build

## Official And Public Plausibility Interpretation

Official/source alignment is acceptable because:

- AmsterdamUMCdb is an ICU/HDU clinical database with local ICU/MC admission identifiers
- the official legacy dictionary exposes explicit urine-output rows in `mL`
- the approved source rows are narrow urine-output families rather than broad body-fluid output rows
- `admissionid` is normalized to the standard `stay_id` role under Amsterdam ICU/MC stay-equivalent semantics
- external anchors such as LOINC are used as orientation points, not as replacements for source-route approval

Public plausibility is acceptable because:

- the source volume distribution is dominated by clinically plausible urine-output event sizes
- the median and p99 approved event volumes are compatible with ICU event-level charting behavior
- the few extreme rows are not allowed into the approved value field
- the total event burden is consistent with a high-frequency ICU urine-output event stream

## Remaining Boundaries And Risks

Approved boundaries:

- event-level urine-output volume
- `mL`
- one grouped event per `stay_id + measuredat`
- Amsterdam `patientid` normalized to `subject_id`
- Amsterdam `admissionid` normalized to `stay_id`
- source component route/family provenance retained

Still not claimed:

- Amsterdam first-day urine-output summary
- Amsterdam urine-output rate
- Amsterdam all-output event foundation
- direct comparability of all urinary routes for every downstream analysis
- a GU-irrigant sign-flip analogue; no such analogue is included in this opening build

Risk handling:

- route heterogeneity is flagged, not hidden
- rare extreme values are raw-retained and approved-value-nullified
- any future newly identified irrigant or urine-like source must reopen this contract rather than be silently appended

## Approval Decision

The two requested approval points are accepted.

Approval point 1:

- the 9 Amsterdam candidate itemids pass source-boundary review
- no structural same-itemid fracture was found in the current evidence
- rare extreme values have an approved hard-valid cleaning rule

Approval point 2:

- the Amsterdam implementation is promoted to local `reviewed_approved`
- the public mapping spec is acceptable
- execute-mode runtime evidence is acceptable
- rerun reproducibility evidence is acceptable
- the public card may list Amsterdam as an approved implementation

Final status:

- `std_icu_urine_output_event` for `AmsterdamUMCdb-1.0.2`: `reviewed_approved`
- public mapping/runtime evidence: approved for publication
- next dependent step: build Amsterdam `std_first_day_urine_output_summary` from this approved event stream

## Source Pointers

Public official/source references:

- AmsterdamUMCdb official repository README: <https://github.com/AmsterdamUMC/AmsterdamUMCdb>
- AmsterdamUMCdb official `numericitems` wiki: <https://github.com/AmsterdamUMC/AmsterdamUMCdb/wiki/numericitems>
- AmsterdamUMCdb official legacy dictionary source: <https://raw.githubusercontent.com/AmsterdamUMC/AmsterdamUMCdb/master/amsterdamumcdb/dictionary/legacy/dictionary.csv>
- MIMIC official `urine_output.sql` concept: <https://raw.githubusercontent.com/MIT-LCP/mimic-code/main/mimic-iv/concepts_postgres/measurement/urine_output.sql>
- MIMIC official `first_day_urine_output.sql` concept: <https://raw.githubusercontent.com/MIT-LCP/mimic-code/main/mimic-iv/concepts_postgres/firstday/first_day_urine_output.sql>
