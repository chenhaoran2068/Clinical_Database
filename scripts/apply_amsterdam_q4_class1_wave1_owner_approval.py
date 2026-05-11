from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


APPROVAL_DATE = "2026-05-08"
REPO_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = REPO_ROOT.parent.parent
STD_MVP_DIR = REPO_ROOT / "docs" / "standard_system_mvp"
AUDIT_DIR = STD_MVP_DIR / "amsterdam_coverage_audit"
AMSTERDAM_ID = "AmsterdamUMCdb-1.0.2"
AMSTERDAM_SLUG = "amsterdamumcdb_1_0_2"

OWNER_REVIEW_PACKET = STD_MVP_DIR / "AMSTERDAM_Q4_CLASS1_WAVE1_DETAILED_OWNER_REVIEW_PACKET.md"
OWNER_REVIEW_PATH = "docs/standard_system_mvp/AMSTERDAM_Q4_CLASS1_WAVE1_DETAILED_OWNER_REVIEW_PACKET.md"
OWNER_SUMMARY_CSV = AUDIT_DIR / "amsterdam_q4_class1_wave1_owner_review_summary.csv"
OWNER_SUMMARY_JSON = AUDIT_DIR / "amsterdam_q4_class1_wave1_owner_review_summary.json"
OWNER_APPROVAL_RECORD = STD_MVP_DIR / "AMSTERDAM_Q4_CLASS1_WAVE1_OWNER_APPROVAL_RECORD.md"
OWNER_APPROVAL_RECORD_PATH = "docs/standard_system_mvp/AMSTERDAM_Q4_CLASS1_WAVE1_OWNER_APPROVAL_RECORD.md"
CANDIDATE_REVIEW_PATH = "docs/standard_system_mvp/AMSTERDAM_Q4_CLASS1_WAVE1_RUNTIME_CANDIDATE_REVIEW.md"

MASTER_INDEX_PATH = (
    WORKSPACE_ROOT
    / "Methods"
    / "Clinical_Database"
    / "local_work"
    / "Layer 5"
    / "Global"
    / "Layer5_StdVariable_MasterIndex.xlsx"
)
LOCAL_LAYER5_BASE = (
    WORKSPACE_ROOT
    / "Methods"
    / "Clinical_Database"
    / "local_work"
    / "Layer 5"
    / AMSTERDAM_ID
)

APPROVE_RECOMMENDATIONS = {
    "std_amylase",
    "std_lipase",
    "std_magnesium",
    "std_phosphate",
    "std_total_cholesterol",
}

CAVEAT_RECOMMENDATIONS = {
    "std_anion_gap",
    "std_ferritin",
    "std_haptoglobin",
    "std_osmolality_measured",
    "std_troponin_t",
}

VARIABLES = (
    "std_anion_gap",
    "std_amylase",
    "std_lipase",
    "std_ferritin",
    "std_haptoglobin",
    "std_magnesium",
    "std_phosphate",
    "std_osmolality_measured",
    "std_total_cholesterol",
    "std_troponin_t",
)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def technical_recommendation(variable_id: str) -> str:
    if variable_id in CAVEAT_RECOMMENDATIONS:
        return "technical_review_recommend_approve_with_caveat"
    if variable_id in APPROVE_RECOMMENDATIONS:
        return "technical_review_recommend_approve"
    raise KeyError(variable_id)


def approval_decision_label(variable_id: str) -> str:
    if variable_id in CAVEAT_RECOMMENDATIONS:
        return "reviewed_approved_with_caveat"
    return "reviewed_approved"


def load_summary_rows() -> list[dict[str, Any]]:
    if OWNER_SUMMARY_JSON.exists():
        payload = read_json(OWNER_SUMMARY_JSON)
        rows = payload.get("rows", [])
        if isinstance(rows, list):
            return [row for row in rows if isinstance(row, dict)]
    if OWNER_SUMMARY_CSV.exists():
        with OWNER_SUMMARY_CSV.open("r", encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle))
    return []


def row_by_variable() -> dict[str, dict[str, Any]]:
    rows = load_summary_rows()
    return {str(row.get("variable_id")): row for row in rows}


def recommendation_reason(variable_id: str, rows: dict[str, dict[str, Any]]) -> str:
    row = rows.get(variable_id, {})
    for key in ("recommendation_reason", "decision_reason"):
        value = str(row.get(key, "")).strip()
        if value:
            return value
    return "Owner approved after detailed Q4 Class1 Wave1 review packet."


