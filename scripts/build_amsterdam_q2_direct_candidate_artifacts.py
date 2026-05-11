from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
STD_MVP_DIR = REPO_ROOT / "docs" / "standard_system_mvp"
DATABASE_ID = "AmsterdamUMCdb-1.0.2"
DATABASE_SLUG = "amsterdamumcdb_1_0_2"
DATE = "2026-05-04"


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def variable_dir(variable_id: str) -> Path:
    return STD_MVP_DIR / variable_id


def standard_ref(variable_id: str) -> str:
    return f"docs/standard_system_mvp/{variable_id}/variable_spec.json"


def execution_ref(variable_id: str) -> str:
    return f"docs/standard_system_mvp/{variable_id}/execution.py"


def mapping_ref(variable_id: str) -> str:
    return f"docs/standard_system_mvp/{variable_id}/mapping_spec_{DATABASE_SLUG}.json"


def evidence_refs(variable_id: str, semantic_folder: str, review_path: str) -> dict[str, str]:
    base5 = f"Methods/Clinical_Database/local_work/Layer 5/{DATABASE_ID}/{variable_id}"
    return {
        "public_card_path": f"docs/std_variable_cards/{variable_id}.md",
        "candidate_evidence_review_path": review_path,
        "local_extract_code_path": f"{base5}/extract_code/Extract_Code_{variable_id}.py",
        "local_output_asset_path": f"Methods/Clinical_Database/local_work/Layer 3/{DATABASE_ID}/{semantic_folder}/{variable_id}/{variable_id}_long.parquet",
        "local_asset_manifest_path": f"{base5}/asset_manifest.md",
        "local_log_archive_dir": f"{base5}/log_archive",
        "local_preview_path": f"{base5}/preview/{variable_id}_preview.csv",
        "local_knowledge_package_path": f"{base5}/Layer5_PerVariable_KnowledgePackage.xlsx",
        "local_query_summary_dir": f"{base5}/query_summary",
    }


def binary_variable_spec(
    *,
    variable_id: str,
    name_en: str,
    semantic_intent: str,
    semantic_definition: str,
    positive_state_meaning: str,
    same_name_rule: str,
    mapping_note: str,
) -> dict[str, Any]:
    return {
        "artifact_type": "variable_spec",
        "artifact_version": "v0_draft",
        "artifact_status": "draft_public_variable_lock",
        "mvp_phase": "class_3_amsterdam_q2_build_first_candidate_mvp",
        "created_at": DATE,
        "public_scope": "github_safe",
        "variable_class": {
            "variable_class_id": "binary_state_episode",
            "class_contract_ref": "Framework_Guideline/StandardVariableClass_BinaryStateEpisode_Contract.md",
        },
        "variable_identity": {
            "variable_id": variable_id,
            "variable_version": "v0_draft",
            "standardized_name_en": name_en,
            "semantic_folder": "treatment_state",
            "category": "treatment_state",
        },
        "immutable_core": {
            "semantic_intent": semantic_intent,
            "semantic_definition": semantic_definition,
            "semantic_grain": "one row per positive state episode",
            "value_family": "binary_state",
            "source_value_class": "positive_state_episode",
            "same_name_cross_database_rule": same_name_rule,
        },
        "state_episode_contract": {
            "target_entity_grain": "ICU stay",
            "anchor_family": "ICU admission anchor",
            "positive_state_meaning": positive_state_meaning,
            "negative_state_representation": "absence_of_row_not_proven_negative",
            "episode_start_rule": "start at the unioned approved parent-support interval start",
            "episode_end_rule": "end at the unioned approved parent-support interval end",
            "continuity_rule": "merge overlapping or exactly contiguous source intervals within the same stay under the locked included support family",
            "allowed_true_value": True,
            "allowed_false_rows": False,
            "no_row_interpretation": "no retained positive episode under the approved or candidate source rule",
        },
        "canonical_representation": {
            "canonical_unit": "none",
            "value_type": "boolean_state_episode",
            "storage_type": "boolean",
            "timestamp_start_required": True,
            "timestamp_end_required": True,
            "duration_required": True,
            "identifier_roles": ["subject_id", "hadm_id", "stay_id"],
            "retained_value_domain": [True],
            "duration_unit": "minutes",
            "time_anchor": "icu_intime",
        },
        "execution_governance": {
            "current_status": "governed_execution_entrypoint_present_candidate_mapping_pending_owner_review",
            "formal_output_rule": "Formal outputs should go through execution.py reading this variable_spec and a database mapping_spec.",
        },
        "current_public_mvp_links": {
            "mapping_specs": [mapping_ref(variable_id)],
            "execution_entrypoint": execution_ref(variable_id),
            "public_card": f"docs/std_variable_cards/{variable_id}.md",
            "class_contract": "Framework_Guideline/StandardVariableClass_BinaryStateEpisode_Contract.md",
            "build_first_note": mapping_note,
        },
    }


