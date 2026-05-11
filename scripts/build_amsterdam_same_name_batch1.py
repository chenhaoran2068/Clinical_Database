from __future__ import annotations

import json
from pathlib import Path
from textwrap import dedent


DATABASE_ID = "AmsterdamUMCdb-1.0.2"
DATABASE_SLUG = "amsterdamumcdb_1_0_2"
REVIEW_DATE = "2026-05-03"

REPO_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = REPO_ROOT.parent.parent
PUBLIC_BASE = REPO_ROOT / "docs" / "standard_system_mvp"
LOCAL_LAYER5_BASE = (
    WORKSPACE_ROOT
    / "Methods"
    / "Clinical_Database"
    / "local_work"
    / "Layer 5"
    / DATABASE_ID
)
LOCAL_LAYER3_BASE = (
    WORKSPACE_ROOT
    / "Methods"
    / "Clinical_Database"
    / "local_work"
    / "Layer 3"
    / DATABASE_ID
)


def item(
    itemid: int,
    label: str,
    item_en: str | None,
    unit: str | None,
    priority: int,
    factor: float = 1.0,
    offset: float = 0.0,
    rule: str = "direct_value",
) -> dict[str, object]:
    return {
        "itemid": itemid,
        "label": label,
        "item_en": item_en,
        "unit": unit,
        "priority": priority,
        "factor": factor,
        "offset": offset,
        "rule": rule,
    }


