from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
AUDIT_DIR = REPO_ROOT / "docs" / "standard_system_mvp" / "amsterdam_coverage_audit"
SOURCE_AUDIT_CSV = AUDIT_DIR / "amsterdam_variable_coverage_audit.csv"
OUTPUT_CSV = AUDIT_DIR / "amsterdam_class1_to_class9_execution_queue.csv"
OUTPUT_JSON = AUDIT_DIR / "amsterdam_class1_to_class9_execution_queue.json"
OUTPUT_MD = REPO_ROOT / "docs" / "standard_system_mvp" / "CLASS1_TO_CLASS9_EXECUTION_QUEUE.md"
STD_MVP_DIR = REPO_ROOT / "docs" / "standard_system_mvp"
CARD_DIR = REPO_ROOT / "docs" / "std_variable_cards"


CLASS_LABELS = {
    "class1_event_level_numeric": "Class 1: event-level numeric primary-source",
    "class2_baseline_summary_window_numeric": "Class 2: baseline/summary/window numeric",
    "class3_binary_state_episode": "Class 3: binary state/active flag/episode",
    "class4_treatment_device_io_event_stream": "Class 4: treatment/device/input-output event stream",
    "class5_episode_interval_bridge": "Class 5: episode/interval/follow-up bridge",
    "class6_ordinal_text_semiquantitative_result": "Class 6: ordinal/text/semiquantitative result",
    "class7_diagnosis_admin_demographic_id_map": "Class 7: diagnosis/admin/demographic/id-map",
    "class8_score_phenotype_composite_derived": "Class 8: score/phenotype/composite derived",
    "class9_microbiology_multi_entity_family": "Class 9: microbiology multi-entity family",
}

CLASS_RANK = {class_id: idx for idx, class_id in enumerate(CLASS_LABELS, start=1)}

QUEUE_LABELS = {
    "Q0_already_public_covered": "Already public-covered; no new build needed in this campaign",
    "Q1_technical_review_owner_approval_pending": "Built/reviewed; technical recommendation exists, owner approval deferred",
    "Q2_direct_build_queue": "Direct build queue; source identity appears buildable without blocking upstream approval",
    "Q3_hold_candidate_problem_found": "Hold; candidate evidence exists but review found a material problem",
    "Q4_bounded_candidate_build_or_review": "Bounded candidate; build/review with narrow source-boundary control",
    "Q5_deferred_pending_approved_parent": "Deferred; needs approved or explicitly bounded upstream parent/component",
    "Q6_split_identity_or_proxy_needed": "Do not force same-name; split identity or local proxy needed",
    "Q7_blocked_current_source_surface": "Blocked under current Amsterdam source surface",
}

QUEUE_RANK = {queue: idx for idx, queue in enumerate(QUEUE_LABELS)}

TECH_RECOMMEND_APPROVE = {
    "std_oxygen_partial_pressure_bg_allspecimen": "Technical review recommends same-name approval; owner approval deferred.",
    "std_carbon_dioxide_partial_pressure_bg_allspecimen": "Technical review recommends same-name approval; owner approval deferred.",
    "std_oxygen_saturation_bg_allspecimen": "Technical review recommends same-name approval; owner approval deferred.",
    "std_total_bilirubin": "Technical review recommends same-name approval; owner approval deferred.",
    "std_inr": "Technical review recommends same-name approval; owner approval deferred.",
    "std_aptt": "Technical review recommends same-name approval; owner approval deferred.",
}

TECH_RECOMMEND_APPROVE_WITH_CAVEAT = {
    "std_albumin": "Technical review recommends approval with distribution caveat; owner approval deferred.",
}

