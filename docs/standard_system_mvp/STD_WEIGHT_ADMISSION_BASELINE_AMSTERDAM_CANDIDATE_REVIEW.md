# std_weight_admission_baseline Amsterdam Candidate Review

Last updated: 2026-04-25

## Review Verdict

Formal decision:

- do not approve the current `AmsterdamUMCdb-1.0.2` local candidate as an approved same-name mapping for `std_weight_admission_baseline`

Practical outcome:

- no public `mapping_spec_amsterdamumcdb_1_0_2.json` should be added for `std_weight_admission_baseline` at this time
- no governed Amsterdam `execution.py` runtime evidence should be generated for this same-name variable until the semantic issue is resolved
- the current public approval remains `MIMIC-IV-3.1` only

This is a content decision, not a technical failure.

The Amsterdam local candidate is useful, but it does not satisfy the current same-name contract for `std_weight_admission_baseline`.

## What Was Reviewed

Reviewed local Amsterdam evidence:

- local asset manifest for `AmsterdamUMCdb-1.0.2/std_weight_admission_baseline`
- local extract wrapper and shared builder
- local query summaries
- local opening review note
- local retained Layer 3 output shape

Reviewed public contract surface:

- `docs/standard_system_mvp/std_weight_admission_baseline/variable_spec.json`
- `docs/standard_system_mvp/std_weight_admission_baseline/mapping_spec_mimic_iv_3_1.json`
- `docs/standard_system_mvp/STD_WEIGHT_ADMISSION_BASELINE_FORMAL_APPROVAL_REVIEW.md`
- `docs/std_variable_cards/std_weight_admission_baseline.md`

Reviewed official/source context:

- AmsterdamUMCdb official repository and wiki
- AmsterdamUMCdb official paper

## Current Same-Name Contract To Match

The current public `std_weight_admission_baseline` contract is:

- admission-start baseline body weight
- target grain: hospital admission encounter
- canonical unit: `kg`
- baseline window: hospital admission start to `min(discharge, admission + 1440 minutes)`
- source style: cleaned event stream with a direct hospital-admission identifier
- selection: closest eligible event to the hospital admission timestamp
- not generic patient-level weight
- not ICU-start baseline weight
- not grouped proxy weight
- not discharge or follow-up weight

This contract was approved for `MIMIC-IV-3.1` only.

## Amsterdam Candidate Content

The Amsterdam local candidate currently says:

- status: `built_pending_user_review`
- target local key: `admissionid`
- retained rows: `23,106`
- unique `admissionid`: `23,106`
- non-null baseline rows: `22,206`
- unresolved rows: `900`
- primary value source: `admissions_core.weightgroup`
- value rule: map grouped weight buckets into kilogram proxy values
- event fallback: use `std_weight_event` within `+/-360` minutes only when `weightgroup` is missing
- retained p25 / p50 / p75: `70.00 / 74.50 / 84.50 kg`

Source-origin distribution:

- `admissions_weightgroup_proxy`: `22,160`
- `event_fallback_near_admission`: `46`
- `unresolved_missing_all_baseline_weight_sources`: `900`

Representation distribution:

- closed bucket midpoint proxy: `19,397`
- open lower boundary proxy: `1,845`
- open upper boundary proxy: `918`
- exact near-admission event numeric kg: `46`
- unresolved: `900`

Weightsource context:

- measured: `1,771`
- anamnestic or asked: `10,235`
- estimated: `6,142`
- unknown: `4,958`

## Official-Source Alignment

The Amsterdam official wiki describes the `admissions` table as data for patients admitted to ICU or MCU.

It defines:

- `admissionid` as the unique identifier for the ICU admission
- `weightgroup` as categorized weight at admission in kg
- `weightsource` as the method used to determine weight at ICU/MCU admission, measured, estimated, or asked

The official repository README also describes the current database as containing ICU and high-dependency unit admissions.

Interpretation:

- Amsterdam's native admission frame is ICU/MCU admission, not a confirmed hospital-admission encounter
- Amsterdam's native `weightgroup` is categorized, not exact continuous weight
- `weightsource` explicitly mixes measured, estimated, and asked/anamnestic sources

These are legitimate Amsterdam semantics.