def update_mapping_spec(variable_id: str, rows: dict[str, dict[str, Any]]) -> None:
    path = STD_MVP_DIR / variable_id / f"mapping_spec_{AMSTERDAM_SLUG}.json"
    mapping = read_json(path)
    decision = approval_decision_label(variable_id)
    recommendation = technical_recommendation(variable_id)
    reason = recommendation_reason(variable_id, rows)

    mapping["artifact_status"] = "reviewed_approved_public_mapping_lock"
    mapping["approval_status"] = "reviewed_approved"
    mapping["mvp_phase"] = "amsterdam_q4_class1_wave1_owner_approved_mvp"
    evidence_refs = mapping.setdefault("evidence_refs", {})
    evidence_refs["owner_review_packet_path"] = OWNER_REVIEW_PATH
    evidence_refs["owner_approval_record_path"] = OWNER_APPROVAL_RECORD_PATH
    evidence_refs["candidate_evidence_review_path"] = CANDIDATE_REVIEW_PATH

    mapping["candidate_boundary_notice"] = {
        "status": "superseded_by_owner_approval",
        "owner_approval_status": "reviewed_approved",
        "owner_approval_date": APPROVAL_DATE,
        "owner_review_packet_path": OWNER_REVIEW_PATH,
        "owner_approval_record_path": OWNER_APPROVAL_RECORD_PATH,
    }
    mapping["review_state"] = {
        "current_stage": "formal_variable_review_closed_owner_approved",
        "approval_gate": f"owner_approved_on_{APPROVAL_DATE}",
        "review_path": OWNER_REVIEW_PATH,
        "owner_approval_record_path": OWNER_APPROVAL_RECORD_PATH,
        "technical_recommendation": recommendation,
        "decision_label": decision,
    }
    mapping["technical_review_recommendation"] = {
        "review_date": "2026-05-05",
        "owner_review_packet_path": OWNER_REVIEW_PATH,
        "recommendation": recommendation,
        "owner_approval_status": "owner_approved",
        "owner_approval_date": APPROVAL_DATE,
    }
    mapping["formal_approval"] = {
        "owner_approval_date": APPROVAL_DATE,
        "owner_approval_record_path": OWNER_APPROVAL_RECORD_PATH,
        "owner_review_packet_path": OWNER_REVIEW_PATH,
        "approval_status": "reviewed_approved",
        "decision_label": decision,
        "technical_recommendation": recommendation,
        "decision_reason": reason,
    }

    validation_contract = mapping.setdefault("validation_contract", {})
    if validation_contract.get("source_code_lock_rule") == (
        "all rows must originate from the reviewed candidate Amsterdam source itemids in this mapping spec"
    ):
        validation_contract["source_code_lock_rule"] = (
            "all rows must originate from the approved Amsterdam source itemids in this mapping spec"
        )
    notes = validation_contract.setdefault("notes", [])
    cleaned_notes = [
        str(note)
        for note in notes
        if "owner approval remains pending" not in str(note)
        and "Detailed owner review packet prepared" not in str(note)
        and "Owner approval recorded" not in str(note)
    ]
    approval_note = (
        f"Owner approval recorded on {APPROVAL_DATE}; approval_status=reviewed_approved; "
        f"decision={decision}; review={OWNER_REVIEW_PATH}; record={OWNER_APPROVAL_RECORD_PATH}."
    )
    cleaned_notes.append(approval_note)
    validation_contract["notes"] = cleaned_notes

    execution_contract = mapping.setdefault("execution_contract", {})
    execution_contract["formal_output_rule"] = (
        f"The governed execution.py entrypoint reads this owner-approved mapping spec and delegates "
        f"to the current local reviewed implementation for {variable_id}."
    )
    execution_contract["non_bypassable_target_rule"] = (
        f"Formal {variable_id} outputs for AmsterdamUMCdb-1.0.2 should be produced only through "
        "the governed execution.py path."
    )
    write_json(path, mapping)


def update_local_extract_status(variable_id: str) -> None:
    path = LOCAL_LAYER5_BASE / variable_id / "extract_code" / f"Extract_Code_{variable_id}.py"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    text = text.replace("pending variable-level approval", "after explicit owner approval")
    text = text.replace("pending detailed review", "after explicit owner approval")
    text = re.sub(r"opening_status=['\"]built_pending_user_review['\"]", 'opening_status="reviewed_approved"', text)
    text = re.sub(r"opening_review_date=['\"]20\d\d-\d\d-\d\d['\"]", f'opening_review_date="{APPROVAL_DATE}"', text)
    path.write_text(text, encoding="utf-8")


