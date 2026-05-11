from __future__ import annotations

import json
from pathlib import Path
from textwrap import dedent
from typing import Any

import build_amsterdam_same_name_batch1 as batch1


DATABASE_ID = "AmsterdamUMCdb-1.0.2"
DATABASE_SLUG = "amsterdamumcdb_1_0_2"
REVIEW_DATE = "2026-05-04"
BATCH_LABEL = "Q4 Class1 Wave1"
BATCH_STATUS = "built_pending_user_review"
REVIEW_PATH = "docs/standard_system_mvp/AMSTERDAM_Q4_CLASS1_WAVE1_RUNTIME_CANDIDATE_REVIEW.md"

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


VARIABLES: dict[str, dict[str, Any]] = {
    "std_anion_gap": {
        "name_en": "anion gap event",
        "intent": "routine chemistry anion gap observation",
        "definition": "A time-stamped anion gap measurement event.",
        "semantic_folder": "laboratory",
        "category": "laboratory",
        "unit": "mEq/L",
        "ucum": "meq/L",
        "precision": 1,
        "storage_type": "Float64",
        "cleaned_min": -5.0,
        "cleaned_max": 60.0,
        "normalized_col": "std_anion_gap_meq_per_l_normalized",
        "cleaned_col": "std_anion_gap_meq_per_l_cleaned",
        "source_value_class": "primary_direct_measurement",
        "items": [
            item(9559, "Anion-Gap (bloed)", None, "mmol/l", 1),
        ],
        "source_selection_reason": "Amsterdam Anion-Gap (bloed) numericitems rows are retained as the direct blood anion-gap source; non-anion calcium/procalcitonin false-positive rows from the broad Q4 scan are excluded.",
    },
    "std_amylase": {
        "name_en": "amylase event",
        "intent": "blood or plasma amylase observation",
        "definition": "A time-stamped blood or plasma amylase measurement event.",
        "semantic_folder": "laboratory",
        "category": "laboratory",
        "unit": "IU/L",
        "ucum": "[IU]/L",
        "precision": 0,
        "storage_type": "Int64",
        "cleaned_min": 1.0,
        "cleaned_max": 5000.0,
        "normalized_col": "std_amylase_iu_per_l_normalized",
        "cleaned_col": "std_amylase_iu_per_l_cleaned",
        "source_value_class": "primary_direct_measurement_with_specimen_scope_boundary",
        "items": [
            item(11986, "Amylase (bloed)", None, "E/l", 1),
            item(6845, "Plasma Amylase", None, "E/l", 2),
        ],
        "source_selection_reason": "Amsterdam blood/plasma amylase rows are retained and E/L is treated as IU/L; urine, drain, ascites, pleural, and generic other-fluid amylase rows are excluded from this blood/plasma same-name candidate.",
    },
    "std_lipase": {
        "name_en": "lipase event",
        "intent": "blood lipase observation",
        "definition": "A time-stamped blood lipase measurement event.",
        "semantic_folder": "laboratory",
        "category": "laboratory",
        "unit": "IU/L",
        "ucum": "[IU]/L",
        "precision": 0,
        "storage_type": "Int64",
        "cleaned_min": 1.0,
        "cleaned_max": 20000.0,
        "normalized_col": "std_lipase_iu_per_l_normalized",
        "cleaned_col": "std_lipase_iu_per_l_cleaned",
        "source_value_class": "primary_direct_measurement_with_specimen_scope_boundary",
        "items": [
            item(12043, "Lipase (bloed)", None, "E/l", 1),
        ],
        "source_selection_reason": "Amsterdam Lipase (bloed) numericitems rows are retained and E/L is treated as IU/L; other-fluid, ascites, drain, and no-unit legacy lipase rows are excluded.",
    },
    "std_ferritin": {
        "name_en": "ferritin event",
        "intent": "blood ferritin observation",
        "definition": "A time-stamped blood ferritin measurement event.",
        "semantic_folder": "laboratory",
        "category": "laboratory",
        "unit": "ng/mL",
        "ucum": "ng/mL",
        "precision": 1,
        "storage_type": "Float64",
        "cleaned_min": 0.5,
        "cleaned_max": 50000.0,
        "normalized_col": "std_ferritin_ng_per_ml_normalized",
        "cleaned_col": "std_ferritin_ng_per_ml_cleaned",
        "source_value_class": "primary_direct_measurement_with_unit_equivalence",
        "items": [
            item(10162, "Ferritine (bloed)", None, "µg/l", 1, 1.0, 0.0, "ferritin_ug_per_l_to_ng_per_ml_equivalent"),
            item(6971, "Ferritine", None, "ng/ml", 2),
        ],
        "source_selection_reason": "Amsterdam blood ferritin rows are retained; ug/L and ng/mL are numerically equivalent for ferritin concentration.",
    },
    "std_haptoglobin": {
        "name_en": "haptoglobin event",
        "intent": "blood haptoglobin observation",
        "definition": "A time-stamped blood haptoglobin measurement event.",
        "semantic_folder": "laboratory",
        "category": "laboratory",
        "unit": "mg/dL",
        "ucum": "mg/dL",
        "precision": 1,
        "storage_type": "Float64",
        "cleaned_min": 5.0,
        "cleaned_max": 700.0,
        "normalized_col": "std_haptoglobin_mg_per_dl_normalized",
        "cleaned_col": "std_haptoglobin_mg_per_dl_cleaned",
        "source_value_class": "primary_direct_measurement_with_unit_conversion",
        "items": [
            item(10129, "Haptoglobine (bloed)", None, "g/l", 1, 100.0, 0.0, "haptoglobin_g_per_l_to_mg_per_dl"),
        ],
        "source_selection_reason": "Amsterdam Haptoglobine (bloed) rows are retained and converted from g/L to mg/dL.",
    },
    "std_magnesium": {
        "name_en": "magnesium event",
        "intent": "blood magnesium observation",
        "definition": "A time-stamped blood or serum magnesium measurement event.",
        "semantic_folder": "laboratory",
        "category": "laboratory",
        "unit": "mg/dL",
        "ucum": "mg/dL",
        "precision": 1,
        "storage_type": "Float64",
        "cleaned_min": 0.1,
        "cleaned_max": 10.0,
        "normalized_col": "std_magnesium_mg_per_dl_normalized",
        "cleaned_col": "std_magnesium_mg_per_dl_cleaned",
        "source_value_class": "primary_direct_measurement_with_unit_conversion",
        "items": [
            item(9952, "Magnesium (bloed)", None, "mmol/l", 1, 2.4305, 0.0, "magnesium_mmol_per_l_to_mg_per_dl"),
            item(6839, "Magnesium", None, "mmol/l", 2, 2.4305, 0.0, "magnesium_mmol_per_l_to_mg_per_dl"),
        ],
        "source_selection_reason": "Amsterdam blood/serum magnesium rows are retained and converted from mmol/L to mg/dL; urine, dialysate, other-fluid, and medication magnesium rows are excluded.",
    },
    "std_phosphate": {
        "name_en": "phosphate event",
        "intent": "blood phosphate observation",
        "definition": "A time-stamped blood or serum phosphate measurement event.",
        "semantic_folder": "laboratory",
        "category": "laboratory",
        "unit": "mg/dL",
        "ucum": "mg/dL",
        "precision": 1,
        "storage_type": "Float64",
        "cleaned_min": 0.1,
        "cleaned_max": 20.0,
        "normalized_col": "std_phosphate_mg_per_dl_normalized",
        "cleaned_col": "std_phosphate_mg_per_dl_cleaned",
        "source_value_class": "primary_direct_measurement_with_unit_conversion",
        "items": [
            item(9935, "Fosfaat (bloed)", None, "mmol/l", 1, 3.096, 0.0, "phosphate_mmol_per_l_to_mg_per_dl"),
            item(6828, "Fosfaat", None, "mmol/l", 2, 3.096, 0.0, "phosphate_mmol_per_l_to_mg_per_dl"),
        ],
        "source_selection_reason": "Amsterdam blood/serum phosphate rows are retained and converted from mmol/L to mg/dL; urine, 24-hour urine, and medication phosphate rows are excluded.",
    },
    "std_osmolality_measured": {
        "name_en": "measured osmolality event",
        "intent": "blood measured osmolality observation",
        "definition": "A time-stamped measured blood osmolality event.",
        "semantic_folder": "laboratory",
        "category": "laboratory",
        "unit": "mOsm/kg",
        "ucum": "mosm/kg",
        "precision": 0,
        "storage_type": "Int64",
        "cleaned_min": 100.0,
        "cleaned_max": 450.0,
        "normalized_col": "std_osmolality_measured_mosm_per_kg_normalized",
        "cleaned_col": "std_osmolality_measured_mosm_per_kg_cleaned",
        "source_value_class": "primary_direct_measurement_with_specimen_scope_boundary",
        "items": [
            item(11918, "Osmolaliteit (bloed)", None, "mosmol/kg", 1),
        ],
        "source_selection_reason": "Amsterdam Osmolaliteit (bloed) rows are retained as measured blood osmolality; urine, stool, other-fluid, nutrition product, and no-unit legacy osmolality rows are excluded.",
    },
    "std_total_cholesterol": {
        "name_en": "total cholesterol event",
        "intent": "blood total cholesterol observation",
        "definition": "A time-stamped blood total cholesterol measurement event.",
        "semantic_folder": "laboratory",
        "category": "laboratory",
        "unit": "mg/dL",
        "ucum": "mg/dL",
        "precision": 1,
        "storage_type": "Float64",
        "cleaned_min": 1.0,
        "cleaned_max": 500.0,
        "normalized_col": "std_total_cholesterol_mg_per_dl_normalized",
        "cleaned_col": "std_total_cholesterol_mg_per_dl_cleaned",
        "source_value_class": "primary_direct_measurement_with_unit_conversion",
        "items": [
            item(9954, "Cholesterol (bloed)", None, "mmol/l", 1, 38.67, 0.0, "cholesterol_mmol_per_l_to_mg_per_dl"),
            item(6820, "Cholesterol", None, "mmol/l", 2, 38.67, 0.0, "cholesterol_mmol_per_l_to_mg_per_dl"),
        ],
        "source_selection_reason": "Amsterdam blood/serum cholesterol rows are retained and converted from mmol/L to mg/dL; broad Q4 false-positive total-volume and bilirubin rows are excluded.",
    },
    "std_troponin_t": {
        "name_en": "troponin T event",
        "intent": "blood troponin T observation",
        "definition": "A time-stamped blood troponin T measurement event.",
        "semantic_folder": "laboratory",
        "category": "laboratory",
        "unit": "ng/mL",
        "ucum": "ng/mL",
        "precision": 3,
        "storage_type": "Float64",
        "cleaned_min": 0.0,
        "cleaned_max": 30.0,
        "normalized_col": "std_troponin_t_ng_per_ml_normalized",
        "cleaned_col": "std_troponin_t_ng_per_ml_cleaned",
        "source_value_class": "primary_direct_measurement_with_unit_equivalence",
        "items": [
            item(10407, "TroponineT (bloed)", None, "µg/l", 1, 1.0, 0.0, "troponin_t_ug_per_l_to_ng_per_ml_equivalent"),
            item(8115, "Troponine", None, "ng/ml", 2),
        ],
        "source_selection_reason": "Amsterdam blood troponin T rows are retained; ug/L and ng/mL are numerically equivalent. The single other-fluid troponin row is excluded.",
    },
}


