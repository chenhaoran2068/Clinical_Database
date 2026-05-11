# Public Variable Coverage Summary

This file is the human-readable coverage summary derived from the current public variable-card layer.

## Snapshot

- catalog version: `2026-05-09`
- public std-variable cards: `465`
- cross-database public cards: `56`

## Coverage by database

| database_id | family_id | role | public card count | example variable ids |
| --- | --- | --- | --- | --- |
| `MIMIC-IV-3.1` | `MIMIC-IV` | core_database | `463` | `std_aado2`, `std_aado2_calc`, `std_advanced_respiratory_support_active`, `std_age`, `std_aki_kdigo`, `std_albumin`, `std_albumin_ascites`, `std_albumin_creatinine_ratio_urine`, `std_albumin_other_body_fluid`, `std_albumin_pleural`, `std_albumin_urine`, `std_alp`, `std_alt`, `std_amylase`, `std_amylase_ascites` |
| `MIMIC-IV-ECHO-1.0` | `MIMIC-IV` | sibling_module | `0` |  |
| `AmsterdamUMCdb-1.0.2` | `AmsterdamUMCdb` | core_database | `58` | `std_albumin`, `std_amylase`, `std_anion_gap`, `std_aptt`, `std_bicarbonate_bg`, `std_bun`, `std_carbon_dioxide_partial_pressure_bg_allspecimen`, `std_chloride`, `std_creatinine`, `std_crrt_family_active`, `std_days_to_next_icu_admission`, `std_days_to_next_icu_mcu_admission`, `std_dbp`, `std_ferritin`, `std_first_day_urine_output_summary` |
| `SICdb-1.0.5` | `SICdb` | core_database | `0` |  |
| `NWICU-0.1.0` | `NWICU` | core_database | `0` |  |
| `eICU-CRD-2.0` | `eICU-CRD` | core_database | `0` |  |
| `Zigong-1.1` | `Zigong` | core_database | `0` |  |

## Coverage by family

| family_id | family union count | family shared count | example shared variable ids |
| --- | --- | --- | --- |
| `MIMIC-IV` | `463` | `0` |  |
| `AmsterdamUMCdb` | `58` | `58` | `std_albumin`, `std_amylase`, `std_anion_gap`, `std_aptt`, `std_bicarbonate_bg`, `std_bun`, `std_carbon_dioxide_partial_pressure_bg_allspecimen`, `std_chloride`, `std_creatinine`, `std_crrt_family_active`, `std_days_to_next_icu_admission`, `std_days_to_next_icu_mcu_admission`, `std_dbp`, `std_ferritin`, `std_first_day_urine_output_summary` |
| `SICdb` | `0` | `0` |  |
| `NWICU` | `0` | `0` |  |
| `eICU-CRD` | `0` | `0` |  |
| `Zigong` | `0` | `0` |  |

## Cross-database examples

`std_albumin`, `std_amylase`, `std_anion_gap`, `std_aptt`, `std_bicarbonate_bg`, `std_bun`, `std_carbon_dioxide_partial_pressure_bg_allspecimen`, `std_chloride`, `std_creatinine`, `std_crrt_family_active`, `std_days_to_next_icu_admission`, `std_dbp`, `std_ferritin`, `std_first_day_urine_output_summary`, `std_glucose`, `std_haptoglobin`, `std_heart_rate`, `std_height`, `std_hematocrit`, `std_hemoglobin`, `std_icu_los_days`, `std_icu_mortality`, `std_icu_urine_output_event`, `std_inr`, `std_invasive_mechanical_ventilation_active`, `std_lactate_bg`, `std_lipase`, `std_magnesium`, `std_map`, `std_non_crrt_rrt_active`
