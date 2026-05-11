from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = REPO_ROOT.parent.parent
CARD_DIR = REPO_ROOT / "docs" / "std_variable_cards"
COVERAGE_PATH = REPO_ROOT / "docs" / "public_exports" / "database_variable_coverage.json"
OUTPUT_DIR = REPO_ROOT / "docs" / "standard_system_mvp" / "amsterdam_coverage_audit"
OUTPUT_JSON = OUTPUT_DIR / "amsterdam_variable_coverage_audit.json"
OUTPUT_CSV = OUTPUT_DIR / "amsterdam_variable_coverage_audit.csv"
OUTPUT_MD = REPO_ROOT / "docs" / "standard_system_mvp" / "AMSTERDAM_FULL_VARIABLE_COVERAGE_AUDIT.md"


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

STATUS_LABELS = {
    "same_name_ready": "same-name route ready or already approved",
    "split_identity_needed": "Amsterdam needs a split/proxy/local critical-care identity",
    "bounded_candidate_only": "source evidence exists, but approval requires bounded source review",
    "not_supported_or_blocked": "not supported or blocked under current Amsterdam source evidence",
}


AMSTERDAM_ALREADY_SPLIT_IDENTITIES = {
    "std_days_to_next_icu_mcu_admission",
    "std_weight_icu_baseline_grouped_proxy",
}

KNOWN_SPLIT_REQUIRED = {
    "std_bmi_admission_baseline",
    "std_bmi_icu_baseline",
    "std_days_to_next_hospital_admission",
    "std_hospital_los_days",
    "std_id_map_subject_hadm",
    "std_id_map_subject_hadm_stay",
    "std_weight_admission_baseline",
    "std_weight_icu_baseline",
}

KNOWN_BOUNDED_ONLY = {
    "std_high_flow_nasal_cannula_active",
    "std_supplemental_oxygen_active",
}

KNOWN_BLOCKED = {
    "std_microbiology_test_event",
    "std_microbiology_organism_isolate",
    "std_microbiology_antibiotic_susceptibility",
    "std_race",
}

CORE_SAME_NAME_READY = {
    "std_map",
    "std_sbp",
    "std_dbp",
    "std_respiratory_rate",
    "std_spo2",
    "std_temp",
    "std_glucose",
    "std_sodium",
    "std_potassium",
    "std_chloride",
    "std_creatinine",
    "std_lactate_bg",
    "std_ph_bg",
    "std_paco2",
    "std_pao2",
    "std_oxygen_partial_pressure_bg_allspecimen",
    "std_carbon_dioxide_partial_pressure_bg_allspecimen",
    "std_oxygen_saturation_bg_allspecimen",
    "std_oxygen_saturation_bg_arterial_specimen",
    "std_bicarbonate_bg",
    "std_bun",
    "std_hemoglobin",
    "std_hematocrit",
    "std_platelet_count",
    "std_wbc_count",
    "std_total_bilirubin",
    "std_albumin",
    "std_inr",
    "std_pt",
    "std_aptt",
}

READY_DERIVED_FROM_APPROVED_SUPPORT = {
    "std_mechanical_ventilation_imv_niv_active",
    "std_advanced_respiratory_support_active",
    "std_vasopressor_support_agent_episode",
}

FOLLOWUP_OR_TRIAL_KEYWORDS = (
    "_28d_",
    "_30d_",
    "_90d_",
    "_365d_",
    "free_days",
    "followup_bridge",
)

HOSPITAL_ONLY_PATTERNS = (
    "std_hospital_current_",
    "std_hospital_medication_",
    "std_hospital_provider_",
    "std_hospital_ecmo_",
    "std_hospital_delirium_",
    "std_ed_current_",
)

SPECIMEN_MODIFIER_TOKENS = (
    "_ascites",
    "_csf",
    "_joint_fluid",
    "_other_body_fluid",
    "_pleural",
    "_stool",
    "_urine",
)