def update_local_asset_manifest_text(variable_id: str) -> None:
    path = LOCAL_LAYER5_BASE / variable_id / "asset_manifest.md"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    text = text.replace("- `current_status`: `built_pending_user_review`", "- `current_status`: `reviewed_approved`")
    text = re.sub(r"- `latest_review_date`: `20\d\d-\d\d-\d\d`", f"- `latest_review_date`: `{APPROVAL_DATE}`", text)
    text = text.replace("candidate asset", "reviewed-approved asset")
    text = text.replace("pending variable-level approval", "after explicit owner approval")
    text = text.rstrip()
    if "## Owner Approval" not in text:
        text += (
            "\n\n## Owner Approval\n\n"
            f"- `owner_approval_status`: `reviewed_approved`\n"
            f"- `owner_approval_date`: `{APPROVAL_DATE}`\n"
            f"- `owner_review_packet_path`: `{OWNER_REVIEW_PATH}`\n"
            f"- `owner_approval_record_path`: `{OWNER_APPROVAL_RECORD_PATH}`\n"
        )
    path.write_text(text + "\n", encoding="utf-8")


def update_master_index_record(variable_id: str, rows: dict[str, dict[str, Any]]) -> None:
    sys.path.insert(0, str(REPO_ROOT / "scripts" / "layer5"))
    from master_index_helper import read_database_asset_records, upsert_database_asset_record

    records = read_database_asset_records(
        workbook_path=MASTER_INDEX_PATH,
        std_variable_id=variable_id,
        database_id=AMSTERDAM_ID,
    )
    if not records:
        raise RuntimeError(f"No Amsterdam master-index row found for {variable_id}")
    record = dict(records[0])
    decision = approval_decision_label(variable_id)
    reason = recommendation_reason(variable_id, rows)
    record["current_status"] = "reviewed_approved"
    record["materialization_status"] = "materialized"
    record["latest_review_date"] = APPROVAL_DATE
    record["remarks"] = (
        f"Owner approval recorded on {APPROVAL_DATE}; decision={decision}; "
        f"{reason}"
    )
    if isinstance(record.get("definition"), str):
        record["definition"] = (
            str(record["definition"])
            .replace("candidate asset built from reviewed numericitems source rows pending variable-level approval", "reviewed-approved asset built from locked numericitems source rows")
            .replace("pending variable-level approval", "after explicit owner approval")
        )
    upsert_database_asset_record(workbook_path=MASTER_INDEX_PATH, record=record)


def update_owner_review_packet(rows: dict[str, dict[str, Any]]) -> None:
    text = OWNER_REVIEW_PACKET.read_text(encoding="utf-8")
    text = re.sub(r"Last updated: \d{4}-\d{2}-\d{2}", f"Last updated: {APPROVAL_DATE}", text, count=1)
    text = re.sub(r"Status: .+", "Status: reviewed_approved_by_owner", text, count=1)
    text = re.sub(
        r"Owner approval boundary:.*?\n\n",
        (
            f"Owner approval note: the project owner explicitly approved all ten variables on {APPROVAL_DATE}. "
            "This packet now records both the technical review and the owner approval decision. "
            "Caveat-bearing variables remain approved but must carry their documented caveats in downstream review.\n\n"
        ),
        text,
        count=1,
        flags=re.DOTALL,
    )
    text = re.sub(
        r"- Technical recommendation: `(technical_review_recommend_approve(?:_with_caveat)?)`\..*",
        (
            r"- Owner approval decision: `reviewed_approved`. Technical recommendation: `\1`. "
            r"Owner approval was recorded on `2026-05-08`; caveats remain active where listed."
        ),
        text,
    )
    text = re.sub(
        r"## Owner Approval Boundary\n\nNo approval action is applied by this packet\..*?(?=\n## References)",
        (
            "## Owner Approval Action\n\n"
            f"Owner approval was recorded on `{APPROVAL_DATE}` for all ten variables in this packet.\n\n"
            "- Amsterdam mapping specs: `artifact_status=reviewed_approved_public_mapping_lock`, `approval_status=reviewed_approved`.\n"
            "- Local Amsterdam Layer 5 master-index rows and asset manifests: `current_status=reviewed_approved`.\n"
            "- Public cross-database cards should list AmsterdamUMCdb-1.0.2 after approved runtime evidence is rerun.\n"
        ),
        text,
        count=1,
        flags=re.DOTALL,
    )
    OWNER_REVIEW_PACKET.write_text(text.rstrip() + "\n", encoding="utf-8")