VARIABLES: dict[str, dict[str, object]] = {
    "std_map": {
        "name_en": "mean arterial pressure event",
        "intent": "mean arterial pressure observation",
        "definition": "A time-stamped mean arterial pressure measurement event.",
        "semantic_folder": "vital_signs",
        "category": "vital_sign",
        "unit": "mmHg",
        "ucum": "mm[Hg]",
        "precision": 0,
        "storage_type": "Int64",
        "cleaned_min": 0,
        "cleaned_max": 300,
        "normalized_col": "std_map_mmhg_normalized",
        "cleaned_col": "std_map_mmhg_cleaned",
        "source_value_class": "primary_direct_measurement_with_rule_based_same_time_derivation",
        "items": [
            item(6642, "ABP gemiddeld", "invasive mean arterial pressure", "mmHg", 1),
            item(6679, "Niet invasieve bloeddruk gemiddeld", "non-invasive mean arterial pressure", "mmHg", 2),
            item(8843, "ABP gemiddeld II", "invasive mean arterial pressure", "mmHg", 3),
        ],
        "source_selection_reason": "Amsterdam has direct invasive and non-invasive mean arterial pressure numericitems; IABP augmentation and target-pressure rows remain excluded.",
    },
    "std_sbp": {
        "name_en": "systolic blood pressure event",
        "intent": "systolic blood pressure observation",
        "definition": "A time-stamped systolic blood-pressure measurement event.",
        "semantic_folder": "vital_signs",
        "category": "vital_sign",
        "unit": "mmHg",
        "ucum": "mm[Hg]",
        "precision": 0,
        "storage_type": "Int64",
        "cleaned_min": 0,
        "cleaned_max": 400,
        "normalized_col": "std_sbp_mmhg_normalized",
        "cleaned_col": "std_sbp_mmhg_cleaned",
        "items": [
            item(6641, "ABP systolisch", "invasive systolic arterial pressure", "mmHg", 1),
            item(6678, "Niet invasieve bloeddruk systolisch", "non-invasive systolic arterial pressure", "mmHg", 2),
            item(8841, "ABP systolisch II", "invasive systolic arterial pressure", "mmHg", 3),
        ],
        "source_selection_reason": "Amsterdam direct invasive and non-invasive systolic blood-pressure rows are retained; IABP and target-pressure rows are excluded.",
    },
    "std_dbp": {
        "name_en": "diastolic blood pressure event",
        "intent": "diastolic blood pressure observation",
        "definition": "A time-stamped diastolic blood-pressure measurement event.",
        "semantic_folder": "vital_signs",
        "category": "vital_sign",
        "unit": "mmHg",
        "ucum": "mm[Hg]",
        "precision": 0,
        "storage_type": "Int64",
        "cleaned_min": 0,
        "cleaned_max": 300,
        "normalized_col": "std_dbp_mmhg_normalized",
        "cleaned_col": "std_dbp_mmhg_cleaned",
        "items": [
            item(6643, "ABP diastolisch", "invasive diastolic arterial pressure", "mmHg", 1),
            item(6680, "Niet invasieve bloeddruk diastolisch", "non-invasive diastolic arterial pressure", "mmHg", 2),
            item(8842, "ABP diastolisch II", "invasive diastolic arterial pressure", "mmHg", 3),
        ],
        "source_selection_reason": "Amsterdam direct invasive and non-invasive diastolic blood-pressure rows are retained; IABP and target-pressure rows are excluded.",
    },
    "std_respiratory_rate": {
        "name_en": "respiratory rate event",
        "intent": "respiratory rate observation",
        "definition": "A time-stamped respiratory-rate measurement event.",
        "semantic_folder": "vital_signs",
        "category": "vital_sign",
        "unit": "breaths_per_minute",
        "ucum": "/min",
        "precision": 0,
        "storage_type": "Int64",
        "cleaned_min": 0,
        "cleaned_max": 80,
        "normalized_col": "std_respiratory_rate_breaths_per_min_normalized",
        "cleaned_col": "std_respiratory_rate_breaths_per_min_cleaned",
        "items": [
            item(12266, "Ademfreq.", "respiratory rate measurement", "/min", 1),
            item(8874, "Ademfrequentie Monitor", "respiratory rate monitor", None, 2),
            item(12577, "Ademfreq. Spontaan nieuw", "respiratory rate spontaneous", "/min", 3),
            item(12348, "Ademfreq.(2)", "respiratory rate measurement", "/min", 4),
        ],
        "source_selection_reason": "Amsterdam patient respiratory-rate measurement and monitor rows are retained; ventilator-set frequency rows are excluded.",
    },
    "std_spo2": {
        "name_en": "pulse oximetry oxygen saturation event",
        "intent": "pulse oximetry oxygen saturation observation",
        "definition": "A time-stamped pulse-oximetry oxygen saturation measurement event.",
        "semantic_folder": "vital_signs",
        "category": "vital_sign",
        "unit": "percent",
        "ucum": "%",
        "precision": 0,
        "storage_type": "Int64",
        "cleaned_min": 1,
        "cleaned_max": 100,
        "normalized_col": "std_spo2_percent_normalized",
        "cleaned_col": "std_spo2_percent_cleaned",
        "items": [item(6709, "Saturatie (Monitor)", "oxygen saturation SpO2", None, 1)],
        "source_selection_reason": "Amsterdam monitor SpO2 is retained; blood oxygen saturation, target SpO2, and ECMO venous saturation rows are excluded.",
    },
    "std_temp": {
        "name_en": "body temperature event",
        "intent": "body temperature observation",
        "definition": "A time-stamped body-temperature measurement event.",
        "semantic_folder": "vital_signs",
        "category": "vital_sign",
        "unit": "degrees_celsius",
        "ucum": "Cel",
        "precision": 1,
        "storage_type": "Float64",
        "cleaned_min": 25.0,
        "cleaned_max": 45.0,
        "normalized_col": "std_temp_c_normalized",
        "cleaned_col": "std_temp_c_cleaned",
        "items": [
            item(13060, "Temp Axillair", "axillary temperature", "°C", 1),
            item(8658, "Temp Bloed", "blood temperature", "°C", 2),
            item(8662, "Temperatuur Perifeer 1", "peripheral temperature", "°C", 3),
            item(13059, "Temp Lies", "groin temperature", "°C", 4),
            item(13062, "Temp Oor", "tympanic temperature", "°C", 5),
            item(16110, "Temp Oesophagus", "esophageal temperature", "°C", 6),
            item(13063, "Temp Huid", "skin temperature", "°C", 7),
            item(13058, "Temp Rectaal", "rectal temperature", "°C", 8),
            item(8659, "Temperatuur Perifeer 2", "peripheral temperature", "°C", 9),
            item(13952, "Temp Blaas", "bladder temperature", "°C", 10),
            item(14047, "PiCCO Tb blood temperature", "PiCCO blood temperature", "°C", 11),
            item(13061, "Temp Oraal", "oral temperature", "°C", 12),
            item(9546, "Cerebrale temp.", None, "°C", 13),
        ],
        "source_selection_reason": "Amsterdam direct patient body-temperature site rows are retained; target temperature, warmer settings, ventilator humidifier temperature, and APACHE summary rows are excluded.",
    },
    "std_glucose": {
        "name_en": "glucose event",
        "intent": "routine chemistry glucose observation",
        "definition": "A time-stamped routine-chemistry glucose measurement event.",
        "semantic_folder": "laboratory",
        "category": "laboratory",
        "unit": "mg/dL",
        "ucum": "mg/dL",
        "precision": 0,
        "storage_type": "Int64",
        "cleaned_min": 1,
        "cleaned_max": 2000,
        "normalized_col": "std_glucose_mg_per_dl_normalized",
        "cleaned_col": "std_glucose_mg_per_dl_cleaned",
        "items": [
            item(9947, "Glucose (bloed)", "glucose", "mmol/l", 1, 18.0182, 0.0, "glucose_mmol_per_l_to_mg_per_dl"),
            item(6833, "Glucose Bloed", "glucose", "mmol/l", 2, 18.0182, 0.0, "glucose_mmol_per_l_to_mg_per_dl"),
        ],
        "source_selection_reason": "Amsterdam blood chemistry glucose rows are retained and converted from mmol/L to mg/dL; Astrup blood-gas glucose and non-blood fluids remain excluded from this routine-chemistry variable.",
    },
    "std_sodium": {
        "name_en": "sodium event",
        "intent": "routine chemistry sodium observation",
        "definition": "A time-stamped routine-chemistry sodium measurement event.",
        "semantic_folder": "laboratory",
        "category": "laboratory",
        "unit": "mEq/L",
        "ucum": "meq/L",
        "precision": 0,
        "storage_type": "Int64",
        "cleaned_min": 80,
        "cleaned_max": 180,
        "normalized_col": "std_sodium_meq_per_l_normalized",
        "cleaned_col": "std_sodium_meq_per_l_cleaned",
        "items": [
            item(10284, "Na (onv.ISE) (bloed)", "sodium - direct ion specific electrode measurement", "mmol/l", 1),
            item(9924, "Natrium (bloed)", "sodium", "mmol/l", 2),
            item(6840, "Natrium", "serum sodium", "mmol/l", 3),
        ],
        "source_selection_reason": "Amsterdam blood/serum sodium chemistry rows are retained; urine, other-fluid, APACHE, and Astrup-only rows are excluded.",
    },
    "std_potassium": {
        "name_en": "potassium event",
        "intent": "routine chemistry potassium observation",
        "definition": "A time-stamped routine-chemistry potassium measurement event.",
        "semantic_folder": "laboratory",
        "category": "laboratory",
        "unit": "mEq/L",
        "ucum": "meq/L",
        "precision": 1,
        "storage_type": "Float64",
        "cleaned_min": 1.0,
        "cleaned_max": 10.0,
        "normalized_col": "std_potassium_meq_per_l_normalized",
        "cleaned_col": "std_potassium_meq_per_l_cleaned",
        "items": [
            item(10285, "K (onv.ISE) (bloed)", "potassium - direct ion specific electrode measurement", "mmol/l", 1),
            item(9927, "Kalium (bloed)", "potassium", "mmol/l", 2),
            item(6835, "Kalium", "serum potassium", "mmol/l", 3),
        ],
        "source_selection_reason": "Amsterdam blood/serum potassium chemistry rows are retained; urine, other-fluid, APACHE, and ventilator-pressure false-positive rows are excluded.",
    },
    "std_chloride": {
        "name_en": "chloride event",
        "intent": "routine chemistry chloride observation",
        "definition": "A time-stamped routine-chemistry chloride measurement event.",
        "semantic_folder": "laboratory",
        "category": "laboratory",
        "unit": "mEq/L",
        "ucum": "meq/L",
        "precision": 0,
        "storage_type": "Int64",
        "cleaned_min": 60.0,
        "cleaned_max": 150.0,
        "normalized_col": "std_chloride_meq_per_l_normalized",
        "cleaned_col": "std_chloride_meq_per_l_cleaned",
        "items": [
            item(9930, "Chloor (bloed)", None, "mmol/l", 1),
            item(6819, "Chloor", None, "mmol/l", 2),
        ],
        "source_selection_reason": "Amsterdam blood/serum chloride chemistry rows are retained; Astrup, urine, other-fluid, and 24-hour rows are excluded from this routine-chemistry variable.",
    },
    "std_creatinine": {
        "name_en": "creatinine event",
        "intent": "routine chemistry creatinine observation",
        "definition": "A time-stamped routine-chemistry creatinine measurement event.",
        "semantic_folder": "laboratory",
        "category": "laboratory",
        "unit": "mg/dL",
        "ucum": "mg/dL",
        "precision": 2,
        "storage_type": "Float64",
        "cleaned_min": 0.1,
        "cleaned_max": 20.0,
        "normalized_col": "std_creatinine_mg_per_dl_normalized",
        "cleaned_col": "std_creatinine_mg_per_dl_cleaned",
        "items": [
            item(9941, "Kreatinine (bloed)", "serum creatinine", "µmol/l", 1, 0.011312217, 0.0, "creatinine_umol_per_l_to_mg_per_dl"),
            item(6836, "Kreatinine", "serum creatinine", "µmol", 2, 0.011312217, 0.0, "creatinine_legacy_umol_to_mg_per_dl"),
            item(14216, "KREAT enzym. (bloed)", "serum creatinine", "µmol/l", 3, 0.011312217, 0.0, "creatinine_umol_per_l_to_mg_per_dl"),
        ],
        "source_selection_reason": "Amsterdam serum/blood creatinine rows are retained and converted from µmol/L-scale values to mg/dL; urine, clearance, other-fluid, and APACHE rows are excluded.",
    },
    "std_lactate_bg": {
        "name_en": "blood-gas lactate event",
        "intent": "blood-gas lactate observation",
        "definition": "A time-stamped blood-gas lactate measurement event.",
        "semantic_folder": "laboratory",
        "category": "laboratory",
        "unit": "mmol/L",
        "ucum": "mmol/L",
        "precision": 2,
        "storage_type": "Float64",
        "cleaned_min": 0.0,
        "cleaned_max": 30.0,
        "normalized_col": "std_lactate_bg_mmol_per_l_normalized",
        "cleaned_col": "std_lactate_bg_mmol_per_l_cleaned",
        "items": [item(9580, "Laktaat Astrup", "lactate (blood gas)", "mmol/l", 1)],
        "source_selection_reason": "Amsterdam Astrup lactate is retained as the blood-gas lactate same-name source; routine chemistry lactate rows are intentionally excluded.",
    },
    "std_paco2": {
        "name_en": "arterial blood-gas carbon dioxide partial pressure event",
        "intent": "arterial blood-gas carbon dioxide partial pressure observation",
        "definition": "A time-stamped arterial blood-gas carbon dioxide partial-pressure measurement event.",
        "semantic_folder": "laboratory",
        "category": "laboratory",
        "unit": "mmHg",
        "ucum": "mm[Hg]",
        "precision": 0,
        "storage_type": "Int64",
        "cleaned_min": 1,
        "cleaned_max": 200,
        "normalized_col": "std_paco2_mmhg_normalized",
        "cleaned_col": "std_paco2_mmhg_cleaned",
        "items": [
            item(9990, "pCO2 (bloed)", "partial pressure of carbon dioxide in blood", "mmHg", 1),
            item(6846, "PCO2", "partial pressure of carbon dioxide in blood", "mmHg", 2),
            item(21213, "PCO2 (bloed) - kPa", "partial pressure of carbon dioxide in blood", "kPa", 3, 7.50062, 0.0, "pco2_kpa_to_mmhg"),
        ],
        "source_row_sql_filter": "coalesce(lower(comment), '') not like '%veneus%' and coalesce(lower(comment), '') not like '%venous%'",
        "source_selection_reason": "Amsterdam blood-gas pCO2 rows are retained, kPa rows are converted to mmHg, and rows explicitly commented as venous are excluded.",
    },
    "std_pao2": {
        "name_en": "arterial blood-gas oxygen partial pressure event",
        "intent": "arterial blood-gas oxygen partial pressure observation",
        "definition": "A time-stamped arterial blood-gas oxygen partial-pressure measurement event.",
        "semantic_folder": "laboratory",
        "category": "laboratory",
        "unit": "mmHg",
        "ucum": "mm[Hg]",
        "precision": 0,
        "storage_type": "Int64",
        "cleaned_min": 1,
        "cleaned_max": 600,
        "normalized_col": "std_pao2_mmhg_normalized",
        "cleaned_col": "std_pao2_mmhg_cleaned",
        "items": [
            item(9996, "PO2 (bloed)", "partial pressure of oxygen blood", "mmHg", 1),
            item(7433, "PO2", "partial pressure of oxygen blood", "mmHg", 2),
            item(21214, "PO2 (bloed) - kPa", "partial pressure of oxygen blood", "kPa", 3, 7.50062, 0.0, "po2_kpa_to_mmhg"),
        ],
        "source_row_sql_filter": "coalesce(lower(comment), '') not like '%veneus%' and coalesce(lower(comment), '') not like '%venous%'",
        "source_selection_reason": "Amsterdam blood-gas pO2 rows are retained, kPa rows are converted to mmHg, and rows explicitly commented as venous are excluded.",
    },
    "std_bicarbonate_bg": {
        "name_en": "blood-gas bicarbonate event",
        "intent": "blood-gas bicarbonate observation",
        "definition": "A time-stamped blood-gas bicarbonate measurement event.",
        "semantic_folder": "laboratory",
        "category": "laboratory",
        "unit": "mmol/L",
        "ucum": "mmol/L",
        "precision": 0,
        "storage_type": "Int64",
        "cleaned_min": 3,
        "cleaned_max": 60,
        "normalized_col": "std_bicarbonate_bg_mmol_per_l_normalized",
        "cleaned_col": "std_bicarbonate_bg_mmol_per_l_cleaned",
        "items": [
            item(9992, "Act.HCO3 (bloed)", None, "mmol/l", 1),
            item(6810, "HCO3", None, "mmol/l", 2),
        ],
        "source_selection_reason": "Amsterdam blood-gas bicarbonate rows are retained; other-fluid bicarbonate rows are excluded.",
    },
    "std_bun": {
        "name_en": "blood urea nitrogen event",
        "intent": "routine chemistry blood urea nitrogen observation",
        "definition": "A time-stamped blood urea nitrogen measurement event.",
        "semantic_folder": "laboratory",
        "category": "laboratory",
        "unit": "mg/dL",
        "ucum": "mg/dL",
        "precision": 0,
        "storage_type": "Int64",
        "cleaned_min": 1.0,
        "cleaned_max": 200.0,
        "normalized_col": "std_bun_mg_per_dl_normalized",
        "cleaned_col": "std_bun_mg_per_dl_cleaned",
        "items": [
            item(9943, "Ureum (bloed)", None, "mmol/l", 1, 2.80112, 0.0, "urea_mmol_per_l_to_bun_mg_per_dl"),
            item(6850, "Ureum", None, "mmol/l", 2, 2.80112, 0.0, "urea_mmol_per_l_to_bun_mg_per_dl"),
        ],
        "source_selection_reason": "Amsterdam blood/serum urea rows are retained and converted to BUN mg/dL; urine, other-fluid, and 24-hour rows are excluded.",
    },
    "std_hemoglobin": {
        "name_en": "hemoglobin event",
        "intent": "hemoglobin observation",
        "definition": "A time-stamped hemoglobin measurement event.",
        "semantic_folder": "laboratory",
        "category": "laboratory",
        "unit": "g/dL",
        "ucum": "g/dL",
        "precision": 1,
        "storage_type": "Float64",
        "cleaned_min": 1.0,
        "cleaned_max": 25.0,
        "normalized_col": "std_hemoglobin_g_per_dl_normalized",
        "cleaned_col": "std_hemoglobin_g_per_dl_cleaned",
        "items": [
            item(10286, "Hb(v.Bgs) (bloed)", "hemoglobin (blood gas)", "mmol/l", 1, 1.6114, 0.0, "hemoglobin_mmol_per_l_to_g_per_dl"),
            item(9960, "Hb (bloed)", "hemoglobin", "mmol/l", 2, 1.6114, 0.0, "hemoglobin_mmol_per_l_to_g_per_dl"),
            item(9553, "CtHB Astrup", "hemoglobin (blood gas)", "mmol/l", 3, 1.6114, 0.0, "hemoglobin_mmol_per_l_to_g_per_dl"),
            item(6778, "Hemoglobine", "hemoglobin", "mmol/l", 4, 1.6114, 0.0, "hemoglobin_mmol_per_l_to_g_per_dl"),
        ],
        "source_selection_reason": "Amsterdam hemoglobin rows are retained and converted from mmol/L to g/dL; Hb fractions, HbA1c, targets, other-fluid, and ECMO device rows are excluded.",
    },
    "std_hematocrit": {
        "name_en": "hematocrit event",
        "intent": "hematocrit observation",
        "definition": "A time-stamped hematocrit measurement event.",
        "semantic_folder": "laboratory",
        "category": "laboratory",
        "unit": "%",
        "ucum": "%",
        "precision": 1,
        "storage_type": "Float64",
        "cleaned_min": 2.0,
        "cleaned_max": 80.0,
        "normalized_col": "std_hematocrit_pct_normalized",
        "cleaned_col": "std_hematocrit_pct_cleaned",
        "items": [
            item(11545, "Ht(v.Bgs) (bloed)", "hematocrit", "Geen", 1, 100.0, 0.0, "hematocrit_fraction_to_percent"),
            item(11423, "Ht (bloed)", "hematocrit", "Geen", 2, 100.0, 0.0, "hematocrit_fraction_to_percent"),
            item(6777, "Hematocriet", "hematocrit", "l", 3, 100.0, 0.0, "hematocrit_fraction_to_percent"),
        ],
        "source_selection_reason": "Amsterdam hematocrit fraction-scale rows are retained and converted to percent; APACHE summary and non-blood-fluid rows are excluded.",
    },
    "std_platelet_count": {
        "name_en": "platelet count event",
        "intent": "platelet count observation",
        "definition": "A time-stamped platelet count measurement event.",
        "semantic_folder": "laboratory",
        "category": "laboratory",
        "unit": "10^3/uL",
        "ucum": "10*3/uL",
        "precision": 0,
        "storage_type": "Int64",
        "cleaned_min": 1.0,
        "cleaned_max": 2000.0,
        "normalized_col": "std_platelet_count_10e3_per_ul_normalized",
        "cleaned_col": "std_platelet_count_10e3_per_ul_cleaned",
        "items": [
            item(9964, "Thrombo's (bloed)", "platelets", "10^9/l", 1),
            item(6797, "Thrombocyten", "platelets", "10^9/l", 2),
            item(10409, "Thrombo's citr. bloed (bloed)", "platelets - in citrate anticoagulated blood measurement", "10^9/l", 3),
        ],
        "source_selection_reason": "Amsterdam platelet count rows are retained on the same numeric scale as 10^3/uL; CD61 flow, target threshold, coagulation-test, and other-fluid rows are excluded.",
    },
    "std_wbc_count": {
        "name_en": "white blood cell count event",
        "intent": "white blood cell count observation",
        "definition": "A time-stamped white blood cell count measurement event.",
        "semantic_folder": "laboratory",
        "category": "laboratory",
        "unit": "10^3/uL",
        "ucum": "10*3/uL",
        "precision": 1,
        "storage_type": "Float64",
        "cleaned_min": 0.0,
        "cleaned_max": 1000.0,
        "normalized_col": "std_wbc_count_10e3_per_ul_normalized",
        "cleaned_col": "std_wbc_count_10e3_per_ul_cleaned",
        "items": [
            item(9965, "Leuco's (bloed)", "white blood cell count", "10^9/l", 1),
            item(6779, "Leucocyten", "white blood cell count", "10^9/l", 2),
        ],
        "source_selection_reason": "Amsterdam blood WBC count rows are retained on the same numeric scale as 10^3/uL; CSF, urine sediment, other-fluid, and APACHE rows are excluded.",
    },
}