def binary_mapping_spec(
    *,
    variable_id: str,
    semantic_intent: str,
    source_status_codes: list[str],
    source_status_labels: dict[str, str],
    normalization_rule_id: str,
    source_rule_summary: str,
    boundary_notice: str,
    local_prepared_input_asset: str,
    supporting_input_assets: list[str],
    status: str,
) -> dict[str, Any]:
    return {
        "artifact_type": "mapping_spec",
        "artifact_version": "v0_candidate",
        "artifact_status": "candidate_mapping_pending_owner_review",
        "approval_status": "not_owner_approved",
        "mvp_phase": "class_3_amsterdam_q2_build_first_candidate_mvp",
        "created_at": DATE,
        "updated_at": DATE,
        "public_scope": "github_safe",
        "variable_spec_ref": standard_ref(variable_id),
        "standard_variable": {
            "variable_id": variable_id,
            "variable_version": "v0_draft",
            "semantic_intent": semantic_intent,
            "semantic_grain": "one row per positive state episode",
            "source_value_class": "positive_state_episode",
            "canonical_unit": "none",
            "canonical_value_family": "binary_state",
        },
        "candidate_boundary_notice": {
            "status": status,
            "owner_approval_status": "not_owner_approved",
            "reason": boundary_notice,
            "approval_gate": "candidate runtime evidence only until detailed review and owner approval close",
        },
        "database_mapping": {
            "database_id": DATABASE_ID,
            "source_locator_mode": "derived_union_from_governed_parent_state_episode_assets",
            "source_package": "Amsterdam governed parent Layer3 assets",
            "source_table": "std_invasive_mechanical_ventilation_active + std_noninvasive_ventilation_active",
            "local_prepared_input_asset": local_prepared_input_asset,
            "supporting_input_assets": supporting_input_assets,
            "source_status_field": "source_parent_variable_set",
            "source_status_codes": source_status_codes,
            "source_status_code_labels": source_status_labels,
            "source_start_field": "support_starttime",
            "source_end_field": "support_endtime",
            "source_duration_field": "support_duration_minutes",
            "source_grain": "one governed Amsterdam parent respiratory-support positive episode",
            "target_grain": "one retained positive derived support-family episode after same-stay interval union",
            "identifier_normalization": {
                "subject_id_role": "patientid inherited from approved parent assets",
                "hadm_id_role": "not separately available in the current Amsterdam opening mapping",
                "stay_id_role": "admissionid inherited from approved parent assets and normalized to ICU/MC stay_id",
                "stay_link_status": "icu_mcu_local_admission_via_admissionid",
            },
        },
        "state_episode_build_translation": {
            "target_entity_grain": "ICU stay",
            "anchor_family": "ICU admission anchor",
            "positive_state_translation": source_rule_summary,
            "negative_state_translation": "do not emit false rows",
            "episode_start_translation": "use the merged parent-support interval start",
            "episode_end_translation": "use the merged parent-support interval end",
            "continuity_translation": "merge overlapping or exactly contiguous included parent intervals within the same stay",
            "no_row_translation": "absence of a row means no retained positive episode under this candidate source rule",
        },
        "representation_and_normalization": {
            "canonical_unit": "none",
            "normalization_rule_id": normalization_rule_id,
            "primary_output_value_field": variable_id,
            "start_time_output_field": "support_starttime",
            "end_time_output_field": "support_endtime",
            "duration_output_field": "support_duration_minutes",
            "relative_anchor_output_field": "anchor_type",
            "relative_start_output_field": "relative_start_time_value",
            "relative_end_output_field": "relative_end_time_value",
            "relative_time_unit": "minutes",
        },
        "validation_contract": {
            "required_non_null_fields": [
                "subject_id",
                "stay_id",
                "support_episode_index",
                "support_starttime",
                "support_endtime",
                "support_duration_minutes",
                variable_id,
            ],
            "duplicate_key": ["stay_id", "support_episode_index"],
            "duplicate_action": "fail",
            "positive_only_no_row_policy_check": "false rows are not emitted; absence of row is not universal negative proof",
            "episode_time_order_action": "fail_when_end_not_after_start",
            "notes": [
                "Build-first candidate mapping; owner approval is explicitly pending.",
                boundary_notice,
            ],
        },
        "execution_contract": {
            "governed_execution_entrypoint": execution_ref(variable_id),
            "current_reference_implementation": f"Methods/Clinical_Database/local_work/Layer 5/{DATABASE_ID}/{variable_id}/extract_code/Extract_Code_{variable_id}.py",
            "formal_output_rule": "Candidate output should be generated through the governed execution.py path and reviewed before approval.",
            "non_bypassable_target_rule": "Approval-facing outputs should be produced only through the governed execution.py path.",
        },
        "evidence_refs": evidence_refs(variable_id, "treatment_state", "docs/standard_system_mvp/AMSTERDAM_Q2_DIRECT_BUILD_CANDIDATE_REVIEW.md"),
    }


