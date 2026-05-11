# Build Log: std_bmi_admission_baseline

- `process_batch_id`: `20260428T134620Z_MIMIC-IV-3.1_std_bmi_admission_baseline`
- `database_id`: `MIMIC-IV-3.1`
- `processed_by`: `Codex`

## Upstream Dependencies

- weight asset: `Methods/Clinical_Database/local_work/Layer 3/MIMIC-IV-3.1/anthropometrics/std_weight_admission_baseline/std_weight_admission_baseline_long.parquet`
- height asset: `Methods/Clinical_Database/local_work/Layer 3/MIMIC-IV-3.1/anthropometrics/std_height/std_height_long.parquet`

## Derivation Contract Used

- formula: `std_weight_kg_baseline / (std_height_cm / 100)^2`
- unit: `kg/m^2`
- precision: `round(2)`
- conservative BMI review range: `[1.0, 80.0] kg/m^2`
- outlier flag is informational at this layer

## Validation Summary

- total rows: `55501`
- unique hadm_id: `55501`
- upstream weight rows total: `69312`
- missing height rows after join: `13811`
- height-join coverage rows: `55501`
- height-join coverage rate vs weight baseline: `0.800742`
- outlier-flagged BMI rows: `38`
- BMI min: `7.54`
- BMI max: `170.99`
- most common source pair: `admission_weight_kg + hosp_omr = 36343`
