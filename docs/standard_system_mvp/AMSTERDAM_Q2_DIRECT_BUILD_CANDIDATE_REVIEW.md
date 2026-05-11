# Amsterdam Q2 Direct Build Candidate Review

Last updated: 2026-05-04

Status: build-first evidence packet; owner approval is not implied

## Scope

This packet covers the six variables from the Class 1-9 execution queue `Q2_direct_build_queue`.

All six variables now have:

- Amsterdam mapping spec
- governed `execution.py`
- first candidate execution runtime
- rerun runtime
- reproducibility report with `overall_status=pass`
- local Layer 3 asset, preview, manifest, build log, and knowledge package

This packet is not an approval packet. It separates reproducible construction from later owner approval.

## External/Official Context Used

- AmsterdamUMCdb official repository states that legacy version `1.0.2` is the last legacy release and that the database contains ICU/HDU admissions; it lists legacy tables including `admissions`, `drugitems`, and `processitems`.
- The AmsterdamUMCdb repository and cited Crit Care Med paper describe `23,106` admissions and `20,109` patients for the adult ICU/HDU database, matching the local `admissions_core` denominator of `23,106`.
- The official repository notes that AmsterdamUMCdb data are ICU-related and that source dictionaries are available via the package/dictionary files. In this local opening surface, no governed dictionary decoding for numeric `destination` codes has been found yet.

References:

- https://github.com/AmsterdamUMC/AmsterdamUMCdb
- Thoral et al. Crit Care Med. 2021;49(6):e563-e577. DOI: 10.1097/CCM.0000000000004916

## Summary Verdicts For Later Review

| variable_id | build result | technical review posture before owner review | main caveat |
| --- | --- | --- | --- |
| `std_mechanical_ventilation_imv_niv_active` | built + rerun pass | approval-review ready | high Amsterdam support prevalence needs clinical review, but source identity is clean IMV/NIV |
| `std_vasopressor_support_agent_episode` | built + rerun pass | approval-review ready with label caveat | Amsterdam has `terlipressin`, not MIMIC `vasopressin`; retained as a true local agent label |
| `std_icu_entry_source` | built + rerun pass | approval-review ready with missingness caveat | `origin` is non-null for only 9,031/23,106 admissions |
| `std_advanced_respiratory_support_active` | built + rerun pass | hold as same-name approval candidate | Amsterdam lacks governed HFNC source, while public concept includes HFNC |
| `std_discharge_disposition` | built + rerun pass | hold/candidate pending dictionary | 20,598/22,886 retained rows are numeric local `destination` codes |
| `std_icu_exit_destination` | built + rerun pass | hold/candidate pending dictionary | same numeric `destination` code issue as discharge disposition |

## `std_advanced_respiratory_support_active`

### Amsterdam Standardized Distribution

- Output rows: `22,630`
- Unique subjects: `15,103`
- Unique stays: `16,428`
- Parent source rows: `22,825`
- Parent source row counts: IMV `18,259`; NIV/CPAP `4,566`
- Parent source combinations after interval union:
  - IMV only: `18,065`
  - NIV only: `4,476`
  - IMV + NIV overlapping/contiguous: `89`
- Duration, minutes: min `1`, p50 `583`, p90 `11,048`, p99 `47,186.86`, max `248,286`
- Short episodes <=60 min: `2,400`
- Prolonged episodes >=7 days: `2,475`
- HFNC source coverage gap flag: `true`

### Other Processed Database Comparison

MIMIC output has `53,872` rows and `37,184` unique stays. Its approved source scope is `InvasiveVent`, `NonInvasiveVent`, and `HFNC`.

MIMIC source-status distribution includes HFNC-only and HFNC-combination episodes:

- `HFNC`: `3,531`
- `HFNC|InvasiveVent`: `737`
- `HFNC|InvasiveVent|NonInvasiveVent`: `52`
- `HFNC|NonInvasiveVent`: `259`

Amsterdam output has no HFNC component because current Amsterdam review has not found a narrow governed HFNC/Optiflow interval source.

### Official/Standard Match