for cfg in VARIABLES.values():
    cfg.setdefault("source_value_class", "raw_measured_only")


def repo_relative(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT.resolve()).as_posix()


def workspace_relative(path: Path) -> str:
    return path.resolve().relative_to(WORKSPACE_ROOT.resolve()).as_posix()


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_variable_spec(variable_id: str, cfg: dict[str, object], existing: dict[str, object] | None) -> dict[str, object]:
    if existing:
        spec = existing
        links = spec.setdefault("current_public_mvp_links", {})
        mapping_specs = links.setdefault("mapping_specs", [])
        amsterdam_mapping = f"docs/standard_system_mvp/{variable_id}/mapping_spec_{DATABASE_SLUG}.json"
        if amsterdam_mapping not in mapping_specs:
            mapping_specs.append(amsterdam_mapping)
        return spec

    unit = str(cfg["unit"])
    return {
        "artifact_type": "variable_spec",
        "artifact_version": "v0_draft",
        "artifact_status": "draft_public_variable_lock",
        "mvp_phase": "single_variable_standard_system_mvp",
        "created_at": REVIEW_DATE,
        "public_scope": "github_safe",
        "variable_class": {
            "variable_class_id": "event_level_numeric_primary_source",
            "class_contract_ref": "Framework_Guideline/StandardVariableClass_EventLevelNumericPrimarySource_Contract.md",
        },
        "variable_identity": {
            "variable_id": variable_id,
            "variable_version": "v0_draft",
            "standardized_name_en": cfg["name_en"],
            "standardized_name_cn_publication_status": "existing_public_card_name_present_but_not_relocked_here",
            "semantic_folder": cfg["semantic_folder"],
            "category": cfg["category"],
        },
        "immutable_core": {
            "semantic_intent": cfg["intent"],
            "semantic_definition": (
                f"{cfg['definition']} The variable is event-level and must not be reused "
                "for baseline, summary, score, or stay-level aggregate outputs."
            ),
            "semantic_grain": "time-stamped measurement event",
            "value_family": "numeric_measurement",
            "source_value_class": cfg["source_value_class"],
            "derived_values_allowed": False,
            "aggregated_values_allowed": False,
            "baseline_or_summary_interpretation_allowed": False,
            "same_name_cross_database_rule": (
                f"Any database asset published as {variable_id} must preserve this "
                f"{cfg['intent']} meaning."
            ),
        },
        "canonical_representation": {
            "canonical_unit": unit,
            "canonical_ucum": cfg["ucum"],
            "value_type": "numeric_measurement",
            "storage_type": cfg["storage_type"],
            "storage_precision_digits": cfg["precision"],
            "display_precision_digits": cfg["precision"],
            "timestamp_required": True,
            "time_precision_requirement": "datetime_or_equivalent_event_time",
            "identifier_roles": ["subject_id", "hadm_id", "stay_id"],
            "cleaned_value_range_in_canonical_unit": [cfg["cleaned_min"], cfg["cleaned_max"]],
            "range_role_note": (
                "This is the current cleaned retained-output range for the governed opening build, "
                "not a claim that every raw source row in every database is already valid."
            ),
        },
        "external_alignment": {
            "alignment_policy": (
                "Use external terminologies as semantic anchors when reliable, but do not make "
                "them the backbone of the standard-variable system."
            ),
            "mapping_type": "none",
            "public_anchor_status": "not_yet_locked_for_this_draft",
            "preferred_anchor_families": ["LOINC", "SNOMED CT"],
        },
        "versioning_contract": {
            "immutable_fields": [
                "variable_id",
                "semantic_intent",
                "semantic_definition",
                "semantic_grain",
                "value_family",
                "source_value_class",
            ],
            "versionable_fields": [
                "canonical_unit",
                "storage_type",
                "storage_precision_digits",
                "display_precision_digits",
                "cleaned_value_range_in_canonical_unit",
                "external_alignment",
                "database_mapping_specs",
            ],
            "new_variable_trigger_examples": [
                f"changing {variable_id} from an event-level measurement to a baseline or summary variable",
                f"changing {variable_id} to a different clinical concept or composite score",
            ],
            "version_bump_trigger_examples": [
                "adding a new reviewed database mapping while preserving the same event-level meaning",
                "locking a reviewed external semantic anchor without changing the variable meaning",
            ],
        },
        "cross_database_contract": {
            "allowed_database_specific_variation": [
                "source code systems and source codes",
                "raw unit labels before normalization",
                "database-specific timing anchors and local structural keys",
            ],
            "disallowed_same_name_variation": [
                "publishing a baseline or stay-level aggregate under the same variable id",
                "publishing a neighboring but clinically distinct measurement under the same variable id",
            ],
        },
        "execution_governance": {
            "current_status": "governed_execution_entrypoint_present",
            "formal_output_rule": (
                f"Formal {variable_id} MVP execution should go through execution.py reading this "
                "variable_spec and an approved mapping_spec."
            ),
            "future_non_bypassable_rule": (
                f"Formal {variable_id} outputs should be generated only through the governed execution.py path."
            ),
        },
        "current_public_mvp_links": {
            "mapping_specs": [f"docs/standard_system_mvp/{variable_id}/mapping_spec_{DATABASE_SLUG}.json"],
            "execution_entrypoint": f"docs/standard_system_mvp/{variable_id}/execution.py",
            "public_card": f"docs/std_variable_cards/{variable_id}.md",
            "roadmap": "docs/STANDARD_SYSTEM_MATURITY_ROADMAP.md",
        },
    }


