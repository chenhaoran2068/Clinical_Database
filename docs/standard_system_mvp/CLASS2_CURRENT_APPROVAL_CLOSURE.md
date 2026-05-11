# Class-2 Current Approval Closure

Last updated: 2026-05-02

## Closure Verdict

Formal decision:

- Class 2, `baseline_summary_window_numeric`, is approved as a current-stage governed standard-system class.
- The current class now has approved representatives for all three intended summary subclasses:
- `duration_summary`
- `baseline_snapshot`
- `window_summary`

This is still a bounded approval.

It means:

- the class definition is stable enough for governed expansion
- the class has real machine-readable specs, mapping specs, governed execution, runtime evidence, rerun evidence, public cards, and formal review notes
- the current public class-2 surface correctly separates duration summaries, exact baseline snapshots, grouped/proxy baseline snapshots, and first-day window summaries

It does not mean:

- every future class-2 variable is already approved
- every class-2 subclass has already been fully industrialized across all databases
- Amsterdam is complete for all class-2 variables
- MIMIC-IV-3.1 class-2 batch expansion is complete

## What Was Reviewed

This closure reviewed the current public class-2 surface:

- `Framework_Guideline/StandardVariableClass_BaselineSummaryWindowNumeric_Contract.md`
- `docs/standard_system_mvp/variable_classes/baseline_summary_window_numeric/README.md`
- `docs/standard_system_mvp/CLASS2_FIRST_MVP_SELECTION.md`
- `docs/standard_system_mvp/STD_ICU_LOS_DAYS_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/STD_HOSPITAL_LOS_DAYS_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/STD_HOSPITAL_LOS_DAYS_AMSTERDAM_CANDIDATE_REVIEW.md`
- `docs/standard_system_mvp/CLASS2_NEXT_SMALL_CANDIDATE_SELECTION.md`
- `docs/standard_system_mvp/STD_DAYS_TO_NEXT_HOSPITAL_ADMISSION_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/AMSTERDAM_HOSPITAL_ADMISSION_BRIDGE_FEASIBILITY_REVIEW.md`
- `docs/standard_system_mvp/AMSTERDAM_NEXT_ICU_MCU_ADMISSION_DURATION_CANDIDATE_REVIEW.md`
- `docs/standard_system_mvp/STD_DAYS_TO_NEXT_ICU_ADMISSION_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/STD_DAYS_TO_NEXT_ICU_MCU_ADMISSION_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/STD_WEIGHT_ADMISSION_BASELINE_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/STD_WEIGHT_ICU_BASELINE_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/STD_WEIGHT_ADMISSION_BASELINE_AMSTERDAM_CANDIDATE_REVIEW.md`
- `docs/standard_system_mvp/STD_WEIGHT_ICU_BASELINE_GROUPED_PROXY_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/STD_FIRST_DAY_URINE_OUTPUT_SUMMARY_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/STD_FIRST_DAY_URINE_OUTPUT_SUMMARY_AMSTERDAM_CANDIDATE_REVIEW.md`
- `docs/standard_system_mvp/STD_FIRST_DAY_URINE_OUTPUT_SUMMARY_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/STD_BMI_ADMISSION_BASELINE_CANDIDATE_REVIEW.md`
- `docs/standard_system_mvp/STD_BMI_ICU_BASELINE_CANDIDATE_REVIEW.md`
- `docs/standard_system_mvp/STD_BMI_ADMISSION_BASELINE_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/STD_BMI_ICU_BASELINE_FORMAL_APPROVAL_REVIEW.md`
- the current class-2 variable specs, mapping specs, execution entrypoints, runtime manifests, validation reports, reproducibility reports, and public cards

This closure also reviewed official/public references for:

- MIMIC-IV v3.1 database scope and ICU/hospital timing concepts
- MIMIC ICU weight item-code context
- MIMIC official urine-output and first-day urine-output concept SQL
- MIMIC ICU output-event source context
- AmsterdamUMCdb ICU/HDU admission scope
- Amsterdam legacy `admissions` table semantics
- Amsterdam legacy `numericitems` and urine-output dictionary source context
- public plausibility references for ICU LOS, body weight distributions, and first-day urine-output interpretation

## Class-2 Meaning

Class 2 is not a database-specific category.

Class 2 means:

- baseline, first-day, window-summary, or duration numeric outputs
- one retained numeric row per anchor-qualified target entity
- not raw event-level output
- dependent on explicit anchor, window, selection, aggregation, and no-source-row rules

The class currently has three intended summary subclasses:

- `baseline_snapshot`
- `window_summary`
- `duration_summary`

## Current Class-2 Content

| Variable | Current status | Database coverage | Summary subclass | Current meaning |
| --- | --- | --- | --- | --- |
| `std_icu_los_days` | approved | `MIMIC-IV-3.1`, `AmsterdamUMCdb-1.0.2` | `duration_summary` | one ICU-stay or ICU-semantic stay-equivalent duration row in days |
| `std_hospital_los_days` | approved | `MIMIC-IV-3.1` only | `duration_summary` | one hospital-admission encounter duration row in days |
| `std_days_to_next_hospital_admission` | approved | `MIMIC-IV-3.1` only | `duration_summary` | one hospital-admission encounter row with nullable observed days from discharge to the first later different hospitalization |
| `std_days_to_next_icu_admission` | approved | `MIMIC-IV-3.1`, `AmsterdamUMCdb-1.0.2` | `duration_summary` | one ICU stay or ICU-semantic local-admission row with nullable observed days from ICU discharge to the first later ICU admission |
| `std_days_to_next_icu_mcu_admission` | approved | `AmsterdamUMCdb-1.0.2` only | `duration_summary` | one Amsterdam ICU/MCU local-admission row with nullable observed days from local discharge to the first later ICU/MCU local admission |
| `std_weight_admission_baseline` | approved | `MIMIC-IV-3.1` only | `baseline_snapshot` | one exact cleaned body-weight event selected inside a hospital-admission baseline window |
| `std_weight_icu_baseline` | approved | `MIMIC-IV-3.1` only | `baseline_snapshot` | one exact cleaned body-weight event selected inside an ICU-admission baseline window |
| `std_bmi_admission_baseline` | approved | `MIMIC-IV-3.1` only | `baseline_snapshot` derived numeric | one hospital-admission baseline BMI row derived from approved admission-baseline weight plus approved height |
| `std_bmi_icu_baseline` | approved | `MIMIC-IV-3.1` only | `baseline_snapshot` derived numeric | one ICU-stay baseline BMI row derived from approved ICU-baseline weight plus approved height |
| `std_weight_icu_baseline_grouped_proxy` | approved | `AmsterdamUMCdb-1.0.2` only | `baseline_snapshot` with grouped/proxy representation | one ICU/MCU local-admission grouped/proxy baseline body-weight row |
| `std_first_day_urine_output_summary` | approved | `MIMIC-IV-3.1`, `AmsterdamUMCdb-1.0.2` | `window_summary` | one ICU-stay or ICU-semantic stay-equivalent first-day urine-output total in mL with official-style NULL behavior |

## Current Candidate-Ready Assets

No Class 2 BMI candidate remains in candidate-only status after this update.

The two BMI variables previously listed here have now been promoted through public spec, MIMIC mapping, governed execution, runtime evidence, rerun evidence, and formal approval review.

Candidate-ready still does not mean approved as a general rule.

It means:

- the content boundary is acceptable
- the upstream dependency logic is acceptable
- no public-card metadata blocker remains
- the governed MVP hard chain is still missing

For `std_bmi_admission_baseline` and `std_bmi_icu_baseline`, that missing hard chain has now been added.

## LOS Duration Identity Rule

Current formal rule:

- `std_icu_los_days` is the first governed Class 2 representative variable and the first dual-database Class 2 MVP.
- `std_hospital_los_days` is not a replacement for `std_icu_los_days`; it is a sibling `duration_summary` variable at hospital-admission encounter grain.
- `std_icu_los_days` is approved for `MIMIC-IV-3.1` and `AmsterdamUMCdb-1.0.2`.
- `std_hospital_los_days` is currently approved for `MIMIC-IV-3.1` only.
- Amsterdam raw `admissionid` is governed under the current public ID contract as the ICU/MCU admission identifier normalized to `stay_id`, not `hadm_id`.
- Amsterdam should be added to `std_hospital_los_days` only if a true hospital-admission encounter layer with hospital admission and discharge boundaries is separately proven.
- If a future Amsterdam asset covers all ICU/MCU local admission duration including `MC`-only rows, it should be reviewed under a distinct variable identity rather than being forced into `std_hospital_los_days`.

Rejected same-name promotion:

- the Amsterdam local weight candidate was not approved as `std_weight_admission_baseline`
- it was split into `std_weight_icu_baseline_grouped_proxy`
- this preserves the difference between hospital-admission exact event baseline weight and Amsterdam ICU/MCU grouped/proxy baseline weight
- Amsterdam was also reviewed for same-name `std_hospital_los_days` and was not approved because the current Amsterdam evidence is ICU/MC or ICU-semantic stay duration rather than hospital-admission encounter duration