The public card defines advanced respiratory support as IMV + NIV + HFNC. Amsterdam official/source surface supports `processitems` interval parents for IMV and NIV/CPAP, but not a governed HFNC source in the current opening review.

### Epidemiology/Reasonableness Check

Amsterdam support coverage is `16,428/23,106` stays (`71.1%`) for IMV/NIV-derived advanced support. This is source-driven and reproducible, but broader than MIMIC's public advanced-support stay coverage because the databases, case mix, and source construction differ. The missing HFNC component is the dominant approval blocker.

### Technical Posture

Build evidence is complete, but same-name approval should be held until HFNC absence is explicitly accepted, a valid HFNC source is added, or the variable is split into an Amsterdam IMV/NIV-only proxy.

## `std_mechanical_ventilation_imv_niv_active`

### Amsterdam Standardized Distribution

- Output rows: `22,630`
- Unique subjects: `15,103`
- Unique stays: `16,428`
- Parent source rows: `22,825`
- Parent source row counts: IMV `18,259`; NIV/CPAP `4,566`
- Parent source combinations after interval union:
  - IMV only: `18,065`
  - NIV only: `4,476`
  - IMV + NIV overlapping/contiguous: `89`
- Duration, minutes: min `1`, p50 `583`, p90 `11,048`, p99 `47,186.86`, max `248,286`
- Short episodes <=60 min: `2,400`
- Prolonged episodes >=7 days: `2,475`

### Other Processed Database Comparison

MIMIC output has `50,470` rows and `35,874` unique stays. MIMIC status-set distribution:

- `InvasiveVent`: `45,644`
- `InvasiveVent|NonInvasiveVent`: `348`
- `NonInvasiveVent`: `4,478`

Amsterdam status-set logic is conceptually aligned: only approved IMV and approved NIV/CPAP parent assets are unioned.

### Official/Standard Match

Amsterdam `processitems` approved parents are:

- `9328 Beademen` for invasive mechanical ventilation
- `10740 Beademen non-invasief` and `9671 CPAP` for noninvasive ventilation/CPAP

The standardized output excludes HFNC, oxygen-only support, and tracheostomy status, matching the public IMV/NIV scope.

### Epidemiology/Reasonableness Check

Amsterdam IMV/NIV coverage is high (`71.1%` of local ICU/MC admissions). This is higher than MIMIC's stay fraction (`35,874/94,458`, `38.0%`) but not automatically contradictory because Amsterdam is an ICU/HDU database with different source processes and the MIMIC denominator includes all ICU stays in a different system. The source identity itself is clean.

### Technical Posture

Approval-review ready, with an explicit note to review the high Amsterdam prevalence and long-duration tail during owner review.

## `std_vasopressor_support_agent_episode`

### Amsterdam Standardized Distribution

- Output rows: `26,616`
- Unique subjects: `12,394`
- Unique stays: `13,487`
- Source rows: `295,488`
- Valid source rows: `295,043`
- Invalid source rows: `445`
- Unlinked child episodes: `0`
- Concurrent-other-agent episodes: `4,750`
- Duration, minutes: min `1`, p50 `684`, p90 `4,229.5`, p99 `13,637.35`, max `71,308`
- Short episodes <=60 min: `1,911`
- Prolonged episodes >=7 days: `540`

Agent episode distribution:

- dopamine: `7,853`
- epinephrine: `376`
- norepinephrine: `18,330`
- phenylephrine: `14`
- terlipressin: `43`

### Other Processed Database Comparison

MIMIC output has `96,606` rows and `26,886` unique stays. MIMIC agent distribution:

- dopamine: `2,961`
- epinephrine: `5,173`
- norepinephrine: `43,798`
- phenylephrine: `34,521`
- vasopressin: `10,153`

Both databases retain norepinephrine as the dominant agent. Amsterdam has much more dopamine and almost no phenylephrine, while MIMIC has substantial phenylephrine and vasopressin. This reflects database-specific medication practice and source availability.

### Official/Standard Match

Amsterdam source is continuous `drugitems_event` syringe-pump evidence with `ordercategoryid=65`, positive rate, valid interval, and approved vasopressor-capable itemids:

- `6818` epinephrine
- `7179` dopamine
- `7229` norepinephrine
- `12467` terlipressin
- `19929` phenylephrine

Every child episode linked to the parent Amsterdam `std_vasopressor_support_active` interval by same-stay containment.

### Epidemiology/Reasonableness Check

The Amsterdam output covers `13,487/23,106` admissions (`58.4%`) with at least one retained agent episode, plausible for an ICU/HDU population but requiring later clinical review. Agent mix differs from MIMIC; the important standardization decision is that terlipressin is retained as `terlipressin` rather than forced into `vasopressin`.

### Technical Posture

Approval-review ready with a label-domain caveat. The public variable spec was expanded to include `terlipressin`; owner review should confirm that cross-database agent domain expansion is acceptable.

## `std_discharge_disposition`

### Amsterdam Standardized Distribution

- Source admissions_core rows: `23,106`
- Retained output rows: `22,886`
- Unique subjects: `19,903`
- Unique stays: `22,886`
- Null source `destination`: `220`
- Local numeric destination-code rows: `20,598`
- Explicit died rows: `2,288`

Top retained values:

- `local_destination_code_15`: `6,060`
- `died`: `2,288`
- `local_destination_code_45`: `1,835`
- `local_destination_code_41`: `1,644`
- `local_destination_code_16`: `1,461`
- `local_destination_code_25`: `1,429`
- `local_destination_code_19`: `1,296`
- `local_destination_code_40`: `893`

### Other Processed Database Comparison

MIMIC discharge-disposition output has `546,028` rows. Grouped MIMIC values include:

- home: `194,204`
- unknown: `149,818`
- home with healthcare: `99,305`
- post-acute care facility: `66,552`
- died: `11,721`

MIMIC has already approved grouped harmonization categories. Amsterdam cannot yet match that grouped standard because most retained rows are numeric local codes.

### Official/Standard Match

Amsterdam official repository confirms `admissions` as the admissions/demographic legacy table. The local `destination` field is available, but current opening evidence has not located an approved dictionary translating numeric destination codes into public discharge categories.

### Epidemiology/Reasonableness Check

Amsterdam explicit `died` fraction is `2,288/22,886` (`10.0%`) among retained non-null destinations. This is plausible for ICU/HDU data, but discharge destination code interpretation is unresolved, so apparent category distribution cannot be compared safely to MIMIC grouped categories yet.

### Technical Posture

Hold/candidate pending official or governed local destination-code dictionary. Do not approve as same-name grouped discharge disposition yet.

## `std_icu_entry_source`

### Amsterdam Standardized Distribution

- Source admissions_core rows: `23,106`
- Retained output rows: `9,031`
- Unique subjects: `8,033`
- Unique stays: `9,031`
- Null source `origin`: `14,075`

Retained value distribution:

- `same_hospital_ward`: `5,027`
- `same_hospital_emergency_department`: `2,661`
- `source_label_ccu_ic_zelfde_ziekenhuis`: `296`
- `source_label_ccu_ic_ander_ziekenhuis`: `239`
- `source_label_recovery_zelfde_ziekenhuis_alleen_bij_niet_geplande_ic_opname`: `217`
- `source_label_special_medium_care_zelfde_ziekenhuis`: `193`
- `other_hospital_emergency_department`: `132`
- `other_hospital_ward`: `91`
- `source_label_huis`: `85`
- `source_label_anders`: `53`

### Other Processed Database Comparison

MIMIC ICU entry source has `94,458` rows and `94,458` unique stays. MIMIC entry status distribution:

- resolved previous careunit: `85,439`
- direct hospital admit to ICU: `9,016`
- unresolved no prior transfer record: `3`

Amsterdam differs because `origin` is missing for `14,075/23,106` admissions and is not a full transfer-event reconstruction.

### Official/Standard Match

Amsterdam `admissions` is the official legacy admission/demographic table. The local `origin` field directly represents pre-ICU/MC admission source when present. The standardized output preserves raw origin and lightly normalizes labels.

### Epidemiology/Reasonableness Check

