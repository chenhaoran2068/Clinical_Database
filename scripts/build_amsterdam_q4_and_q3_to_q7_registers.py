from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import duckdb

import build_amsterdam_coverage_audit as coverage


REPO_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = REPO_ROOT.parent.parent
STD_MVP_DIR = REPO_ROOT / "docs" / "standard_system_mvp"
CARD_DIR = REPO_ROOT / "docs" / "std_variable_cards"
AUDIT_DIR = STD_MVP_DIR / "amsterdam_coverage_audit"
QUEUE_CSV = AUDIT_DIR / "amsterdam_class1_to_class9_execution_queue.csv"
DICTIONARY_PARQUET = (
    WORKSPACE_ROOT
    / "Methods"
    / "Clinical_Database"
    / "local_work"
    / "Layer 2"
    / "AmsterdamUMCdb-1.0.2"
    / "reviewed_unsplit"
    / "amsterdam_item_dictionary_legacy.parquet"
)
LOCAL_Q4_DIR = (
    WORKSPACE_ROOT
    / "Methods"
    / "Clinical_Database"
    / "local_work"
    / "Layer 5"
    / "AmsterdamUMCdb-1.0.2"
    / "q4_bounded_candidate_batch_source_review"
)

Q4_REGISTER_CSV = AUDIT_DIR / "amsterdam_q4_bounded_candidate_batch_build_register.csv"
Q4_REGISTER_JSON = AUDIT_DIR / "amsterdam_q4_bounded_candidate_batch_build_register.json"
Q4_HITS_CSV = AUDIT_DIR / "amsterdam_q4_bounded_candidate_source_item_hits.csv"
Q4_HITS_JSON = AUDIT_DIR / "amsterdam_q4_bounded_candidate_source_item_hits.json"
FREEZE_CSV = AUDIT_DIR / "amsterdam_q3_q5_q6_q7_freeze_dependency_split_register.csv"
FREEZE_JSON = AUDIT_DIR / "amsterdam_q3_q5_q6_q7_freeze_dependency_split_register.json"
Q4_MD = STD_MVP_DIR / "AMSTERDAM_Q4_BOUNDED_CANDIDATE_BATCH_BUILD_REGISTER.md"
FREEZE_MD = STD_MVP_DIR / "AMSTERDAM_Q3_Q5_Q6_Q7_FREEZE_DEPENDENCY_SPLIT_REGISTER.md"

Q3_QUEUE = "Q3_hold_candidate_problem_found"
Q4_QUEUE = "Q4_bounded_candidate_build_or_review"
Q5_QUEUE = "Q5_deferred_pending_approved_parent"
Q6_QUEUE = "Q6_split_identity_or_proxy_needed"
Q7_QUEUE = "Q7_blocked_current_source_surface"

SOURCE_TABLE_PREFERENCES = {
    "class1_event_level_numeric": {"numericitems"},
    "class3_binary_state_episode": {"processitems", "listitems", "drugitems", "procedureorderitems"},
    "class4_treatment_device_io_event_stream": {
        "drugitems",
        "numericitems",
        "processitems",
        "procedureorderitems",
        "listitems",
    },
    "class6_ordinal_text_semiquantitative_result": {"listitems", "freetextitems", "numericitems"},
}

SPECIMEN_TOKENS = {
    "_ascites": ("ascites", "ascitic", "buikvocht"),
    "_csf": ("csf", "liquor", "cerebrospinal"),
    "_joint_fluid": ("joint", "gewricht", "synovial"),
    "_other_body_fluid": ("other", "overig", "body fluid", "vocht"),
    "_pleural": ("pleural", "pleura"),
    "_stool": ("stool", "feces", "faeces", "ontlasting"),
    "_urine": ("urine", "urin"),
    "_whole_blood": ("whole blood", "bloed", "blood"),
    "_bg": ("astrup", "bloed", "blood gas", "blood"),
    "_allspecimen": ("bloed", "blood", "overig", "other"),
    "_arterial_specimen": ("arterial", "arterie", "bloed", "blood"),
}


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def repo_relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        try:
            return path.resolve().relative_to(WORKSPACE_ROOT).as_posix()
        except ValueError:
            return path.as_posix()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_card_bullet(text: str, label: str) -> str:
    match = re.search(rf"- `{re.escape(label)}`:\s*`?(.+?)`?\s*$", text, flags=re.MULTILINE)
    if match:
        return match.group(1).strip().strip("`")
    match = re.search(rf"- {re.escape(label)}:\s*`?(.+?)`?\s*$", text, flags=re.MULTILINE)
    return match.group(1).strip().strip("`") if match else ""