They are just not the same as the current MIMIC same-name contract.

## Why Same-Name Approval Fails

The current Amsterdam candidate fails same-name approval for three independent reasons.

### 1. Anchor mismatch

MIMIC current contract:

- hospital admission start

Amsterdam current candidate:

- ICU/MCU local admission context

Why this matters:

- `std_weight_admission_baseline` currently means hospital-admission baseline
- approving Amsterdam would silently shift the same variable toward ICU/MCU-admission baseline

That would violate the immutable anchor-family rule in the class-2 contract.

### 2. Value representation mismatch

MIMIC current contract:

- selected cleaned numeric weight event in kg

Amsterdam current candidate:

- mostly grouped `weightgroup` proxy values such as `64.5`, `74.5`, `84.5`
- open boundary buckets mapped to boundary proxies such as `59.0` and `110.0`

Why this matters:

- grouped proxy values can be useful
- they are not equivalent to exact continuous measured event values
- using the same variable ID would hide this difference from downstream users

That would violate the representation and provenance transparency rule.

### 3. Source-quality mismatch

MIMIC current contract:

- source values come from cleaned event rows

Amsterdam current candidate:

- only `1,771` rows have measured context
- most rows are anamnestic, estimated, or unknown-source context

Why this matters:

- the current Amsterdam asset is closer to a mixed-source admission body-size baseline
- it should not be described as the same evidence class as the MIMIC event-selected baseline without a stronger proxy-specific contract

That would violate the same-name cross-database comparability rule.

## What Is Still Acceptable

The Amsterdam candidate is not rejected as useless.

It is acceptable as:

- a local retained candidate
- a useful source audit for Amsterdam baseline body-size context
- a possible future proxy/binned baseline-weight variable
- a possible future Amsterdam-specific mapping after the variable contract is explicitly widened or split

It is not acceptable as:

- an approved same-name `std_weight_admission_baseline` mapping under the current MIMIC-derived contract
- a dual-database closure for the current variable
- an exact continuous admission-baseline weight event equivalent

## Recommended Next Action

Recommended next action:

- keep `std_weight_admission_baseline` MIMIC-only for now
- do not add Amsterdam runtime evidence for this same-name variable
- create a separate future decision for one of the following:
  - define a new proxy/binned variable for Amsterdam-style admission weightgroup semantics
  - revise the global variable contract to explicitly allow proxy and exact subclasses
  - find or build a true Amsterdam continuous event-based baseline that can meet the current same-name contract

The most conservative preferred path is:

- create a distinct proxy variable if this Amsterdam asset is needed for analysis

Candidate future variable names to review later:

- `std_weight_admission_baseline_proxy`
- `std_weight_admission_baseline_grouped`
- `std_weight_icu_admission_baseline_proxy`

No candidate name is approved by this note.

## Follow-Up Decision

Follow-up completed on 2026-04-25:

- the Amsterdam grouped/proxy asset was split into a separate variable named `std_weight_icu_baseline_grouped_proxy`
- that separate variable preserves ICU/MCU admission context and grouped/proxy representation rather than pretending to be hospital-admission continuous weight
- see `docs/standard_system_mvp/STD_WEIGHT_ICU_BASELINE_GROUPED_PROXY_FORMAL_APPROVAL_REVIEW.md`

## Final Decision

The current Amsterdam candidate should remain:

- local-only
- pending user review
- excluded from public same-name approval

Formal conclusion:

- `std_weight_admission_baseline` remains approved only for `MIMIC-IV-3.1`
- Amsterdam should not be promoted into the same variable until anchor and representation semantics are explicitly resolved

## Source Pointers

Public official/source references used in this review:

- AmsterdamUMCdb official repository README: <https://github.com/AmsterdamUMC/AmsterdamUMCdb>
- AmsterdamUMCdb official `admissions` wiki: <https://github.com/AmsterdamUMC/AmsterdamUMCdb/wiki/admissions>
- AmsterdamUMCdb official `listitems` wiki: <https://github.com/AmsterdamUMC/AmsterdamUMCdb/wiki/listitems>
- AmsterdamUMCdb official paper: <https://pmc.ncbi.nlm.nih.gov/articles/PMC8132908/>
