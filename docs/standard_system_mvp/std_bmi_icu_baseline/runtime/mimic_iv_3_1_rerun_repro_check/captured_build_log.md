# Build Log: std_bmi_icu_baseline

- `process_batch_id`: `20260428T134645Z_MIMIC-IV-3.1_std_bmi_icu_baseline`
- `database_id`: `MIMIC-IV-3.1`
- `processed_by`: `Codex`

## Upstream Dependencies

- weight asset: `Methods/Clinical_Database/local_work/Layer 3/MIMIC-IV-3.1/anthropometrics/std_weight_icu_baseline/std_weight_icu_baseline_long.parquet`
- height asset: `Methods/Clinical_Database/local_work/Layer 3/MIMIC-IV-3.1/anthropometrics/std_height/std_height_long.parquet`

## Derivation Contract Used

- formula: `std_weight_kg_baseline / (std_height_cm / 100)^2`
- unit: `kg/m^2`
- precision: `round(2)`
- conservative BMI review range: `[1.0, 80.0] kg/m^2`
- outlier flag is informational at this layer

## Validation Summary

- total rows: `73432`
- unique stay_id: `73432`
- upstream weight rows total: `88690`
- missing height rows after join: `15258`
- height-join coverage rows: `73432`
- height-join coverage rate vs weight baseline: `0.827963`
- outlier-flagged BMI rows: `53`
- BMI min: `7.47`
- BMI max: `170.63`
- most common source pair: `admission_weight_kg + hosp_omr = 38205`
