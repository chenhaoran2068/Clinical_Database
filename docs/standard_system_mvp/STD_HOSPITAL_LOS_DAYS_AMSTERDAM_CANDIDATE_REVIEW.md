# `std_hospital_los_days` Amsterdam Candidate Review

Review date: `2026-04-28`

## Formal Verdict

Formal decision:

- do not approve `AmsterdamUMCdb-1.0.2` as a same-name implementation of `std_hospital_los_days` at this time
- do not add `docs/standard_system_mvp/std_hospital_los_days/mapping_spec_amsterdamumcdb_1_0_2.json`
- do not generate Amsterdam governed runtime evidence under this same hospital-LOS variable identity
- keep the current same-name approval bounded to `MIMIC-IV-3.1`

This is a semantic-boundary decision, not a failure of Amsterdam LOS evidence.

Amsterdam already has approved duration evidence, but the approved evidence belongs to ICU or ICU-semantic stay duration, not to hospital-admission encounter duration.

## What Was Reviewed

Reviewed public standard-system surface:

- `docs/standard_system_mvp/std_hospital_los_days/variable_spec.json`
- `docs/standard_system_mvp/std_hospital_los_days/mapping_spec_mimic_iv_3_1.json`
- `docs/standard_system_mvp/STD_HOSPITAL_LOS_DAYS_FORMAL_APPROVAL_REVIEW.md`
- `docs/std_variable_cards/std_hospital_los_days.md`
- `docs/standard_system_mvp/std_icu_los_days/variable_spec.json`
- `docs/standard_system_mvp/std_icu_los_days/mapping_spec_amsterdamumcdb_1_0_2.json`
- `docs/standard_system_mvp/STD_ICU_LOS_DAYS_FORMAL_APPROVAL_REVIEW.md`
- `Framework_Guideline/ID_Normalization_Contract.md`
- `Framework_Guideline/AmsterdamUMCdb_TimeSemantics_Contract.md`

Reviewed local Amsterdam evidence:

- `Methods/Clinical_Database/local_work/Layer 5/AmsterdamUMCdb-1.0.2/std_icu_los_days/asset_manifest.md`
- `Methods/Clinical_Database/local_work/Layer 5/AmsterdamUMCdb-1.0.2/std_icu_los_days/std_icu_los_days_opening_review_20260425.md`
- `Methods/Clinical_Database/local_work/Layer 5/AmsterdamUMCdb-1.0.2/std_icu_los_days/query_summary/std_icu_los_days_source_audit_summary.json`
- `Methods/Clinical_Database/local_work/Layer 5/AmsterdamUMCdb-1.0.2/std_icu_los_days/query_summary/std_icu_los_days_distribution_summary.json`
- `Methods/Clinical_Database/local_work/Layer 5/AmsterdamUMCdb-1.0.2/std_icu_los_days/query_summary/std_icu_los_days_quality_summary.json`

Reviewed official/source context:

- AmsterdamUMCdb official repository README
- AmsterdamUMCdb official legacy `admissions` wiki
- AmsterdamUMCdb official paper

## Current Same-Name Contract To Match

The current `std_hospital_los_days` contract is:

- one retained row per hospital admission encounter
- canonical key includes `hadm_id`
- canonical unit is `days`
- start boundary is hospital admission time
- end boundary is hospital discharge time
- retained value is hospital admission duration, not ICU stay duration
- rare source-edge negative durations may be retained only with explicit validity status

The same-name variable must not mean:

- ICU length of stay
- ICU/MC local admission duration
- critical-care-unit stay duration without a verified hospital-admission encounter layer
- patient-level follow-up time
- ICU-subset audit field only

## Amsterdam Evidence Currently Available

Amsterdam already has an approved governed duration asset:

- variable: `std_icu_los_days`
- database: `AmsterdamUMCdb-1.0.2`
- current status: `reviewed_approved`
- retained rows: `18,386`
- unique admissions: `18,386`
- retained grain: Amsterdam ICU-semantic `admissionid` as local stay-equivalent key
- same-name scope: `location in (IC, IC&MC, MC&IC)`
- excluded from same-name ICU denominator: `MC`
- primary source: raw offset duration from `admittedat` and `dischargedat`
- audit-only reference field: `lengthofstay`
- zero-duration rows: `3`
- negative-duration rows: `0`
- median raw-offset ICU LOS: `1.244097` days
- official paper ICU LOS summary reproduced from `lengthofstay / 24`: `1.25 (0.92-4.71) days`

The local source audit also records:

- all Amsterdam admissions rows: `23,106`
- ICU-semantic rows retained for same-name ICU LOS: `18,386`
- excluded same-name rows: `4,720`
- raw offset p25 / p50 / p75: `0.904 / 1.244 / 4.699` days
- reported `lengthofstay / 24` p25 / p50 / p75: `0.917 / 1.25 / 4.708` days

Interpretation:

- Amsterdam duration evidence is real and useful
- the current approved evidence is critical-care stay duration
- the current approved evidence is not a separate hospital-admission encounter duration

## Why Same-Name `std_hospital_los_days` Approval Fails

### 1. Identifier grain does not match

The ID normalization contract currently maps Amsterdam:

- raw `patientid` to canonical `subject_id`
- raw `admissionid` to canonical `stay_id`

It also states:

- do not publish raw `admissionid` as canonical `hadm_id` by default
- the current Amsterdam public opening surface has not yet published a separate hospital-admission canonical layer

Why this matters:

- `std_hospital_los_days` requires hospital-admission encounter grain
- the current Amsterdam retained duration evidence is stay-equivalent critical-care admission grain
- reusing `std_hospital_los_days` would make `hadm_id` and `stay_id` semantics collapse into one another

### 2. Source boundaries are critical-care admission boundaries

The Amsterdam LOS evidence uses:

- `admittedat`
- `dischargedat`
- `lengthofstay` as audit-only summary

The time semantics contract says:

- raw offsets such as `admittedat` and `dischargedat` are timing truth
- `lengthofstay` is a source-supplied summary duration, usually whole hours

That supports the current `std_icu_los_days` build.

It does not prove a hospital admission/discharge interval.

### 3. Official Amsterdam source scope is ICU/HDU, not general hospital encounter

The official AmsterdamUMCdb repository describes the database as ICU and high-dependency unit admission data.

The legacy `admissions` table is the admissions and demographic surface for patients admitted to ICU or MCU.

Interpretation:

- Amsterdam official scope supports an ICU/MCU stay-duration interpretation
- it does not, by itself, expose the hospital-admission encounter layer required by `std_hospital_los_days`

### 4. A correct neighboring variable already exists

Amsterdam is already approved under:

- `std_icu_los_days`

That is the correct same-name duration identity for the current Amsterdam evidence because it preserves:

- ICU-semantic stay-equivalent target grain
- ICU admission anchor family
- raw admitted/discharged offset timing truth
- exclusion of MC-only rows from the current same-name ICU denominator

Forcing the same evidence into `std_hospital_los_days` would weaken, not strengthen, the standard.

## Split Decision

The correct split is:

| Evidence type | Current decision |
| --- | --- |
| true hospital admission duration with verified hospital admission and discharge boundaries | eligible for `std_hospital_los_days` after separate Amsterdam evidence exists |
| ICU or ICU-semantic stay-equivalent duration | already belongs under `std_icu_los_days` |
| all ICU/MCU local admission duration including MC-only rows | possible future distinct variable, not approved here |

Possible future variable identity to review if all Amsterdam ICU/MCU rows are needed:

- `std_critical_care_los_days`
- `std_icu_mcu_los_days`

No future name is approved by this note.

The current decision only says:

- do not call Amsterdam ICU/MCU stay duration `std_hospital_los_days`
- keep the already approved Amsterdam ICU-semantic duration under `std_icu_los_days`
- create a separate all-ICU/MCU duration variable later only if there is a real analysis need

## What Would Be Needed For Future Same-Name Approval

Before Amsterdam can be approved for `std_hospital_los_days`, it must show:

1. a real hospital-admission encounter identifier or bridge that can normalize to `hadm_id`
2. hospital admission start boundary
3. hospital discharge boundary
4. one retained row per hospital admission encounter
5. an explicit relationship between any ICU/MC local admissions and the hospital encounter
6. validation that multiple critical-care stays inside one hospital admission do not become duplicate hospital LOS rows
7. governed Amsterdam mapping spec, execution, validation report, manifest, and rerun reproducibility report

Until then, Amsterdam duration evidence should remain in ICU/stay-duration identities.

## Practical Outcome

For the current public repository:

- `std_hospital_los_days` remains `MIMIC-IV-3.1` only
- Amsterdam is not listed as an approved same-name database for `std_hospital_los_days`
- no Amsterdam runtime directory is added under `std_hospital_los_days`
- the Amsterdam `std_icu_los_days` approval remains valid
- any future all-ICU/MCU duration expansion should be reviewed as a separate variable identity

Follow-up bridge review:

- `docs/standard_system_mvp/AMSTERDAM_HOSPITAL_ADMISSION_BRIDGE_FEASIBILITY_REVIEW.md` confirms that the current Amsterdam opening layer still does not prove the hospital-admission/discharge bridge needed for same-name hospital-level duration or next-hospital-admission variables

## Final Decision

Amsterdam cannot be approved as same-name `std_hospital_los_days` under the current evidence.

The current Amsterdam duration evidence should remain under ICU or ICU/MC stay-duration semantics, not hospital-admission duration semantics.

Formal conclusion:

- `std_hospital_los_days`: approved for `MIMIC-IV-3.1` only
- `AmsterdamUMCdb-1.0.2`: not approved for same-name `std_hospital_los_days`
- no new mapping/runtime evidence should be generated for Amsterdam under this variable until hospital-admission semantics are proven

## Source Pointers

Public official/source references used in this review:

- AmsterdamUMCdb official repository README: <https://github.com/AmsterdamUMC/AmsterdamUMCdb>
- AmsterdamUMCdb official legacy `admissions` wiki: <https://github.com/AmsterdamUMC/AmsterdamUMCdb/wiki/admissions>
- AmsterdamUMCdb official paper: <https://pmc.ncbi.nlm.nih.gov/articles/PMC8132908/>