def build_mapping_spec(variable_id: str, cfg: dict[str, object], variable_spec: dict[str, object]) -> dict[str, object]:
    public_dir = PUBLIC_BASE / variable_id
    layer5_dir = LOCAL_LAYER5_BASE / variable_id
    semantic_folder = str(cfg["semantic_folder"])
    source_codes = [int(src["itemid"]) for src in cfg["items"]]  # type: ignore[index]
    source_labels = {str(src["itemid"]): src["label"] for src in cfg["items"]}  # type: ignore[index]
    conversion_rules = {
        str(src["itemid"]): {
            "source_unit": src["unit"],
            "conversion_factor": src["factor"],
            "conversion_offset": src["offset"],
            "conversion_rule_id": src["rule"],
        }
        for src in cfg["items"]  # type: ignore[index]
    }
    variable_identity = variable_spec["variable_identity"]
    immutable_core = variable_spec["immutable_core"]
    canonical = variable_spec["canonical_representation"]
    return {
        "artifact_type": "mapping_spec",
        "artifact_version": "v0_draft",
        "artifact_status": "reviewed_approved_public_mapping_lock",
        "approval_status": "reviewed_approved",
        "mvp_phase": "single_variable_standard_system_mvp",
        "created_at": REVIEW_DATE,
        "public_scope": "github_safe",
        "variable_spec_ref": repo_relative(public_dir / "variable_spec.json"),
        "standard_variable": {
            "variable_id": variable_id,
            "variable_version": variable_identity["variable_version"],
            "semantic_intent": immutable_core["semantic_intent"],
            "category": variable_identity["category"],
            "semantic_grain": immutable_core["semantic_grain"],
            "source_value_class": immutable_core["source_value_class"],
            "aggregation_status": "not_aggregated",
            "canonical_unit": canonical["canonical_unit"],
            "canonical_value_family": immutable_core["value_family"],
            "current_output_storage_type": canonical["storage_type"],
            "current_output_precision_digits": canonical["storage_precision_digits"],
        },
        "database_mapping": {
            "database_id": DATABASE_ID,
            "source_package": "numericitems",
            "source_table": "numericitems_event",
            "local_prepared_input_asset": workspace_relative(
                WORKSPACE_ROOT
                / "Methods"
                / "Clinical_Database"
                / "local_work"
                / "Layer 2"
                / DATABASE_ID
                / "reviewed_unsplit"
                / "numericitems_event.parquet"
            ),
            "source_code_system": "itemid",
            "source_codes": source_codes,
            "source_code_labels": source_labels,
            "source_fields": {
                "local_identifier_fields": ["patientid", "admissionid"],
                "time_field": "event_time_primary_ms_raw",
                "relative_time_field": "event_time_primary_minutes_relative",
                "raw_value_numeric_field": "value",
                "raw_unit_field": "unit",
                "raw_comment_field": "comment",
                "lab_flag_field": "islabresult",
                "source_code_field": "itemid",
                "source_label_field": "item",
            },
            "identifier_normalization": {
                "subject_id_role": "raw patientid should normalize to subject_id",
                "stay_id_role": "raw admissionid is the Amsterdam ICU-semantic stay-equivalent identifier and should normalize to stay_id",
                "hadm_id_role": "not separately available in the current opening Amsterdam public mapping",
                "stay_link_status": "icu_semantic_stay_equivalent_via_admissionid",
            },
            "source_grain": "one row per Amsterdam numericitems event before exact duplicate collapse",
            "target_grain": "one row per normalized standard measurement event",
            "join_dependencies": [
                {
                    "join_table": "admissions_core",
                    "local_prepared_input_asset": workspace_relative(
                        WORKSPACE_ROOT
                        / "Methods"
                        / "Clinical_Database"
                        / "local_work"
                        / "Layer 2"
                        / DATABASE_ID
                        / "reviewed_unsplit"
                        / "admissions_core.parquet"
                    ),
                    "join_key": "admissionid",
                    "join_cardinality": "many_to_one",
                    "required_fields": ["patientid", "admissioncount", "admittedat", "dischargedat"],
                    "failure_action": "fail",
                },
                {
                    "join_table": "amsterdam_item_dictionary_legacy",
                    "local_prepared_input_asset": workspace_relative(
                        WORKSPACE_ROOT
                        / "Methods"
                        / "Clinical_Database"
                        / "local_work"
                        / "Layer 2"
                        / DATABASE_ID
                        / "reviewed_unsplit"
                        / "amsterdam_item_dictionary_legacy.parquet"
                    ),
                    "join_key": "itemid",
                    "required_fields": ["item", "item_en", "unit", "ucum_code", "table"],
                    "dictionary_lock": {
                        "itemids": source_codes,
                        "table": "numericitems",
                        "labels": source_labels,
                    },
                    "failure_action": "fail",
                },
            ],
        },
        "representation_and_normalization": {
            "anchor_type": "icu_admission_anchor",
            "relative_time_unit": "minutes",
            "measurement_time_precision": "milliseconds_offset",
            "canonical_unit": canonical["canonical_unit"],
            "source_unit_expectations_by_itemid": {
                str(src["itemid"]): src["unit"] for src in cfg["items"]  # type: ignore[index]
            },
            "conversion_rules_by_itemid": conversion_rules,
            "normalization_rule_id": f"amsterdam_numericitems_{variable_id}_batch1_source_specific_conversion_round_{cfg['precision']}",
            "rounding_rule": (
                "nearest_integer_half_away_from_zero"
                if cfg["precision"] == 0
                else f"round_{cfg['precision']}_half_away_from_zero"
            ),
            "cleaned_range_in_canonical_unit": [cfg["cleaned_min"], cfg["cleaned_max"]],
            "outlier_action": "retain_normalized_value_mark_is_outlier_and_null_cleaned_value",
            "cleaned_value_field": cfg["cleaned_col"],
            "normalized_value_field": cfg["normalized_col"],
            "outlier_flag_field": "is_outlier_by_contract",
            "cleaning_status_field": "cleaning_status",
        },
        "validation_contract": {
            "required_non_null_fields": [
                "patientid",
                "admissionid",
                "measurement_time_offset_ms_raw",
                "source_value_numeric_raw",
            ],
            "source_code_lock_rule": "all rows must originate from the approved Amsterdam source itemids in this mapping spec",
            "dictionary_alignment_rule": "each source itemid must match the locked Amsterdam legacy dictionary label, unit, and numericitems table",
            "duplicate_key": ["source_measurement_id"],
            "duplicate_action": "fail",
            "missing_timestamp_action": "fail",
            "missing_numeric_value_action": "fail",
            "join_failure_action": "fail",
            "notes": [
                "Amsterdam retained absolute time is a raw milliseconds offset and should not be interpreted as a wall-clock datetime.",
                "admissionid is treated as the local ICU-semantic stay-equivalent identifier for standard stay_id normalization.",
                str(cfg["source_selection_reason"]),
            ],
        },
        "execution_contract": {
            "governed_execution_entrypoint": repo_relative(public_dir / "execution.py"),
            "current_reference_implementation": workspace_relative(
                layer5_dir / "extract_code" / f"Extract_Code_{variable_id}.py"
            ),
            "formal_output_rule": "The governed execution.py entrypoint reads this mapping spec and delegates to the current local reviewed implementation.",
            "non_bypassable_target_rule": f"Formal {variable_id} outputs for {DATABASE_ID} should be produced only through the governed execution.py path.",
        },
        "evidence_refs": {
            "public_card_path": f"docs/std_variable_cards/{variable_id}.md",
            "formal_approval_review_path": "docs/standard_system_mvp/AMSTERDAM_CLASS1_BATCH1_FORMAL_APPROVAL_REVIEW.md",
            "local_extract_code_path": workspace_relative(layer5_dir / "extract_code" / f"Extract_Code_{variable_id}.py"),
            "local_output_asset_path": workspace_relative(LOCAL_LAYER3_BASE / semantic_folder / variable_id / f"{variable_id}_long.parquet"),
            "local_asset_manifest_path": workspace_relative(layer5_dir / "asset_manifest.md"),
            "local_log_archive_dir": workspace_relative(layer5_dir / "log_archive"),
            "local_preview_path": workspace_relative(layer5_dir / "preview" / f"{variable_id}_preview.csv"),
            "local_knowledge_package_path": workspace_relative(layer5_dir / "Layer5_PerVariable_KnowledgePackage.xlsx"),
            "local_query_summary_dir": workspace_relative(layer5_dir / "query_summary"),
        },
    }