def admin_variable_spec(
    *,
    variable_id: str,
    name_en: str,
    semantic_folder: str,
    semantic_intent: str,
    semantic_definition: str,
    semantic_grain: str,
    target_entity_grain: str,
    normalization_rule: str,
) -> dict[str, Any]:
    return {
        "artifact_type": "variable_spec",
        "artifact_version": "v0_draft",
        "artifact_status": "draft_public_variable_lock",
        "mvp_phase": "class_7_amsterdam_q2_build_first_candidate_mvp",
        "created_at": DATE,
        "public_scope": "github_safe",
        "variable_class": {
            "variable_class_id": "diagnosis_admin_demographic_id_map",
            "class_contract_ref": "Framework_Guideline/StandardVariableClass_DiagnosisAdminDemographicIdMap_Contract.md",
        },
        "variable_identity": {
            "variable_id": variable_id,
            "variable_version": "v0_draft",
            "standardized_name_en": name_en,
            "semantic_folder": semantic_folder,
            "category": semantic_folder,
        },
        "immutable_core": {
            "semantic_intent": semantic_intent,
            "semantic_definition": semantic_definition,
            "semantic_grain": semantic_grain,
            "value_family": "administrative_category",
            "source_value_class": "source_recorded_admin_category",
            "same_name_cross_database_rule": "Database mappings must preserve the declared administrative grain and keep source-faithful local categories visible unless a governed grouping rule is explicitly approved.",
        },
        "admin_demographic_contract": {
            "target_entity_grain": target_entity_grain,
            "identifier_scope_rule": "subject_id and stay_id are required; hadm_id may be unavailable in Amsterdam and must remain visibly null rather than fabricated",
            "source_authority_rule": "use the source administrative admission/discharge field as the authority for the retained category",
            "normalization_rule": normalization_rule,
            "no_row_interpretation": "no retained source category under the current source-field rule; not proof that the administrative concept is absent",
        },
        "canonical_representation": {
            "canonical_unit": "none",
            "value_type": "categorical_text_admin_record",
            "storage_type": "string_label",
            "identifier_roles": ["subject_id", "hadm_id", "stay_id"],
            "time_anchor": "icu_intime_or_administrative_record",
        },
        "execution_governance": {
            "current_status": "governed_execution_entrypoint_present_candidate_mapping_pending_owner_review",
            "formal_output_rule": "Formal outputs should go through execution.py reading this variable_spec and a database mapping_spec.",
        },
        "current_public_mvp_links": {
            "mapping_specs": [mapping_ref(variable_id)],
            "execution_entrypoint": execution_ref(variable_id),
            "public_card": f"docs/std_variable_cards/{variable_id}.md",
            "class_contract": "Framework_Guideline/StandardVariableClass_DiagnosisAdminDemographicIdMap_Contract.md",
        },
    }