Among non-null Amsterdam origins, same-hospital ward and emergency department dominate, which is clinically plausible. The high null fraction (`60.9%`) is the key limitation and must be visible in later review.

### Technical Posture

Approval-review ready with a missingness caveat. Same-name approval should explicitly state that the Amsterdam asset is source-faithful for non-null origin rows and does not reconstruct missing transfer history.

## `std_icu_exit_destination`

### Amsterdam Standardized Distribution

- Source admissions_core rows: `23,106`
- Retained output rows: `22,886`
- Unique subjects: `19,903`
- Unique stays: `22,886`
- Null source `destination`: `220`
- Local numeric destination-code rows: `20,598`
- Explicit died rows: `2,288`

Top retained values:

- `local_exit_destination_code_15`: `6,060`
- `died`: `2,288`
- `local_exit_destination_code_45`: `1,835`
- `local_exit_destination_code_41`: `1,644`
- `local_exit_destination_code_16`: `1,461`
- `local_exit_destination_code_25`: `1,429`
- `local_exit_destination_code_19`: `1,296`
- `local_exit_destination_code_40`: `893`

### Other Processed Database Comparison

MIMIC ICU exit destination has `94,458` rows. MIMIC exit status distribution:

- resolved next careunit: `77,724`
- direct hospital discharge after ICU: `16,720`
- unresolved missing ICU outtime: `14`

MIMIC preserves raw transfer-event semantics; Amsterdam currently preserves local `destination` codes. These are not yet crosswalked.

### Official/Standard Match

Amsterdam official legacy `admissions` table supports using admission-level discharge/destination context. However, current local evidence does not prove the numeric `destination` code meanings, so the standardized output is source-faithful but not harmonized.

### Epidemiology/Reasonableness Check

The explicit death count matches the discharge-disposition asset because both use `admissions_core.destination`. Numeric local-code dominance prevents safe epidemiologic interpretation of other destinations.

### Technical Posture

Hold/candidate pending official or governed local destination-code dictionary. Do not approve as same-name ICU exit destination yet.

## Runtime Evidence Paths

| variable_id | first runtime | rerun runtime |
| --- | --- | --- |
| `std_advanced_respiratory_support_active` | `docs/standard_system_mvp/std_advanced_respiratory_support_active/runtime/amsterdamumcdb_1_0_2_first_candidate_execution` | `docs/standard_system_mvp/std_advanced_respiratory_support_active/runtime/amsterdamumcdb_1_0_2_rerun_repro_check` |
| `std_mechanical_ventilation_imv_niv_active` | `docs/standard_system_mvp/std_mechanical_ventilation_imv_niv_active/runtime/amsterdamumcdb_1_0_2_first_candidate_execution` | `docs/standard_system_mvp/std_mechanical_ventilation_imv_niv_active/runtime/amsterdamumcdb_1_0_2_rerun_repro_check` |
| `std_vasopressor_support_agent_episode` | `docs/standard_system_mvp/std_vasopressor_support_agent_episode/runtime/amsterdamumcdb_1_0_2_first_candidate_execution` | `docs/standard_system_mvp/std_vasopressor_support_agent_episode/runtime/amsterdamumcdb_1_0_2_rerun_repro_check` |
| `std_discharge_disposition` | `docs/standard_system_mvp/std_discharge_disposition/runtime/amsterdamumcdb_1_0_2_first_candidate_execution` | `docs/standard_system_mvp/std_discharge_disposition/runtime/amsterdamumcdb_1_0_2_rerun_repro_check` |
| `std_icu_entry_source` | `docs/standard_system_mvp/std_icu_entry_source/runtime/amsterdamumcdb_1_0_2_first_candidate_execution` | `docs/standard_system_mvp/std_icu_entry_source/runtime/amsterdamumcdb_1_0_2_rerun_repro_check` |
| `std_icu_exit_destination` | `docs/standard_system_mvp/std_icu_exit_destination/runtime/amsterdamumcdb_1_0_2_first_candidate_execution` | `docs/standard_system_mvp/std_icu_exit_destination/runtime/amsterdamumcdb_1_0_2_rerun_repro_check` |

