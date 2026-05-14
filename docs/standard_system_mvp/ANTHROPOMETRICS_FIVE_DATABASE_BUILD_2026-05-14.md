# Anthropometrics Five-Database Local Build Summary

- Date: 2026-05-14
- Status: local build completed; pending owner review
- Scope: MIMIC-IV-3.1, AmsterdamUMCdb-1.0.2, eICU-CRD-2.0, SICdb-1.0.8, NWICU-0.1.0
- Local evidence package: `Methods/Clinical_Database/local_work/Layer 5/Global/anthropometrics/2026-05-14_anthropometrics_five_database_build_review.md`
- Local policy: `Methods/Clinical_Database/local_work/Layer 4/Global/2026-05-14_std_anthropometrics_height_weight_bmi_policy.md`

## Variables

- `std_height`
- `std_height_interval`
- `std_weight_icu_admission_baseline`
- `std_weight_icu_admission_baseline_interval`
- `std_bmi_icu_admission_baseline`
- `std_weight_event`

## Unit Policy

- Height: cm, float64 storage, 1 display decimal.
- Weight: kg, float64 storage, 1 display decimal.
- BMI: kg/m^2, float64 storage, 2 display decimals.
- BMI formula: `weight_kg / (height_cm / 100)^2`, calculated from unrounded stored values.

## Height QC Policy

- Numeric height evidence is retained when `0 < height_cm < 300`.
- `80-250 cm` is the default adult-plausible band.
- `0-29.9 cm`, `30-79.9 cm`, and `250-299.9 cm` are retained only with review-required QC flags.
- Default adult analyses should use `height_default_analysis_eligible_flag=true`.
- Default BMI analyses should use `bmi_default_analysis_eligible_flag=true`.
- Known source units are converted from source metadata; unknown units are not inferred from numeric values alone.

## Current Caveats

- This is not an owner-approved public release package yet.
- Exact numeric rows and grouped/proxy interval rows must not be treated as equal precision.
- Adult ICU analyses should review or exclude non-adult-plausible height rows unless a predeclared sensitivity rule permits them.
- Amsterdam height and baseline weight include grouped-source midpoint/proxy handling.
- eICU and SICdb currently have limited boundary/static weight-event surfaces rather than dense repeated ICU weight trajectories.
- NWICU height and weight require unit conversion from inch and ounce source fields.
- Layer 3 parquet assets remain local data products and are not copied into the public GitHub repository.