def admin_mapping_spec(
    *,
    variable_id: str,
    semantic_folder: str,
    semantic_intent: str,
    semantic_grain: str,
    target_entity_grain: str,
    source_value_field: str,
    primary_output_value_field: str,
    normalization_rule_id: str,
    value_normalization_translation: str,
    source_rule_summary: str,
    boundary_notice: str,
    status: str,
) -> dict[str, Any]:
    return {
        "artifact_type": "mapping_spec",
        "artifact_version": "v0_candidate",
        "artifact_status": "candidate_mapping_pending_owner_review",
        "approval_status": "not_owner_approved",
        "mvp_phase": "class_7_amsterdam_q2_build_first_candidate_mvp",
        "created_at": DATE,
        "updated_at": DATE,
        "public_scope": "github_safe",
        "variable_spec_ref": standard_ref(variable_id),
        "standard_variable": {
            "variable_id": variable_id,
            "variable_version": "v0_draft",
            "semantic_intent": semantic_intent,
            "semantic_grain": semantic_grain,
            "source_value_class": "source_recorded_admin_category",
            "canonical_unit": "none",
            "canonical_value_family": "administrative_category",
        },
        "candidate_boundary_notice": {
            "status": status,
            "owner_approval_status": "not_owner_approved",
            "reason": boundary_notice,
            "approval_gate": "candidate runtime evidence only until detailed review and owner approval close",
        },
        "database_mapping": {
            "database_id": DATABASE_ID,
            "source_locator_mode": "direct_admissions_core_admin_field",
            "source_package": "Amsterdam admissions",
            "source_table": "admissions_core",
            "local_prepared_input_asset": f"Methods/Clinical_Database/local_work/Layer 2/{DATABASE_ID}/reviewed_unsplit/admissions_core.parquet",
            "source_value_field": source_value_field,
            "source_grain": "one Amsterdam admissions_core local ICU/MC admission row",
            "target_grain": target_entity_grain,
            "identifier_normalization": {
                "subject_id_role": "patientid",
                "hadm_id_role": "not separately available in the current Amsterdam opening mapping",
                "stay_id_role": "admissionid normalized to ICU/MC stay_id",
                "stay_link_status": "icu_mcu_local_admission_via_admissionid",
            },
        },
        "admin_demographic_build_translation": {
            "target_entity_grain": target_entity_grain,
            "identifier_translation": "emit subject_id from patientid and stay_id from admissionid; keep hadm_id null because no separate hospital admission id is currently available",
            "value_normalization_translation": value_normalization_translation,
            "no_row_translation": "rows with null source values are not emitted in this first candidate asset",
        },
        "representation_and_normalization": {
            "canonical_unit": "none",
            "normalization_rule_id": normalization_rule_id,
            "primary_output_value_field": primary_output_value_field,
            "source_value_output_field": source_value_field,
        },
        "validation_contract": {
            "required_non_null_fields": [
                "subject_id",
                "stay_id",
                "admin_record_index",
                primary_output_value_field,
            ],
            "duplicate_key": ["stay_id", "admin_record_index"],
            "duplicate_action": "fail",
            "notes": [
                "Build-first candidate mapping; owner approval is explicitly pending.",
                source_rule_summary,
                boundary_notice,
            ],
        },
        "execution_contract": {
            "governed_execution_entrypoint": execution_ref(variable_id),
            "current_reference_implementation": f"Methods/Clinical_Database/local_work/Layer 5/{DATABASE_ID}/{variable_id}/extract_code/Extract_Code_{variable_id}.py",
            "formal_output_rule": "Candidate output should be generated through the governed execution.py path and reviewed before approval.",
            "non_bypassable_target_rule": "Approval-facing outputs should be produced only through the governed execution.py path.",
        },
        "evidence_refs": evidence_refs(variable_id, semantic_folder, "docs/standard_system_mvp/AMSTERDAM_Q2_DIRECT_BUILD_CANDIDATE_REVIEW.md"),
    }