def write_execution_py(variable_id: str) -> None:
    public_dir = PUBLIC_BASE / variable_id
    public_dir.mkdir(parents=True, exist_ok=True)
    (public_dir / "execution.py").write_text(
        dedent(
            """\
            from __future__ import annotations

            import sys
            from pathlib import Path


            VARIABLE_DIR = Path(__file__).resolve().parent
            REPO_ROOT = VARIABLE_DIR.parents[2]
            sys.path.insert(0, str(REPO_ROOT / "scripts"))

            from standard_system_mvp_engine import run_event_level_numeric_primary_source


            if __name__ == "__main__":
                raise SystemExit(
                    run_event_level_numeric_primary_source(
                        variable_dir=VARIABLE_DIR,
                        execution_entrypoint_path=Path(__file__).resolve(),
                    )
                )
            """
        ),
        encoding="utf-8",
    )


def py_str(value: object) -> str:
    return repr(value)


def write_local_extract(variable_id: str, cfg: dict[str, object]) -> None:
    extract_dir = LOCAL_LAYER5_BASE / variable_id / "extract_code"
    extract_dir.mkdir(parents=True, exist_ok=True)
    source_items = []
    for src in cfg["items"]:  # type: ignore[index]
        source_items.append(
            "        SourceItemSpec(\n"
            f"            itemid={src['itemid']},\n"
            f"            expected_item_label={py_str(src['label'])},\n"
            f"            expected_item_en={py_str(src['item_en'])},\n"
            f"            expected_unit={py_str(src['unit'])},\n"
            f"            priority={src['priority']},\n"
            f"            conversion_factor={src['factor']},\n"
            f"            conversion_offset={src['offset']},\n"
            f"            conversion_rule_id={py_str(src['rule'])},\n"
            "        )"
        )
    source_items_text = ",\n".join(source_items)
    source_filter_text = ""
    if cfg.get("source_row_sql_filter"):
        source_filter_text = f"    source_row_sql_filter={py_str(cfg['source_row_sql_filter'])},\n"

    script_text = f"""from __future__ import annotations

from pathlib import Path
import sys


SHARED_DIR = Path(__file__).resolve().parents[2] / "shared_extract_code"
if str(SHARED_DIR) not in sys.path:
    sys.path.insert(0, str(SHARED_DIR))

from _amsterdam_numericitems_multisource_decimal_builder import (  # noqa: E402
    BuildSpec,
    SourceItemSpec,
    run_build,
)


SPEC = BuildSpec(
    std_variable_id={py_str(variable_id)},
    std_variable_name_cn="not_yet_public_cn",
    std_variable_name_en={py_str(cfg["name_en"])},
    semantic_folder={py_str(cfg["semantic_folder"])},
    definition=(
        {py_str(cfg["definition"] + " Amsterdam Batch1 same-name asset built from reviewed numericitems source rows.")}
    ),
    source_table="numericitems_event",
    source_items=(
{source_items_text},
    ),
    normalized_unit={py_str(cfg["unit"])},
    normalized_ucum={py_str(cfg["ucum"])},
    precision_digits={cfg["precision"]},
    cleaned_min={cfg["cleaned_min"]},
    cleaned_max={cfg["cleaned_max"]},
    normalized_col={py_str(cfg["normalized_col"])},
    cleaned_col={py_str(cfg["cleaned_col"])},
    normalization_rule={py_str("amsterdam_numericitems_" + variable_id + "_batch1_source_specific_conversion")},
    official_expected_range_note="Amsterdam opening Batch1 uses the public standard cleaned range; outliers are retained with null cleaned value.",
    global_contract_reference={py_str("Amsterdam same-name Batch1 implementation preserving the public standard variable identity.")},
    source_selection_reason={py_str(cfg["source_selection_reason"])},
    opening_status="reviewed_approved",
    opening_review_date="{REVIEW_DATE}",
{source_filter_text})


def main() -> None:
    payload = run_build(SPEC, Path(__file__))
    print(f"Built {{SPEC.std_variable_id}}")
    print(f"process_batch_id={{payload['process_batch_id']}}")
    print(f"{{SPEC.std_variable_id}}.asset_path={{payload['asset_path']}}")
    print(f"{{SPEC.std_variable_id}}.manifest_path={{payload['manifest_path']}}")
    print(f"{{SPEC.std_variable_id}}.build_log_path={{payload['build_log_path']}}")
    print(f"{{SPEC.std_variable_id}}.effective_status={{payload['effective_status']}}")


if __name__ == "__main__":
    main()
"""
    (extract_dir / f"Extract_Code_{variable_id}.py").write_text(script_text, encoding="utf-8")


