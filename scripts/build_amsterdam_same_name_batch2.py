from __future__ import annotations

import json
from pathlib import Path
from textwrap import dedent

import build_amsterdam_same_name_batch1 as batch1


DATABASE_ID = "AmsterdamUMCdb-1.0.2"
DATABASE_SLUG = "amsterdamumcdb_1_0_2"
REVIEW_DATE = "2026-05-04"
BATCH_LABEL = "Batch2"
BATCH_STATUS = "built_pending_user_review"
REVIEW_PATH = "docs/standard_system_mvp/AMSTERDAM_CLASS1_BATCH2_CANDIDATE_EVIDENCE_REVIEW.md"

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

item = batch1.item
repo_relative = batch1.repo_relative
workspace_relative = batch1.workspace_relative
write_json = batch1.write_json
write_execution_py = batch1.write_execution_py


VARIABLES: dict[str, dict[str, object]] = {
    "std_oxygen_partial_pressure_bg_allspecimen": {
        "name_en": "blood-gas oxygen partial pressure all-specimen event",
        "intent": "blood-gas oxygen partial pressure observation across all retained specimen labels",
        "definition": "A time-stamped blood-gas oxygen partial-pressure measurement event retaining all available Amsterdam specimen scope.",
        "semantic_folder": "laboratory",
        "category": "laboratory",
        "unit": "mmHg",
        "ucum": "mm[Hg]",
        "precision": 0,
        "storage_type": "Int64",
        "cleaned_min": 1,
        "cleaned_max": 600,
        "normalized_col": "std_oxygen_partial_pressure_bg_allspecimen_mmhg_normalized",
        "cleaned_col": "std_oxygen_partial_pressure_bg_allspecimen_mmhg_cleaned",
        "source_value_class": "primary_direct_measurement_with_specimen_scope_boundary",
        "process_slug": "std_po2_bg_all",
        "items": [
            item(7433, "PO2", "partial pressure of oxygen blood", "mmHg", 1),
            item(9996, "PO2 (bloed)", "partial pressure of oxygen blood", "mmHg", 2),
            item(9997, "pO2 (overig)", None, "mmHg", 3),
            item(21214, "PO2 (bloed) - kPa", "partial pressure of oxygen blood", "kPa", 4, 7.50062, 0.0, "po2_kpa_to_mmhg"),
        ],
        "source_selection_reason": "Amsterdam blood-gas pO2 blood and other-specimen numericitems are retained for the all-specimen candidate; kPa rows are converted to mmHg; monitor SpO2 and target oxygen rows are excluded.",
    },
    "std_carbon_dioxide_partial_pressure_bg_allspecimen": {
        "name_en": "blood-gas carbon dioxide partial pressure all-specimen event",
        "intent": "blood-gas carbon dioxide partial pressure observation across all retained specimen labels",
        "definition": "A time-stamped blood-gas carbon dioxide partial-pressure measurement event retaining all available Amsterdam specimen scope.",
        "semantic_folder": "laboratory",
        "category": "laboratory",
        "unit": "mmHg",
        "ucum": "mm[Hg]",
        "precision": 0,
        "storage_type": "Int64",
        "cleaned_min": 1,
        "cleaned_max": 200,
        "normalized_col": "std_carbon_dioxide_partial_pressure_bg_allspecimen_mmhg_normalized",
        "cleaned_col": "std_carbon_dioxide_partial_pressure_bg_allspecimen_mmhg_cleaned",
        "source_value_class": "primary_direct_measurement_with_specimen_scope_boundary",
        "process_slug": "std_pco2_bg_all",
        "items": [
            item(6846, "PCO2", "partial pressure of carbon dioxide in blood", "mmHg", 1),
            item(9990, "pCO2 (bloed)", "partial pressure of carbon dioxide in blood", "mmHg", 2),
            item(9991, "pCO2 (overig)", None, "mmHg", 3),
            item(21213, "PCO2 (bloed) - kPa", "partial pressure of carbon dioxide in blood", "kPa", 4, 7.50062, 0.0, "pco2_kpa_to_mmhg"),
        ],
        "source_selection_reason": "Amsterdam blood-gas pCO2 blood and other-specimen numericitems are retained for the all-specimen candidate; kPa rows are converted to mmHg; end-tidal CO2 and target CO2 rows are excluded.",
    },
    "std_oxygen_saturation_bg_allspecimen": {
        "name_en": "blood-gas oxygen saturation all-specimen event",
        "intent": "blood-gas oxygen saturation observation across all retained specimen labels",
        "definition": "A time-stamped blood-gas oxygen-saturation measurement event retaining all available Amsterdam specimen scope.",
        "semantic_folder": "laboratory",
        "category": "laboratory",
        "unit": "percent",
        "ucum": "%",
        "precision": 0,
        "storage_type": "Int64",
        "cleaned_min": 1,
        "cleaned_max": 100,
        "normalized_col": "std_oxygen_saturation_bg_allspecimen_percent_normalized",
        "cleaned_col": "std_oxygen_saturation_bg_allspecimen_percent_cleaned",
        "source_value_class": "primary_direct_measurement_with_source_scale_normalization",
        "process_slug": "std_so2_bg_all",
        "items": [
            item(8903, "SO2", None, None, 1),
            item(11543, "SO2 (Hb) (bloed)", None, "Geen", 2),
            item(12311, "O2-Saturatie (bloed)", None, "Geen", 3, 100.0, 0.0, "fraction_to_percent_for_o2_saturation_blood"),
        ],
        "source_selection_reason": "Amsterdam blood-gas oxygen-saturation rows are retained; O2-Saturatie fraction-scale rows are converted to percent; monitor SpO2, target SpO2, and ECMO venous saturation rows are excluded.",
    },
    "std_oxygen_saturation_bg_arterial_specimen": {
        "name_en": "blood-gas oxygen saturation arterial-specimen event",
        "intent": "arterial blood-gas oxygen saturation observation",
        "definition": "A time-stamped arterial-scope blood-gas oxygen-saturation measurement event.",
        "semantic_folder": "laboratory",
        "category": "laboratory",
        "unit": "percent",
        "ucum": "%",
        "precision": 0,
        "storage_type": "Int64",
        "cleaned_min": 1,
        "cleaned_max": 100,
        "normalized_col": "std_oxygen_saturation_bg_arterial_specimen_percent_normalized",
        "cleaned_col": "std_oxygen_saturation_bg_arterial_specimen_percent_cleaned",
        "source_value_class": "primary_direct_measurement_with_candidate_arterial_scope_boundary",
        "process_slug": "std_so2_bg_art",
        "items": [
            item(8903, "SO2", None, None, 1),
            item(11543, "SO2 (Hb) (bloed)", None, "Geen", 2),
            item(12311, "O2-Saturatie (bloed)", None, "Geen", 3, 100.0, 0.0, "fraction_to_percent_for_o2_saturation_blood"),
        ],
        "source_row_sql_filter": "coalesce(lower(comment), '') not like '%veneus%' and coalesce(lower(comment), '') not like '%venous%'",
        "source_selection_reason": "Amsterdam blood-gas oxygen-saturation arterial-specimen candidate retains blood-gas SO2 rows while excluding rows explicitly commented as venous; the absence of a universal structured specimen flag must remain visible during review.",
    },
    "std_total_bilirubin": {
        "name_en": "total bilirubin event",
        "intent": "routine chemistry total bilirubin observation",
        "definition": "A time-stamped routine-chemistry total bilirubin measurement event.",
        "semantic_folder": "laboratory",
        "category": "laboratory",
        "unit": "mg/dL",
        "ucum": "mg/dL",
        "precision": 1,
        "storage_type": "Float64",
        "cleaned_min": 0.1,
        "cleaned_max": 60.0,
        "normalized_col": "std_total_bilirubin_mg_per_dl_normalized",
        "cleaned_col": "std_total_bilirubin_mg_per_dl_cleaned",
        "source_value_class": "primary_direct_measurement_with_unit_conversion",
        "items": [
            item(6813, "Bili Totaal", "bilirubin total", "µmol", 1, 0.058467, 0.0, "bilirubin_umol_per_l_to_mg_per_dl"),
            item(9945, "Bilirubine (bloed)", "bilirubin total", "µmol/l", 2, 0.058467, 0.0, "bilirubin_umol_per_l_to_mg_per_dl"),
        ],
        "source_selection_reason": "Amsterdam total bilirubin blood/chemistry rows are retained and converted from umol/L scale to mg/dL; conjugated, urine, ascites, drain, and other-fluid bilirubin rows are excluded.",
    },
    "std_albumin": {
        "name_en": "albumin event",
        "intent": "routine chemistry albumin observation",
        "definition": "A time-stamped routine-chemistry albumin measurement event.",
        "semantic_folder": "laboratory",
        "category": "laboratory",
        "unit": "g/dL",
        "ucum": "g/dL",
        "precision": 1,
        "storage_type": "Float64",
        "cleaned_min": 0.5,
        "cleaned_max": 10.0,
        "normalized_col": "std_albumin_g_per_dl_normalized",
        "cleaned_col": "std_albumin_g_per_dl_cleaned",
        "source_value_class": "primary_direct_measurement_with_unit_conversion",
        "items": [
            item(6801, "Albumine chemisch", None, "g/l", 1, 0.1, 0.0, "albumin_g_per_l_to_g_per_dl"),
            item(9975, "Albumine (imm.) (bloed)", None, "g/l", 2, 0.1, 0.0, "albumin_g_per_l_to_g_per_dl"),
        ],
        "source_selection_reason": "Amsterdam blood/chemistry albumin rows are retained and converted from g/L to g/dL; liquor, urine, dialysate, and drug albumin rows are excluded.",
    },
    "std_inr": {
        "name_en": "INR event",
        "intent": "international normalized ratio coagulation observation",
        "definition": "A time-stamped INR coagulation measurement event.",
        "semantic_folder": "laboratory",
        "category": "laboratory",
        "unit": "unitless",
        "ucum": "{INR}",
        "precision": 2,
        "storage_type": "Float64",
        "cleaned_min": 0.1,
        "cleaned_max": 30.0,
        "normalized_col": "std_inr_normalized",
        "cleaned_col": "std_inr_cleaned",
        "source_value_class": "primary_direct_measurement",
        "items": [
            item(11893, "Prothrombinetijd (bloed)", None, "INR", 1),
            item(11894, "Prothrombinetijd  (bloed)", None, "INR", 2),
        ],
        "source_selection_reason": "Amsterdam Prothrombinetijd rows with INR unit are retained for std_inr; PT seconds rows, medication rows, and target/process rows are excluded.",
    },
    "std_pt": {
        "name_en": "PT event",
        "intent": "prothrombin time coagulation observation",
        "definition": "A time-stamped prothrombin-time coagulation measurement event.",
        "semantic_folder": "laboratory",
        "category": "laboratory",
        "unit": "sec",
        "ucum": "s",
        "precision": 1,
        "storage_type": "Float64",
        "cleaned_min": 1.0,
        "cleaned_max": 300.0,
        "normalized_col": "std_pt_seconds_normalized",
        "cleaned_col": "std_pt_seconds_cleaned",
        "source_value_class": "primary_direct_measurement_with_candidate_unit_review_required",
        "items": [
            item(6789, "Protrombinetijd", None, "sec", 1),
        ],
        "source_selection_reason": "Amsterdam legacy Protrombinetijd rows are the only seconds-labeled candidate source for std_pt, but their distribution is INR-like and must be reviewed before approval.",
    },
    "std_aptt": {
        "name_en": "APTT event",
        "intent": "activated partial thromboplastin time coagulation observation",
        "definition": "A time-stamped activated partial thromboplastin time coagulation measurement event.",
        "semantic_folder": "laboratory",
        "category": "laboratory",
        "unit": "sec",
        "ucum": "s",
        "precision": 1,
        "storage_type": "Float64",
        "cleaned_min": 1.0,
        "cleaned_max": 200.0,
        "normalized_col": "std_aptt_seconds_normalized",
        "cleaned_col": "std_aptt_seconds_cleaned",
        "source_value_class": "primary_direct_measurement",
        "items": [
            item(11944, "APTT  (bloed)", None, "sec", 1),
            item(17982, "APTT (bloed)", None, "sec", 2),
        ],
        "source_selection_reason": "Amsterdam direct APTT blood seconds rows are retained; corrected APTT, target APTT, CVVH treatment targets, procedure orders, and free-text inhibitor comments are excluded.",
    },
}