def _patch_batch1_runtime_constants() -> None:
    batch1.REVIEW_DATE = REVIEW_DATE


def py_str(value: object) -> str:
    return repr(value)


def write_local_extract(variable_id: str, cfg: dict[str, Any]) -> None:
    extract_dir = LOCAL_LAYER5_BASE / variable_id / "extract_code"
    extract_dir.mkdir(parents=True, exist_ok=True)
    source_items = []
    for src in cfg["items"]:
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


PROCESS_BATCH_VARIABLE_ID = {py_str(variable_id)}


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
        {py_str(cfg["definition"] + " Amsterdam Q4 Class1 Wave1 candidate asset built from reviewed numericitems source rows pending variable-level approval.")}
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
    normalization_rule={py_str("amsterdam_numericitems_" + variable_id + "_q4_class1_wave1_source_specific_conversion")},
    official_expected_range_note="Amsterdam Q4 Class1 Wave1 candidate uses the public standard cleaned range; outliers are retained with null cleaned value.",
    global_contract_reference={py_str("Amsterdam Q4 bounded candidate preserving the public standard variable identity pending detailed review.")},
    source_selection_reason={py_str(cfg["source_selection_reason"])},
    opening_status={py_str(BATCH_STATUS)},
    opening_review_date="{REVIEW_DATE}",
)


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