HOLD_REASONS = {
    "std_advanced_respiratory_support_active": (
        "Amsterdam governed build now exists from approved IMV and NIV parents, but the public same-name concept "
        "includes HFNC and no narrow Amsterdam HFNC source is approved in the current source surface."
    ),
    "std_oxygen_saturation_bg_arterial_specimen": (
        "Amsterdam candidate is almost identical to all-specimen blood-gas oxygen saturation and lacks a universal "
        "structured arterial specimen proof."
    ),
    "std_pt": (
        "Amsterdam legacy seconds-labeled prothrombin-time source has an INR-like distribution, not a PT-seconds "
        "distribution."
    ),
    "std_discharge_disposition": (
        "Amsterdam governed build now exists from admissions_core.destination, but most retained destination values are "
        "numeric local codes without an approved destination-code dictionary for same-name grouped discharge disposition."
    ),
    "std_icu_exit_destination": (
        "Amsterdam governed build now exists from admissions_core.destination, but most retained destination values are "
        "numeric local codes without an approved destination-code dictionary for same-name ICU exit destination."
    ),
}

DEFERRED_CLASS_IDS = {
    "class2_baseline_summary_window_numeric",
    "class8_score_phenotype_composite_derived",
}

DEFERRED_PHASE_TOKENS = (
    "followup",
    "summary",
    "window",
    "component",
    "phenotype",
    "score",
)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_bool(value: str) -> bool:
    return str(value).strip().lower() == "true"