def _patch_batch1_runtime_constants() -> None:
    batch1.REVIEW_DATE = REVIEW_DATE


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

from datetime import datetime, timezone
from pathlib import Path
import sys


SHARED_DIR = Path(__file__).resolve().parents[2] / "shared_extract_code"
if str(SHARED_DIR) not in sys.path:
    sys.path.insert(0, str(SHARED_DIR))

import _amsterdam_numericitems_multisource_decimal_builder as builder  # noqa: E402
from _amsterdam_numericitems_multisource_decimal_builder import (  # noqa: E402
    BuildSpec,
    SourceItemSpec,
)


PROCESS_BATCH_VARIABLE_ID = {py_str(str(cfg.get("process_slug", variable_id)))}


def _short_process_batch_id(std_variable_id: str, database_id: str = "AmsterdamUMCdb-1.0.2") -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{{stamp}}_{{database_id}}_{{PROCESS_BATCH_VARIABLE_ID}}"


builder.process_batch_id = _short_process_batch_id


SPEC = BuildSpec(
    std_variable_id={py_str(variable_id)},
    std_variable_name_cn="not_yet_public_cn",
    std_variable_name_en={py_str(cfg["name_en"])},
    semantic_folder={py_str(cfg["semantic_folder"])},
    definition=(
        {py_str(cfg["definition"] + " Amsterdam Batch2 candidate asset built from reviewed numericitems source rows pending variable-level approval.")}
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
    normalization_rule={py_str("amsterdam_numericitems_" + variable_id + "_batch2_source_specific_conversion")},
    official_expected_range_note="Amsterdam Batch2 candidate uses the public standard cleaned range; outliers are retained with null cleaned value.",
    global_contract_reference={py_str("Amsterdam same-name Batch2 candidate implementation preserving the public standard variable identity pending review.")},
    source_selection_reason={py_str(cfg["source_selection_reason"])},
    opening_status={py_str(str(cfg.get("opening_status", BATCH_STATUS)))},
    opening_review_date="{REVIEW_DATE}",
{source_filter_text})


def main() -> None:
    payload = builder.run_build(SPEC, Path(__file__))
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


def build_mapping_spec(variable_id: str, cfg: dict[str, object], variable_spec: dict[str, object]) -> dict[str, object]:
    mapping_spec = batch1.build_mapping_spec(variable_id, cfg, variable_spec)
    mapping_spec["created_at"] = REVIEW_DATE
    mapping_spec["artifact_status"] = "candidate_mapping_pending_user_review"
    mapping_spec["approval_status"] = BATCH_STATUS
    mapping_spec["review_state"] = {
        "current_stage": "candidate_runtime_evidence_built_pending_variable_review",
        "approval_gate": "do_not_treat_as_reviewed_approved_until formal variable-level review closes",
        "planned_review_path": REVIEW_PATH,
    }
    normalization = mapping_spec["representation_and_normalization"]
    normalization["normalization_rule_id"] = str(normalization["normalization_rule_id"]).replace("_batch1_", "_batch2_")
    mapping_spec["evidence_refs"]["formal_approval_review_path"] = REVIEW_PATH
    mapping_spec["evidence_refs"]["candidate_evidence_review_path"] = REVIEW_PATH
    return mapping_spec


def write_review_scaffold() -> None:
    rows = []
    for variable_id, cfg in VARIABLES.items():
        source_scope = ", ".join(f"{src['itemid']} {src['label']}" for src in cfg["items"])  # type: ignore[index]
        rows.append(
            f"| `{variable_id}` | `{cfg['unit']}` | `{source_scope}` | `{cfg['source_selection_reason']}` |"
        )
    review_path = PUBLIC_BASE / "AMSTERDAM_CLASS1_BATCH2_CANDIDATE_EVIDENCE_REVIEW.md"
    review_path.write_text(
        "# Amsterdam Class 1 Batch2 Candidate Evidence Review\n\n"
        f"Last updated: {REVIEW_DATE}\n\n"
        "Status: built_pending_user_review\n\n"
        "This note records the candidate source boundaries for the Amsterdam same-name-ready Batch2 Class 1 variables. "
        "It is intentionally not a formal approval review. Variable-level approval is reserved for the next review pass.\n\n"
        "## Batch Scope\n\n"
        "| variable | canonical unit | retained Amsterdam source itemids | candidate boundary |\n"
        "| --- | --- | --- | --- |\n"
        + "\n".join(rows)
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    _patch_batch1_runtime_constants()
    for variable_id, cfg in VARIABLES.items():
        public_dir = PUBLIC_BASE / variable_id
        existing_spec_path = public_dir / "variable_spec.json"
        existing_spec = (
            json.loads(existing_spec_path.read_text(encoding="utf-8"))
            if existing_spec_path.exists()
            else None
        )
        variable_spec = batch1.build_variable_spec(variable_id, cfg, existing_spec)
        write_json(existing_spec_path, variable_spec)
        write_execution_py(variable_id)
        write_local_extract(variable_id, cfg)
        write_json(public_dir / f"mapping_spec_{DATABASE_SLUG}.json", build_mapping_spec(variable_id, cfg, variable_spec))
    write_review_scaffold()
    print(f"Wrote Amsterdam same-name Batch2 candidate artifacts for {len(VARIABLES)} variables.")


if __name__ == "__main__":
    main()