def build_mapping_spec(variable_id: str, cfg: dict[str, Any], variable_spec: dict[str, Any]) -> dict[str, Any]:
    mapping_spec = batch1.build_mapping_spec(variable_id, cfg, variable_spec)
    mapping_spec["created_at"] = REVIEW_DATE
    mapping_spec["artifact_status"] = "candidate_mapping_q4_class1_wave1_pending_user_review"
    mapping_spec["approval_status"] = "not_owner_approved"
    mapping_spec["mvp_phase"] = "amsterdam_q4_class1_wave1_build_first_candidate_mvp"
    mapping_spec["candidate_boundary_notice"] = {
        "status": "built_candidate_owner_approval_pending",
        "owner_approval_status": "not_owner_approved",
        "reason": "Q4 bounded-candidate runtime evidence exists, but variable-level source/distribution review and project-owner approval are still pending.",
        "approval_gate": "do not treat as reviewed_approved until the detailed review packet is explicitly approved",
    }
    mapping_spec["review_state"] = {
        "current_stage": "candidate_runtime_evidence_built_pending_variable_review",
        "approval_gate": "owner approval is explicit and is not implied by runtime success",
        "planned_review_path": REVIEW_PATH,
    }
    normalization = mapping_spec["representation_and_normalization"]
    normalization["normalization_rule_id"] = str(normalization["normalization_rule_id"]).replace(
        "_batch1_",
        "_q4_class1_wave1_",
    )
    validation = mapping_spec["validation_contract"]
    validation["notes"] = [
        "Build-first Q4 bounded candidate mapping; owner approval is explicitly pending.",
        str(cfg["source_selection_reason"]),
    ]
    mapping_spec["evidence_refs"]["formal_approval_review_path"] = REVIEW_PATH
    mapping_spec["evidence_refs"]["candidate_evidence_review_path"] = REVIEW_PATH
    return mapping_spec