def write_owner_approval_record(rows: dict[str, dict[str, Any]]) -> None:
    lines = [
        "# Amsterdam Q4 Class1 Wave1 Owner Approval Record",
        "",
        f"Approval date: {APPROVAL_DATE}",
        "",
        "Status: reviewed_approved_by_owner",
        "",
        "Scope: AmsterdamUMCdb-1.0.2 Q4 Class1 Wave1 ten variables reviewed in `AMSTERDAM_Q4_CLASS1_WAVE1_DETAILED_OWNER_REVIEW_PACKET.md`.",
        "",
        "| variable | owner approval | technical recommendation | caveat retained |",
        "| --- | --- | --- | --- |",
    ]
    for variable_id in VARIABLES:
        decision = approval_decision_label(variable_id)
        recommendation = technical_recommendation(variable_id)
        caveat = "yes" if decision.endswith("_with_caveat") else "no"
        lines.append(f"| `{variable_id}` | `reviewed_approved` | `{recommendation}` | `{caveat}` |")
    lines.extend(
        [
            "",
            "Approval boundary:",
            "",
            "- This record applies only to the ten variables listed above.",
            "- Caveats documented in the owner review packet remain part of the approved interpretation.",
            "- Adjacent specimen/body-fluid, calculated, proxy, medication, and parent-dependent variables remain outside this approval.",
            "",
        ]
    )
    OWNER_APPROVAL_RECORD.write_text("\n".join(lines), encoding="utf-8")


def update_summary_files(rows: dict[str, dict[str, Any]]) -> None:
    payload = read_json(OWNER_SUMMARY_JSON)
    summary_rows = payload.get("rows", [])
    decision_counts: Counter[str] = Counter()
    for row in summary_rows:
        if not isinstance(row, dict):
            continue
        variable_id = str(row.get("variable_id", ""))
        if variable_id not in VARIABLES:
            continue
        decision = approval_decision_label(variable_id)
        row["owner_approval_status"] = "owner_approved"
        row["owner_approval_date"] = APPROVAL_DATE
        row["approval_status"] = "reviewed_approved"
        row["approval_decision_label"] = decision
        row["owner_approval_record_path"] = OWNER_APPROVAL_RECORD_PATH
        decision_counts[decision] += 1
    payload["artifact_type"] = "amsterdam_q4_class1_wave1_owner_approved_review_summary"
    payload["owner_approval_status"] = "owner_approved"
    payload["owner_approval_date"] = APPROVAL_DATE
    payload["owner_approval_record_path"] = OWNER_APPROVAL_RECORD_PATH
    payload["approved_variable_count"] = len(VARIABLES)
    payload["approval_decision_counts"] = dict(sorted(decision_counts.items()))
    write_json(OWNER_SUMMARY_JSON, payload)

    fieldnames: list[str] = []
    csv_rows: list[dict[str, Any]] = []
    for row in summary_rows:
        if not isinstance(row, dict):
            continue
        flat: dict[str, Any] = {}
        for key, value in row.items():
            flat[key] = json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else value
        csv_rows.append(flat)
        for key in flat:
            if key not in fieldnames:
                fieldnames.append(key)
    with OWNER_SUMMARY_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_rows)


def main() -> None:
    rows = row_by_variable()
    missing = sorted(set(VARIABLES) - set(rows))
    if missing:
        raise RuntimeError(f"Owner review summary is missing rows: {missing}")
    write_owner_approval_record(rows)
    update_owner_review_packet(rows)
    update_summary_files(rows)
    for variable_id in VARIABLES:
        update_mapping_spec(variable_id, rows)
        update_local_extract_status(variable_id)
        update_local_asset_manifest_text(variable_id)
        update_master_index_record(variable_id, rows)
    print(f"Applied owner approval for {len(VARIABLES)} Amsterdam Q4 Class1 Wave1 variables.")
    print("approval_status=reviewed_approved")


if __name__ == "__main__":
    main()