SOURCE_TABLE_CAPABILITIES = {
    "admissions_core": (
        "ICU/MCU admission rows, gender, grouped age/weight/height, origin/destination, "
        "stay boundary, and date-of-death fields."
    ),
    "numericitems_event": (
        "high-volume bedside numeric observations, blood gases, routine labs, device settings, "
        "and numeric intake/output records."
    ),
    "listitems_event": (
        "categorical/ordinal bedside states, admission context, retrospective score/admin fields, "
        "and selected support or assessment states."
    ),
    "drugitems_event": (
        "medication and continuous infusion records, including vasoactive support and fluid inputs."
    ),
    "processitems_interval": (
        "start-stop process/device intervals, including ventilation/RRT/tracheostomy-adjacent states."
    ),
    "procedureorderitems_event": "procedure/order workflow records, not a full hospital CPOE equivalent.",
    "freetextitems_event": "free-text events, useful for bounded review only.",
    "amsterdam_item_dictionary_legacy": "official legacy item dictionary mirror used for item-level source search.",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_bullet(text: str, label: str) -> str:
    match = re.search(rf"- `{re.escape(label)}`:\s*(.+)", text)
    if match:
        return match.group(1).strip().strip("`")
    match = re.search(rf"- {re.escape(label)}:\s*(.+)", text)
    return match.group(1).strip().strip("`") if match else ""


def parse_card(variable_id: str) -> dict[str, str]:
    path = CARD_DIR / f"{variable_id}.md"
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8", errors="replace")
    approved_databases: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line.startswith("| ") and "reviewed_approved" in line:
            cells = [cell.strip(" `") for cell in line.strip("|").split("|")]
            if cells:
                approved_databases.append(cells[0])
    return {
        "standardized_english_name": parse_bullet(text, "standardized English name"),
        "semantic_folder": parse_bullet(text, "semantic folder"),
        "standard_unit": parse_bullet(text, "standard unit"),
        "value_type": parse_bullet(text, "value type"),
        "grain": parse_bullet(text, "grain"),
        "approved_database_list": ";".join(sorted(set(approved_databases))),
    }


def load_variable_universe() -> tuple[list[str], set[str]]:
    coverage = load_json(COVERAGE_PATH)
    variable_ids: set[str] = set()
    amsterdam_ids: set[str] = set()
    for db in coverage["database_coverage"]:
        ids = set(db.get("variable_ids", []))
        variable_ids.update(ids)
        if db.get("database_id") == "AmsterdamUMCdb-1.0.2":
            amsterdam_ids = ids
    return sorted(variable_ids), amsterdam_ids


def classify_variable(variable_id: str, meta: dict[str, str]) -> str:
    vid = variable_id
    semantic_folder = meta.get("semantic_folder", "")
    value_type = meta.get("value_type", "")
    grain = meta.get("grain", "")

    if "microbiology" in vid:
        return "class9_microbiology_multi_entity_family"

    if any(token in vid for token in FOLLOWUP_OR_TRIAL_KEYWORDS):
        return "class5_episode_interval_bridge"

    score_terms = (
        "sofa",
        "sapsii",
        "oasis",
        "apsiii",
        "lods",
        "meld",
        "gcs",
        "aki",
        "kdigo",
        "sepsis",
        "septic",
        "sirs",
        "sic_",
        "suspected_infection",
        "charlson",
        "delirium_assessment_same_time_summary",
    )
    if any(term in vid for term in score_terms) or semantic_folder in {"scores", "diagnosis_computable"}:
        return "class8_score_phenotype_composite_derived"

    if (
        "urinalysis_result" in vid
        or "sediment_result" in vid
        or vid.endswith("_casts_urine")
        or "_casts_urine_" in vid
        or "lupus_anticoagulant_result" in vid
    ):
        return "class6_ordinal_text_semiquantitative_result"

    if "episode" in vid or "bridge" in vid:
        return "class5_episode_interval_bridge"

    admin_terms = (
        "id_map",
        "sex",
        "diagnosis",
        "procedure_icd",
        "hcpcs",
        "drg",
        "discharge_disposition",
        "entry_source",
        "exit_destination",
        "provider_order",
        "medication_order",
        "order_workflow",
        "order_intent",
    )
    if (
        any(term in vid for term in admin_terms)
        or vid in {"std_age", "std_race"}
        or semantic_folder
        in {
        "demographics",
        "diagnosis_current",
        "encounter_information",
        "id_mapping",
        "orders",
        }
    ):
        return "class7_diagnosis_admin_demographic_id_map"

    if (
        vid.endswith("_active")
        or "_active_" in vid
        or vid.endswith("_observed")
        or "reintubation" in vid
        or value_type in {"state_episode", "binary state"}
    ):
        return "class3_binary_state_episode"

    class4_terms = (
        "input_event",
        "output_event",
        "parameter_event",
        "infusion_event",
        "administration_event",
        "administration_detail",
        "fluid_removal_event",
        "medication_input",
        "ingredient_component",
        "performed_intervention_event",
        "device_parameter",
        "ventilator_parameter",
        "urine_output_event",
    )
    if any(term in vid for term in class4_terms) or semantic_folder in {
        "medication",
        "intake_output_balance",
        "treatment_intervention",
    }:
        return "class4_treatment_device_io_event_stream"

    class2_terms = (
        "baseline",
        "summary",
        "los_days",
        "days_to_",
        "bmi_",
        "balance_daily",
        "balance_hourly",
        "mortality",
        "readmission",
    )
    if any(term in vid for term in class2_terms) or "summary" in grain:
        return "class2_baseline_summary_window_numeric"

    if semantic_folder in {"laboratory", "vital_signs", "anthropometrics"} or "numeric" in value_type:
        return "class1_event_level_numeric"

    return "class7_diagnosis_admin_demographic_id_map"


def source_aliases(variable_id: str) -> list[str]:
    alias_map = {
        "std_map": ["mean arterial", "gemiddelde", "map"],
        "std_sbp": ["systolic", "systolische"],
        "std_dbp": ["diastolic", "diastolische"],
        "std_spo2": ["spo2", "oxygen saturation spo2", "saturatie"],
        "std_respiratory_rate": ["respiratory rate", "ademfreq", "ademfrequentie"],
        "std_temp": ["temperature", "temperatuur", "temp "],
        "std_glucose": ["glucose"],
        "std_sodium": ["sodium", "natrium"],
        "std_potassium": ["potassium", "kalium"],
        "std_chloride": ["chloride", "chloor"],
        "std_creatinine": ["creatinine", "kreatinine"],
        "std_lactate_bg": ["lactate", "lactaat"],
        "std_ph_bg": ["blood ph", "ph (bloed)"],
        "std_paco2": ["pco2"],
        "std_pao2": ["po2"],
        "std_hemoglobin": ["hemoglobin", "hemoglobine"],
        "std_hematocrit": ["hematocrit", "hematocriet"],
        "std_platelet_count": ["platelets", "thrombo"],
        "std_wbc_count": ["leukocytes", "leukocyten", "white blood"],
        "std_bun": ["urea", "ureum", "bun"],
        "std_total_bilirubin": ["bilirubin total", "bili totaal", "bilirubine"],
        "std_albumin": ["albumin", "albumine"],
        "std_inr": ["inr"],
        "std_pt": ["prothrombin", "pt "],
        "std_aptt": ["aptt"],
        "std_base_excess_bg": ["base excess", "base-excess"],
        "std_bicarbonate_bg": ["bicarbonate", "hco3"],
    }
    if variable_id in alias_map:
        return alias_map[variable_id]
    base = re.sub(r"^(std_|trial_style_)", "", variable_id)
    base = re.sub(
        r"_(ascites|csf|joint_fluid|other_body_fluid|pleural|stool|urine|bg|whole_blood|allspecimen|arterial_specimen)$",
        "",
        base,
    )
    tokens = [item for item in re.split(r"[_\W]+", base) if len(item) >= 4]
    return [" ".join(tokens)] + tokens[:4]


def load_dictionary_search_text() -> list[dict[str, str]]:
    dictionary_path = (
        WORKSPACE_ROOT
        / "Methods"
        / "Clinical_Database"
        / "local_work"
        / "Layer 2"
        / "AmsterdamUMCdb-1.0.2"
        / "reviewed_unsplit"
        / "amsterdam_item_dictionary_legacy.parquet"
    )
    if not dictionary_path.exists():
        return []
    try:
        import duckdb  # type: ignore
    except ImportError:
        return []
    query = """
        SELECT "table" AS source_table,
               lower(coalesce(item, '') || ' ' || coalesce(item_en, '') || ' ' || coalesce(abbreviation, '')) AS text
        FROM read_parquet(?)
    """
    rows = duckdb.connect().execute(query, [dictionary_path.as_posix()]).fetchall()
    return [{"source_table": source_table or "", "text": text or ""} for source_table, text in rows]


def dictionary_hits(variable_id: str, dictionary_rows: list[dict[str, str]]) -> tuple[int, str]:
    aliases = [alias.lower().strip() for alias in source_aliases(variable_id) if alias.strip()]
    if not aliases or not dictionary_rows:
        return 0, ""
    hit_tables: Counter[str] = Counter()
    for row in dictionary_rows:
        text = row["text"]
        if any(alias in text for alias in aliases):
            hit_tables[row["source_table"]] += 1
    if not hit_tables:
        return 0, ""
    return sum(hit_tables.values()), ";".join(f"{table}:{count}" for table, count in sorted(hit_tables.items()))


def decide_status(
    *,
    variable_id: str,
    class_id: str,
    amsterdam_ids: set[str],
    source_hit_count: int,
) -> tuple[str, str, str]:
    vid = variable_id

    if vid in amsterdam_ids:
        if vid in AMSTERDAM_ALREADY_SPLIT_IDENTITIES:
            return (
                "same_name_ready",
                "already_public_covered",
                "Amsterdam-specific split identity is already public-covered under its own exact name.",
            )
        return (
            "same_name_ready",
            "already_public_covered",
            "Already public-covered for Amsterdam under current governed evidence.",
        )

    if vid in KNOWN_SPLIT_REQUIRED:
        return (
            "split_identity_needed",
            "known_boundary_from_prior_review",
            "Prior Amsterdam review showed the same-name route would mix hospital-level or exact-measurement semantics; split/proxy identity is needed.",
        )

    if vid in KNOWN_BOUNDED_ONLY:
        return (
            "bounded_candidate_only",
            "known_bounded_candidate_from_prior_review",
            "Amsterdam source evidence exists, but current item/state semantics are not narrow enough for same-name approval.",
        )

    if vid in KNOWN_BLOCKED:
        return (
            "not_supported_or_blocked",
            "known_source_boundary",
            "Current Amsterdam opening source does not prove the required same-name source hierarchy or demographic field.",
        )

    if any(vid.startswith(pattern) for pattern in HOSPITAL_ONLY_PATTERNS):
        return (
            "not_supported_or_blocked",
            "hospital_level_surface_absent",
            "Amsterdam opening source is ICU/MCU centered and does not expose the required MIMIC-like hospital workflow surface.",
        )

    if vid.startswith("std_hospital_admission_") or vid in {
        "std_hospital_mortality",
        "std_hospital_readmission_30d",
    }:
        return (
            "split_identity_needed",
            "hospital_vs_icu_followup_boundary",
            "Amsterdam can support ICU/local-admission outcome variants only after a separate follow-up or mortality bridge.",
        )

    if vid.startswith("std_icu_admission_") or vid.startswith("trial_style_"):
        return (
            "bounded_candidate_only",
            "followup_bridge_needed",
            "Amsterdam date-of-death and local admission timing can support bounded review, but follow-up/free-day semantics need a bridge first.",
        )

    if class_id == "class9_microbiology_multi_entity_family":
        return (
            "not_supported_or_blocked",
            "microbiology_hierarchy_absent",
            "No Amsterdam opening microbiology parent/organism/susceptibility hierarchy has been proven.",
        )

    if vid in READY_DERIVED_FROM_APPROVED_SUPPORT:
        return (
            "same_name_ready",
            "derivable_from_approved_support_family",
            "Required parent support layers are already approved or source-bounded enough for the next governed candidate.",
        )

    if class_id == "class1_event_level_numeric":
        if vid in CORE_SAME_NAME_READY:
            return (
                "same_name_ready",
                "direct_numeric_source_ready",
                "Amsterdam numericitems/dictionary evidence supports a direct event-level candidate with low semantic risk.",
            )
        if source_hit_count > 0:
            if any(token in vid for token in SPECIMEN_MODIFIER_TOKENS):
                return (
                    "bounded_candidate_only",
                    "specimen_or_body_fluid_scope_needs_review",
                    "Dictionary evidence exists, but specimen/body-fluid identity needs item-level source review before approval.",
                )
            if "_bg" in vid or "_whole_blood" in vid or "_allspecimen" in vid or "_arterial_specimen" in vid:
                return (
                    "bounded_candidate_only",
                    "blood_gas_item_family_needs_review",
                    "Blood-gas source evidence exists, but the all-specimen/arterial/source-family rule must be locked.",
                )
            return (
                "bounded_candidate_only",
                "numeric_dictionary_hit_needs_item_review",
                "Amsterdam dictionary has candidate numeric items, but this long-tail variable needs item-level review.",
            )
        return (
            "not_supported_or_blocked",
            "no_dictionary_hit_in_opening_scan",
            "No clear Amsterdam item-dictionary hit was found in the opening scan.",
        )

    if class_id == "class2_baseline_summary_window_numeric":
        if "icu" in vid or "first_day" in vid or "balance" in vid:
            return (
                "bounded_candidate_only",
                "icu_window_or_summary_candidate",
                "Amsterdam ICU/MCU timing can support a bounded candidate, but the source window and denominator must be governed.",
            )
        return (
            "split_identity_needed",
            "summary_requires_amsterdam_specific_anchor",
            "The summary/window identity needs an Amsterdam ICU/MCU anchor or split identity before same-name use.",
        )

    if class_id == "class3_binary_state_episode":
        return (
            "bounded_candidate_only",
            "state_source_review_needed",
            "Amsterdam processitems/listitems/drugitems may support this state, but item/state boundaries need a focused source audit.",
        )

    if class_id == "class4_treatment_device_io_event_stream":
        return (
            "bounded_candidate_only",
            "event_stream_source_review_needed",
            "Amsterdam drugitems/numericitems/procedure/process tables support event-stream candidates, but unit/grain/source-family rules need review.",
        )

    if class_id == "class5_episode_interval_bridge":
        return (
            "bounded_candidate_only",
            "interval_or_followup_bridge_needed",
            "Amsterdam has ICU/MCU interval evidence, but parent-link or follow-up bridge rules must be proven.",
        )

    if class_id == "class6_ordinal_text_semiquantitative_result":
        if source_hit_count > 0:
            return (
                "bounded_candidate_only",
                "ordinal_source_hit_needs_domain_review",
                "Amsterdam list/freetext/numeric evidence exists, but the result domain must be locked before approval.",
            )
        return (
            "not_supported_or_blocked",
            "no_clear_ordinal_source_hit",
            "No clear Amsterdam ordinal/text source hit was found in the opening scan.",
        )

    if class_id == "class7_diagnosis_admin_demographic_id_map":
        if vid == "std_age":
            return (
                "split_identity_needed",
                "age_group_not_exact_age",
                "Amsterdam exposes agegroup, not exact MIMIC-like age; grouped-age identity is needed for exactness.",
            )
        if vid in {"std_icu_entry_source", "std_icu_exit_destination", "std_discharge_disposition"}:
            return (
                "same_name_ready",
                "admissions_core_admin_field_ready",
                "Amsterdam admissions_core has local origin/destination/discharge context for governed review.",
            )
        return (
            "bounded_candidate_only",
            "admin_or_demographic_review_needed",
            "Amsterdam has some admission-level fields, but this identity needs explicit grain and source review.",
        )

    if class_id == "class8_score_phenotype_composite_derived":
        return (
            "bounded_candidate_only",
            "score_or_phenotype_component_review_needed",
            "Amsterdam may support score/phenotype construction, but component trace and timing rules must be governed.",
        )

    return (
        "bounded_candidate_only",
        "default_conservative_candidate",
        "Conservative default: source review is required before approval.",
    )


def priority_tier(variable_id: str, class_id: str, status: str, phase: str) -> str:
    if phase == "already_public_covered":
        return "0_already_covered"
    if status != "same_name_ready":
        return "9_not_in_ready_batch"
    if variable_id in {
        "std_map",
        "std_sbp",
        "std_dbp",
        "std_respiratory_rate",
        "std_spo2",
        "std_temp",
        "std_glucose",
        "std_sodium",
        "std_potassium",
        "std_chloride",
        "std_creatinine",
        "std_lactate_bg",
        "std_paco2",
        "std_pao2",
        "std_bicarbonate_bg",
        "std_bun",
        "std_hemoglobin",
        "std_hematocrit",
        "std_platelet_count",
        "std_wbc_count",
    }:
        return "1_high_yield_next_batch"
    if class_id == "class1_event_level_numeric":
        return "2_numeric_spine_later"
    return "3_ready_after_current_batch"


def build_records() -> list[dict[str, Any]]:
    variable_ids, amsterdam_ids = load_variable_universe()
    dictionary_rows = load_dictionary_search_text()
    records: list[dict[str, Any]] = []
    for variable_id in variable_ids:
        meta = parse_card(variable_id)
        class_id = classify_variable(variable_id, meta)
        hit_count, hit_tables = dictionary_hits(variable_id, dictionary_rows)
        status, phase, rationale = decide_status(
            variable_id=variable_id,
            class_id=class_id,
            amsterdam_ids=amsterdam_ids,
            source_hit_count=hit_count,
        )
        tier = priority_tier(variable_id, class_id, status, phase)
        records.append(
            {
                "variable_id": variable_id,
                "semantic_folder": meta.get("semantic_folder", ""),
                "value_type": meta.get("value_type", ""),
                "grain": meta.get("grain", ""),
                "class_id": class_id,
                "class_label": CLASS_LABELS[class_id],
                "amsterdam_status_bucket": status,
                "amsterdam_status_label": STATUS_LABELS[status],
                "amsterdam_phase": phase,
                "amsterdam_already_public_covered": variable_id in amsterdam_ids,
                "dictionary_hit_count": hit_count,
                "dictionary_hit_tables": hit_tables,
                "priority_tier": tier,
                "rationale": rationale,
            }
        )
    return records


def write_outputs(records: list[dict[str, Any]]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    class_counts = Counter(row["class_id"] for row in records)
    status_counts = Counter(row["amsterdam_status_bucket"] for row in records)
    class_status_counts: dict[str, dict[str, int]] = defaultdict(dict)
    for class_id in CLASS_LABELS:
        subset = [row for row in records if row["class_id"] == class_id]
        status_counter = Counter(row["amsterdam_status_bucket"] for row in subset)
        class_status_counts[class_id] = {status: status_counter.get(status, 0) for status in STATUS_LABELS}

    payload = {
        "artifact_type": "amsterdam_full_variable_coverage_audit",
        "artifact_version": "v1",
        "created_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "database_id": "AmsterdamUMCdb-1.0.2",
        "variable_count": len(records),
        "status_buckets": STATUS_LABELS,
        "class_labels": CLASS_LABELS,
        "source_table_capabilities": SOURCE_TABLE_CAPABILITIES,
        "class_counts": dict(class_counts),
        "status_counts": dict(status_counts),
        "class_status_counts": class_status_counts,
        "records": records,
    }
    OUTPUT_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    fieldnames = [
        "variable_id",
        "semantic_folder",
        "value_type",
        "grain",
        "class_id",
        "amsterdam_status_bucket",
        "amsterdam_phase",
        "amsterdam_already_public_covered",
        "dictionary_hit_count",
        "dictionary_hit_tables",
        "priority_tier",
        "rationale",
    ]
    with OUTPUT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in records:
            writer.writerow({field: row[field] for field in fieldnames})

    high_yield = [
        row
        for row in records
        if row["priority_tier"] == "1_high_yield_next_batch" and not row["amsterdam_already_public_covered"]
    ]
    high_yield.sort(key=lambda item: (
        [
            "std_map",
            "std_sbp",
            "std_dbp",
            "std_respiratory_rate",
            "std_spo2",
            "std_temp",
            "std_glucose",
            "std_sodium",
            "std_potassium",
            "std_chloride",
            "std_creatinine",
            "std_lactate_bg",
            "std_paco2",
            "std_pao2",
            "std_bicarbonate_bg",
            "std_bun",
            "std_hemoglobin",
            "std_hematocrit",
            "std_platelet_count",
            "std_wbc_count",
        ].index(item["variable_id"])
        if item["variable_id"]
        in {
            "std_map",
            "std_sbp",
            "std_dbp",
            "std_respiratory_rate",
            "std_spo2",
            "std_temp",
            "std_glucose",
            "std_sodium",
            "std_potassium",
            "std_chloride",
            "std_creatinine",
            "std_lactate_bg",
            "std_paco2",
            "std_pao2",
            "std_bicarbonate_bg",
            "std_bun",
            "std_hemoglobin",
            "std_hematocrit",
            "std_platelet_count",
            "std_wbc_count",
        }
        else 999
    ))

    lines: list[str] = []
    lines.append("# Amsterdam Full Variable Coverage Audit")
    lines.append("")
    lines.append("Last generated: " + payload["created_at_utc"])
    lines.append("")
    lines.append("## Purpose")
    lines.append("")
    lines.append(
        "This audit assigns the current public standard-variable universe to Class 1-9 and "
        "labels each variable with an AmsterdamUMCdb-1.0.2 feasibility bucket."
    )
    lines.append("")
    lines.append("The four Amsterdam buckets are:")
    lines.append("")
    for status, label in STATUS_LABELS.items():
        lines.append(f"- `{status}`: {label}")
    lines.append("")
    lines.append("Machine-readable outputs:")
    lines.append("")
    lines.append("- `docs/standard_system_mvp/amsterdam_coverage_audit/amsterdam_variable_coverage_audit.csv`")
    lines.append("- `docs/standard_system_mvp/amsterdam_coverage_audit/amsterdam_variable_coverage_audit.json`")
    lines.append("")
    lines.append("## Source Surface Scanned")
    lines.append("")
    for source_name, description in SOURCE_TABLE_CAPABILITIES.items():
        lines.append(f"- `{source_name}`: {description}")
    lines.append("")
    lines.append("## Headline Counts")
    lines.append("")
    lines.append(f"- public variable denominator: `{len(records)}`")
    lines.append(f"- already public-covered in Amsterdam: `{sum(1 for row in records if row['amsterdam_already_public_covered'])}`")
    for status in STATUS_LABELS:
        lines.append(f"- `{status}`: `{status_counts.get(status, 0)}`")
    lines.append("")
    lines.append("## Counts By Class")
    lines.append("")
    lines.append("| Class | Total | same_name_ready | split_identity_needed | bounded_candidate_only | not_supported_or_blocked |")
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: |")
    for class_id, label in CLASS_LABELS.items():
        by_status = class_status_counts[class_id]
        lines.append(
            f"| {label} | `{class_counts.get(class_id, 0)}` | "
            f"`{by_status.get('same_name_ready', 0)}` | "
            f"`{by_status.get('split_identity_needed', 0)}` | "
            f"`{by_status.get('bounded_candidate_only', 0)}` | "
            f"`{by_status.get('not_supported_or_blocked', 0)}` |"
        )
    lines.append("")
    lines.append("## Immediate Same-Name High-Yield Batch")
    lines.append("")
    lines.append(
        "These are not yet approvals. They are the recommended next governed Amsterdam candidate "
        "batch because they are direct ICU numeric event variables with high downstream reuse."
    )
    lines.append("")
    lines.append("| Order | Variable | Class | Source scan | Rationale |")
    lines.append("| ---: | --- | --- | --- | --- |")
    for index, row in enumerate(high_yield, start=1):
        source_scan = row["dictionary_hit_tables"] or "opening numeric source route"
        lines.append(
            f"| {index} | `{row['variable_id']}` | {row['class_label']} | "
            f"`{source_scan}` | {row['rationale']} |"
        )
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append(
        "`same_name_ready` means Amsterdam can enter governed candidate execution under the current "
        "standard variable identity, or is already approved. It is not a blanket approval."
    )
    lines.append("")
    lines.append(
        "`split_identity_needed` means Amsterdam has useful data, but using the MIMIC same name would "
        "mix hospital-level, exact-measurement, or other incompatible semantics."
    )
    lines.append("")
    lines.append(
        "`bounded_candidate_only` means source evidence exists but the row family, item set, unit, "
        "interval, or parent-link rule still needs focused review before approval."
    )
    lines.append("")
    lines.append(
        "`not_supported_or_blocked` means the current Amsterdam opening source surface does not support "
        "the required same-name source structure."
    )
    lines.append("")
    lines.append("## Immediate Recommendation")
    lines.append("")
    lines.append(
        "Start with the high-yield Class 1 batch above, then rerun this audit after each approved batch "
        "so Amsterdam coverage moves from source-ready to governed-approved in controlled waves."
    )
    OUTPUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    records = build_records()
    write_outputs(records)
    print(f"Wrote {OUTPUT_CSV}")
    print(f"Wrote {OUTPUT_JSON}")
    print(f"Wrote {OUTPUT_MD}")
    print(f"variable_count={len(records)}")
    status_counts = Counter(row["amsterdam_status_bucket"] for row in records)
    for status in STATUS_LABELS:
        print(f"{status}={status_counts.get(status, 0)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