def load_json_if_exists(path: Path) -> dict[str, Any] | None:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def load_runtime_summary(variable_id: str) -> dict[str, Any]:
    summary_path = (
        LOCAL_LAYER5_BASE
        / variable_id
        / "query_summary"
        / f"{variable_id}_amsterdam_review_summary.json"
    )
    if not summary_path.exists():
        return {}
    return json.loads(summary_path.read_text(encoding="utf-8"))


def runtime_status(variable_id: str) -> str:
    runtime_dir = PUBLIC_BASE / variable_id / "runtime"
    first = runtime_dir / f"{DATABASE_SLUG}_q4_class1_wave1_first_candidate_execution"
    rerun = runtime_dir / f"{DATABASE_SLUG}_q4_class1_wave1_rerun_repro_check"
    if (rerun / "reproducibility_report.json").exists():
        try:
            report = json.loads((rerun / "reproducibility_report.json").read_text(encoding="utf-8"))
            if report.get("overall_status") == "pass":
                return "runtime_and_rerun_repro_pass"
        except json.JSONDecodeError:
            return "runtime_repro_report_invalid"
    if (first / "validation_report.json").exists():
        return "first_runtime_present_rerun_missing"
    return "runtime_not_yet_run"


def source_scope(cfg: dict[str, Any]) -> str:
    return "; ".join(
        f"{src['itemid']} {src['label']} ({src['unit']}; factor={src['factor']})"
        for src in cfg["items"]
    )