def parse_public_card(variable_id: str) -> dict[str, str]:
    path = CARD_DIR / f"{variable_id}.md"
    if not path.exists():
        return {
            "standardized_english_name": "",
            "standard_unit": "",
            "primary_retained_value_column": "",
            "approved_value_range_note": "",
            "default_anchor_type": "",
            "card_path": "",
        }
    text = path.read_text(encoding="utf-8", errors="replace")
    return {
        "standardized_english_name": parse_card_bullet(text, "standardized English name"),
        "standard_unit": parse_card_bullet(text, "standard unit"),
        "primary_retained_value_column": parse_card_bullet(text, "primary retained value column"),
        "approved_value_range_note": parse_card_bullet(text, "current approved value range note"),
        "default_anchor_type": parse_card_bullet(text, "default anchor type"),
        "card_path": repo_relative(path),
    }


def load_dictionary_rows() -> list[dict[str, Any]]:
    if not DICTIONARY_PARQUET.exists():
        raise FileNotFoundError(f"Amsterdam dictionary not found: {DICTIONARY_PARQUET}")
    query = """
        select
            cast(itemid as bigint) as itemid,
            coalesce("table", '') as source_table,
            coalesce(item, '') as item,
            coalesce(item_en, '') as item_en,
            coalesce(abbreviation, '') as abbreviation,
            coalesce(unit, '') as unit,
            coalesce(ucum_code, '') as ucum_code,
            expected_min_value,
            expected_max_value,
            cast(coalesce(count, 0) as bigint) as dictionary_count,
            count_validated,
            coalesce(category, '') as category,
            coalesce(category_en, '') as category_en,
            islabresult,
            coalesce(vocabulary_id, '') as vocabulary_id,
            coalesce(vocabulary_concept_code, '') as vocabulary_concept_code,
            coalesce(vocabulary_concept_name, '') as vocabulary_concept_name
        from read_parquet(?)
    """
    con = duckdb.connect()
    rows = con.execute(query, [str(DICTIONARY_PARQUET)]).fetchdf().to_dict("records")
    con.close()
    for row in rows:
        row["search_text"] = " ".join(
            str(row.get(field, "")).lower()
            for field in ("item", "item_en", "abbreviation", "category", "category_en", "vocabulary_concept_name")
        )
    return rows


def clean_aliases(variable_id: str) -> list[str]:
    aliases = []
    for alias in coverage.source_aliases(variable_id):
        alias = alias.lower().strip()
        if not alias:
            continue
        aliases.append(alias)
    return sorted(set(aliases), key=lambda item: (-len(item), item))


def required_modifier_terms(variable_id: str) -> tuple[str, ...]:
    terms: list[str] = []
    for token, token_terms in SPECIMEN_TOKENS.items():
        if token in variable_id:
            terms.extend(token_terms)
    return tuple(sorted(set(terms)))


def modifier_match(search_text: str, modifier_terms: tuple[str, ...]) -> bool:
    if not modifier_terms:
        return True
    return any(term in search_text for term in modifier_terms)


def preferred_table_match(class_id: str, source_table: str) -> bool:
    return source_table in SOURCE_TABLE_PREFERENCES.get(class_id, set())


def fit_category(class_id: str, source_table: str, has_modifier: bool) -> str:
    if class_id == "class1_event_level_numeric":
        if source_table == "numericitems" and has_modifier:
            return "strong_numericitems_modifier_or_unmodified_hit"
        if source_table == "numericitems":
            return "numericitems_base_hit_modifier_missing"
        return "non_numeric_supporting_or_false_positive_hit"
    if class_id == "class3_binary_state_episode":
        if source_table in {"processitems", "listitems", "drugitems"}:
            return "state_source_family_hit"
        return "state_adjacent_source_hit"
    if class_id == "class4_treatment_device_io_event_stream":
        if source_table in SOURCE_TABLE_PREFERENCES[class_id]:
            return "event_stream_source_family_hit"
        return "event_stream_adjacent_source_hit"
    if class_id == "class6_ordinal_text_semiquantitative_result":
        if source_table in {"listitems", "freetextitems"}:
            return "ordinal_domain_source_hit"
        if source_table == "numericitems":
            return "numeric_semiquantitative_or_sediment_source_hit"
        return "ordinal_adjacent_source_hit"
    return "candidate_hit"


def score_hit(
    *,
    class_id: str,
    source_table: str,
    matched_aliases: list[str],
    has_modifier: bool,
    dictionary_count: int,
) -> int:
    score = 10 * len(matched_aliases)
    if preferred_table_match(class_id, source_table):
        score += 25
    if has_modifier:
        score += 20
    if source_table == "numericitems" and class_id == "class1_event_level_numeric":
        score += 20
    if dictionary_count > 0:
        score += min(20, len(str(dictionary_count)) * 3)
    return score