def public_card_amsterdam_status(variable_id: str) -> str:
    path = CARD_DIR / f"{variable_id}.md"
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8", errors="replace")
    for line in text.splitlines():
        if "AmsterdamUMCdb-1.0.2" not in line:
            continue
        cells = [cell.strip(" `") for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 2 and cells[0] == "AmsterdamUMCdb-1.0.2":
            if cells[1] in {
                "reviewed_approved",
                "reviewed_approved_with_caveat",
                "candidate",
                "not_approved",
                "blocked",
            }:
                return cells[1]
    return ""


def amsterdam_mapping_status(variable_id: str) -> dict[str, str]:
    path = STD_MVP_DIR / variable_id / "mapping_spec_amsterdamumcdb_1_0_2.json"
    if not path.exists():
        return {
            "mapping_spec_path": "",
            "mapping_artifact_status": "",
            "mapping_approval_status": "",
        }
    try:
        data = read_json(path)
    except json.JSONDecodeError:
        return {
            "mapping_spec_path": str(path.relative_to(REPO_ROOT)).replace("\\", "/"),
            "mapping_artifact_status": "json_decode_failed",
            "mapping_approval_status": "json_decode_failed",
        }
    return {
        "mapping_spec_path": str(path.relative_to(REPO_ROOT)).replace("\\", "/"),
        "mapping_artifact_status": str(data.get("artifact_status", "")),
        "mapping_approval_status": str(data.get("approval_status", "")),
    }


def amsterdam_runtime_status(variable_id: str) -> dict[str, str]:
    runtime_dir = STD_MVP_DIR / variable_id / "runtime"
    if not runtime_dir.exists():
        return {
            "runtime_status": "no_amsterdam_runtime",
            "amsterdam_runtime_dirs": "",
            "has_validation_report": "False",
            "has_reproducibility_report": "False",
        }
    dirs = sorted(
        d for d in runtime_dir.iterdir() if d.is_dir() and "amsterdamumcdb_1_0_2" in d.name.lower()
    )
    if not dirs:
        return {
            "runtime_status": "no_amsterdam_runtime",
            "amsterdam_runtime_dirs": "",
            "has_validation_report": "False",
            "has_reproducibility_report": "False",
        }
    has_validation = any((d / "validation_report.json").exists() for d in dirs)
    has_repro = any((d / "reproducibility_report.json").exists() for d in dirs)
    if has_validation and has_repro:
        status = "amsterdam_runtime_and_rerun_repro_present"
    elif has_validation:
        status = "amsterdam_first_runtime_validation_present"
    else:
        status = "amsterdam_runtime_dir_present_without_standard_reports"
    return {
        "runtime_status": status,
        "amsterdam_runtime_dirs": ";".join(str(d.relative_to(REPO_ROOT)).replace("\\", "/") for d in dirs),
        "has_validation_report": str(has_validation),
        "has_reproducibility_report": str(has_repro),
    }


def default_build_status(mapping: dict[str, str], runtime: dict[str, str]) -> str:
    if runtime["runtime_status"] == "amsterdam_runtime_and_rerun_repro_present":
        return "built_runtime_repro_pass"
    if runtime["runtime_status"] == "amsterdam_first_runtime_validation_present":
        return "built_first_runtime_only"
    if mapping["mapping_spec_path"]:
        return "mapping_spec_exists_runtime_missing"
    return "not_built"


def classify_queue(row: dict[str, str], card_status: str, build_status: str) -> dict[str, str]:
    variable_id = row["variable_id"]
    class_id = row["class_id"]
    bucket = row["amsterdam_status_bucket"]
    phase = row["amsterdam_phase"]
    audit_public_covered = normalize_bool(row["amsterdam_already_public_covered"])

    if variable_id in TECH_RECOMMEND_APPROVE_WITH_CAVEAT:
        return {
            "execution_queue": "Q1_technical_review_owner_approval_pending",
            "dependency_status": "no_blocking_dependency_identified",
            "review_status": "technical_review_recommend_approve_with_caveat",
            "owner_approval_status": "owner_approval_pending",
            "next_action": "carry to future owner approval wave with the documented distribution caveat",
            "queue_reason": TECH_RECOMMEND_APPROVE_WITH_CAVEAT[variable_id],
        }

    if variable_id in TECH_RECOMMEND_APPROVE:
        return {
            "execution_queue": "Q1_technical_review_owner_approval_pending",
            "dependency_status": "no_blocking_dependency_identified",
            "review_status": "technical_review_recommend_approve",
            "owner_approval_status": "owner_approval_pending",
            "next_action": "carry to future owner approval wave; do not count as owner-approved yet",
            "queue_reason": TECH_RECOMMEND_APPROVE[variable_id],
        }

    if variable_id in HOLD_REASONS:
        return {
            "execution_queue": "Q3_hold_candidate_problem_found",
            "dependency_status": "source_identity_problem_not_parent_dependency",
            "review_status": "hold_candidate_problem_found",
            "owner_approval_status": "not_owner_approved",
            "next_action": "keep candidate evidence, resolve source-boundary problem, and do not approve in same-name wave",
            "queue_reason": HOLD_REASONS[variable_id],
        }

    if audit_public_covered or card_status in {"reviewed_approved", "reviewed_approved_with_caveat"}:
        return {
            "execution_queue": "Q0_already_public_covered",
            "dependency_status": "not_applicable_or_already_resolved",
            "review_status": "prior_public_covered_or_reviewed",
            "owner_approval_status": "owner_approved_or_preexisting_public_covered",
            "next_action": "no new build in this campaign; retain as upstream evidence when semantically appropriate",
            "queue_reason": "Already public-covered in Amsterdam under the current public audit/card surface.",
        }

    if bucket == "same_name_ready":
        dependency_status = "no_blocking_dependency_identified"
        if "derivable_from_approved_support_family" in phase:
            dependency_status = "approved_or_bounded_support_parent_available"
        if class_id == "class7_diagnosis_admin_demographic_id_map":
            dependency_status = "source_grain_review_required_but_no_upstream_parent"
        if build_status == "built_runtime_repro_pass":
            return {
                "execution_queue": "Q2_direct_build_queue",
                "dependency_status": dependency_status,
                "review_status": "built_runtime_repro_pass_pending_detailed_review",
                "owner_approval_status": "not_owner_approved",
                "next_action": "carry to the next detailed review packet; do not treat as owner-approved yet",
                "queue_reason": "Governed Amsterdam build, first execution, rerun, and reproducibility evidence are present.",
            }
        if build_status == "built_first_runtime_only":
            return {
                "execution_queue": "Q2_direct_build_queue",
                "dependency_status": dependency_status,
                "review_status": "built_first_runtime_only_rerun_needed",
                "owner_approval_status": "not_owner_approved",
                "next_action": "run rerun reproducibility before detailed review",
                "queue_reason": "First governed Amsterdam runtime exists but rerun reproducibility evidence is not complete.",
            }
        return {
            "execution_queue": "Q2_direct_build_queue",
            "dependency_status": dependency_status,
            "review_status": "not_reviewed_in_current_owner_wave",
            "owner_approval_status": "not_owner_approved",
            "next_action": "build governed mapping, first execution, rerun reproducibility, then prepare detailed review block",
            "queue_reason": "Same-name route is marked ready and no blocking upstream approval is visible.",
        }

    if bucket == "split_identity_needed":
        return {
            "execution_queue": "Q6_split_identity_or_proxy_needed",
            "dependency_status": "same_name_identity_not_supported",
            "review_status": "same_name_not_approval_ready",
            "owner_approval_status": "not_owner_approved",
            "next_action": "define or reuse a split/proxy identity; do not force same-name approval",
            "queue_reason": "Audit says Amsterdam source semantics do not match the current same-name identity.",
        }

    if bucket == "not_supported_or_blocked":
        return {
            "execution_queue": "Q7_blocked_current_source_surface",
            "dependency_status": "source_surface_blocked",
            "review_status": "blocked_under_current_source_surface",
            "owner_approval_status": "not_owner_approved",
            "next_action": "do not build now; reopen only if a new Amsterdam source surface is admitted",
            "queue_reason": "Audit says the current Amsterdam opening source surface does not support a safe build.",
        }

    if bucket == "bounded_candidate_only":
        if class_id in DEFERRED_CLASS_IDS or any(token in phase for token in DEFERRED_PHASE_TOKENS):
            return {
                "execution_queue": "Q5_deferred_pending_approved_parent",
                "dependency_status": "upstream_parent_or_component_approval_needed",
                "review_status": "deferred_before_owner_review",
                "owner_approval_status": "not_owner_approved",
                "next_action": "wait for required parent/component approval or run engineering-only dry-run with explicit non-approval label",
                "queue_reason": "Variable requires upstream window, bridge, score, phenotype, or component evidence before approval-facing build.",
            }
        return {
            "execution_queue": "Q4_bounded_candidate_build_or_review",
            "dependency_status": "source_boundary_review_needed",
            "review_status": "bounded_candidate_not_reviewed",
            "owner_approval_status": "not_owner_approved",
            "next_action": "perform item/source-domain review; build only under a bounded candidate label until evidence supports approval",
            "queue_reason": "Source evidence exists but needs bounded source review before approval.",
        }

    return {
        "execution_queue": "Q7_blocked_current_source_surface",
        "dependency_status": "unclassified_blocked_pending_manual_triage",
        "review_status": "unclassified",
        "owner_approval_status": "not_owner_approved",
        "next_action": "manual triage required",
        "queue_reason": "No matching queue rule.",
    }


def build_rows() -> list[dict[str, str]]:
    source_rows = read_csv_rows(SOURCE_AUDIT_CSV)
    output_rows: list[dict[str, str]] = []
    for row in source_rows:
        variable_id = row["variable_id"]
        mapping = amsterdam_mapping_status(variable_id)
        runtime = amsterdam_runtime_status(variable_id)
        card_status = public_card_amsterdam_status(variable_id)
        build_status = default_build_status(mapping, runtime)
        queue = classify_queue(row, card_status, build_status)
        execution_queue = queue["execution_queue"]
        output_rows.append(
            {
                "queue_rank": str(QUEUE_RANK[execution_queue]),
                "class_rank": str(CLASS_RANK.get(row["class_id"], 99)),
                "variable_id": variable_id,
                "class_id": row["class_id"],
                "class_label": CLASS_LABELS.get(row["class_id"], row["class_id"]),
                "semantic_folder": row["semantic_folder"],
                "value_type": row["value_type"],
                "grain": row["grain"],
                "amsterdam_status_bucket": row["amsterdam_status_bucket"],
                "amsterdam_phase": row["amsterdam_phase"],
                "priority_tier": row["priority_tier"],
                "amsterdam_already_public_covered_audit": row["amsterdam_already_public_covered"],
                "current_public_card_amsterdam_status": card_status,
                "execution_queue": execution_queue,
                "execution_queue_label": QUEUE_LABELS[execution_queue],
                "build_status": build_status,
                "dependency_status": queue["dependency_status"],
                "review_status": queue["review_status"],
                "owner_approval_status": queue["owner_approval_status"],
                "mapping_artifact_status": mapping["mapping_artifact_status"],
                "mapping_approval_status": mapping["mapping_approval_status"],
                "runtime_status": runtime["runtime_status"],
                "has_validation_report": runtime["has_validation_report"],
                "has_reproducibility_report": runtime["has_reproducibility_report"],
                "mapping_spec_path": mapping["mapping_spec_path"],
                "amsterdam_runtime_dirs": runtime["amsterdam_runtime_dirs"],
                "queue_reason": queue["queue_reason"],
                "next_action": queue["next_action"],
                "audit_rationale": row["rationale"],
                "dictionary_hit_count": row["dictionary_hit_count"],
                "dictionary_hit_tables": row["dictionary_hit_tables"],
            }
        )
    return sorted(
        output_rows,
        key=lambda r: (
            int(r["queue_rank"]),
            int(r["class_rank"]),
            r["priority_tier"],
            r["variable_id"],
        ),
    )


def markdown_table(headers: list[str], rows: list[list[str]]) -> list[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(cell).replace("\n", " ") for cell in row) + " |")
    return lines


