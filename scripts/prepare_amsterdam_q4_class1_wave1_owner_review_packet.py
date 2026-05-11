from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


REVIEW_DATE = "2026-05-05"
REPO_ROOT = Path(__file__).resolve().parents[1]
STD_MVP_DIR = REPO_ROOT / "docs" / "standard_system_mvp"
AUDIT_DIR = STD_MVP_DIR / "amsterdam_coverage_audit"

OLD_REPORT = STD_MVP_DIR / "AMSTERDAM_Q4_CLASS1_WAVE1_FORMAL_APPROVAL_REVIEW.md"
NEW_REPORT = STD_MVP_DIR / "AMSTERDAM_Q4_CLASS1_WAVE1_DETAILED_OWNER_REVIEW_PACKET.md"
OLD_SUMMARY_CSV = AUDIT_DIR / "amsterdam_q4_class1_wave1_formal_approval_review_summary.csv"
NEW_SUMMARY_CSV = AUDIT_DIR / "amsterdam_q4_class1_wave1_owner_review_summary.csv"
OLD_SUMMARY_JSON = AUDIT_DIR / "amsterdam_q4_class1_wave1_formal_approval_review_summary.json"
NEW_SUMMARY_JSON = AUDIT_DIR / "amsterdam_q4_class1_wave1_owner_review_summary.json"
OLD_REVIEW_PATH = "docs/standard_system_mvp/AMSTERDAM_Q4_CLASS1_WAVE1_FORMAL_APPROVAL_REVIEW.md"
NEW_REVIEW_PATH = "docs/standard_system_mvp/AMSTERDAM_Q4_CLASS1_WAVE1_DETAILED_OWNER_REVIEW_PACKET.md"
CANDIDATE_REVIEW_PATH = "docs/standard_system_mvp/AMSTERDAM_Q4_CLASS1_WAVE1_RUNTIME_CANDIDATE_REVIEW.md"
AMSTERDAM_SLUG = "amsterdamumcdb_1_0_2"
AMSTERDAM_ID = "AmsterdamUMCdb-1.0.2"
WORKSPACE_ROOT = REPO_ROOT.parent.parent
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

VARIABLES = tuple(sorted(APPROVE_RECOMMENDATIONS | CAVEAT_RECOMMENDATIONS))


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


def transform_decision(value: str, variable_id: str | None = None) -> str:
    if variable_id in VARIABLES and value in {"reviewed_approved", "reviewed_approved_with_caveat"}:
        return technical_recommendation(variable_id)
    return (
        value.replace("reviewed_approved_with_caveat", "technical_review_recommend_approve_with_caveat")
        .replace("reviewed_approved", "technical_review_recommend_approve")
    )


def build_owner_review_report() -> None:
    if OLD_REPORT.exists():
        text = OLD_REPORT.read_text(encoding="utf-8")
    elif NEW_REPORT.exists():
        text = NEW_REPORT.read_text(encoding="utf-8")
    else:
        raise FileNotFoundError("No Q4 Class1 Wave1 review report source exists.")

    text = text.replace(
        "# Amsterdam Q4 Class1 Wave1 Formal Approval Review",
        "# Amsterdam Q4 Class1 Wave1 Detailed Owner Review Packet",
    )
    text = re.sub(r"Status: .+", "Status: technical_review_complete_owner_approval_pending", text, count=1)
    text = re.sub(
        r"Owner approval note:.*?\n\n",
        (
            "Owner approval boundary: this document is a technical review packet only. "
            "It records Codex's recommendation after distribution, source, cross-database, "
            "official-document, and literature checks. It does not approve any variable. "
            "Promotion to `reviewed_approved` requires the project owner's later explicit approval.\n\n"
        ),
        text,
        count=1,
        flags=re.DOTALL,
    )
    text = text.replace("explicit decision", "explicit technical recommendation")
    text = text.replace("## Verdict Summary", "## Technical Recommendation Summary")
    text = text.replace("| variable | verdict |", "| variable | technical recommendation |")
    text = text.replace("The approved rows below are locked", "The reviewed candidate rows below are locked")
    text = text.replace("mapping is database-specific same-name/bounded-source approval", "mapping is a database-specific same-name/bounded-source owner-review candidate")
    text = text.replace("so approval carries", "so the recommendation carries")
    text = text.replace("This approval is", "This recommendation is")
    text = transform_decision(text)
    text = text.replace(
        "Promotion to `technical_review_recommend_approve` requires",
        "Promotion to `reviewed_approved` requires",
    )
    text = text.replace(
        "do not treat as technical_review_recommend_approve until",
        "do not treat as reviewed_approved until",
    )
    text = re.sub(
        r"- Decision: `(technical_review_recommend_approve(?:_with_caveat)?)`\..*",
        (
            r"- Technical recommendation: `\1`. Owner approval has not been recorded; "
            r"mapping, master-index, asset-manifest, and public-card status must remain "
            r"`not_owner_approved` / `built_pending_user_review` until the project owner explicitly approves."
        ),
        text,
    )
    text = text.replace("## Approval Action", "## Owner Approval Boundary")
    text = re.sub(
        r"The following actions were applied by `scripts/approve_amsterdam_q4_class1_wave1_reviewed_variables.py`:\n\n"
        r"- Amsterdam mapping specs:.*?\n"
        r"- Local Amsterdam Layer 5 master-index rows:.*?\n"
        r"- Local Amsterdam asset manifests:.*?\n"
        r"- Public cross-database cards should be regenerated after this script so MIMIC-IV-3.1 and AmsterdamUMCdb-1.0.2 are both listed\.\n",
        (
            "No approval action is applied by this packet. The corrected status propagation is:\n\n"
            "- Amsterdam mapping specs: `artifact_status=candidate_mapping_q4_class1_wave1_pending_user_review`, `approval_status=not_owner_approved`.\n"
            "- Local Amsterdam Layer 5 master-index rows and asset manifests: `current_status=built_pending_user_review`.\n"
            "- Public cross-database cards must not list AmsterdamUMCdb-1.0.2 for these variables until explicit owner approval is recorded.\n"
        ),
        text,
        count=1,
        flags=re.DOTALL,
    )
    text = text.replace(OLD_REVIEW_PATH, NEW_REVIEW_PATH)
    NEW_REPORT.write_text(text.rstrip() + "\n", encoding="utf-8")