Newly approved same-name expansion:

- Amsterdam is now approved as `std_first_day_urine_output_summary`
- the upstream Amsterdam `std_icu_urine_output_event` prerequisite is built, reviewed-approved, and backed by governed execute/rerun evidence
- the Amsterdam summary-specific mapping, first-day window execution, NULL/zero behavior review, runtime evidence, and rerun evidence are now present
- the approval is bounded to ICU-semantic Amsterdam admissions: `IC`, `IC&MC`, and `MC&IC`
- `MC`-only admissions remain excluded from this same-name ICU summary

BMI governed-promotion update:

- `std_bmi_admission_baseline` and `std_bmi_icu_baseline` public cards no longer contain `########` review-date metadata
- both BMI variables have content-level candidate reviews
- both now have public variable specs, MIMIC mapping specs, governed execution entrypoints, execute/rerun runtime evidence, reproducibility reports, and formal approval reviews
- both are now included in the approved-current-assets table as MIMIC-only governed Class 2 derived baseline snapshots

Post-discharge observed follow-up duration update:

- `std_days_to_next_hospital_admission` was selected as the next small Class 2 candidate after BMI
- it now has a public variable spec, MIMIC mapping spec, governed execution entrypoint, execute/rerun runtime evidence, reproducibility report, and formal approval review
- the approval is MIMIC-only and keeps null semantics explicit: null means no later different hospitalization was observed in the captured MIMIC source snapshot, not zero days and not all-system absence of rehospitalization
- `AMSTERDAM_HOSPITAL_ADMISSION_BRIDGE_FEASIBILITY_REVIEW.md` now records that the current Amsterdam opening layer does not prove the required hospital-admission encounter bridge
- `AMSTERDAM_NEXT_ICU_MCU_ADMISSION_DURATION_CANDIDATE_REVIEW.md` records the safer Amsterdam follow-up path as local ICU/MCU admission timing, with MC-inclusive timing requiring a split identity such as `std_days_to_next_icu_mcu_admission`
- `std_days_to_next_icu_mcu_admission` has now been approved for Amsterdam as that split ICU/MCU local-admission duration identity, with governed execute/rerun evidence and explicit separation from both hospital readmission timing and ICU-only timing
- `std_days_to_next_icu_admission` has now also been approved for Amsterdam as the narrower same-name ICU-only local-admission duration identity, with governed execute/rerun evidence and explicit MC-only exclusion

## Full Content Interpretation

### `std_icu_los_days`

Current approved content:

- summary subclass: `duration_summary`
- target grain: ICU stay or ICU-semantic stay-equivalent
- canonical unit: `days`
- MIMIC retained rows: `94,458`
- MIMIC observed rows: `94,444`
- Amsterdam retained rows: `18,386`
- Amsterdam observed rows: `18,386`
- MIMIC runtime validation: pass
- Amsterdam runtime validation: pass
- MIMIC rerun reproducibility: pass
- Amsterdam rerun reproducibility: pass

Meaning:

- this is the class-2 proof that duration summaries belong in Class 2
- it is not raw event-level data
- it is not hospital length of stay
- it gives the first dual-database class-2 closure

### `std_hospital_los_days`

Current approved content:

- summary subclass: `duration_summary`
- target grain: hospital admission encounter
- canonical unit: `days`
- approved database: `MIMIC-IV-3.1`
- retained rows: `546,028`
- unique `hadm_id`: `546,028`
- nonnegative duration rows: `545,853`
- negative duration rows: `175`
- zero-duration rows: `5`
- raw minimum duration: `-0.9451388888888889` days
- raw maximum duration: `515.5625` days
- ICU-linked official audit comparable rows: `94,458`
- ICU-linked official audit mismatch rows: `0`
- runtime validation: pass
- rerun reproducibility: pass

Meaning:

- this is a hospital-admission encounter duration summary
- it is not ICU length of stay
- it is not the Amsterdam ICU/MC local admission duration currently represented by `std_icu_los_days`
- it is not subject-level follow-up time
- it computes duration from `admittime` to `dischtime`
- it keeps negative-duration source edge cases with `hospital_los_validity_status` instead of silently removing them
- it extends the Class 2 `duration_summary` proof beyond ICU-stay duration

### `std_days_to_next_hospital_admission`

Current approved content:

- summary subclass: `duration_summary`
- target grain: hospital admission encounter
- canonical unit: `days`
- approved database: `MIMIC-IV-3.1`
- retained rows: `546,028`
- unique `hadm_id`: `546,028`
- observed next-hospital-admission rows: `321,561`
- no later hospitalization observed rows: `224,467`
- minimum observed days: `0.001`
- median observed days: `85.111`
- p95 observed days: `1774.269`
- maximum observed days: `5340.54`
- MIMIC runtime validation: pass
- MIMIC rerun reproducibility: pass

Meaning:

- this is a post-discharge observed future-duration summary, not current-stay length of stay
- it extends Class 2 into observed follow-up duration while preserving explicit anchor, selection, aggregation, and null behavior
- it is not a 30-day readmission binary flag
- it is not all-system rehospitalization follow-up
- it does not approve Amsterdam same-name handling without a separate hospital-admission bridge

### `std_days_to_next_icu_admission`

Current approved content:

- summary subclass: `duration_summary`
- target grain: ICU stay or ICU-semantic local admission
- canonical unit: `days`
- approved databases: `MIMIC-IV-3.1`, `AmsterdamUMCdb-1.0.2`
- MIMIC retained rows: `94458`
- MIMIC observed next ICU admission rows: `29091`
- MIMIC no later ICU admission observed rows: `65353`
- Amsterdam retained ICU-semantic rows: `18386`
- Amsterdam observed next ICU admission rows: `1860`
- Amsterdam no later ICU admission observed rows: `16526`
- Amsterdam excluded MC-only rows: `4720`
- Amsterdam minimum observed days: `0.001`
- Amsterdam median observed days: `9.289`
- Amsterdam p95 observed days: `1609.622`
- Amsterdam maximum observed days: `4187.087`
- Amsterdam negative or zero observed duration rows: `0`
- Amsterdam runtime validation: pass
- Amsterdam rerun reproducibility: pass

Meaning:

- this is an ICU-only post-discharge observed future-duration summary
- it is not hospital readmission timing
- it is not a binary ICU readmission flag
- it is not all-system future critical-care follow-up
- Amsterdam same-name approval is bounded to ICU-semantic rows only: `IC`, `IC&MC`, and `MC&IC`
- Amsterdam MC-only rows remain excluded here and belong to the split ICU/MCU variable if retained

### `std_days_to_next_icu_mcu_admission`

Current approved content:

- summary subclass: `duration_summary`
- target grain: Amsterdam ICU/MCU local admission
- canonical unit: `days`
- approved database: `AmsterdamUMCdb-1.0.2`
- retained rows: `23,106`
- unique `subject_id`: `20,109`
- unique `stay_id`: `23,106`
- observed next ICU/MCU local admission rows: `2,967`
- no later ICU/MCU local admission observed rows: `20,139`
- minimum observed days: `0.001`
- median observed days: `12.838`
- p95 observed days: `1592.307`
- maximum observed days: `4531.061`
- Amsterdam runtime validation: pass
- Amsterdam rerun reproducibility: pass

Meaning:

- this is Amsterdam ICU/MCU local critical-care follow-up timing, not hospital readmission timing
- it intentionally includes MC-only rows and therefore uses a split identity rather than same-name `std_days_to_next_icu_admission`
- null means no later Amsterdam ICU/MCU local admission was observed after current local discharge, not zero days or all-system absence of future critical care
- `dateofdeath` is retained only as context flags, not as the primary ordering rule

### `std_weight_admission_baseline`

Current approved content:

- summary subclass: `baseline_snapshot`
- target grain: hospital admission encounter
- canonical unit: `kg`
- approved database: `MIMIC-IV-3.1`
- retained rows: `69,312`
- all-admission coverage: `69,312 / 546,028 = 0.126939`
- ICU-admission coverage: `69,312 / 85,242 = 0.81312`
- p25 / p50 / p75: `65.1 / 77.8 / 92.7 kg`
- runtime validation: pass
- rerun reproducibility: pass

Meaning:

- this is the first exact-event MIMIC baseline-snapshot example for Class 2
- it is hospital-admission anchored
- it is not an ICU-start baseline
- it is not generic patient-level stable weight
- it is not an Amsterdam grouped/proxy weight

### `std_weight_icu_baseline`

Current approved content:

- summary subclass: `baseline_snapshot`
- target grain: ICU stay
- canonical unit: `kg`
- approved database: `MIMIC-IV-3.1`
- retained rows: `88,690`
- all-ICU-stay coverage: `88,690 / 94,458 = 0.938936`
- selected `admission_weight_kg` rows: `65,549`
- selected `admission_weight_lbs` rows: `16,448`
- selected `daily_weight_kg` rows: `6,693`
- runtime validation: pass
- rerun reproducibility: pass