def vasopressor_agent_mapping_spec() -> dict[str, Any]:
    variable_id = "std_vasopressor_support_agent_episode"
    return {
        "artifact_type": "mapping_spec",
        "artifact_version": "v0_candidate",
        "artifact_status": "candidate_mapping_pending_owner_review",
        "approval_status": "not_owner_approved",
        "mvp_phase": "class_5_amsterdam_q2_build_first_candidate_mvp",
        "created_at": DATE,
        "updated_at": DATE,
        "public_scope": "github_safe",
        "variable_spec_ref": standard_ref(variable_id),
        "standard_variable": {
            "variable_id": variable_id,
            "variable_version": "v0_draft",
            "semantic_intent": "agent-specific vasopressor support episode",
            "semantic_grain": "one row per retained ICU stay agent-specific support episode interval",
            "source_value_class": "positive_agent_episode",
            "canonical_unit": "none",
            "canonical_value_family": "categorical_episode",
        },
        "candidate_boundary_notice": {
            "status": "built_candidate_owner_approval_pending",
            "owner_approval_status": "not_owner_approved",
            "reason": "Amsterdam exposes continuous syringe-pump drugitems rows for vasopressor-capable agents and an approved parent std_vasopressor_support_active asset. Terlipressin is retained as its own agent label rather than silently mapped to vasopressin.",
            "approval_gate": "candidate runtime evidence only until detailed review and owner approval close",
        },
        "database_mapping": {
            "database_id": DATABASE_ID,
            "source_locator_mode": "child_agent_reconstruction_from_reviewed_drugitems_and_parent_vasopressor_support_active",
            "source_package": "drugitems_event plus parent std_vasopressor_support_active",
            "source_table": "drugitems_event + std_vasopressor_support_active",
            "local_prepared_input_asset": f"Methods/Clinical_Database/local_work/Layer 2/{DATABASE_ID}/reviewed_unsplit/drugitems_event.parquet",
            "supporting_input_assets": [
                f"Methods/Clinical_Database/local_work/Layer 3/{DATABASE_ID}/treatment_state/std_vasopressor_support_active/std_vasopressor_support_active_long.parquet",
                f"Methods/Clinical_Database/local_work/Layer 2/{DATABASE_ID}/reviewed_unsplit/admissions_core.parquet",
            ],
            "source_status_field": "std_vasoactive_agent",
            "source_status_codes": ["dopamine", "epinephrine", "norepinephrine", "phenylephrine", "terlipressin"],
            "source_itemid_labels": {
                "6818": "Adrenaline (Epinefrine) -> epinephrine",
                "7179": "Dopamine (Inotropin) -> dopamine",
                "7229": "Noradrenaline (Norepinefrine) -> norepinephrine",
                "12467": "Terlipressine (Glypressin) -> terlipressin",
                "19929": "Fenylefrine -> phenylephrine",
            },
            "source_start_field": "agent_support_starttime",
            "source_end_field": "agent_support_endtime",
            "source_grain": "one reviewed Amsterdam vasoactive drug course before same-agent interval union",
            "target_grain": "one retained positive agent-specific support episode row",
            "identifier_normalization": {
                "subject_id_role": "patientid joined from Amsterdam admissions_core by admissionid",
                "hadm_id_role": "not separately available in the current Amsterdam opening mapping",
                "stay_id_role": "admissionid normalized to ICU/MC stay_id",
                "stay_link_status": "icu_mcu_local_admission_via_admissionid",
            },
        },
        "episode_interval_build_translation": {
            "target_entity_grain": "ICU stay",
            "anchor_family": "ICU admission anchor",
            "episode_label_translation": "retain standardized vasoactive agent labels dopamine, epinephrine, norepinephrine, phenylephrine, and terlipressin",
            "episode_start_translation": "use merged same-agent support interval start",
            "episode_end_translation": "use merged same-agent support interval end",
            "continuity_translation": "merge overlapping or exactly contiguous intervals only when stay_id and std_vasoactive_agent match",
            "parent_link_translation": "link to the same-stay Amsterdam std_vasopressor_support_active parent episode by interval containment when available",
            "no_row_translation": "absence of a retained child row means no positive agent-specific episode under this source rule",
        },
        "representation_and_normalization": {
            "canonical_unit": "none",
            "normalization_rule_id": "amsterdam_drugitems_agent_specific_vasopressor_episode_with_terlipressin_retained_v1",
            "primary_output_value_field": "std_vasopressor_support_agent_episode",
            "primary_episode_label_field": "std_vasoactive_agent",
            "start_time_output_field": "agent_support_starttime",
            "end_time_output_field": "agent_support_endtime",
            "duration_output_field": "agent_support_duration_minutes",
            "relative_anchor_output_field": "anchor_type",
            "relative_start_output_field": "relative_start_time_value",
            "relative_end_output_field": "relative_end_time_value",
            "relative_time_unit": "minutes",
        },
        "validation_contract": {
            "required_non_null_fields": [
                "subject_id",
                "stay_id",
                "source_agent_support_episode_id",
                "std_vasoactive_agent",
                "agent_support_starttime",
                "agent_support_endtime",
                "agent_support_duration_minutes",
                "std_vasopressor_support_agent_episode",
            ],
            "duplicate_key": ["source_agent_support_episode_id"],
            "duplicate_action": "fail",
            "no_row_policy_check": "absence of row is not universal proof of no vasopressor support; use parent std_vasopressor_support_active for any-support timing",
            "episode_time_order_action": "fail_when_end_not_after_start",
            "label_domain_check": ["dopamine", "epinephrine", "norepinephrine", "phenylephrine", "terlipressin"],
            "notes": [
                "Build-first candidate mapping; owner approval is explicitly pending.",
                "Terlipressin is a source-retained Amsterdam label and is not silently collapsed to vasopressin.",
            ],
        },
        "execution_contract": {
            "governed_execution_entrypoint": execution_ref(variable_id),
            "current_reference_implementation": f"Methods/Clinical_Database/local_work/Layer 5/{DATABASE_ID}/{variable_id}/extract_code/Extract_Code_{variable_id}.py",
            "formal_output_rule": "Candidate output should be generated through the governed execution.py path and reviewed before approval.",
            "non_bypassable_target_rule": "Approval-facing outputs should be produced only through the governed execution.py path.",
        },
        "evidence_refs": evidence_refs(variable_id, "treatment_state", "docs/standard_system_mvp/AMSTERDAM_Q2_DIRECT_BUILD_CANDIDATE_REVIEW.md"),
    }