def build_owner_review_summary_csv() -> None:
    if OLD_SUMMARY_CSV.exists():
        source = OLD_SUMMARY_CSV
        rows = list(csv.DictReader(source.open("r", encoding="utf-8", newline="")))
    else:
        source = NEW_SUMMARY_JSON
        payload = read_json(source)
        rows = payload.get("rows", [])
        if not isinstance(rows, list):
            raise RuntimeError(f"Summary JSON rows must be a list: {source}")
    if not rows:
        raise RuntimeError(f"No rows found in {source}")

    transformed: list[dict[str, str]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        variable_id = row["variable_id"]
        new_row: dict[str, str] = {}
        for key, value in row.items():
            text_value = json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else str(value)
            if key == "decision":
                new_row["technical_recommendation"] = technical_recommendation(variable_id)
            elif key == "technical_recommendation":
                new_row["technical_recommendation"] = technical_recommendation(variable_id)
            elif key == "decision_reason":
                new_row["recommendation_reason"] = text_value.replace("approval carries", "recommendation carries")
            elif key == "recommendation_reason":
                new_row["recommendation_reason"] = text_value.replace("approval carries", "recommendation carries")
            else:
                new_row[key] = transform_decision(text_value, variable_id)
        new_row["owner_approval_status"] = "owner_approval_pending"
        transformed.append(new_row)

    fieldnames: list[str] = []
    for row in transformed:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    NEW_SUMMARY_CSV.parent.mkdir(parents=True, exist_ok=True)
    with NEW_SUMMARY_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(transformed)


def transform_summary_json() -> None:
    source = OLD_SUMMARY_JSON if OLD_SUMMARY_JSON.exists() else NEW_SUMMARY_JSON
    payload = read_json(source)
    rows = payload.get("rows", [])
    if not isinstance(rows, list):
        raise RuntimeError(f"Summary JSON rows must be a list: {source}")

    recommendation_counts: Counter[str] = Counter()
    for row in rows:
        if not isinstance(row, dict):
            continue
        variable_id = str(row.get("variable_id", ""))
        recommendation = technical_recommendation(variable_id)
        row["technical_recommendation"] = recommendation
        row.pop("decision", None)
        if "decision_reason" in row:
            row["recommendation_reason"] = str(row.pop("decision_reason")).replace(
                "approval carries",
                "recommendation carries",
            )
        row["owner_approval_status"] = "owner_approval_pending"
        recommendation_counts[recommendation] += 1

    payload["artifact_type"] = "amsterdam_q4_class1_wave1_owner_review_summary"
    payload["review_date"] = REVIEW_DATE
    payload["owner_review_path"] = NEW_REVIEW_PATH
    payload["candidate_runtime_review_path"] = CANDIDATE_REVIEW_PATH
    payload["reviewed_variable_count"] = len(rows)
    payload["owner_approval_status"] = "owner_approval_pending"
    payload["recommendation_counts"] = dict(sorted(recommendation_counts.items()))
    payload.pop("formal_review_path", None)
    payload.pop("approved_variable_count", None)
    payload.pop("decision_counts", None)
    write_json(NEW_SUMMARY_JSON, payload)


def update_mapping_spec(variable_id: str) -> None:
    path = STD_MVP_DIR / variable_id / f"mapping_spec_{AMSTERDAM_SLUG}.json"
    mapping = read_json(path)
    recommendation = technical_recommendation(variable_id)
    mapping["artifact_status"] = "candidate_mapping_q4_class1_wave1_pending_user_review"
    mapping["approval_status"] = "not_owner_approved"
    mapping["mvp_phase"] = "amsterdam_q4_class1_wave1_owner_review_packet_pending_approval_mvp"
    evidence_refs = mapping.setdefault("evidence_refs", {})
    evidence_refs.pop("formal_approval_review_path", None)
    evidence_refs["owner_review_packet_path"] = NEW_REVIEW_PATH
    evidence_refs["candidate_evidence_review_path"] = CANDIDATE_REVIEW_PATH
    mapping["candidate_boundary_notice"] = {
        "status": "technical_review_packet_ready_owner_approval_pending",
        "owner_approval_status": "not_owner_approved",
        "reason": "Runtime evidence and detailed variable-level review packet exist, but project-owner approval has not been recorded.",
        "approval_gate": "do not treat as reviewed_approved until the project owner explicitly approves this variable",
        "owner_review_packet_path": NEW_REVIEW_PATH,
    }
    mapping["review_state"] = {
        "current_stage": "detailed_variable_review_packet_ready_pending_owner_approval",
        "approval_gate": "owner approval is explicit and is not implied by technical recommendation or runtime success",
        "planned_review_path": NEW_REVIEW_PATH,
        "technical_recommendation": recommendation,
    }
    mapping["technical_review_recommendation"] = {
        "review_date": REVIEW_DATE,
        "owner_review_packet_path": NEW_REVIEW_PATH,
        "recommendation": recommendation,
        "owner_approval_status": "owner_approval_pending",
    }
    mapping.pop("formal_approval", None)
    validation_contract = mapping.setdefault("validation_contract", {})
    if validation_contract.get("source_code_lock_rule") == "all rows must originate from the approved Amsterdam source itemids in this mapping spec":
        validation_contract["source_code_lock_rule"] = (
            "all rows must originate from the reviewed candidate Amsterdam source itemids in this mapping spec"
        )
    execution_contract = mapping.setdefault("execution_contract", {})
    if "formal_output_rule" in execution_contract:
        execution_contract["formal_output_rule"] = (
            f"The governed execution.py entrypoint reads this pending-review mapping spec and delegates "
            f"to the current local candidate implementation for {variable_id}."
        )
    if "non_bypassable_target_rule" in execution_contract:
        execution_contract["non_bypassable_target_rule"] = (
            f"Candidate {variable_id} outputs for AmsterdamUMCdb-1.0.2 should be produced only through "
            "the governed execution.py path until owner approval is explicit."
        )

    notes = validation_contract.setdefault("notes", [])
    cleaned_notes = [
        str(note)
        for note in notes
        if "Formal approval closed" not in str(note)
        and "reviewed_approved" not in str(note)
        and "owner approval is explicitly pending" not in str(note)
    ]
    pending_note = (
        f"Detailed owner review packet prepared on {REVIEW_DATE}; "
        f"technical_recommendation={recommendation}; owner approval remains pending; "
        f"review={NEW_REVIEW_PATH}."
    )
    if pending_note not in cleaned_notes:
        cleaned_notes.append(pending_note)
    mapping["validation_contract"]["notes"] = cleaned_notes
    write_json(path, mapping)


def reset_local_master_index_record(variable_id: str) -> None:
    sys.path.insert(0, str(REPO_ROOT / "scripts" / "layer5"))
    from master_index_helper import read_database_asset_records, upsert_database_asset_record

    records = read_database_asset_records(
        workbook_path=MASTER_INDEX_PATH,
        std_variable_id=variable_id,
        database_id=AMSTERDAM_ID,
    )
    if not records:
        return
    record = dict(records[0])
    recommendation = technical_recommendation(variable_id)
    record["current_status"] = "built_pending_user_review"
    record["latest_review_date"] = REVIEW_DATE
    record["remarks"] = (
        "Status corrected on 2026-05-05: detailed owner-review packet is ready, "
        f"technical_recommendation={recommendation}, owner approval remains pending. "
        "Do not count as reviewed_approved until explicit owner approval."
    )
    if isinstance(record.get("definition"), str):
        record["definition"] = (
            str(record["definition"])
            .replace("reviewed-approved asset built from locked numericitems source rows", "candidate asset built from reviewed numericitems source rows pending variable-level approval")
            .replace("after formal variable-level approval", "pending variable-level approval")
        )
    upsert_database_asset_record(workbook_path=MASTER_INDEX_PATH, record=record)


def reset_local_asset_manifest_text(variable_id: str) -> None:
    path = LOCAL_LAYER5_BASE / variable_id / "asset_manifest.md"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    text = text.replace("- `current_status`: `reviewed_approved`", "- `current_status`: `built_pending_user_review`")
    text = text.replace("reviewed-approved asset", "candidate asset")
    text = text.replace("after formal variable-level approval", "pending variable-level approval")
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def remove_erroneous_approval_artifacts() -> None:
    for path in (OLD_REPORT, OLD_SUMMARY_CSV, OLD_SUMMARY_JSON):
        if path.exists():
            path.unlink()


def main() -> None:
    build_owner_review_report()
    build_owner_review_summary_csv()
    transform_summary_json()
    for variable_id in VARIABLES:
        update_mapping_spec(variable_id)
        reset_local_master_index_record(variable_id)
        reset_local_asset_manifest_text(variable_id)
    remove_erroneous_approval_artifacts()
    print(f"Wrote owner-review packet for {len(VARIABLES)} Amsterdam Q4 Class1 Wave1 variables.")
    print("owner_approval_status=owner_approval_pending")


if __name__ == "__main__":
    main()
