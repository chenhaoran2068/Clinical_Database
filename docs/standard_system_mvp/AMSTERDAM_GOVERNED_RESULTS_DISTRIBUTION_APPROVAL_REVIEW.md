# Amsterdam Governed Results Distribution Approval Review

Last updated: 2026-04-28

## Formal Decision

The current governed Amsterdam result distributions have been reviewed and approved for the five Amsterdam variables that already have public governed runtime evidence.

Approved in this review:

- `std_heart_rate`
- `std_icu_los_days`
- `std_weight_icu_baseline_grouped_proxy`
- `std_icu_urine_output_event`
- `std_first_day_urine_output_summary`

This review confirms:

- internal result distributions are acceptable
- runtime validation evidence is acceptable
- rerun reproducibility evidence is acceptable
- official AmsterdamUMCdb source alignment is acceptable
- public clinical plausibility comparison is acceptable
- the existing approval boundaries remain required

This review does not newly approve:

- Amsterdam `std_hospital_los_days`
- Amsterdam `std_bmi_admission_baseline`
- Amsterdam `std_bmi_icu_baseline`
- Amsterdam exact same-name `std_weight_admission_baseline`
- Amsterdam exact same-name `std_weight_icu_baseline`

## Why This Review Exists

The individual Amsterdam approval notes already establish variable-level semantics, mapping, runtime evidence, and rerun evidence.

This additional review records the cross-variable distribution-level approval requested before treating the current Amsterdam governed results as accepted.

The review question is:

- after the variables have passed governed execution, do their actual result counts and distributions look internally coherent and externally plausible?

## Approved Scope

| Variable | Current Amsterdam status after this review | Result-distribution judgment | Boundary |
| --- | --- | --- | --- |
| `std_heart_rate` | approved | acceptable | event-level heart-rate stream only |
| `std_icu_los_days` | approved | acceptable | ICU-semantic stay duration, not hospital LOS |
| `std_weight_icu_baseline_grouped_proxy` | approved with proxy boundary | acceptable as grouped/proxy | not exact continuous measured weight |
| `std_icu_urine_output_event` | approved | acceptable | urine-output event layer only |
| `std_first_day_urine_output_summary` | approved | acceptable | ICU-semantic first-day urine-output summary only |

## Internal Runtime Evidence Summary

All five Amsterdam governed runtime directories report:

- first governed execution validation: `pass`
- rerun reproducibility: `pass`
- spec, mapping, execution path, output signature, and summary fields recorded

### `std_heart_rate`

Current Amsterdam governed result:

- total rows: `37,732,398`
- kept rows: `37,732,286`
- excluded outlier rows: `112`
- unique patients: `20,109`
- unique admissions/stays: `23,105`
- unit: `/min`
- kept p01 / p50 / p99: `49 / 86 / 135 bpm`
- kept mean: `87.076 bpm`
- kept maximum: `250 bpm`
- zero kept rows: `6,237`

Interpretation:

- the central distribution is clinically plausible for an ICU vital-sign event stream
- the outlier exclusion count is tiny relative to the total stream
- the retained range does not suggest a hidden unit conversion error
- zero heart-rate events remain a known edge case for future derived summaries, but are not a blocker for the current event-level asset

### `std_icu_los_days`

Current Amsterdam governed result:

- retained rows: `18,386`
- unique patients: `16,518`
- unique stays: `18,386`
- positive duration rows: `18,383`
- zero duration rows: `3`
- negative duration rows: `0`
- p01 / p50 / p99: `0.205 / 1.244 / 52.706 days`
- maximum: `237.366 days`

Interpretation:

- the denominator exactly matches the official Amsterdam ICU-admission count
- the median closely matches the official Amsterdam ICU LOS summary
- the distribution does not suggest an hours-versus-days error
- the approval remains ICU/stay-duration only, not hospital length of stay

### `std_weight_icu_baseline_grouped_proxy`

Current Amsterdam governed result:

- retained rows: `23,106`
- unique patients: `20,109`
- unique admissions: `23,106`
- non-null baseline rows: `22,206`
- null baseline rows: `900`
- grouped-proxy rows: `22,160`
- repair-only event fallback rows: `46`
- p25 / p50 / p75: `70.0 / 74.5 / 84.5 kg`
- measured context rows: `1,771`
- anamnestic context rows: `10,235`
- estimated context rows: `6,142`
- unknown context rows: `4,958`

Interpretation:

- the adult ICU/MCU baseline body-size distribution is plausible
- the distribution shape is expected because most values come from official grouped weight buckets
- this is approved only as a grouped/proxy variable
- it must not be treated as exact continuous body weight for precise dosing or BMI derivation without a separate approved rule

### `std_icu_urine_output_event`

Current Amsterdam governed result:

- source component rows: `1,681,873`
- grouped event rows: `1,672,309`
- unique patients: `19,924`
- unique stays: `22,798`
- total raw urine output: `234,950,412 mL`
- total approved urine output: `226,262,072 mL`
- median approved event volume: `100 mL`
- p99 approved event volume: `500 mL`
- maximum approved event volume: `4,450 mL`
- hard-invalid excluded approved-value rows: `5`

Same-itemid audit:

- all included units are `mL`
- all included `unitid` values are `6`
- all included `islabresult` values are `0`
- all source rows have non-null `fluidout`
- all source rows have non-null `measuredat`
- `value` equals `fluidout` when both are present
- exact duplicate source rows: `0`
- audit problems: none

Interpretation:

- the approved urine-output event stream is internally coherent
- the itemid lock does not hide a detected unit, lab-flag, timestamp, or value/fluidout fracture
- rare impossible raw values are retained for audit and excluded from the approved value field
- this approval remains event-layer urine output only, not urine-output rate or intake-output balance

### `std_first_day_urine_output_summary`

Current Amsterdam governed result:

- retained rows: `18,386`
- unique patients: `16,518`
- unique stays: `18,386`
- all Amsterdam admissions: `23,106`
- ICU-semantic target rows: `18,386`
- excluded MC-only rows: `4,720`
- stays with first-day urine output: `18,115`
- stays without first-day urine output: `271`
- first-day approved value rows: `286,024`
- first-day source excluded outlier rows: `1`
- complete 24-hour rows: `11,074`
- partial-window rows: `7,312`
- median first-day urine output: `1,670 mL`
- p25 / p75: `1,115 / 2,350 mL`
- maximum: `14,150 mL`
- hard-range violation rows: `0`

Interpretation:

- the ICU denominator exactly matches the official Amsterdam ICU-admission count
- the MC-only exclusion exactly matches the official MCU count
- first-day urine-output magnitude is clinically plausible
- missing first-day urine rows correctly remain `NULL`, not zero-filled
- this approval remains first-day total urine output only, not oliguria phenotype, urine-output rate, or intake-output balance

## Official AmsterdamUMCdb Alignment

The strongest official alignment points are:

- AmsterdamUMCdb official publication reports `20,109` patients and `23,106` admissions.
- The official publication reports `18,386` ICU admissions and `4,720` MCU admissions.
- The current Amsterdam `std_icu_los_days` denominator is `18,386`.
- The current Amsterdam `std_first_day_urine_output_summary` denominator is `18,386`.
- The current Amsterdam first-day urine-output build excludes `4,720` MC-only rows.
- The official Amsterdam ICU LOS median is about `1.25` days.
- The current Amsterdam `std_icu_los_days` median is `1.244` days.

Interpretation:

- the current ICU-semantic denominator is correct
- the ICU/MC boundary is not being silently mixed in the same-name ICU summaries
- the LOS unit and anchor are consistent with the official Amsterdam descriptive distribution

## Public Clinical Plausibility Alignment

Current plausibility judgment: acceptable.

Heart rate:

- retained p50 `86 bpm`, p95 `120 bpm`, and p99 `135 bpm` are plausible for ICU event-level monitoring
- the distribution is not consistent with a hidden seconds/minutes or unit-conversion error

ICU LOS:

- retained p50 `1.244 days` matches the Amsterdam official ICU subgroup median of about `1.25 days`
- p99 and maximum are long but plausible as extreme ICU stays after no negative-duration rows were found

First-day urine output:

- median `1,670 mL/day` and p25/p75 `1,115 / 2,350 mL/day` are plausible for adult ICU first-day urine output
- the values are above common oliguria-threshold scale for a typical adult, while still allowing low-output patients to exist
- this does not approve an oliguria phenotype; it only supports plausibility of the total-output summary

Weight grouped proxy:

- p25/p50/p75 `70.0 / 74.5 / 84.5 kg` is plausible for adult ICU/MCU body-size context
- the distribution must be interpreted as bucket-derived proxy values rather than exact measured weights

Urine-output events:

- median event volume `100 mL` and p99 `500 mL` are plausible for charted urine-output events
- a very small number of impossible raw values is handled by the hard-valid cleaning rule

## Approval Boundaries

The following boundaries remain active:

- Amsterdam `admissionid` is used under the standard `stay_id` role for ICU/MCU local admission or ICU-semantic stay-equivalent records.
- Amsterdam `std_icu_los_days` is not hospital length of stay.
- Amsterdam `std_first_day_urine_output_summary` excludes MC-only admissions.
- Amsterdam `std_first_day_urine_output_summary` keeps no-source stays as `NULL`, not zero.
- Amsterdam `std_weight_icu_baseline_grouped_proxy` is grouped/proxy and should not be silently used as exact measured weight.
- Amsterdam BMI variables remain unapproved until compatible exact weight/height upstream evidence is separately governed.
- Amsterdam same-name exact `std_weight_admission_baseline` and `std_weight_icu_baseline` remain unapproved.
- Amsterdam same-name `std_hospital_los_days` remains unapproved until true hospital-admission encounter boundaries are proven.

## Final Approval Statement

The current Amsterdam governed result distributions for the five scoped variables are approved.

No blocking result-distribution, official-alignment, public-plausibility, runtime-validation, or rerun-reproducibility finding remains for these scoped variables.

This approval strengthens the current Amsterdam pilot surface, but it does not make Amsterdam complete across all variable classes.

## Source Pointers

Public official/source references used in this review:

- AmsterdamUMCdb official repository README: <https://github.com/AmsterdamUMC/AmsterdamUMCdb>
- AmsterdamUMCdb official legacy `admissions` wiki: <https://github.com/AmsterdamUMC/AmsterdamUMCdb/wiki/admissions>
- AmsterdamUMCdb official `numericitems` wiki: <https://github.com/AmsterdamUMC/AmsterdamUMCdb/wiki/numericitems>
- AmsterdamUMCdb official paper: <https://pmc.ncbi.nlm.nih.gov/articles/PMC8132908/>
- KDIGO acute kidney injury guideline page: <https://kdigo.org/guidelines/acute-kidney-injury/>
- MedlinePlus pulse reference: <https://medlineplus.gov/ency/article/003399.htm>