def update_vasopressor_agent_variable_spec() -> None:
    path = variable_dir("std_vasopressor_support_agent_episode") / "variable_spec.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    labels = data.setdefault("canonical_representation", {}).setdefault("retained_label_domain", [])
    if "terlipressin" not in labels:
        labels.append("terlipressin")
    data["canonical_representation"]["retained_label_domain"] = sorted(labels)
    links = data.setdefault("current_public_mvp_links", {})
    mappings = links.setdefault("mapping_specs", [])
    amsterdam_mapping = mapping_ref("std_vasopressor_support_agent_episode")
    if amsterdam_mapping not in mappings:
        mappings.append(amsterdam_mapping)
    data.setdefault("versioning_contract", {}).setdefault("version_bump_trigger_examples", []).append(
        "adding Amsterdam candidate mapping that retains terlipressin as a source-faithful agent label pending owner review"
    )
    write_json(path, data)


def main() -> None:
    imv_asset = f"Methods/Clinical_Database/local_work/Layer 3/{DATABASE_ID}/treatment_state/std_invasive_mechanical_ventilation_active/std_invasive_mechanical_ventilation_active_long.parquet"
    niv_asset = f"Methods/Clinical_Database/local_work/Layer 3/{DATABASE_ID}/treatment_state/std_noninvasive_ventilation_active/std_noninvasive_ventilation_active_long.parquet"

    binary_specs = {
        "std_advanced_respiratory_support_active": binary_variable_spec(
            variable_id="std_advanced_respiratory_support_active",
            name_en="Advanced respiratory support active",
            semantic_intent="advanced respiratory support active state",
            semantic_definition="A positive-only episode asset retaining one row for each ICU-stay interval during which advanced respiratory support is active under the locked database-specific source rule.",
            positive_state_meaning="advanced respiratory support active",
            same_name_rule="Same-name mappings must preserve the intended advanced respiratory support family. If a database cannot source HFNC while the public concept expects it, the gap must remain visible and owner approval must not be implied.",
            mapping_note="Amsterdam candidate is built from approved IMV and NIV parent assets but carries an explicit HFNC source-coverage gap.",
        ),
        "std_mechanical_ventilation_imv_niv_active": binary_variable_spec(
            variable_id="std_mechanical_ventilation_imv_niv_active",
            name_en="Mechanical ventilation IMV/NIV active",
            semantic_intent="mechanical ventilation IMV/NIV active state",
            semantic_definition="A positive-only episode asset retaining one row for each ICU-stay interval during which invasive or noninvasive mechanical ventilation is active.",
            positive_state_meaning="invasive or noninvasive mechanical ventilation active",
            same_name_rule="Same-name mappings must preserve IMV/NIV scope and must not silently expand to HFNC, oxygen-only support, tracheostomy status, or broader respiratory support.",
            mapping_note="Amsterdam candidate is built from approved IMV and NIV parent assets.",
        ),
    }
    for variable_id, payload in binary_specs.items():
        write_json(variable_dir(variable_id) / "variable_spec.json", payload)

    write_json(
        variable_dir("std_advanced_respiratory_support_active") / f"mapping_spec_{DATABASE_SLUG}.json",
        binary_mapping_spec(
            variable_id="std_advanced_respiratory_support_active",
            semantic_intent="advanced respiratory support active state",
            source_status_codes=["std_invasive_mechanical_ventilation_active", "std_noninvasive_ventilation_active"],
            source_status_labels={
                "std_invasive_mechanical_ventilation_active": "approved Amsterdam invasive mechanical ventilation parent",
                "std_noninvasive_ventilation_active": "approved Amsterdam NIV/CPAP parent",
            },
            normalization_rule_id="amsterdam_approved_imv_niv_parent_union_to_advanced_respiratory_support_candidate_with_hfnc_gap_v1",
            source_rule_summary="retain unioned IMV and NIV/CPAP parent episodes; HFNC is not sourced in Amsterdam current source surface",
            boundary_notice="The candidate output lacks a narrow Amsterdam HFNC source even though the public advanced-respiratory-support concept includes HFNC.",
            local_prepared_input_asset=imv_asset,
            supporting_input_assets=[niv_asset],
            status="built_candidate_hfnc_source_gap_owner_approval_pending",
        ),
    )
    write_json(
        variable_dir("std_mechanical_ventilation_imv_niv_active") / f"mapping_spec_{DATABASE_SLUG}.json",
        binary_mapping_spec(
            variable_id="std_mechanical_ventilation_imv_niv_active",
            semantic_intent="mechanical ventilation IMV/NIV active state",
            source_status_codes=["std_invasive_mechanical_ventilation_active", "std_noninvasive_ventilation_active"],
            source_status_labels={
                "std_invasive_mechanical_ventilation_active": "approved Amsterdam invasive mechanical ventilation parent",
                "std_noninvasive_ventilation_active": "approved Amsterdam NIV/CPAP parent",
            },
            normalization_rule_id="amsterdam_approved_imv_niv_parent_union_to_mechanical_ventilation_imv_niv_candidate_v1",
            source_rule_summary="retain unioned IMV and NIV/CPAP parent episodes",
            boundary_notice="The candidate preserves the explicit IMV/NIV scope and does not include HFNC, oxygen-only support, or tracheostomy status.",
            local_prepared_input_asset=imv_asset,
            supporting_input_assets=[niv_asset],
            status="built_candidate_owner_approval_pending",
        ),
    )

    admin_specs = {
        "std_discharge_disposition": admin_variable_spec(
            variable_id="std_discharge_disposition",
            name_en="Discharge disposition",
            semantic_folder="outcomes",
            semantic_intent="encounter discharge disposition category",
            semantic_definition="An administrative category asset retaining discharge/destination disposition information at the encounter-like grain available in the source database.",
            semantic_grain="one row per retained encounter discharge disposition candidate",
            target_entity_grain="encounter",
            normalization_rule="retain source-faithful discharge/destination category; group died when explicit and keep local destination codes visible pending dictionary review",
        ),
        "std_icu_entry_source": admin_variable_spec(
            variable_id="std_icu_entry_source",
            name_en="ICU entry source",
            semantic_folder="encounter_information",
            semantic_intent="ICU stay entry-source category",
            semantic_definition="A stay-level administrative category preserving source-faithful immediate pre-ICU or pre-ICU/MC entry context when available.",
            semantic_grain="one row per retained ICU stay entry-source category",
            target_entity_grain="ICU stay",
            normalization_rule="retain source-faithful origin category with light public-safe label normalization",
        ),
        "std_icu_exit_destination": admin_variable_spec(
            variable_id="std_icu_exit_destination",
            name_en="ICU exit destination",
            semantic_folder="encounter_information",
            semantic_intent="ICU stay exit-destination category",
            semantic_definition="A stay-level administrative category preserving source-faithful immediate ICU or ICU/MC exit destination when available.",
            semantic_grain="one row per retained ICU stay exit-destination category",
            target_entity_grain="ICU stay",
            normalization_rule="retain source-faithful destination category and keep local destination codes visible pending dictionary review",
        ),
    }
    for variable_id, payload in admin_specs.items():
        write_json(variable_dir(variable_id) / "variable_spec.json", payload)

    admin_mappings = {
        "std_discharge_disposition": admin_mapping_spec(
            variable_id="std_discharge_disposition",
            semantic_folder="outcomes",
            semantic_intent="encounter discharge disposition category",
            semantic_grain="one row per retained encounter discharge disposition candidate",
            target_entity_grain="encounter",
            source_value_field="destination",
            primary_output_value_field="std_discharge_disposition_grouped",
            normalization_rule_id="amsterdam_destination_to_discharge_disposition_candidate_with_local_codes_v1",
            value_normalization_translation="map Overleden to died; retain numeric Amsterdam destination codes as local_destination_code_* pending official dictionary adjudication",
            source_rule_summary="Amsterdam admissions_core.destination is the available discharge/destination field in the current source surface.",
            boundary_notice="Amsterdam destination appears mostly as numeric local codes, so grouped same-name approval is pending official code-dictionary review.",
            status="built_candidate_destination_code_dictionary_pending_owner_approval",
        ),
        "std_icu_entry_source": admin_mapping_spec(
            variable_id="std_icu_entry_source",
            semantic_folder="encounter_information",
            semantic_intent="ICU stay entry-source category",
            semantic_grain="one row per retained ICU stay entry-source category",
            target_entity_grain="ICU stay",
            source_value_field="origin",
            primary_output_value_field="std_icu_entry_source",
            normalization_rule_id="amsterdam_origin_to_icu_entry_source_source_faithful_candidate_v1",
            value_normalization_translation="retain admissions_core.origin with light public-safe category labels while preserving the raw origin field",
            source_rule_summary="Amsterdam admissions_core.origin gives local pre-ICU/MC source context when non-null.",
            boundary_notice="Amsterdam origin is source-faithful local admission context, not yet harmonized to a cross-database transfer taxonomy.",
            status="built_candidate_owner_approval_pending",
        ),
        "std_icu_exit_destination": admin_mapping_spec(
            variable_id="std_icu_exit_destination",
            semantic_folder="encounter_information",
            semantic_intent="ICU stay exit-destination category",
            semantic_grain="one row per retained ICU stay exit-destination category",
            target_entity_grain="ICU stay",
            source_value_field="destination",
            primary_output_value_field="std_icu_exit_destination",
            normalization_rule_id="amsterdam_destination_to_icu_exit_destination_candidate_with_local_codes_v1",
            value_normalization_translation="retain admissions_core.destination as local exit-destination labels; numeric codes are exposed as local_exit_destination_code_* pending dictionary adjudication",
            source_rule_summary="Amsterdam admissions_core.destination gives local ICU/MC exit or discharge destination context when non-null.",
            boundary_notice="Amsterdam destination appears mostly as numeric local codes, so same-name approval is pending official code-dictionary review.",
            status="built_candidate_destination_code_dictionary_pending_owner_approval",
        ),
    }
    for variable_id, payload in admin_mappings.items():
        write_json(variable_dir(variable_id) / f"mapping_spec_{DATABASE_SLUG}.json", payload)

    update_vasopressor_agent_variable_spec()
    write_json(variable_dir("std_vasopressor_support_agent_episode") / f"mapping_spec_{DATABASE_SLUG}.json", vasopressor_agent_mapping_spec())
    print("Wrote Amsterdam Q2 direct candidate specs and mappings for 6 variables.")


if __name__ == "__main__":
    main()