def render_markdown(rows: list[dict[str, str]], generated_at: str) -> str:
    queue_counts = Counter(row["execution_queue"] for row in rows)
    class_counts = Counter(row["class_id"] for row in rows)
    queue_by_class: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        queue_by_class[row["class_id"]][row["execution_queue"]] += 1

    lines: list[str] = []
    lines.append("# Amsterdam Class 1-9 Execution Queue")
    lines.append("")
    lines.append(f"Last generated: {generated_at}")
    lines.append("")
    lines.append("Status: generated build-first/approval-later queue; owner approval is not implied")
    lines.append("")
    lines.append("## Source")
    lines.append("")
    lines.append("- `docs/standard_system_mvp/amsterdam_coverage_audit/amsterdam_variable_coverage_audit.csv`")
    lines.append("- `docs/standard_system_mvp/CLASS1_TO_CLASS9_BUILD_FIRST_APPROVAL_LATER_PLAN.md`")
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("This table is an execution queue, not an approval table.")
    lines.append("")
    lines.append("A variable can be built, technically reviewed, or already public-covered without being newly approved by the project owner in the current approval wave.")
    lines.append("")
    lines.append("## Generated Files")
    lines.append("")
    lines.append("- `docs/standard_system_mvp/amsterdam_coverage_audit/amsterdam_class1_to_class9_execution_queue.csv`")
    lines.append("- `docs/standard_system_mvp/amsterdam_coverage_audit/amsterdam_class1_to_class9_execution_queue.json`")
    lines.append("")
    lines.append("## Queue Counts")
    lines.append("")
    queue_rows = [
        [queue, str(queue_counts.get(queue, 0)), QUEUE_LABELS[queue]]
        for queue in QUEUE_LABELS
    ]
    lines.extend(markdown_table(["queue", "count", "meaning"], queue_rows))
    lines.append("")
    lines.append("## Class Counts")
    lines.append("")
    class_rows = [
        [class_id, str(class_counts.get(class_id, 0)), CLASS_LABELS[class_id]]
        for class_id in CLASS_LABELS
    ]
    lines.extend(markdown_table(["class_id", "count", "label"], class_rows))
    lines.append("")
    lines.append("## Queue By Class")
    lines.append("")
    headers = ["class_id"] + list(QUEUE_LABELS)
    table_rows: list[list[str]] = []
    for class_id in CLASS_LABELS:
        table_rows.append([class_id] + [str(queue_by_class[class_id].get(queue, 0)) for queue in QUEUE_LABELS])
    lines.extend(markdown_table(headers, table_rows))
    lines.append("")

    lines.append("## Owner-Approval Pending Technical Recommendations")
    lines.append("")
    tech_rows = [
        row
        for row in rows
        if row["execution_queue"] == "Q1_technical_review_owner_approval_pending"
    ]
    lines.extend(
        markdown_table(
            ["variable_id", "class", "review_status", "build_status", "public_card_status", "next_action"],
            [
                [
                    row["variable_id"],
                    row["class_id"],
                    row["review_status"],
                    row["build_status"],
                    row["current_public_card_amsterdam_status"] or "none",
                    row["next_action"],
                ]
                for row in tech_rows
            ],
        )
    )
    lines.append("")

    lines.append("## Direct Build Queue")
    lines.append("")
    direct_rows = [row for row in rows if row["execution_queue"] == "Q2_direct_build_queue"]
    lines.extend(
        markdown_table(
            ["variable_id", "class", "phase", "dependency_status", "next_action"],
            [
                [
                    row["variable_id"],
                    row["class_id"],
                    row["amsterdam_phase"],
                    row["dependency_status"],
                    row["next_action"],
                ]
                for row in direct_rows
            ],
        )
    )
    lines.append("")

    lines.append("## Hold Candidates")
    lines.append("")
    hold_rows = [row for row in rows if row["execution_queue"] == "Q3_hold_candidate_problem_found"]
    lines.extend(
        markdown_table(
            ["variable_id", "class", "build_status", "reason", "next_action"],
            [
                [
                    row["variable_id"],
                    row["class_id"],
                    row["build_status"],
                    row["queue_reason"],
                    row["next_action"],
                ]
                for row in hold_rows
            ],
        )
    )
    lines.append("")

    lines.append("## Split Identity Needed")
    lines.append("")
    split_rows = [row for row in rows if row["execution_queue"] == "Q6_split_identity_or_proxy_needed"]
    lines.extend(
        markdown_table(
            ["variable_id", "class", "phase", "audit_rationale"],
            [
                [
                    row["variable_id"],
                    row["class_id"],
                    row["amsterdam_phase"],
                    row["audit_rationale"],
                ]
                for row in split_rows
            ],
        )
    )
    lines.append("")

    lines.append("## Next Work Rule")
    lines.append("")
    lines.append("Start with `Q2_direct_build_queue` unless the project owner explicitly opens an approval wave.")
    lines.append("")
    lines.append("Keep `Q1_technical_review_owner_approval_pending` visible for later approval, but do not spend the next build round trying to approve it.")
    lines.append("")
    lines.append("Use the CSV/JSON files for the full 465-variable queue.")
    lines.append("")
    return "\n".join(lines)


def write_outputs(rows: list[dict[str, str]], generated_at: str) -> None:
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with OUTPUT_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    payload = {
        "artifact_type": "amsterdam_class1_to_class9_execution_queue",
        "generated_at": generated_at,
        "source_audit_csv": str(SOURCE_AUDIT_CSV.relative_to(REPO_ROOT)).replace("\\", "/"),
        "owner_approval_rule": "owner approval is explicit and is not implied by build or technical review status",
        "queue_labels": QUEUE_LABELS,
        "rows": rows,
    }
    OUTPUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUTPUT_MD.write_text(render_markdown(rows, generated_at), encoding="utf-8")


def main() -> None:
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    rows = build_rows()
    write_outputs(rows, generated_at)
    print(f"Wrote: {OUTPUT_CSV}")
    print(f"Wrote: {OUTPUT_JSON}")
    print(f"Wrote: {OUTPUT_MD}")
    print(f"Rows: {len(rows)}")
    for queue, count in Counter(row["execution_queue"] for row in rows).most_common():
        print(f"{queue}: {count}")


if __name__ == "__main__":
    main()