def write_review_scaffold() -> None:
    rows = []
    for variable_id, cfg in VARIABLES.items():
        source_scope = ", ".join(f"{src['itemid']} {src['label']}" for src in cfg["items"])  # type: ignore[index]
        rows.append(
            f"| `{variable_id}` | `{cfg['unit']}` | `{source_scope}` | `{cfg['source_selection_reason']}` |"
        )
    review_path = PUBLIC_BASE / "AMSTERDAM_CLASS1_BATCH1_FORMAL_APPROVAL_REVIEW.md"
    review_path.write_text(
        "# Amsterdam Class 1 Batch1 Formal Approval Review\n\n"
        f"Last updated: {REVIEW_DATE}\n\n"
        "Status: reviewed_approved_pending_runtime_refresh\n\n"
        "This scaffold records the approved source boundaries for the Amsterdam same-name-ready Batch1 variables. "
        "Runtime counts are filled after governed first execution, rerun, and reproducibility validation.\n\n"
        "## Batch Scope\n\n"
        "| variable | canonical unit | retained Amsterdam source itemids | approval boundary |\n"
        "| --- | --- | --- | --- |\n"
        + "\n".join(rows)
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    for variable_id, cfg in VARIABLES.items():
        public_dir = PUBLIC_BASE / variable_id
        existing_spec_path = public_dir / "variable_spec.json"
        existing_spec = (
            json.loads(existing_spec_path.read_text(encoding="utf-8"))
            if existing_spec_path.exists()
            else None
        )
        variable_spec = build_variable_spec(variable_id, cfg, existing_spec)
        write_json(existing_spec_path, variable_spec)
        write_execution_py(variable_id)
        write_local_extract(variable_id, cfg)
        write_json(public_dir / f"mapping_spec_{DATABASE_SLUG}.json", build_mapping_spec(variable_id, cfg, variable_spec))
    write_review_scaffold()
    print(f"Wrote Amsterdam same-name Batch1 artifacts for {len(VARIABLES)} variables.")


if __name__ == "__main__":
    main()
