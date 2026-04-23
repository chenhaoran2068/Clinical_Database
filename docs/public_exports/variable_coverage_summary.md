# Public Variable Coverage Summary

This file is the human-readable coverage summary derived from the current public variable-card layer.

## Snapshot

- catalog version: `2026-04-21`
- public std-variable cards: `463`
- cross-database public cards: `7`

## Coverage by database

| database_id | family_id | role | public card count | example variable ids |
| --- | --- | --- | --- | --- |
| `MIMIC-IV-3.1` | `MIMIC-IV` | core_database | `463` | `std_aado2`, `std_aado2_calc`, `std_advanced_respiratory_support_active`, `std_age`, `std_aki_kdigo`, `std_albumin`, `std_albumin_ascites`, `std_albumin_creatinine_ratio_urine`, `std_albumin_other_body_fluid`, `std_albumin_pleural`, `std_albumin_urine`, `std_alp`, `std_alt`, `std_amylase`, `std_amylase_ascites` |
| `MIMIC-IV-ECHO-1.0` | `MIMIC-IV` | sibling_module | `0` |  |
| `AmsterdamUMCdb-1.0.2` | `AmsterdamUMCdb` | core_database | `7` | `std_heart_rate`, `std_height`, `std_icu_los_days`, `std_icu_mortality`, `std_ph_bg`, `std_sex`, `std_weight_event` |

## Coverage by family

| family_id | family union count | family shared count | example shared variable ids |
| --- | --- | --- | --- |
| `MIMIC-IV` | `463` | `0` |  |
| `AmsterdamUMCdb` | `7` | `7` | `std_heart_rate`, `std_height`, `std_icu_los_days`, `std_icu_mortality`, `std_ph_bg`, `std_sex`, `std_weight_event` |

## Cross-database examples

`std_heart_rate`, `std_height`, `std_icu_los_days`, `std_icu_mortality`, `std_ph_bg`, `std_sex`, `std_weight_event`