def review_row(variable_id: str, cfg: dict[str, Any]) -> list[str]:
    summary = load_runtime_summary(variable_id)
    nested = summary.get("review_summary", {}) if summary else {}
    source_items = summary.get("source_item_rows_after_dedup", []) if summary else []
    total_rows = nested.get("total_rows", "")
    kept_rows = nested.get("kept_rows", "")
    unique_admissions = nested.get("unique_admissions", "")
    raw_p50 = nested.get("raw_p50", "")
    raw_p99 = nested.get("raw_p99", "")
    kept_p50 = nested.get("kept_p50", "")
    kept_p99 = nested.get("kept_p99", "")
    item_rows = "; ".join(
        f"{item.get('source_itemid_raw')}={item.get('total_rows_after_dedup')}"
        for item in source_items
    )
    return [
        f"`{variable_id}`",
        f"`{cfg['unit']}`",
        f"`{runtime_status(variable_id)}`",
        f"`{total_rows}`",
        f"`{kept_rows}`",
        f"`{unique_admissions}`",
        f"`{raw_p50}`",
        f"`{raw_p99}`",
        f"`{kept_p50}`",
        f"`{kept_p99}`",
        f"`{item_rows}`",
        source_scope(cfg),
        str(cfg["source_selection_reason"]),
    ]


def write_review_scaffold() -> None:
    review_path = PUBLIC_BASE / "AMSTERDAM_Q4_CLASS1_WAVE1_RUNTIME_CANDIDATE_REVIEW.md"
    headers = [
        "variable",
        "unit",
        "runtime status",
        "rows",
        "kept",
        "stays",
        "raw p50",
        "raw p99",
        "kept p50",
        "kept p99",
        "rows by item",
        "retained Amsterdam source boundary",
        "candidate caveat",
    ]
    lines = [
        "# Amsterdam Q4 Class1 Wave1 Runtime Candidate Review",
        "",
        f"Last updated: {REVIEW_DATE}",
        "",
        "Status: built-first candidate runtime evidence; owner approval not requested and not implied",
        "",
        "## Scope",
        "",
        (
            "This packet covers the first high-confidence Q4 Class1 numeric bounded-candidate wave. "
            "Variables were selected only when the Amsterdam item label, source unit, specimen scope, "
            "and deterministic unit conversion were clear enough for runtime construction."
        ),
        "",
        "Excluded from this wave: specimen/body-fluid variables with unresolved modifier boundaries, broad alias false positives, and variables needing parent/component approval.",
        "",
        "## Candidate Runtime Summary",
        "",
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for variable_id, cfg in VARIABLES.items():
        row = [cell.replace("\n", " ").replace("|", "/") for cell in review_row(variable_id, cfg)]
        lines.append("| " + " | ".join(row) + " |")
    lines.extend(
        [
            "",
            "## Approval Boundary",
            "",
            "These rows are candidate runtime evidence only. Detailed owner-facing review still needs the full per-variable distribution comparison, source-document agreement, and cross-database/epidemiology plausibility check required by `VARIABLE_REVIEW_REPORTING_STANDARD.md`.",
            "",
        ]
    )
    review_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    _patch_batch1_runtime_constants()
    for variable_id, cfg in VARIABLES.items():
        public_dir = PUBLIC_BASE / variable_id
        existing_spec_path = public_dir / "variable_spec.json"
        existing_spec = load_json_if_exists(existing_spec_path)
        variable_spec = batch1.build_variable_spec(variable_id, cfg, existing_spec)
        write_json(existing_spec_path, variable_spec)
        write_execution_py(variable_id)
        write_local_extract(variable_id, cfg)
        write_json(
            public_dir / f"mapping_spec_{DATABASE_SLUG}.json",
            build_mapping_spec(variable_id, cfg, variable_spec),
        )
    write_review_scaffold()
    runtime_plan = {
        "artifact_type": "amsterdam_q4_class1_wave1_runtime_plan",
        "created_at": REVIEW_DATE,
        "database_id": DATABASE_ID,
        "owner_approval_status": "not_owner_approved",
        "variables": list(VARIABLES),
        "first_runtime_dir_suffix": f"{DATABASE_SLUG}_q4_class1_wave1_first_candidate_execution",
        "rerun_runtime_dir_suffix": f"{DATABASE_SLUG}_q4_class1_wave1_rerun_repro_check",
        "review_packet": REVIEW_PATH,
    }
    write_json(
        PUBLIC_BASE / "amsterdam_coverage_audit" / "amsterdam_q4_class1_wave1_runtime_plan.json",
        runtime_plan,
    )
    print(f"Wrote Amsterdam {BATCH_LABEL} candidate artifacts for {len(VARIABLES)} variables.")


if __name__ == "__main__":
    main()