Meaning:

- this is the MIMIC ICU-admission-anchor sibling of `std_weight_admission_baseline`
- it is ICU-stay anchored, not hospital-admission anchored
- it is selected from cleaned exact event-level weight rows
- it is not an Amsterdam grouped/proxy weight
- it is not a patient-level stable body weight

### `std_weight_icu_baseline_grouped_proxy`

Current approved content:

- summary subclass: `baseline_snapshot`
- target grain: Amsterdam ICU/MCU local admission encounter
- canonical unit: `kg`
- approved database: `AmsterdamUMCdb-1.0.2`
- retained rows: `23,106`
- non-null baseline rows: `22,206`
- null baseline rows: `900`
- grouped-proxy rows: `22,160`
- repair-only event fallback rows: `46`
- p25 / p50 / p75: `70.0 / 74.5 / 84.5 kg`
- measured context rows: `1,771`
- anamnestic context rows: `10,235`
- estimated context rows: `6,142`
- unknown context rows: `4,958`
- runtime validation: pass
- rerun reproducibility: pass

Meaning:

- this is a useful Amsterdam baseline body-size variable
- it is transparent about grouped/proxy values
- it is not exact continuous measured weight
- it is not a same-name equivalent of `std_weight_admission_baseline`

### `std_first_day_urine_output_summary`

Current approved content:

- summary subclass: `window_summary`
- target grain: ICU stay or ICU-semantic stay-equivalent
- canonical unit: `mL`
- approved databases: `MIMIC-IV-3.1`, `AmsterdamUMCdb-1.0.2`
- MIMIC retained rows: `94,458`
- MIMIC stays with first-day urine output: `89,442`
- MIMIC stays without first-day urine output: `5,016`
- MIMIC complete 24-hour rows: `74,829`
- MIMIC partial-window rows: `19,629`
- MIMIC total first-day urine output: `152,814,080.4930113 mL`
- MIMIC median first-day urine output: `1,475.0 mL`
- MIMIC official reference row count: `94,458`
- MIMIC official reference non-null rows: `89,442`
- MIMIC official exact-match rows: `94,458`
- MIMIC official value-mismatch rows: `0`
- Amsterdam retained ICU-semantic rows: `18,386`
- Amsterdam excluded MC-only rows: `4,720`
- Amsterdam stays with first-day urine output: `18,115`
- Amsterdam stays without first-day urine output: `271`
- Amsterdam complete 24-hour rows: `11,074`
- Amsterdam partial-window rows: `7,312`
- Amsterdam total first-day urine output: `33,246,351.0 mL`
- Amsterdam median first-day urine output: `1,670.0 mL`
- Amsterdam hard-range violation rows: `0`
- MIMIC runtime validation: pass
- MIMIC rerun reproducibility: pass
- Amsterdam runtime validation: pass
- Amsterdam rerun reproducibility: pass

Meaning:

- this is the first governed Class-2 `window_summary` example
- it is an ICU-stay first-day total-output summary
- it preserves official MIMIC NULL behavior when there is no qualifying first-day urine row
- it is not raw urine-output events
- it is not intake-output balance
- it is not urine-output rate
- it is not zero-filled missingness
- it now has a bounded Amsterdam same-name approval for ICU-semantic admissions only

### `std_bmi_admission_baseline`

Current approved content:

- candidate subclass: `baseline_snapshot` derived numeric
- target grain: hospital admission encounter
- approved database: `MIMIC-IV-3.1` only
- upstream dependencies: `std_weight_admission_baseline` plus `std_height`
- formula: `weight_kg / (height_m ^ 2)`
- canonical unit: `kg/m^2`
- display precision: `round(2)`
- local retained rows: `55,501`
- upstream admission-baseline weight rows: `69,312`
- missing height rows after join: `13,811`
- outlier-flagged BMI rows: `38`
- latest local review date: `2026-04-01`

Meaning:

- this is a hospital-admission baseline BMI governed variable
- it inherits the admission anchor from `std_weight_admission_baseline`
- it inherits height availability limits from `std_height`
- it is not ICU-baseline BMI
- it is not patient-fixed lifetime BMI
- it is now governed-approved for MIMIC-IV-3.1 because public spec, mapping, execution, runtime, rerun, and formal review evidence have been added

### `std_bmi_icu_baseline`

Current approved content:

- candidate subclass: `baseline_snapshot` derived numeric
- target grain: ICU stay
- approved database: `MIMIC-IV-3.1` only
- upstream dependencies: `std_weight_icu_baseline` plus `std_height`
- formula: `weight_kg / (height_m ^ 2)`
- canonical unit: `kg/m^2`
- display precision: `round(2)`
- local retained rows: `73,432`
- upstream ICU-baseline weight rows: `88,690`
- missing height rows after join: `15,258`
- outlier-flagged BMI rows: `53`
- latest local review date: `2026-04-01`

Meaning:

- this is an ICU-baseline BMI governed variable
- it inherits the ICU anchor from `std_weight_icu_baseline`
- it inherits height availability limits from `std_height`
- it is not admission-baseline BMI
- it is not patient-fixed lifetime BMI
- it is now governed-approved for MIMIC-IV-3.1 because public spec, mapping, execution, runtime, rerun, and formal review evidence have been added

## Official-Source Alignment

### MIMIC-IV

Current alignment judgment: acceptable.

Official MIMIC-IV v3.1 context supports the current class-2 MIMIC mappings because:

- MIMIC-IV v3.1 reports `546,028` hospitalizations and `94,458` ICU stays
- MIMIC separates hospital `hosp` and ICU `icu` provenance
- ICU event tables link to `icustays` through `stay_id`
- `admittime` and `dischtime` define hospital-admission timing
- `intime` and `outtime` define unit timing; in `icustays`, the unit is always ICU
- the MIMIC FHIR `chartevents` item surface exposes the relevant ICU weight item family:
- `226512`: Admission Weight (Kg)
- `226531`: Admission Weight (lbs.)
- `224639`: Daily Weight
- the official MIMIC code surface includes `urine_output.sql` and `first_day_urine_output.sql`
- the current `std_first_day_urine_output_summary` output exactly matches the official first-day urine-output reference on all `94,458` rows

Interpretation:

- `std_icu_los_days` is aligned with ICU-stay timing semantics
- `std_hospital_los_days` is aligned with hospital-admission timing semantics and the official hospital-admission count
- `std_weight_admission_baseline` is aligned with hospital-admission timing and ICU charted weight source semantics
- `std_first_day_urine_output_summary` is aligned with official MIMIC first-day urine-output semantics

### AmsterdamUMCdb

Current alignment judgment: acceptable for currently approved Amsterdam class-2 assets.

Official AmsterdamUMCdb context supports the current Amsterdam class-2 mappings because:

- AmsterdamUMCdb contains ICU and high-dependency unit admission data
- the current repository README reports `23,106` admissions and `20,109` patients
- the legacy `admissions` table is described as admissions and demographic data for patients admitted to ICU or MCU
- `admissionid` is the unique local ICU admission identifier
- `lengthofstay` is recorded in hours
- `weightgroup` is categorized weight at admission in kg
- `weightsource` records whether weight was measured, estimated, or asked/anamnestic
- the legacy `numericitems` source has explicit urine-output rows in `mL`, including core urine, nephrostomy, and ureteral-splint candidates

Interpretation:

- Amsterdam `admissionid` is suitable as an ICU/MCU local admission or stay-equivalent key
- Amsterdam `weightgroup` is suitable for a grouped/proxy variable
- Amsterdam `weightgroup` is not suitable for silent same-name approval as exact continuous hospital-admission baseline weight
- Amsterdam `admissionid` and the current admitted/discharged offset duration evidence support ICU/MC or ICU-semantic stay duration, not same-name hospital-admission LOS
- Amsterdam `std_icu_urine_output_event` is now approved as the required upstream event layer
- Amsterdam first-day urine-output mapping is now approved after summary-specific governed execute/rerun evidence from the approved event layer
- Amsterdam `std_days_to_next_icu_admission` is now approved only for ICU-semantic local admissions and keeps MC-only rows out of the same-name variable

## Public Research Plausibility

Current plausibility judgment: acceptable.

### ICU LOS

The AmsterdamUMCdb publication reports:

- total admissions: `23,106`
- ICU admissions: `18,386`
- ICU length of stay median in the ICU subgroup: about `1.25` days

The current `std_icu_los_days` Amsterdam retained result has:

- `18,386` retained ICU-scope rows
- p50 `1.244` days

Interpretation:

- this strongly supports that the Amsterdam ICU LOS unit and scope are correct

For MIMIC:

- the current retained MIMIC ICU LOS median is `1.966` days
- public ICU LOS literature using MIMIC-IV commonly treats ICU LOS as the ICU admission-to-discharge interval for a stay-level episode

