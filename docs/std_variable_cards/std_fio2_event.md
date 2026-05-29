# Public Variable Card: std_fio2_event

Owner approval closure recorded on 2026-05-29.
This is a GitHub-safe public metadata summary, not the full local Layer 5 execution evidence package.

## Identity

- `std_variable_id`: `std_fio2_event`
- standardized English name: `fraction of inspired oxygen event`
- semantic folder: `respiratory_support`
- standard unit: `fraction and percent`
- value type: `numeric event`
- grain: `fio2_event`

## Standard Definition

Standardized event-level directly recorded FiO2 evidence. The analysis value is represented as cleaned FiO2 fraction and the review/display value as cleaned FiO2 percent.

## Cross-Database Status

- MIMIC-IV-3.1: owner-approved and materialized; union of blood-gas-aligned effective FiO2 and ventilator/support setting FiO2.
- AmsterdamUMCdb-1.0.2: owner-approved and materialized; numeric FiO2/O2-concentration source set, with APACHE, transport-only, and ECMO helper fields excluded.
- eICU-CRD-2.0: owner-approved and materialized; lab FiO2 plus respiratoryCharting FiO2 labels, with LPM-like evidence retained but not formula-converted.
- SICdb-1.0.8: owner-approved and materialized; blood-gas FiO2, respirator setting FiO2, and Optiflow/HFNC setting FiO2. Shared lineage with `std_oxygen_device_event` must be considered for Optiflow evidence.
- NWICU-0.1.0: owner-approved unavailable; no direct FiO2 / inspired oxygen concentration source identified in reviewed dictionaries.

## Global Warnings

- This is a general FiO2 event surface, not a blood-gas-aligned FiO2 input table.
- Do not substitute this variable for `std_fio2_bg_input` without an approved temporal matching and source-priority policy.
- Do not infer FiO2 from oxygen flow, oxygen device, oxygen therapy, ventilator mode, airway status, or room-air assumptions.
- Do not fill missing values with 21% room air.
- Do not back-calculate FiO2 from PaO2/FiO2 ratio.
- Do not use this event table as an active interval without a separately approved carry-forward or state policy.
- P/F, S/F, and A-aDO2 calculations require separately approved aligned/calculated derivation contracts.

## Current Approved Database Assets

| database_id | current_status | row_count | latest_review_date |
| --- | --- | ---: | --- |
| MIMIC-IV-3.1 | reviewed_approved | 1,528,297 | 2026-05-29 |
| AmsterdamUMCdb-1.0.2 | reviewed_approved | 31,383,713 | 2026-05-29 |
| eICU-CRD-2.0 | reviewed_approved | 3,587,472 | 2026-05-29 |
| SICdb-1.0.8 | reviewed_approved | 626,351 | 2026-05-29 |
| NWICU-0.1.0 | reviewed_approved_unavailable | 0 | 2026-05-29 |

## Publication Rule

Detailed source-table mappings, database-specific build logs, source item identifiers, value-cleaning flags, and local review history remain in local Layer 5 evidence packages rather than this public card.