def candidate_hits_for_variable(
    row: dict[str, str],
    dictionary_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    variable_id = row["variable_id"]
    class_id = row["class_id"]
    aliases = clean_aliases(variable_id)
    modifier_terms = required_modifier_terms(variable_id)
    hits: list[dict[str, Any]] = []
    for item in dictionary_rows:
        search_text = str(item["search_text"])
        matched_aliases = [alias for alias in aliases if alias in search_text]
        if not matched_aliases:
            continue
        has_modifier = modifier_match(search_text, modifier_terms)
        source_table = str(item["source_table"])
        dictionary_count = int(item.get("dictionary_count") or 0)
        hit = {
            "variable_id": variable_id,
            "class_id": class_id,
            "semantic_folder": row["semantic_folder"],
            "source_itemid": int(item["itemid"]),
            "source_table": source_table,
            "source_item": str(item["item"]),
            "source_item_en": str(item["item_en"]),
            "source_abbreviation": str(item["abbreviation"]),
            "source_unit": str(item["unit"]),
            "source_ucum_code": str(item["ucum_code"]),
            "dictionary_expected_min_value": item.get("expected_min_value"),
            "dictionary_expected_max_value": item.get("expected_max_value"),
            "dictionary_count": dictionary_count,
            "dictionary_count_validated": item.get("count_validated"),
            "category": str(item["category"]),
            "category_en": str(item["category_en"]),
            "islabresult": item.get("islabresult"),
            "vocabulary_id": str(item["vocabulary_id"]),
            "vocabulary_concept_code": str(item["vocabulary_concept_code"]),
            "vocabulary_concept_name": str(item["vocabulary_concept_name"]),
            "matched_aliases": ";".join(matched_aliases[:8]),
            "modifier_terms_required": ";".join(modifier_terms),
            "modifier_match": str(has_modifier),
            "preferred_table_for_class": str(preferred_table_match(class_id, source_table)),
            "candidate_fit_category": fit_category(class_id, source_table, has_modifier),
            "candidate_score": score_hit(
                class_id=class_id,
                source_table=source_table,
                matched_aliases=matched_aliases,
                has_modifier=has_modifier,
                dictionary_count=dictionary_count,
            ),
        }
        hits.append(hit)
    return sorted(
        hits,
        key=lambda item: (
            -int(item["candidate_score"]),
            str(item["source_table"]),
            -int(item["dictionary_count"]),
            int(item["source_itemid"]),
        ),
    )


def table_counts(hits: list[dict[str, Any]]) -> str:
    counts = Counter(str(hit["source_table"]) for hit in hits)
    return ";".join(f"{key}:{counts[key]}" for key in sorted(counts))


def q4_lane(row: dict[str, str], hits: list[dict[str, Any]]) -> str:
    class_id = row["class_id"]
    variable_id = row["variable_id"]
    if class_id == "class1_event_level_numeric":
        if required_modifier_terms(variable_id):
            return "Q4A_class1_specimen_or_body_fluid_numeric_candidate"
        if "_bg" in variable_id or "fio2" in variable_id or "ratio" in variable_id:
            return "Q4B_class1_blood_gas_or_calculated_numeric_candidate"
        return "Q4C_class1_long_tail_numeric_dictionary_candidate"
    if class_id == "class3_binary_state_episode":
        return "Q4D_class3_state_episode_source_candidate"
    if class_id == "class4_treatment_device_io_event_stream":
        return "Q4E_class4_event_stream_source_candidate"
    if class_id == "class6_ordinal_text_semiquantitative_result":
        return "Q4F_class6_ordinal_domain_source_candidate"
    return "Q4Z_other_bounded_candidate"


def q4_construct_status(row: dict[str, str], hits: list[dict[str, Any]]) -> tuple[str, str]:
    runtime = q4_runtime_status(row["variable_id"])
    if runtime == "candidate_runtime_and_rerun_repro_pass":
        return (
            "candidate_runtime_built_repro_pass_pending_detailed_review",
            "Q4 bounded candidate runtime and rerun reproducibility evidence are present; owner approval and detailed variable-level review are still pending.",
        )
    if runtime == "candidate_first_runtime_present_rerun_missing":
        return (
            "candidate_first_runtime_present_rerun_missing",
            "Q4 bounded candidate first runtime evidence is present, but rerun reproducibility is not complete.",
        )
    if not hits:
        return (
            "candidate_source_scan_empty_manual_recheck",
            "The old broad audit recorded a hit, but this item-level source package did not reproduce a dictionary hit with the current alias rules.",
        )
    class_id = row["class_id"]
    fit_counts = Counter(str(hit["candidate_fit_category"]) for hit in hits)
    if class_id == "class1_event_level_numeric" and fit_counts["strong_numericitems_modifier_or_unmodified_hit"] > 0:
        return (
            "source_candidate_package_built_not_runtime_item_lock_needed",
            "Numericitems source candidates were built; itemids, source units, conversion rules, and specimen boundaries still need variable-level review before runtime construction.",
        )
    if class_id == "class1_event_level_numeric" and fit_counts["numericitems_base_hit_modifier_missing"] > 0:
        return (
            "source_candidate_package_built_not_runtime_modifier_gap",
            "Numericitems candidates exist, but the modifier or specimen boundary is not proven by the current alias scan.",
        )
    if class_id == "class6_ordinal_text_semiquantitative_result":
        return (
            "source_domain_candidate_package_built_not_runtime_domain_lock_needed",
            "Ordinal or semiquantitative source candidates were built; retained result domain and ordered value mapping must be locked before runtime construction.",
        )
    if class_id in {"class3_binary_state_episode", "class4_treatment_device_io_event_stream"}:
        return (
            "source_family_candidate_package_built_not_runtime_grain_lock_needed",
            "State or event-stream source candidates were built; start/end/event grain and parent-link rules must be locked before runtime construction.",
        )
    return (
        "source_candidate_package_built_not_runtime_manual_review_needed",
        "Candidate dictionary evidence was built, but this queue remains bounded pending manual source review.",
    )


def q4_runtime_status(variable_id: str) -> str:
    runtime_root = STD_MVP_DIR / variable_id / "runtime"
    if not runtime_root.exists():
        return "not_runtime_constructed"
    dirs = [
        item
        for item in runtime_root.iterdir()
        if item.is_dir() and "amsterdamumcdb_1_0_2" in item.name.lower()
    ]
    if not dirs:
        return "not_runtime_constructed"
    if any((item / "reproducibility_report.json").exists() for item in dirs):
        for item in dirs:
            report_path = item / "reproducibility_report.json"
            if not report_path.exists():
                continue
            try:
                report = json.loads(report_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                return "candidate_runtime_repro_report_invalid"
            if report.get("overall_status") == "pass":
                return "candidate_runtime_and_rerun_repro_pass"
        return "candidate_runtime_repro_present_not_pass"
    if any((item / "validation_report.json").exists() for item in dirs):
        return "candidate_first_runtime_present_rerun_missing"
    return "runtime_dir_present_without_standard_reports"


def build_q4_register(
    queue_rows: list[dict[str, str]],
    dictionary_rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    q4_rows = [row for row in queue_rows if row["execution_queue"] == Q4_QUEUE]
    register_rows: list[dict[str, Any]] = []
    hit_rows: list[dict[str, Any]] = []
    for row in q4_rows:
        card = parse_public_card(row["variable_id"])
        hits = candidate_hits_for_variable(row, dictionary_rows)
        hit_rows.extend(hits)
        locked_itemids, locked_labels = locked_runtime_source_scope(row["variable_id"])
        top_hits = hits[:10]
        status, caveat = q4_construct_status(row, hits)
        if locked_itemids:
            top_candidate_itemids = ";".join(locked_itemids)
            top_candidate_labels = " | ".join(locked_labels)
        else:
            top_candidate_itemids = ";".join(str(hit["source_itemid"]) for hit in top_hits)
            top_candidate_labels = " | ".join(
                f"{hit['source_table']}:{hit['source_itemid']}:{hit['source_item']}"
                for hit in top_hits[:5]
            )
        register_rows.append(
            {
                "variable_id": row["variable_id"],
                "class_id": row["class_id"],
                "semantic_folder": row["semantic_folder"],
                "standardized_english_name": card["standardized_english_name"],
                "standard_unit": card["standard_unit"],
                "primary_retained_value_column": card["primary_retained_value_column"],
                "approved_value_range_note": card["approved_value_range_note"],
                "q4_lane": q4_lane(row, hits),
                "q4_batch_construct_status": status,
                "owner_approval_status": "not_owner_approved",
                "runtime_status_after_this_batch": q4_runtime_status(row["variable_id"]),
                "candidate_hit_count": len(hits),
                "candidate_hit_tables": table_counts(hits),
                "candidate_numericitems_hit_count": sum(
                    1 for hit in hits if hit["source_table"] == "numericitems"
                ),
                "candidate_preferred_table_hit_count": sum(
                    1 for hit in hits if hit["preferred_table_for_class"] == "True"
                ),
                "top_candidate_itemids": top_candidate_itemids,
                "top_candidate_labels": top_candidate_labels,
                "source_boundary_caveat": caveat,
                "next_action": q4_next_action(row, status),
                "audit_rationale": row["audit_rationale"],
                "queue_reason": row["queue_reason"],
                "public_card_path": card["card_path"],
                "source_item_hits_file": repo_relative(Q4_HITS_CSV),
            }
        )
    return register_rows, hit_rows


def locked_runtime_source_scope(variable_id: str) -> tuple[list[str], list[str]]:
    mapping_path = STD_MVP_DIR / variable_id / "mapping_spec_amsterdamumcdb_1_0_2.json"
    if not mapping_path.exists():
        return [], []
    try:
        mapping = json.loads(mapping_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return [], []
    status = str(mapping.get("artifact_status", ""))
    if "candidate_mapping_q4_class1_wave1" not in status:
        return [], []
    source_codes = mapping.get("database_mapping", {}).get("source_codes", [])
    source_labels = mapping.get("database_mapping", {}).get("source_code_labels", {})
    itemids = [str(item) for item in source_codes if str(item).strip()]
    labels = [
        f"numericitems:{itemid}:{source_labels.get(str(itemid), '')}"
        for itemid in itemids
    ]
    return itemids, labels


def q4_next_action(row: dict[str, str], status: str) -> str:
    class_id = row["class_id"]
    if "scan_empty" in status:
        return "manual recheck; keep bounded and do not open runtime build until a reproducible source item is found"
    if class_id == "class1_event_level_numeric":
        return "lock retained itemids, source units, conversion factor, duplicate rule, cleaned range, then generate per-variable runtime candidate"
    if class_id == "class6_ordinal_text_semiquantitative_result":
        return "lock allowed result labels and ordered/positive-domain mapping, then generate class-6 runtime candidate"
    if class_id == "class3_binary_state_episode":
        return "lock positive state definition, source start/end rules, and no-row meaning before runtime candidate"
    if class_id == "class4_treatment_device_io_event_stream":
        return "lock event grain, source table family, unit/event-time rules, and parent-link rule before runtime candidate"
    return "manual bounded review before runtime candidate"


def q3_problem_type(variable_id: str) -> str:
    mapping = {
        "std_oxygen_saturation_bg_arterial_specimen": "specimen_boundary_not_proven",
        "std_pt": "unit_distribution_conflict",
        "std_advanced_respiratory_support_active": "source_family_gap_hfnc_missing",
        "std_discharge_disposition": "local_destination_code_dictionary_missing",
        "std_icu_exit_destination": "local_destination_code_dictionary_missing",
    }
    return mapping.get(variable_id, "candidate_problem_found")


def infer_dependency(variable_id: str, class_id: str) -> tuple[str, str]:
    vid = variable_id
    if "urine_output" in vid:
        return (
            "std_icu_urine_output_event owner-approved or explicitly accepted as bounded parent",
            "approve or bounded-lock urine-output event grain, unit, and ICU-window denominator",
        )
    if "intake_output" in vid or "balance" in vid:
        return (
            "approved input/output event parents plus ICU-window denominator",
            "lock input/output event families, daily/hourly windowing, and missingness denominator",
        )
    if "intubation" in vid:
        return (
            "approved intubation or IMV/post-entry procedure parent",
            "lock post-ICU-entry start anchor and first-event selection rule",
        )
    if "tracheostomy" in vid:
        return (
            "approved tracheostomy observed/status parent",
            "lock post-entry anchor and source-status boundary",
        )
    if "free_days" in vid:
        return (
            "approved support episode parent plus mortality/follow-up bridge",
            "lock death censoring, day-28 denominator, and episode overlap rules",
        )
    if "mortality" in vid:
        return (
            "approved admission/follow-up death bridge",
            "lock local admission anchor, date-of-death availability, and censoring rule",
        )
    if class_id == "class8_score_phenotype_composite_derived":
        return (
            "approved component variables for the score, phenotype, or computable diagnosis",
            "lock component source variables, timing window, missing-component policy, and scoring formula",
        )
    if class_id == "class2_baseline_summary_window_numeric":
        return (
            "approved event-level parent variable and governed summary/window rule",
            "lock parent asset, anchor, lookback/lookforward window, and summary statistic",
        )
    return (
        "approved upstream parent or component family",
        "lock parent/component identity and candidate denominator before approval-facing build",
    )


def split_identity(variable_id: str) -> tuple[str, str]:
    mapping = {
        "std_age": (
            "define std_age_grouped_proxy or Amsterdam age-group identity",
            "Amsterdam exposes agegroup rather than exact age; same-name std_age would overclaim precision.",
        ),
        "std_weight_icu_baseline": (
            "reuse or extend std_weight_icu_baseline_grouped_proxy",
            "Amsterdam grouped/proxy ICU weight should not be forced into exact baseline weight.",
        ),
        "std_weight_admission_baseline": (
            "define std_weight_admission_baseline_grouped_proxy",
            "Amsterdam admission weight evidence is grouped/proxy rather than exact same-name baseline.",
        ),
        "std_bmi_icu_baseline": (
            "define std_bmi_icu_baseline_grouped_proxy after grouped height/weight parents are locked",
            "BMI would inherit grouped/proxy parent uncertainty.",
        ),
        "std_bmi_admission_baseline": (
            "define std_bmi_admission_baseline_grouped_proxy after grouped height/weight parents are locked",
            "Admission BMI would inherit grouped/proxy parent uncertainty.",
        ),
        "std_days_to_next_hospital_admission": (
            "reuse std_days_to_next_icu_mcu_admission for local ICU/MCU readmission",
            "Amsterdam current source surface supports ICU/MCU local admissions, not full hospital readmission.",
        ),
        "std_hospital_los_days": (
            "define std_icu_mcu_los_days or local_admission_los_days identity",
            "Amsterdam opening source is ICU/MCU centered and lacks MIMIC-like hospital admission grain.",
        ),
        "std_hospital_mortality": (
            "define local_admission_or_icu_mcu_mortality identity",
            "Hospital-level mortality should not be inferred without a hospital admission bridge.",
        ),
        "std_hospital_readmission_30d": (
            "define local_icu_mcu_readmission_30d identity",
            "The safe source anchor is local ICU/MCU readmission rather than full hospital readmission.",
        ),
        "std_id_map_subject_hadm": (
            "define std_id_map_subject_local_admission",
            "Amsterdam admissionid is ICU/MCU local-admission/stay-like and is not a separate hospital admission id.",
        ),
        "std_id_map_subject_hadm_stay": (
            "define std_id_map_subject_local_admission_stay or subject_stay map",
            "Amsterdam does not expose the MIMIC subject-hadm-stay three-level key structure.",
        ),
    }
    if variable_id.startswith("std_hospital_admission_") and variable_id.endswith("_mortality"):
        return (
            "define local_admission_followup_mortality variant",
            "Amsterdam can support local admission mortality after a follow-up bridge, not same-name hospital admission mortality.",
        )
    return mapping.get(
        variable_id,
        (
            "define Amsterdam-specific split/proxy identity",
            "Current source semantics do not preserve the same-name identity.",
        ),
    )


def q7_unlock(variable_id: str, class_id: str, phase: str) -> str:
    if class_id == "class9_microbiology_multi_entity_family":
        return "open only after a microbiology hierarchy with test, organism/isolate, and susceptibility linkage is admitted"
    if variable_id == "std_race":
        return "open only if an Amsterdam demographic race/ethnicity source is admitted"
    if variable_id.startswith("std_hospital_") or variable_id.startswith("std_ed_"):
        return "open only if hospital/ED workflow, orders, provider, medication, or admission-grain source surfaces are admitted"
    if "no_dictionary_hit" in phase:
        return "open only if a new source table or dictionary release provides a clear analyte/procedure/source-family hit"
    return "open only if the required Amsterdam source surface is added and passes item-level review"


def build_freeze_register(queue_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in queue_rows:
        queue = row["execution_queue"]
        if queue not in {Q3_QUEUE, Q5_QUEUE, Q6_QUEUE, Q7_QUEUE}:
            continue
        variable_id = row["variable_id"]
        class_id = row["class_id"]
        if queue == Q3_QUEUE:
            action = "freeze_candidate_evidence_do_not_approve"
            dependency_or_split = q3_problem_type(variable_id)
            unlock = "resolve the material candidate problem and rebuild/review before any owner approval"
            allowed = "preserve existing candidate runtime evidence; do not expand same-name approval"
        elif queue == Q5_QUEUE:
            parent, unlock = infer_dependency(variable_id, class_id)
            action = "defer_until_parent_or_component_approved"
            dependency_or_split = parent
            allowed = "engineering-only dry-run is allowed only with explicit non-approval label"
        elif queue == Q6_QUEUE:
            proposal, unlock = split_identity(variable_id)
            action = "split_identity_or_proxy_required"
            dependency_or_split = proposal
            allowed = "do not build under the current same-name variable id; create or reuse split/proxy identity"
        else:
            action = "blocked_under_current_source_surface"
            dependency_or_split = row["amsterdam_phase"]
            unlock = q7_unlock(variable_id, class_id, row["amsterdam_phase"])
            allowed = "no runtime build in the current Amsterdam opening surface"
        rows.append(
            {
                "variable_id": variable_id,
                "class_id": class_id,
                "semantic_folder": row["semantic_folder"],
                "execution_queue": queue,
                "freeze_or_route_action": action,
                "current_build_status": row["build_status"],
                "owner_approval_status": "not_owner_approved",
                "dependency_or_split_identity": dependency_or_split,
                "unlock_condition": unlock,
                "allowed_next_work": allowed,
                "queue_reason": row["queue_reason"],
                "audit_rationale": row["audit_rationale"],
                "dictionary_hit_count": row["dictionary_hit_count"],
                "dictionary_hit_tables": row["dictionary_hit_tables"],
            }
        )
    return rows


def markdown_table(headers: list[str], rows: list[list[Any]]) -> list[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        safe_row = [str(cell).replace("\n", " ").replace("|", "/") for cell in row]
        lines.append("| " + " | ".join(safe_row) + " |")
    return lines


def render_q4_markdown(rows: list[dict[str, Any]], generated_at: str) -> str:
    lane_counts = Counter(row["q4_lane"] for row in rows)
    status_counts = Counter(row["q4_batch_construct_status"] for row in rows)
    class_counts = Counter(row["class_id"] for row in rows)
    lines: list[str] = []
    lines.append("# Amsterdam Q4 Bounded Candidate Batch Build Register")
    lines.append("")
    lines.append(f"Last generated: {generated_at}")
    lines.append("")
    lines.append("Status: Q4 source-boundary candidate package built; not owner-approved and not runtime-approved")
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append(
        "Q4 variables have useful Amsterdam source evidence but need item, unit, specimen, result-domain, "
        "grain, or parent-link review before approval-facing runtime construction."
    )
    lines.append("")
    lines.append(
        "This batch constructs the item-level source-candidate evidence package. It intentionally does not mark "
        "the 208 Q4 variables as owner-approved or runtime-reproducible."
    )
    lines.append("")
    lines.append("## Generated Files")
    lines.append("")
    lines.append(f"- `{repo_relative(Q4_REGISTER_CSV)}`")
    lines.append(f"- `{repo_relative(Q4_REGISTER_JSON)}`")
    lines.append(f"- `{repo_relative(Q4_HITS_CSV)}`")
    lines.append(f"- `{repo_relative(Q4_HITS_JSON)}`")
    lines.append(f"- `{repo_relative(LOCAL_Q4_DIR / 'asset_manifest.md')}`")
    lines.append("")
    lines.append("## Counts By Class")
    lines.append("")
    lines.extend(markdown_table(["class_id", "count"], [[key, class_counts[key]] for key in sorted(class_counts)]))
    lines.append("")
    lines.append("## Counts By Lane")
    lines.append("")
    lines.extend(markdown_table(["q4_lane", "count"], [[key, lane_counts[key]] for key in sorted(lane_counts)]))
    lines.append("")
    lines.append("## Counts By Construct Status")
    lines.append("")
    lines.extend(markdown_table(["status", "count"], [[key, status_counts[key]] for key in sorted(status_counts)]))
    lines.append("")
    lines.append("## Full Q4 Register")
    lines.append("")
    lines.extend(
        markdown_table(
            [
                "variable_id",
                "class",
                "unit",
                "lane",
                "status",
                "hit_tables",
                "top_candidate_itemids",
                "next_action",
            ],
            [
                [
                    row["variable_id"],
                    row["class_id"],
                    row["standard_unit"],
                    row["q4_lane"],
                    row["q4_batch_construct_status"],
                    row["candidate_hit_tables"],
                    row["top_candidate_itemids"],
                    row["next_action"],
                ]
                for row in rows
            ],
        )
    )
    lines.append("")
    return "\n".join(lines) + "\n"


def render_freeze_markdown(rows: list[dict[str, Any]], generated_at: str) -> str:
    queue_counts = Counter(row["execution_queue"] for row in rows)
    action_counts = Counter(row["freeze_or_route_action"] for row in rows)
    lines: list[str] = []
    lines.append("# Amsterdam Q3/Q5/Q6/Q7 Freeze, Dependency, And Split Register")
    lines.append("")
    lines.append(f"Last generated: {generated_at}")
    lines.append("")
    lines.append("Status: active no-approval routing register")
    lines.append("")
    lines.append("## Rule")
    lines.append("")
    lines.append(
        "These variables should not be pushed through same-name approval in the current build wave. "
        "Each row records whether the correct route is freeze, dependency deferral, split/proxy identity, or source-surface block."
    )
    lines.append("")
    lines.append("## Generated Files")
    lines.append("")
    lines.append(f"- `{repo_relative(FREEZE_CSV)}`")
    lines.append(f"- `{repo_relative(FREEZE_JSON)}`")
    lines.append("")
    lines.append("## Counts By Queue")
    lines.append("")
    lines.extend(markdown_table(["queue", "count"], [[key, queue_counts[key]] for key in sorted(queue_counts)]))
    lines.append("")
    lines.append("## Counts By Action")
    lines.append("")
    lines.extend(markdown_table(["action", "count"], [[key, action_counts[key]] for key in sorted(action_counts)]))
    lines.append("")
    lines.append("## Full Register")
    lines.append("")
    lines.extend(
        markdown_table(
            [
                "variable_id",
                "queue",
                "class",
                "action",
                "dependency_or_split_identity",
                "unlock_condition",
                "allowed_next_work",
            ],
            [
                [
                    row["variable_id"],
                    row["execution_queue"],
                    row["class_id"],
                    row["freeze_or_route_action"],
                    row["dependency_or_split_identity"],
                    row["unlock_condition"],
                    row["allowed_next_work"],
                ]
                for row in rows
            ],
        )
    )
    lines.append("")
    return "\n".join(lines) + "\n"


def write_local_manifest(q4_rows: list[dict[str, Any]], hit_rows: list[dict[str, Any]], generated_at: str) -> None:
    LOCAL_Q4_DIR.mkdir(parents=True, exist_ok=True)
    lane_counts = Counter(row["q4_lane"] for row in q4_rows)
    manifest = [
        "# Amsterdam Q4 Bounded Candidate Batch Source Review Manifest",
        "",
        f"- generated_at_utc: `{generated_at}`",
        "- database_id: `AmsterdamUMCdb-1.0.2`",
        "- status: `source_candidate_package_built_not_runtime_constructed`",
        f"- q4_variable_count: `{len(q4_rows)}`",
        f"- source_item_hit_row_count: `{len(hit_rows)}`",
        f"- public_register_csv: `{repo_relative(Q4_REGISTER_CSV)}`",
        f"- public_source_item_hits_csv: `{repo_relative(Q4_HITS_CSV)}`",
        "",
        "## Lane Counts",
        "",
    ]
    manifest.extend(
        f"- `{lane}`: `{lane_counts[lane]}`"
        for lane in sorted(lane_counts)
    )
    manifest.extend(
        [
            "",
            "## Boundary",
            "",
            "This package is an item-level source-boundary build for Q4 bounded candidates. "
            "It does not contain patient-level rows and does not assert owner approval.",
            "",
        ]
    )
    (LOCAL_Q4_DIR / "asset_manifest.md").write_text("\n".join(manifest), encoding="utf-8")


def main() -> int:
    generated_at = now_utc()
    queue_rows = read_csv(QUEUE_CSV)
    dictionary_rows = load_dictionary_rows()
    q4_rows, hit_rows = build_q4_register(queue_rows, dictionary_rows)
    freeze_rows = build_freeze_register(queue_rows)

    q4_fields = [
        "variable_id",
        "class_id",
        "semantic_folder",
        "standardized_english_name",
        "standard_unit",
        "primary_retained_value_column",
        "approved_value_range_note",
        "q4_lane",
        "q4_batch_construct_status",
        "owner_approval_status",
        "runtime_status_after_this_batch",
        "candidate_hit_count",
        "candidate_hit_tables",
        "candidate_numericitems_hit_count",
        "candidate_preferred_table_hit_count",
        "top_candidate_itemids",
        "top_candidate_labels",
        "source_boundary_caveat",
        "next_action",
        "audit_rationale",
        "queue_reason",
        "public_card_path",
        "source_item_hits_file",
    ]
    hit_fields = [
        "variable_id",
        "class_id",
        "semantic_folder",
        "source_itemid",
        "source_table",
        "source_item",
        "source_item_en",
        "source_abbreviation",
        "source_unit",
        "source_ucum_code",
        "dictionary_expected_min_value",
        "dictionary_expected_max_value",
        "dictionary_count",
        "dictionary_count_validated",
        "category",
        "category_en",
        "islabresult",
        "vocabulary_id",
        "vocabulary_concept_code",
        "vocabulary_concept_name",
        "matched_aliases",
        "modifier_terms_required",
        "modifier_match",
        "preferred_table_for_class",
        "candidate_fit_category",
        "candidate_score",
    ]
    freeze_fields = [
        "variable_id",
        "class_id",
        "semantic_folder",
        "execution_queue",
        "freeze_or_route_action",
        "current_build_status",
        "owner_approval_status",
        "dependency_or_split_identity",
        "unlock_condition",
        "allowed_next_work",
        "queue_reason",
        "audit_rationale",
        "dictionary_hit_count",
        "dictionary_hit_tables",
    ]

    write_csv(Q4_REGISTER_CSV, q4_rows, q4_fields)
    write_json(
        Q4_REGISTER_JSON,
        {
            "artifact_type": "amsterdam_q4_bounded_candidate_batch_build_register",
            "generated_at_utc": generated_at,
            "status": "source_candidate_package_built_not_runtime_constructed",
            "owner_approval_rule": "owner approval is explicit and is not implied by this Q4 source-candidate package",
            "rows": q4_rows,
        },
    )
    write_csv(Q4_HITS_CSV, hit_rows, hit_fields)
    write_json(
        Q4_HITS_JSON,
        {
            "artifact_type": "amsterdam_q4_bounded_candidate_source_item_hits",
            "generated_at_utc": generated_at,
            "rows": hit_rows,
        },
    )
    write_csv(FREEZE_CSV, freeze_rows, freeze_fields)
    write_json(
        FREEZE_JSON,
        {
            "artifact_type": "amsterdam_q3_q5_q6_q7_freeze_dependency_split_register",
            "generated_at_utc": generated_at,
            "owner_approval_rule": "these queues are not approval queues",
            "rows": freeze_rows,
        },
    )
    Q4_MD.write_text(render_q4_markdown(q4_rows, generated_at), encoding="utf-8")
    FREEZE_MD.write_text(render_freeze_markdown(freeze_rows, generated_at), encoding="utf-8")
    write_local_manifest(q4_rows, hit_rows, generated_at)

    print(f"Wrote {repo_relative(Q4_REGISTER_CSV)}")
    print(f"Wrote {repo_relative(Q4_HITS_CSV)}")
    print(f"Wrote {repo_relative(FREEZE_CSV)}")
    print(f"Wrote {repo_relative(Q4_MD)}")
    print(f"Wrote {repo_relative(FREEZE_MD)}")
    print(f"q4_variables={len(q4_rows)}")
    print(f"q4_source_item_hits={len(hit_rows)}")
    print(f"freeze_rows={len(freeze_rows)}")
    for key, count in Counter(row["q4_batch_construct_status"] for row in q4_rows).most_common():
        print(f"q4_status.{key}={count}")
    for key, count in Counter(row["freeze_or_route_action"] for row in freeze_rows).most_common():
        print(f"freeze_action.{key}={count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