Interpretation:

- the MIMIC distribution is plausible and does not suggest an hours/days unit error

### Body Weight

A public MIMIC-IV cohort table reports MIMIC-IV weight around:

- training p25 / median / p75: `65.1 / 77.8 / 92.6 kg`
- testing p25 / median / p75: `66.0 / 78.5 / 93.3 kg`

The current `std_weight_admission_baseline` MIMIC retained result has:

- p25 / p50 / p75: `65.1 / 77.8 / 92.7 kg`

Interpretation:

- this strongly argues against pounds/kg inversion or major source-family mismatch

For Amsterdam grouped/proxy weight:

- p25 / p50 / p75: `70.0 / 74.5 / 84.5 kg`

Interpretation:

- these values are plausible for grouped adult ICU/MCU baseline body-size context
- the distribution should not be compared as exact continuous weight because it is shaped by bucket midpoints and boundary proxies

### First-Day Urine Output

The current `std_first_day_urine_output_summary` MIMIC retained result has:

- median first-day urine output: `1,475.0 mL`
- observed first-day urine output in `89,442 / 94,458` ICU stays
- exact agreement with the official MIMIC first-day urine-output reference

Interpretation:

- the strongest evidence is not only clinical plausibility but exact official-reference matching
- first-day urine-output total should not be confused with urine-output rate, KDIGO-style oliguria logic, or intake-output balance

## What Is Already Acceptable

The current class-2 surface is acceptable because:

- class contract exists
- class skeleton exists
- controlled summary subclasses exist
- all three intended subclasses now have current-stage governed representatives
- variable specs lock class, identity, semantic core, representation, and build-rule semantics
- mapping specs exist for every approved current database-variable pair
- governed `execution.py` exists for every approved current variable
- runtime manifests and validation reports exist
- rerun reproducibility reports exist
- public cards exist
- official-source alignment is documented
- public plausibility checks are documented
- the Amsterdam proxy-weight semantic split was made correctly instead of forcing false same-name harmonization
- the first-day urine-output summary preserves NULL semantics rather than silently zero-filling missing rows
- the Amsterdam first-day urine-output summary correctly uses the approved upstream event layer rather than rescanning raw numericitems
- `std_days_to_next_hospital_admission` keeps source-observed future-utilization scope explicit instead of turning nulls into zeros or all-system no-readmission claims
- `std_days_to_next_icu_admission` now keeps Amsterdam same-name comparability by excluding MC-only rows rather than silently broadening the ICU-only denominator

## Remaining Boundaries And Risks

The current class-2 closure still has important boundaries:

- Amsterdam is not approved for exact `std_weight_admission_baseline`
- Amsterdam is not approved for same-name `std_hospital_los_days` until a true hospital-admission encounter layer and hospital discharge boundary are proven
- Amsterdam is not approved for same-name `std_days_to_next_hospital_admission` until the same hospital-admission encounter bridge is proven
- Amsterdam ICU-only next-local-admission timing is approved under same-name `std_days_to_next_icu_admission`; MC-inclusive timing is approved only under split identity `std_days_to_next_icu_mcu_admission`
- MC-inclusive rows must not be silently attached to same-name `std_days_to_next_icu_admission`
- Amsterdam `std_first_day_urine_output_summary` is approved only for ICU-semantic admissions and does not include MC-only admissions
- MIMIC-IV-3.1 class-2 batch expansion is not complete
- Amsterdam class-2 backfill is not complete
- grouped/proxy variables require explicit downstream cautions for dose calculation, BMI calculation, and sensitivity analysis
- BMI baseline variables are approved for MIMIC-IV-3.1 only and remain unapproved for Amsterdam until compatible upstream exact weight and height evidence is separately governed
- first-day urine-output totals must not be reused as urine-output rate, intake-output balance, or zero-filled missing-output variables
- `std_sofa_first_day` should not be forced into Class 2 before deciding whether score/composite governance belongs to Class 8

## Fixes Required Now

No blocking fix is required before approving the current class-2 closure.

Recommended non-blocking maintenance:

- keep this closure note discoverable from the public README, Getting Started, MVP README, and release manifest
- keep Amsterdam same-name promotion decisions explicit rather than implied

## Next Execution Recommendation

After this closure, the current class-2 work should be read as:

1. treat `std_weight_icu_baseline` as the first completed post-closure MIMIC expansion
2. treat `std_hospital_los_days` as the second completed post-closure MIMIC expansion
3. treat BMI public metadata repair and candidate review as completed
4. treat `std_bmi_admission_baseline` and `std_bmi_icu_baseline` as completed governed MIMIC-IV-3.1 BMI promotions
5. treat `std_days_to_next_hospital_admission` as the completed next-small-candidate MIMIC Class 2 approval
6. treat `std_days_to_next_icu_mcu_admission` as the completed Amsterdam split-identity ICU/MCU follow-up duration approval
7. treat `std_days_to_next_icu_admission` as the completed Amsterdam same-name ICU-only follow-up duration approval

The detailed decision is recorded in:

- `docs/standard_system_mvp/CLASS2_TOTAL_CLOSURE_REVIEW_AND_MIMIC_EXPANSION_DECISION.md`
- `docs/standard_system_mvp/CLASS2_NEXT_SMALL_CANDIDATE_SELECTION.md`
- `docs/standard_system_mvp/STD_DAYS_TO_NEXT_ICU_ADMISSION_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`

Do not:

- force Amsterdam grouped/proxy variables into exact MIMIC variable identities
- treat this current closure as completion of all Class 2 work
- directly promote Amsterdam same-name `std_days_to_next_hospital_admission` before proving hospital-admission encounter boundaries
- promote Amsterdam MC-inclusive next ICU/MCU timing as same-name `std_days_to_next_icu_admission`
- treat no urine-output row as zero unless a separate variable identity explicitly approves that behavior

## Final Decision

Class 2 is approved as a current-stage governed class.

Approved current class-2 assets:

- `std_icu_los_days`
- `std_hospital_los_days`
- `std_days_to_next_hospital_admission`
- `std_days_to_next_icu_admission`
- `std_days_to_next_icu_mcu_admission`
- `std_weight_admission_baseline`
- `std_weight_icu_baseline`
- `std_bmi_admission_baseline`
- `std_bmi_icu_baseline`
- `std_weight_icu_baseline_grouped_proxy`
- `std_first_day_urine_output_summary`

Candidate-ready assets pending governed approval:

- none currently recorded in this closure

Current approval level:

- class-level current closure: approved
- subclass representation coverage: currently complete for the three intended subclasses
- full class-2 industrialization: not yet claimed
- next MIMIC-IV-3.1 expansion route: completed the first post-BMI small Class 2 candidate; any next candidate should again be scoped deliberately rather than inferred from quantity targets

## Source Pointers

Public official/source references used in this closure:

- MIMIC-IV v3.1 official dataset page: <https://physionet.org/content/mimiciv/3.1/>
- MIMIC-IV core concepts documentation: <https://lcp.mit.edu/mimic.mit.edu/docs/IV/about/concepts.html>
- MIMIC-IV ICU module documentation: <https://lcp.mit.edu/mimic.mit.edu/docs/IV/modules/icu/>
- MIMIC FHIR `chartevents` `d_items` code-system surface: <https://mimic.mit.edu/fhir/CodeSystem-mimic-chartevents-d-items.html>
- MIMIC FHIR `outputevents` `d_items` code-system surface: <https://mimic.mit.edu/fhir/CodeSystem-mimic-outputevents-d-items.html>
- MIMIC official `urine_output.sql` concept: <https://raw.githubusercontent.com/MIT-LCP/mimic-code/main/mimic-iv/concepts_postgres/measurement/urine_output.sql>
- MIMIC official `first_day_urine_output.sql` concept: <https://raw.githubusercontent.com/MIT-LCP/mimic-code/main/mimic-iv/concepts_postgres/firstday/first_day_urine_output.sql>
- AmsterdamUMCdb official repository README: <https://github.com/AmsterdamUMC/AmsterdamUMCdb>
- AmsterdamUMCdb official legacy `admissions` wiki: <https://github.com/AmsterdamUMC/AmsterdamUMCdb/wiki/admissions>
- AmsterdamUMCdb official `numericitems` wiki: <https://github.com/AmsterdamUMC/AmsterdamUMCdb/wiki/numericitems>
- AmsterdamUMCdb official legacy dictionary source: <https://raw.githubusercontent.com/AmsterdamUMC/AmsterdamUMCdb/master/amsterdamumcdb/dictionary/legacy/dictionary.csv>
- AmsterdamUMCdb official paper: <https://pmc.ncbi.nlm.nih.gov/articles/PMC8132908/>
- public MIMIC-IV cohort table with comparable weight distribution: <https://bmcmedinformdecismak.biomedcentral.com/articles/10.1186/s12911-024-02807-6/tables/1>
