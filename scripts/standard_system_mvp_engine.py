from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_WORKSPACE_ROOT = REPO_ROOT.parent.parent
RUNTIME_CONTRACT_REF = "Framework_Guideline/StandardSystem_RuntimeEvidence_Contract.md"
ABSOLUTE_PATH_TEXT_PATTERN = re.compile(r"^[A-Za-z]:[\\/].*")
LAYER3_WORKSPACE_PREFIX = "Methods/Clinical_Database/local_work/Layer 3/"
LAYER3_LAYOUT_CONTRACT_REF = "Framework_Guideline/Layer3_Directory_Contract.md"
LEGACY_ROOT_LEVEL_LAYER3_DATABASE_IDS = {"MIMIC-IV-3.1"}
EVENT_LEVEL_NUMERIC_PRIMARY_SOURCE_CLASS_ID = "event_level_numeric_primary_source"
BASELINE_SUMMARY_WINDOW_NUMERIC_CLASS_ID = "baseline_summary_window_numeric"
BINARY_STATE_EPISODE_CLASS_ID = "binary_state_episode"
TREATMENT_DEVICE_IO_EVENT_STREAM_CLASS_ID = "treatment_device_io_event_stream"
EPISODE_INTERVAL_BRIDGE_CLASS_ID = "episode_interval_bridge"
ORDINAL_TEXT_SEMIQUANTITATIVE_RESULT_CLASS_ID = "ordinal_text_semiquantitative_result"
DIAGNOSIS_ADMIN_DEMOGRAPHIC_ID_MAP_CLASS_ID = "diagnosis_admin_demographic_id_map"
SCORE_PHENOTYPE_COMPOSITE_DERIVED_CLASS_ID = "score_phenotype_composite_derived"
MICROBIOLOGY_MULTI_ENTITY_FAMILY_CLASS_ID = "microbiology_multi_entity_family"


def now_utc_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def slugify(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_").lower()


def repo_relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def workspace_relative(path: Path, workspace_root: Path) -> str:
    try:
        return path.resolve().relative_to(workspace_root).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def sha256_path(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def parse_scalar(raw_value: str) -> Any:
    if raw_value in {"true", "false"}:
        return raw_value == "true"
    if re.fullmatch(r"-?\d+", raw_value):
        try:
            return int(raw_value)
        except ValueError:
            return raw_value
    if re.fullmatch(r"-?\d+\.\d+", raw_value):
        try:
            return float(raw_value)
        except ValueError:
            return raw_value
    if (
        (raw_value.startswith("{") and raw_value.endswith("}"))
        or (raw_value.startswith("[") and raw_value.endswith("]"))
        or (raw_value.startswith("(") and raw_value.endswith(")"))
    ):
        try:
            return ast.literal_eval(raw_value)
        except (SyntaxError, ValueError):
            return raw_value
    return raw_value


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_workspace_relative_path(workspace_root: Path, raw_path: str) -> Path:
    path = Path(raw_path)
    if path.is_absolute():
        return path.resolve()
    return (workspace_root / path).resolve()


def add_check(
    checks: list[dict[str, str]],
    check_id: str,
    ok: bool,
    success_message: str,
    failure_message: str,
) -> None:
    checks.append(
        {
            "check_id": check_id,
            "status": "pass" if ok else "fail",
            "message": success_message if ok else failure_message,
        }
    )


def print_validation_summary(report: dict[str, Any]) -> None:
    print("Standard-system MVP validation summary")
    print(f"- variable_id: {report['variable_id']}")
    print(f"- database_id: {report['database_id']}")
    print(f"- variable_spec: {report['variable_spec_path']}")
    print(f"- mapping_spec: {report['mapping_spec_path']}")
    print(f"- overall_status: {report['overall_status']}")
    for item in report["checks"]:
        print(f"  [{item['status']}] {item['check_id']}: {item['message']}")


def parse_structured_stdout_payload(stdout_text: str) -> dict[str, Any]:
    stripped = stdout_text.strip()
    if not stripped or not stripped.startswith("{") or not stripped.endswith("}"):
        return {}
    try:
        payload = ast.literal_eval(stripped)
    except (SyntaxError, ValueError):
        return {}
    return payload if isinstance(payload, dict) else {}


def parse_process_batch_id(stdout_text: str) -> str | None:
    for raw_line in stdout_text.splitlines():
        line = raw_line.strip()
        if line.startswith("process_batch_id="):
            return line.split("=", 1)[1].strip() or None
    payload = parse_structured_stdout_payload(stdout_text)
    process_batch_id = payload.get("process_batch_id")
    if isinstance(process_batch_id, str) and process_batch_id.strip():
        return process_batch_id.strip()
    return None


def public_safe_string(value: str, workspace_root: Path) -> str:
    if ABSOLUTE_PATH_TEXT_PATTERN.match(value):
        return workspace_relative(Path(value), workspace_root)
    return value


def validate_layer3_output_path_for_database(raw_path: str, database_id: str) -> tuple[bool, str]:
    normalized = raw_path.replace("\\", "/").strip()
    if not normalized:
        return True, "mapping_spec does not declare local_output_asset_path; Layer 3 layout check skipped"
    if not normalized.startswith(LAYER3_WORKSPACE_PREFIX):
        return False, (
            "mapping_spec evidence_refs.local_output_asset_path must use a public-safe "
            f"workspace-relative Layer 3 path governed by {LAYER3_LAYOUT_CONTRACT_REF}"
        )

    suffix = normalized[len(LAYER3_WORKSPACE_PREFIX) :].strip("/")
    parts = [part for part in suffix.split("/") if part]
    if not parts:
        return False, "mapping_spec evidence_refs.local_output_asset_path stops at the Layer 3 root"
    if parts[0] == database_id:
        return True, f"Layer 3 output path is database-scoped under {database_id}"
    if database_id in LEGACY_ROOT_LEVEL_LAYER3_DATABASE_IDS:
        return True, (
            f"legacy root-level Layer 3 path accepted temporarily for {database_id}; "
            f"new outputs should follow {LAYER3_LAYOUT_CONTRACT_REF}"
        )
    return False, (
        "Layer 3 output path must be database-scoped as "
        f"{LAYER3_WORKSPACE_PREFIX}{database_id}/<semantic_folder>/<std_variable_id>/..."
    )


def sanitize_build_summary(
    build_summary: dict[str, Any],
    workspace_root: Path,
) -> dict[str, Any]:
    sanitized: dict[str, Any] = {}
    for key, value in build_summary.items():
        if isinstance(value, str):
            sanitized[key] = public_safe_string(value, workspace_root)
        else:
            sanitized[key] = value
    return sanitized


def stringify_summary_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def render_public_stdout_log(
    *,
    variable_id: str,
    process_batch_id: str | None,
    build_summary: dict[str, Any],
) -> str:
    if not build_summary:
        lines = [f"Built {variable_id}"]
        if process_batch_id:
            lines.append(f"process_batch_id={process_batch_id}")
        return "\n".join(lines) + "\n"

    lines = [f"Built {variable_id}"]
    if process_batch_id:
        lines.append(f"process_batch_id={process_batch_id}")
    for key, value in build_summary.items():
        if key == "process_batch_id":
            continue
        lines.append(f"{key}={stringify_summary_value(value)}")
    return "\n".join(lines) + "\n"


def normalize_build_summary_key(raw_key: str) -> str:
    key = raw_key.strip()
    prefixed_match = re.fullmatch(r"(std_[A-Za-z0-9_]+)\.(.+)", key)
    if prefixed_match:
        key = prefixed_match.group(2).strip()
    key = re.sub(r"[^A-Za-z0-9_]+", "__", key).strip("_")
    return key


def parse_build_summary(stdout_text: str) -> dict[str, Any]:
    summary: dict[str, Any] = {}
    for raw_line in stdout_text.splitlines():
        line = raw_line.strip()
        if "=" not in line:
            continue
        key, raw_value = line.split("=", 1)
        key = normalize_build_summary_key(key)
        raw_value = raw_value.strip()
        if not key:
            continue
        summary[key] = parse_scalar(raw_value)
    if summary:
        return summary

    payload = parse_structured_stdout_payload(stdout_text)
    if not payload:
        return {}

    for key in (
        "process_batch_id",
        "asset_path",
        "manifest_path",
        "build_log_path",
        "registry_name",
        "effective_status",
    ):
        value = payload.get(key)
        if isinstance(value, (str, int, float, bool)):
            summary[key] = value

    review_summary = payload.get("review_summary")
    if isinstance(review_summary, dict):
        nested_summary = review_summary.get("review_summary")
        if isinstance(nested_summary, dict):
            for key, value in nested_summary.items():
                key = normalize_build_summary_key(str(key))
                if isinstance(value, (str, int, float, bool)):
                    summary[key] = value
        for key in (
            "dictionary_count",
            "dictionary_count_validated",
            "dictionary_expected_min_value",
            "dictionary_expected_max_value",
            "dictionary_unit",
            "dictionary_ucum_code",
            "source_row_count_matches_dictionary_count",
        ):
            value = review_summary.get(key)
            if isinstance(value, (str, int, float, bool)):
                summary[normalize_build_summary_key(key)] = value
    return summary


def build_default_mapping_spec_path(variable_dir: Path, database_id: str) -> Path:
    return variable_dir / f"mapping_spec_{slugify(database_id)}.json"


def discover_output_artifacts(
    *,
    mapping_spec: dict[str, Any],
    workspace_root: Path,
    process_batch_id: str,
) -> dict[str, str]:
    evidence_refs = mapping_spec.get("evidence_refs", {})
    output_artifacts: dict[str, str] = {}

    static_fields = {
        "primary_output_asset": "local_output_asset_path",
        "preview_csv": "local_preview_path",
        "asset_manifest": "local_asset_manifest_path",
        "knowledge_package": "local_knowledge_package_path",
    }
    for artifact_name, field_name in static_fields.items():
        raw_path = str(evidence_refs.get(field_name, "")).strip()
        if not raw_path:
            raise FileNotFoundError(
                f"mapping_spec evidence_refs.{field_name} is required for execute-mode runtime evidence"
            )
        resolved_path = resolve_workspace_relative_path(workspace_root, raw_path)
        if not resolved_path.exists():
            raise FileNotFoundError(
                f"execute-mode output artifact not found for {artifact_name}: {resolved_path}"
            )
        output_artifacts[artifact_name] = workspace_relative(resolved_path, workspace_root)

    log_archive_raw = str(evidence_refs.get("local_log_archive_dir", "")).strip()
    if not log_archive_raw:
        raise FileNotFoundError(
            "mapping_spec evidence_refs.local_log_archive_dir is required for execute-mode runtime evidence"
        )
    log_archive_dir = resolve_workspace_relative_path(workspace_root, log_archive_raw)
    if not log_archive_dir.exists():
        raise FileNotFoundError(f"execute-mode log archive directory not found: {log_archive_dir}")

    build_log_matches = sorted(log_archive_dir.glob(f"{process_batch_id}__*__build_log__*.md"))
    if len(build_log_matches) != 1:
        raise FileNotFoundError(
            "expected exactly one build-log artifact for execute-mode runtime evidence under "
            f"{workspace_relative(log_archive_dir, workspace_root)}, found {len(build_log_matches)}"
        )
    output_artifacts["build_log"] = workspace_relative(build_log_matches[0], workspace_root)
    return output_artifacts


def build_output_signatures(
    *,
    output_artifacts: dict[str, str],
    workspace_root: Path,
) -> dict[str, dict[str, Any]]:
    signatures: dict[str, dict[str, Any]] = {}
    for artifact_name, raw_path in output_artifacts.items():
        resolved_path = resolve_workspace_relative_path(workspace_root, raw_path)
        signatures[artifact_name] = {
            "sha256": sha256_path(resolved_path),
            "size_bytes": resolved_path.stat().st_size,
        }
    return signatures


def capture_runtime_local_append_only_artifacts(
    *,
    output_artifacts: dict[str, str],
    workspace_root: Path,
    runtime_output_dir: Path,
) -> dict[str, str]:
    captured = dict(output_artifacts)
    build_log_raw = captured.get("build_log")
    if not build_log_raw:
        return captured

    build_log_path = resolve_workspace_relative_path(workspace_root, build_log_raw)
    captured_build_log_path = runtime_output_dir / "captured_build_log.md"
    captured_build_log_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(build_log_path, captured_build_log_path)
    captured["build_log"] = workspace_relative(captured_build_log_path, workspace_root)
    return captured


def build_validation_report(
    *,
    variable_spec_path: Path,
    mapping_spec_path: Path,
    variable_spec: dict[str, Any],
    mapping_spec: dict[str, Any],
    checks: list[dict[str, str]],
) -> dict[str, Any]:
    overall_status = "pass" if all(item["status"] == "pass" for item in checks) else "fail"
    return {
        "artifact_type": "validation_report",
        "artifact_version": "v0_draft",
        "contract_ref": RUNTIME_CONTRACT_REF,
        "generated_at": now_utc_iso(),
        "validation_scope": "pre_execution_spec_and_environment_checks",
        "overall_status": overall_status,
        "variable_id": variable_spec["variable_identity"]["variable_id"],
        "database_id": mapping_spec["database_mapping"]["database_id"],
        "variable_spec_path": repo_relative(variable_spec_path),
        "mapping_spec_path": repo_relative(mapping_spec_path),
        "workspace_layout": "workspace root containing Github/ and Methods/ as sibling directories",
        "spec_hashes": {
            "variable_spec_sha256": sha256_path(variable_spec_path),
            "mapping_spec_sha256": sha256_path(mapping_spec_path),
        },
        "checks": checks,
    }


def build_execution_manifest(
    *,
    variable_spec_path: Path,
    mapping_spec_path: Path,
    workspace_root: Path,
    reference_implementation_path: Path,
    local_input_asset_path: Path,
    validation_report: dict[str, Any],
    execution_mode: str,
    command: list[str],
    process_batch_id: str | None,
    subprocess_return_code: int | None,
    started_at: str | None,
    finished_at: str | None,
    output_artifacts: dict[str, str],
    output_signatures: dict[str, dict[str, Any]],
    build_summary: dict[str, Any],
    execution_entrypoint_path: Path,
) -> dict[str, Any]:
    return {
        "artifact_type": "execution_manifest",
        "artifact_version": "v0_draft",
        "contract_ref": RUNTIME_CONTRACT_REF,
        "generated_at": now_utc_iso(),
        "variable_id": validation_report["variable_id"],
        "database_id": validation_report["database_id"],
        "execution_mode": execution_mode,
        "validation_status": validation_report["overall_status"],
        "variable_spec_path": repo_relative(variable_spec_path),
        "mapping_spec_path": repo_relative(mapping_spec_path),
        "execution_entrypoint_path": repo_relative(execution_entrypoint_path),
        "workspace_layout": "workspace root containing Github/ and Methods/ as sibling directories",
        "reference_implementation_path": workspace_relative(reference_implementation_path, workspace_root),
        "local_input_asset_path": workspace_relative(local_input_asset_path, workspace_root),
        "command": command,
        "process_batch_id": process_batch_id,
        "subprocess_return_code": subprocess_return_code,
        "started_at": started_at,
        "finished_at": finished_at,
        "spec_hashes": validation_report["spec_hashes"],
        "output_artifacts": output_artifacts,
        "output_signatures": output_signatures,
        "build_summary": build_summary,
    }


def write_runtime_artifacts(
    output_dir: Path,
    validation_report: dict[str, Any],
    manifest: dict[str, Any],
    stdout_text: str | None = None,
    stderr_text: str | None = None,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "validation_report.json").write_text(
        json.dumps(validation_report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    if stdout_text is not None:
        (output_dir / "execution_stdout.log").write_text(stdout_text, encoding="utf-8")
    if stderr_text is not None:
        (output_dir / "execution_stderr.log").write_text(stderr_text, encoding="utf-8")


def build_parser(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "--database-id",
        required=True,
        help="Database id to run against, such as MIMIC-IV-3.1.",
    )
    parser.add_argument(
        "--workspace-root",
        help="Optional workspace root containing Github/ and Methods/ as sibling directories.",
    )
    parser.add_argument(
        "--variable-spec",
        help="Optional explicit variable_spec.json path.",
    )
    parser.add_argument(
        "--mapping-spec",
        help="Optional explicit mapping_spec JSON path.",
    )
    parser.add_argument(
        "--output-dir",
        help="Optional directory for validation_report.json, manifest.json, and execution logs.",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Validate spec and environment consistency without executing the current local reference implementation.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the governed command without executing the current local reference implementation.",
    )
    return parser


def resolve_primary_local_input_asset_raw(database_mapping: dict[str, Any]) -> str:
    raw_single = str(database_mapping.get("local_prepared_input_asset", "")).strip()
    if raw_single:
        return raw_single
    raw_list = database_mapping.get("local_prepared_input_assets", [])
    if isinstance(raw_list, list):
        for item in raw_list:
            if isinstance(item, str) and item.strip():
                return item.strip()
    return ""


def validate_event_level_numeric_primary_source_contract(
    *,
    checks: list[dict[str, str]],
    variable_dir: Path,
    variable_spec: dict[str, Any],
    mapping_spec: dict[str, Any],
) -> None:
    variable_identity = variable_spec.get("variable_identity", {})
    immutable_core = variable_spec.get("immutable_core", {})
    canonical_representation = variable_spec.get("canonical_representation", {})
    variable_class = variable_spec.get("variable_class", {})
    standard_variable = mapping_spec.get("standard_variable", {})
    database_mapping = mapping_spec.get("database_mapping", {})
    representation = mapping_spec.get("representation_and_normalization", {})
    validation_contract = mapping_spec.get("validation_contract", {})

    variable_id = str(variable_identity.get("variable_id", "")).strip()
    variable_class_id = str(variable_class.get("variable_class_id", "")).strip()
    declared_or_wrapper_ok = (
        variable_class_id == EVENT_LEVEL_NUMERIC_PRIMARY_SOURCE_CLASS_ID
        or not variable_class_id
    )
    add_check(
        checks,
        "event_numeric_class_lock",
        declared_or_wrapper_ok,
        (
            "variable is compatible with the event-level numeric primary-source class "
            f"for {variable_id or variable_dir.name}"
        ),
        "variable_class.variable_class_id conflicts with the event-level numeric primary-source wrapper",
    )
    add_check(
        checks,
        "variable_directory_alignment",
        variable_dir.name == variable_id,
        f"variable directory name matches variable_id {variable_id}",
        f"variable directory name {variable_dir.name!r} does not match variable_id {variable_id!r}",
    )
    add_check(
        checks,
        "numeric_value_family_lock",
        immutable_core.get("value_family") == "numeric_measurement"
        and canonical_representation.get("value_type") == "numeric_measurement",
        "value family and representation are both locked as numeric_measurement",
        "event-level numeric class requires numeric_measurement in both immutable_core and canonical_representation",
    )
    add_check(
        checks,
        "timestamp_required_lock",
        canonical_representation.get("timestamp_required") is True,
        "timestamp_required is locked to true for the event-level numeric class",
        "event-level numeric class requires canonical_representation.timestamp_required = true",
    )
    add_check(
        checks,
        "source_table_present",
        isinstance(database_mapping.get("source_table"), str) and str(database_mapping.get("source_table")).strip() != "",
        "mapping_spec declares a concrete primary source_table",
        "event-level numeric class requires a concrete database_mapping.source_table",
    )
    source_codes = database_mapping.get("source_codes")
    add_check(
        checks,
        "source_codes_present",
        isinstance(source_codes, list) and len(source_codes) >= 1,
        "mapping_spec locks at least one concrete primary source code",
        "event-level numeric class requires a non-empty database_mapping.source_codes list",
    )
    add_check(
        checks,
        "source_code_system_present",
        isinstance(database_mapping.get("source_code_system"), str)
        and str(database_mapping.get("source_code_system")).strip() != "",
        "mapping_spec declares a concrete primary source_code_system",
        "event-level numeric class requires a concrete database_mapping.source_code_system",
    )
    add_check(
        checks,
        "mapping_semantic_grain_is_event_level",
        standard_variable.get("semantic_grain") == "time-stamped measurement event",
        "mapping_spec standard_variable.semantic_grain is locked to time-stamped measurement event",
        "event-level numeric class requires standard_variable.semantic_grain = time-stamped measurement event",
    )
    add_check(
        checks,
        "normalization_rule_present",
        isinstance(representation.get("normalization_rule_id"), str)
        and str(representation.get("normalization_rule_id")).strip() != "",
        "mapping_spec declares a normalization_rule_id",
        "event-level numeric class requires representation_and_normalization.normalization_rule_id",
    )
    add_check(
        checks,
        "required_non_null_fields_present",
        isinstance(validation_contract.get("required_non_null_fields"), list)
        and len(validation_contract.get("required_non_null_fields", [])) >= 1,
        "mapping_spec declares required_non_null_fields for validation",
        "event-level numeric class requires validation_contract.required_non_null_fields",
    )


def validate_baseline_summary_window_numeric_contract(
    *,
    checks: list[dict[str, str]],
    variable_dir: Path,
    variable_spec: dict[str, Any],
    mapping_spec: dict[str, Any],
) -> None:
    variable_identity = variable_spec.get("variable_identity", {})
    immutable_core = variable_spec.get("immutable_core", {})
    canonical_representation = variable_spec.get("canonical_representation", {})
    variable_class = variable_spec.get("variable_class", {})
    summary_contract = variable_spec.get("summary_contract", {})
    standard_variable = mapping_spec.get("standard_variable", {})
    database_mapping = mapping_spec.get("database_mapping", {})
    summary_build_translation = mapping_spec.get("summary_build_translation", {})
    representation = mapping_spec.get("representation_and_normalization", {})
    validation_contract = mapping_spec.get("validation_contract", {})

    variable_id = str(variable_identity.get("variable_id", "")).strip()
    variable_class_id = str(variable_class.get("variable_class_id", "")).strip()
    declared_or_wrapper_ok = (
        variable_class_id == BASELINE_SUMMARY_WINDOW_NUMERIC_CLASS_ID
        or not variable_class_id
    )
    add_check(
        checks,
        "summary_window_numeric_class_lock",
        declared_or_wrapper_ok,
        (
            "variable is compatible with the baseline-summary-window numeric class "
            f"for {variable_id or variable_dir.name}"
        ),
        "variable_class.variable_class_id conflicts with the baseline-summary-window numeric wrapper",
    )
    add_check(
        checks,
        "variable_directory_alignment",
        variable_dir.name == variable_id,
        f"variable directory name matches variable_id {variable_id}",
        f"variable directory name {variable_dir.name!r} does not match variable_id {variable_id!r}",
    )

    add_check(
        checks,
        "summary_subclass_allowed",
        summary_contract.get("summary_subclass") in {"baseline_snapshot", "window_summary", "duration_summary"},
        "summary_subclass is one of the currently allowed class-2 summary subclasses",
        "class-2 variable_spec requires summary_contract.summary_subclass in {baseline_snapshot, window_summary, duration_summary}",
    )

    for field_name in (
        "target_entity_grain",
        "anchor_family",
        "window_label",
        "window_start_rule",
        "window_end_rule",
        "qualifying_row_rule",
        "selection_rule",
        "aggregation_rule",
        "tie_break_rule",
        "no_source_row_action",
        "partial_window_action",
    ):
        add_check(
            checks,
            f"summary_contract_{field_name}_present",
            isinstance(summary_contract.get(field_name), str) and str(summary_contract.get(field_name)).strip() != "",
            f"summary_contract.{field_name} is explicitly locked",
            f"class-2 variable_spec requires a non-empty summary_contract.{field_name}",
        )

    add_check(
        checks,
        "summary_value_family_present",
        isinstance(immutable_core.get("value_family"), str) and str(immutable_core.get("value_family")).strip() != "",
        "immutable_core.value_family is explicitly locked for the class-2 summary variable",
        "class-2 variable_spec requires a non-empty immutable_core.value_family",
    )
    add_check(
        checks,
        "representation_value_type_present",
        isinstance(canonical_representation.get("value_type"), str)
        and str(canonical_representation.get("value_type")).strip() != "",
        "canonical_representation.value_type is explicitly locked for the class-2 summary variable",
        "class-2 variable_spec requires canonical_representation.value_type",
    )
    add_check(
        checks,
        "anchor_window_context_flags_are_boolean",
        isinstance(canonical_representation.get("anchor_timestamp_required"), bool)
        and isinstance(canonical_representation.get("window_bounds_required"), bool),
        "anchor_timestamp_required and window_bounds_required are explicitly boolean",
        "class-2 variable_spec requires boolean anchor_timestamp_required and window_bounds_required flags",
    )
    add_check(
        checks,
        "hard_valid_range_shape",
        isinstance(canonical_representation.get("hard_valid_range_in_canonical_unit"), list)
        and len(canonical_representation.get("hard_valid_range_in_canonical_unit", [])) == 2,
        "hard_valid_range_in_canonical_unit is present with two endpoints",
        "class-2 variable_spec requires hard_valid_range_in_canonical_unit with two endpoints",
    )
    add_check(
        checks,
        "plausible_range_shape",
        isinstance(canonical_representation.get("plausible_range_in_canonical_unit"), list)
        and len(canonical_representation.get("plausible_range_in_canonical_unit", [])) == 2,
        "plausible_range_in_canonical_unit is present with two endpoints",
        "class-2 variable_spec requires plausible_range_in_canonical_unit with two endpoints",
    )

    add_check(
        checks,
        "mapping_summary_subclass_match",
        summary_contract.get("summary_subclass") == standard_variable.get("summary_subclass"),
        "summary_subclass matches across variable_spec and mapping_spec",
        "summary_subclass mismatch between variable_spec and mapping_spec",
    )
    add_check(
        checks,
        "mapping_target_entity_grain_match",
        summary_contract.get("target_entity_grain") == standard_variable.get("target_entity_grain"),
        "target_entity_grain matches across variable_spec and mapping_spec",
        "target_entity_grain mismatch between variable_spec and mapping_spec",
    )
    add_check(
        checks,
        "mapping_anchor_family_match",
        summary_contract.get("anchor_family") == standard_variable.get("anchor_family"),
        "anchor_family matches across variable_spec and mapping_spec",
        "anchor_family mismatch between variable_spec and mapping_spec",
    )

    add_check(
        checks,
        "source_locator_mode_present",
        isinstance(database_mapping.get("source_locator_mode"), str)
        and str(database_mapping.get("source_locator_mode")).strip() != "",
        "mapping_spec declares source_locator_mode for the class-2 summary variable",
        "class-2 mapping_spec requires database_mapping.source_locator_mode",
    )
    add_check(
        checks,
        "primary_source_tables_present",
        isinstance(database_mapping.get("primary_source_tables"), list)
        and len(database_mapping.get("primary_source_tables", [])) >= 1,
        "mapping_spec declares at least one primary_source_table",
        "class-2 mapping_spec requires a non-empty database_mapping.primary_source_tables list",
    )
    add_check(
        checks,
        "source_grain_present",
        isinstance(database_mapping.get("source_grain"), str) and str(database_mapping.get("source_grain")).strip() != "",
        "mapping_spec declares source_grain",
        "class-2 mapping_spec requires database_mapping.source_grain",
    )
    add_check(
        checks,
        "target_grain_present",
        isinstance(database_mapping.get("target_grain"), str) and str(database_mapping.get("target_grain")).strip() != "",
        "mapping_spec declares target_grain",
        "class-2 mapping_spec requires database_mapping.target_grain",
    )

    for field_name in (
        "window_label",
        "anchor_family",
        "window_start_translation",
        "window_end_translation",
        "qualifying_row_translation",
        "selection_translation",
        "aggregation_translation",
        "tie_break_translation",
        "no_source_row_translation",
        "partial_window_translation",
    ):
        add_check(
            checks,
            f"summary_build_translation_{field_name}_present",
            isinstance(summary_build_translation.get(field_name), str)
            and str(summary_build_translation.get(field_name)).strip() != "",
            f"summary_build_translation.{field_name} is explicitly locked",
            f"class-2 mapping_spec requires a non-empty summary_build_translation.{field_name}",
        )

    add_check(
        checks,
        "normalization_rule_present",
        isinstance(representation.get("normalization_rule_id"), str)
        and str(representation.get("normalization_rule_id")).strip() != "",
        "mapping_spec declares a normalization_rule_id",
        "class-2 mapping_spec requires representation_and_normalization.normalization_rule_id",
    )
    add_check(
        checks,
        "primary_output_value_field_present",
        isinstance(representation.get("primary_output_value_field"), str)
        and str(representation.get("primary_output_value_field")).strip() != "",
        "mapping_spec declares the primary_output_value_field",
        "class-2 mapping_spec requires representation_and_normalization.primary_output_value_field",
    )
    add_check(
        checks,
        "required_non_null_fields_present",
        isinstance(validation_contract.get("required_non_null_fields"), list)
        and len(validation_contract.get("required_non_null_fields", [])) >= 1,
        "mapping_spec declares required_non_null_fields for validation",
        "class-2 mapping_spec requires validation_contract.required_non_null_fields",
    )
    add_check(
        checks,
        "no_source_row_policy_check_present",
        isinstance(validation_contract.get("no_source_row_policy_check"), str)
        and str(validation_contract.get("no_source_row_policy_check")).strip() != "",
        "mapping_spec explicitly locks a no_source_row_policy_check",
        "class-2 mapping_spec requires validation_contract.no_source_row_policy_check",
    )


def validate_binary_state_episode_contract(
    *,
    checks: list[dict[str, str]],
    variable_dir: Path,
    variable_spec: dict[str, Any],
    mapping_spec: dict[str, Any],
) -> None:
    variable_identity = variable_spec.get("variable_identity", {})
    immutable_core = variable_spec.get("immutable_core", {})
    canonical_representation = variable_spec.get("canonical_representation", {})
    variable_class = variable_spec.get("variable_class", {})
    state_episode_contract = variable_spec.get("state_episode_contract", {})
    standard_variable = mapping_spec.get("standard_variable", {})
    database_mapping = mapping_spec.get("database_mapping", {})
    state_episode_translation = mapping_spec.get("state_episode_build_translation", {})
    representation = mapping_spec.get("representation_and_normalization", {})
    validation_contract = mapping_spec.get("validation_contract", {})

    variable_id = str(variable_identity.get("variable_id", "")).strip()
    variable_class_id = str(variable_class.get("variable_class_id", "")).strip()
    declared_or_wrapper_ok = (
        variable_class_id == BINARY_STATE_EPISODE_CLASS_ID
        or not variable_class_id
    )
    add_check(
        checks,
        "binary_state_episode_class_lock",
        declared_or_wrapper_ok,
        f"variable is compatible with the binary-state episode class for {variable_id or variable_dir.name}",
        "variable_class.variable_class_id conflicts with the binary-state episode wrapper",
    )
    add_check(
        checks,
        "variable_directory_alignment",
        variable_dir.name == variable_id,
        f"variable directory name matches variable_id {variable_id}",
        f"variable directory name {variable_dir.name!r} does not match variable_id {variable_id!r}",
    )
    add_check(
        checks,
        "binary_state_value_family_lock",
        immutable_core.get("value_family") == "binary_state"
        and canonical_representation.get("value_type") == "boolean_state_episode",
        "value family is binary_state and representation is boolean_state_episode",
        "binary-state episode class requires immutable_core.value_family=binary_state and canonical_representation.value_type=boolean_state_episode",
    )
    add_check(
        checks,
        "positive_state_source_class_lock",
        immutable_core.get("source_value_class") == "positive_state_episode",
        "source_value_class is locked to positive_state_episode",
        "binary-state episode class requires immutable_core.source_value_class = positive_state_episode",
    )
    add_check(
        checks,
        "interval_requirements_are_boolean_true",
        canonical_representation.get("timestamp_start_required") is True
        and canonical_representation.get("timestamp_end_required") is True
        and canonical_representation.get("duration_required") is True,
        "start timestamp, end timestamp, and duration are required",
        "binary-state episode class requires timestamp_start_required, timestamp_end_required, and duration_required to be true",
    )
    add_check(
        checks,
        "retained_value_domain_true_only",
        canonical_representation.get("retained_value_domain") == [True],
        "retained value domain is locked to true-only rows",
        "binary-state episode class requires canonical_representation.retained_value_domain = [true]",
    )

    for field_name in (
        "target_entity_grain",
        "anchor_family",
        "positive_state_meaning",
        "negative_state_representation",
        "episode_start_rule",
        "episode_end_rule",
        "continuity_rule",
        "no_row_interpretation",
    ):
        add_check(
            checks,
            f"state_episode_contract_{field_name}_present",
            isinstance(state_episode_contract.get(field_name), str)
            and str(state_episode_contract.get(field_name)).strip() != "",
            f"state_episode_contract.{field_name} is explicitly locked",
            f"binary-state episode variable_spec requires state_episode_contract.{field_name}",
        )

    add_check(
        checks,
        "allowed_true_value_locked",
        state_episode_contract.get("allowed_true_value") is True
        and state_episode_contract.get("allowed_false_rows") is False,
        "state_episode_contract locks true rows only and disallows false rows",
        "binary-state episode class requires allowed_true_value=true and allowed_false_rows=false",
    )
    add_check(
        checks,
        "source_locator_mode_present",
        isinstance(database_mapping.get("source_locator_mode"), str)
        and str(database_mapping.get("source_locator_mode")).strip() != "",
        "mapping_spec declares source_locator_mode",
        "binary-state episode mapping_spec requires database_mapping.source_locator_mode",
    )
    add_check(
        checks,
        "source_table_present",
        isinstance(database_mapping.get("source_table"), str)
        and str(database_mapping.get("source_table")).strip() != "",
        "mapping_spec declares a concrete source_table",
        "binary-state episode mapping_spec requires database_mapping.source_table",
    )
    add_check(
        checks,
        "source_status_field_present",
        isinstance(database_mapping.get("source_status_field"), str)
        and str(database_mapping.get("source_status_field")).strip() != "",
        "mapping_spec declares source_status_field",
        "binary-state episode mapping_spec requires database_mapping.source_status_field",
    )
    source_status_codes = database_mapping.get("source_status_codes")
    add_check(
        checks,
        "source_status_codes_present",
        isinstance(source_status_codes, list) and len(source_status_codes) >= 1,
        "mapping_spec locks at least one included source status",
        "binary-state episode mapping_spec requires non-empty database_mapping.source_status_codes",
    )
    for field_name in ("source_start_field", "source_end_field", "source_grain", "target_grain"):
        add_check(
            checks,
            f"database_mapping_{field_name}_present",
            isinstance(database_mapping.get(field_name), str)
            and str(database_mapping.get(field_name)).strip() != "",
            f"database_mapping.{field_name} is explicitly locked",
            f"binary-state episode mapping_spec requires database_mapping.{field_name}",
        )

    for field_name in (
        "target_entity_grain",
        "anchor_family",
        "positive_state_translation",
        "negative_state_translation",
        "episode_start_translation",
        "episode_end_translation",
        "continuity_translation",
        "no_row_translation",
    ):
        add_check(
            checks,
            f"state_episode_translation_{field_name}_present",
            isinstance(state_episode_translation.get(field_name), str)
            and str(state_episode_translation.get(field_name)).strip() != "",
            f"state_episode_build_translation.{field_name} is explicitly locked",
            f"binary-state episode mapping_spec requires state_episode_build_translation.{field_name}",
        )

    add_check(
        checks,
        "target_entity_grain_match",
        state_episode_contract.get("target_entity_grain") == state_episode_translation.get("target_entity_grain"),
        "target_entity_grain matches across variable_spec and mapping_spec",
        "target_entity_grain mismatch between variable_spec and mapping_spec",
    )
    add_check(
        checks,
        "anchor_family_match",
        state_episode_contract.get("anchor_family") == state_episode_translation.get("anchor_family"),
        "anchor_family matches across variable_spec and mapping_spec",
        "anchor_family mismatch between variable_spec and mapping_spec",
    )
    add_check(
        checks,
        "mapping_semantic_grain_match",
        standard_variable.get("semantic_grain") == immutable_core.get("semantic_grain"),
        "mapping_spec standard_variable.semantic_grain matches variable_spec immutable_core.semantic_grain",
        "binary-state episode semantic_grain mismatch between variable_spec and mapping_spec",
    )
    add_check(
        checks,
        "normalization_rule_present",
        isinstance(representation.get("normalization_rule_id"), str)
        and str(representation.get("normalization_rule_id")).strip() != "",
        "mapping_spec declares a normalization_rule_id",
        "binary-state episode mapping_spec requires representation_and_normalization.normalization_rule_id",
    )
    for field_name in (
        "primary_output_value_field",
        "start_time_output_field",
        "end_time_output_field",
        "duration_output_field",
    ):
        add_check(
            checks,
            f"representation_{field_name}_present",
            isinstance(representation.get(field_name), str)
            and str(representation.get(field_name)).strip() != "",
            f"representation_and_normalization.{field_name} is explicitly locked",
            f"binary-state episode mapping_spec requires representation_and_normalization.{field_name}",
        )
    add_check(
        checks,
        "required_non_null_fields_present",
        isinstance(validation_contract.get("required_non_null_fields"), list)
        and len(validation_contract.get("required_non_null_fields", [])) >= 1,
        "mapping_spec declares required_non_null_fields for validation",
        "binary-state episode mapping_spec requires validation_contract.required_non_null_fields",
    )
    add_check(
        checks,
        "positive_only_no_row_policy_present",
        isinstance(validation_contract.get("positive_only_no_row_policy_check"), str)
        and str(validation_contract.get("positive_only_no_row_policy_check")).strip() != "",
        "mapping_spec explicitly locks a positive-only no-row policy check",
        "binary-state episode mapping_spec requires validation_contract.positive_only_no_row_policy_check",
    )


def validate_episode_interval_bridge_contract(
    *,
    checks: list[dict[str, str]],
    variable_dir: Path,
    variable_spec: dict[str, Any],
    mapping_spec: dict[str, Any],
) -> None:
    variable_identity = variable_spec.get("variable_identity", {})
    immutable_core = variable_spec.get("immutable_core", {})
    canonical_representation = variable_spec.get("canonical_representation", {})
    variable_class = variable_spec.get("variable_class", {})
    episode_contract = variable_spec.get("episode_interval_contract", {})
    standard_variable = mapping_spec.get("standard_variable", {})
    database_mapping = mapping_spec.get("database_mapping", {})
    episode_translation = mapping_spec.get("episode_interval_build_translation", {})
    representation = mapping_spec.get("representation_and_normalization", {})
    validation_contract = mapping_spec.get("validation_contract", {})

    variable_id = str(variable_identity.get("variable_id", "")).strip()
    variable_class_id = str(variable_class.get("variable_class_id", "")).strip()
    declared_or_wrapper_ok = (
        variable_class_id == EPISODE_INTERVAL_BRIDGE_CLASS_ID
        or not variable_class_id
    )
    add_check(
        checks,
        "episode_interval_bridge_class_lock",
        declared_or_wrapper_ok,
        f"variable is compatible with the episode-interval bridge class for {variable_id or variable_dir.name}",
        "variable_class.variable_class_id conflicts with the episode-interval bridge wrapper",
    )
    add_check(
        checks,
        "variable_directory_alignment",
        variable_dir.name == variable_id,
        f"variable directory name matches variable_id {variable_id}",
        f"variable directory name {variable_dir.name!r} does not match variable_id {variable_id!r}",
    )
    add_check(
        checks,
        "episode_value_family_lock",
        immutable_core.get("value_family") == "categorical_episode"
        and canonical_representation.get("value_type") == "categorical_interval_episode",
        "value family is categorical_episode and representation is categorical_interval_episode",
        "episode-interval bridge class requires immutable_core.value_family=categorical_episode and canonical_representation.value_type=categorical_interval_episode",
    )
    add_check(
        checks,
        "episode_source_class_lock",
        immutable_core.get("source_value_class")
        in {"positive_modality_episode", "positive_agent_episode", "positive_interval_bridge"},
        "source_value_class is locked to a positive episode/interval class",
        (
            "episode-interval bridge class requires immutable_core.source_value_class "
            "to be positive_modality_episode, positive_agent_episode, or positive_interval_bridge"
        ),
    )
    add_check(
        checks,
        "interval_requirements_are_boolean_true",
        canonical_representation.get("timestamp_start_required") is True
        and canonical_representation.get("timestamp_end_required") is True
        and canonical_representation.get("duration_required") is True,
        "start timestamp, end timestamp, and duration are required",
        "episode-interval bridge class requires timestamp_start_required, timestamp_end_required, and duration_required to be true",
    )
    add_check(
        checks,
        "label_domain_present",
        isinstance(canonical_representation.get("retained_label_domain"), list)
        and len(canonical_representation.get("retained_label_domain", [])) >= 1,
        "retained label domain is explicitly locked",
        "episode-interval bridge class requires canonical_representation.retained_label_domain",
    )

    for field_name in (
        "target_entity_grain",
        "anchor_family",
        "episode_label_meaning",
        "episode_start_rule",
        "episode_end_rule",
        "continuity_rule",
        "parent_link_rule",
        "no_row_interpretation",
    ):
        add_check(
            checks,
            f"episode_interval_contract_{field_name}_present",
            isinstance(episode_contract.get(field_name), str)
            and str(episode_contract.get(field_name)).strip() != "",
            f"episode_interval_contract.{field_name} is explicitly locked",
            f"episode-interval bridge variable_spec requires episode_interval_contract.{field_name}",
        )

    add_check(
        checks,
        "source_locator_mode_present",
        isinstance(database_mapping.get("source_locator_mode"), str)
        and str(database_mapping.get("source_locator_mode")).strip() != "",
        "mapping_spec declares source_locator_mode",
        "episode-interval bridge mapping_spec requires database_mapping.source_locator_mode",
    )
    add_check(
        checks,
        "source_table_present",
        isinstance(database_mapping.get("source_table"), str)
        and str(database_mapping.get("source_table")).strip() != "",
        "mapping_spec declares a concrete source_table",
        "episode-interval bridge mapping_spec requires database_mapping.source_table",
    )
    add_check(
        checks,
        "source_status_field_present",
        isinstance(database_mapping.get("source_status_field"), str)
        and str(database_mapping.get("source_status_field")).strip() != "",
        "mapping_spec declares source_status_field",
        "episode-interval bridge mapping_spec requires database_mapping.source_status_field",
    )
    source_status_codes = database_mapping.get("source_status_codes")
    add_check(
        checks,
        "source_status_codes_present",
        isinstance(source_status_codes, list) and len(source_status_codes) >= 1,
        "mapping_spec locks at least one retained episode label or status",
        "episode-interval bridge mapping_spec requires non-empty database_mapping.source_status_codes",
    )
    for field_name in ("source_start_field", "source_end_field", "source_grain", "target_grain"):
        add_check(
            checks,
            f"database_mapping_{field_name}_present",
            isinstance(database_mapping.get(field_name), str)
            and str(database_mapping.get(field_name)).strip() != "",
            f"database_mapping.{field_name} is explicitly locked",
            f"episode-interval bridge mapping_spec requires database_mapping.{field_name}",
        )

    for field_name in (
        "target_entity_grain",
        "anchor_family",
        "episode_label_translation",
        "episode_start_translation",
        "episode_end_translation",
        "continuity_translation",
        "parent_link_translation",
        "no_row_translation",
    ):
        add_check(
            checks,
            f"episode_interval_translation_{field_name}_present",
            isinstance(episode_translation.get(field_name), str)
            and str(episode_translation.get(field_name)).strip() != "",
            f"episode_interval_build_translation.{field_name} is explicitly locked",
            f"episode-interval bridge mapping_spec requires episode_interval_build_translation.{field_name}",
        )

    add_check(
        checks,
        "target_entity_grain_match",
        episode_contract.get("target_entity_grain") == episode_translation.get("target_entity_grain"),
        "target_entity_grain matches across variable_spec and mapping_spec",
        "target_entity_grain mismatch between variable_spec and mapping_spec",
    )
    add_check(
        checks,
        "anchor_family_match",
        episode_contract.get("anchor_family") == episode_translation.get("anchor_family"),
        "anchor_family matches across variable_spec and mapping_spec",
        "anchor_family mismatch between variable_spec and mapping_spec",
    )
    add_check(
        checks,
        "mapping_semantic_grain_match",
        standard_variable.get("semantic_grain") == immutable_core.get("semantic_grain"),
        "mapping_spec standard_variable.semantic_grain matches variable_spec immutable_core.semantic_grain",
        "episode-interval bridge semantic_grain mismatch between variable_spec and mapping_spec",
    )
    add_check(
        checks,
        "normalization_rule_present",
        isinstance(representation.get("normalization_rule_id"), str)
        and str(representation.get("normalization_rule_id")).strip() != "",
        "mapping_spec declares a normalization_rule_id",
        "episode-interval bridge mapping_spec requires representation_and_normalization.normalization_rule_id",
    )
    for field_name in (
        "primary_output_value_field",
        "primary_episode_label_field",
        "start_time_output_field",
        "end_time_output_field",
        "duration_output_field",
    ):
        add_check(
            checks,
            f"representation_{field_name}_present",
            isinstance(representation.get(field_name), str)
            and str(representation.get(field_name)).strip() != "",
            f"representation_and_normalization.{field_name} is explicitly locked",
            f"episode-interval bridge mapping_spec requires representation_and_normalization.{field_name}",
        )
    add_check(
        checks,
        "required_non_null_fields_present",
        isinstance(validation_contract.get("required_non_null_fields"), list)
        and len(validation_contract.get("required_non_null_fields", [])) >= 1,
        "mapping_spec declares required_non_null_fields for validation",
        "episode-interval bridge mapping_spec requires validation_contract.required_non_null_fields",
    )
    add_check(
        checks,
        "no_row_policy_present",
        isinstance(validation_contract.get("no_row_policy_check"), str)
        and str(validation_contract.get("no_row_policy_check")).strip() != "",
        "mapping_spec explicitly locks a no-row policy check",
        "episode-interval bridge mapping_spec requires validation_contract.no_row_policy_check",
    )


def validate_treatment_device_io_event_stream_contract(
    *,
    checks: list[dict[str, str]],
    variable_dir: Path,
    variable_spec: dict[str, Any],
    mapping_spec: dict[str, Any],
) -> None:
    variable_identity = variable_spec.get("variable_identity", {})
    immutable_core = variable_spec.get("immutable_core", {})
    canonical_representation = variable_spec.get("canonical_representation", {})
    variable_class = variable_spec.get("variable_class", {})
    event_stream_contract = variable_spec.get("event_stream_contract", {})
    standard_variable = mapping_spec.get("standard_variable", {})
    database_mapping = mapping_spec.get("database_mapping", {})
    event_stream_translation = mapping_spec.get("event_stream_build_translation", {})
    representation = mapping_spec.get("representation_and_normalization", {})
    validation_contract = mapping_spec.get("validation_contract", {})

    variable_id = str(variable_identity.get("variable_id", "")).strip()
    variable_class_id = str(variable_class.get("variable_class_id", "")).strip()
    declared_or_wrapper_ok = (
        variable_class_id == TREATMENT_DEVICE_IO_EVENT_STREAM_CLASS_ID
        or not variable_class_id
    )
    add_check(
        checks,
        "treatment_device_io_event_stream_class_lock",
        declared_or_wrapper_ok,
        f"variable is compatible with the treatment/device/IO event-stream class for {variable_id or variable_dir.name}",
        "variable_class.variable_class_id conflicts with the treatment/device/IO event-stream wrapper",
    )
    add_check(
        checks,
        "variable_directory_alignment",
        variable_dir.name == variable_id,
        f"variable directory name matches variable_id {variable_id}",
        f"variable directory name {variable_dir.name!r} does not match variable_id {variable_id!r}",
    )
    add_check(
        checks,
        "event_stream_value_family_lock",
        immutable_core.get("value_family") == "numeric_event_with_context"
        and canonical_representation.get("value_type") == "numeric_event_with_metadata",
        "value family is numeric_event_with_context and representation is numeric_event_with_metadata",
        "treatment/device/IO event-stream class requires immutable_core.value_family=numeric_event_with_context and canonical_representation.value_type=numeric_event_with_metadata",
    )
    add_check(
        checks,
        "event_stream_source_class_lock",
        immutable_core.get("source_value_class") == "source_recorded_treatment_device_io_amount_event",
        "source_value_class is locked to source-recorded treatment/device/IO amount events",
        "treatment/device/IO event-stream class requires immutable_core.source_value_class = source_recorded_treatment_device_io_amount_event",
    )
    add_check(
        checks,
        "timestamp_required_lock",
        canonical_representation.get("timestamp_required") is True,
        "timestamp_required is locked to true for the event-stream class",
        "treatment/device/IO event-stream class requires canonical_representation.timestamp_required = true",
    )
    add_check(
        checks,
        "context_field_required_lock",
        canonical_representation.get("context_fields_required") is True,
        "context_fields_required is locked to true for the event-stream class",
        "treatment/device/IO event-stream class requires canonical_representation.context_fields_required = true",
    )

    for field_name in (
        "target_entity_grain",
        "anchor_family",
        "event_time_rule",
        "event_value_meaning",
        "unit_rule",
        "context_role_rule",
        "parent_link_rule",
        "downstream_aggregation_rule",
        "no_row_interpretation",
    ):
        add_check(
            checks,
            f"event_stream_contract_{field_name}_present",
            isinstance(event_stream_contract.get(field_name), str)
            and str(event_stream_contract.get(field_name)).strip() != "",
            f"event_stream_contract.{field_name} is explicitly locked",
            f"treatment/device/IO event-stream variable_spec requires event_stream_contract.{field_name}",
        )

    add_check(
        checks,
        "source_locator_mode_present",
        isinstance(database_mapping.get("source_locator_mode"), str)
        and str(database_mapping.get("source_locator_mode")).strip() != "",
        "mapping_spec declares source_locator_mode",
        "treatment/device/IO event-stream mapping_spec requires database_mapping.source_locator_mode",
    )
    add_check(
        checks,
        "source_table_present",
        isinstance(database_mapping.get("source_table"), str)
        and str(database_mapping.get("source_table")).strip() != "",
        "mapping_spec declares a concrete source_table or source-family expression",
        "treatment/device/IO event-stream mapping_spec requires database_mapping.source_table",
    )
    source_itemids = database_mapping.get("source_itemids")
    add_check(
        checks,
        "source_itemids_present",
        isinstance(source_itemids, list) and len(source_itemids) >= 1,
        "mapping_spec locks at least one source itemid or source code",
        "treatment/device/IO event-stream mapping_spec requires non-empty database_mapping.source_itemids",
    )
    for field_name in ("source_time_field", "source_value_field", "source_unit_field", "source_grain", "target_grain"):
        add_check(
            checks,
            f"database_mapping_{field_name}_present",
            isinstance(database_mapping.get(field_name), str)
            and str(database_mapping.get(field_name)).strip() != "",
            f"database_mapping.{field_name} is explicitly locked",
            f"treatment/device/IO event-stream mapping_spec requires database_mapping.{field_name}",
        )

    for field_name in (
        "target_entity_grain",
        "anchor_family",
        "event_time_translation",
        "event_value_translation",
        "unit_translation",
        "context_translation",
        "parent_link_translation",
        "downstream_aggregation_translation",
        "no_row_translation",
    ):
        add_check(
            checks,
            f"event_stream_translation_{field_name}_present",
            isinstance(event_stream_translation.get(field_name), str)
            and str(event_stream_translation.get(field_name)).strip() != "",
            f"event_stream_build_translation.{field_name} is explicitly locked",
            f"treatment/device/IO event-stream mapping_spec requires event_stream_build_translation.{field_name}",
        )

    add_check(
        checks,
        "target_entity_grain_match",
        event_stream_contract.get("target_entity_grain") == event_stream_translation.get("target_entity_grain"),
        "target_entity_grain matches across variable_spec and mapping_spec",
        "target_entity_grain mismatch between variable_spec and mapping_spec",
    )
    add_check(
        checks,
        "anchor_family_match",
        event_stream_contract.get("anchor_family") == event_stream_translation.get("anchor_family"),
        "anchor_family matches across variable_spec and mapping_spec",
        "anchor_family mismatch between variable_spec and mapping_spec",
    )
    add_check(
        checks,
        "mapping_semantic_grain_match",
        standard_variable.get("semantic_grain") == immutable_core.get("semantic_grain"),
        "mapping_spec standard_variable.semantic_grain matches variable_spec immutable_core.semantic_grain",
        "treatment/device/IO event-stream semantic_grain mismatch between variable_spec and mapping_spec",
    )
    add_check(
        checks,
        "normalization_rule_present",
        isinstance(representation.get("normalization_rule_id"), str)
        and str(representation.get("normalization_rule_id")).strip() != "",
        "mapping_spec declares a normalization_rule_id",
        "treatment/device/IO event-stream mapping_spec requires representation_and_normalization.normalization_rule_id",
    )
    for field_name in (
        "primary_output_value_field",
        "event_time_output_field",
        "standard_unit_output_field",
        "source_context_output_field",
    ):
        add_check(
            checks,
            f"representation_{field_name}_present",
            isinstance(representation.get(field_name), str)
            and str(representation.get(field_name)).strip() != "",
            f"representation_and_normalization.{field_name} is explicitly locked",
            f"treatment/device/IO event-stream mapping_spec requires representation_and_normalization.{field_name}",
        )
    add_check(
        checks,
        "required_non_null_fields_present",
        isinstance(validation_contract.get("required_non_null_fields"), list)
        and len(validation_contract.get("required_non_null_fields", [])) >= 1,
        "mapping_spec declares required_non_null_fields for validation",
        "treatment/device/IO event-stream mapping_spec requires validation_contract.required_non_null_fields",
    )
    add_check(
        checks,
        "no_row_policy_present",
        isinstance(validation_contract.get("no_row_policy_check"), str)
        and str(validation_contract.get("no_row_policy_check")).strip() != "",
        "mapping_spec explicitly locks a no-row policy check",
        "treatment/device/IO event-stream mapping_spec requires validation_contract.no_row_policy_check",
    )


def validate_ordinal_text_semiquantitative_result_contract(
    *,
    checks: list[dict[str, str]],
    variable_dir: Path,
    variable_spec: dict[str, Any],
    mapping_spec: dict[str, Any],
) -> None:
    variable_identity = variable_spec.get("variable_identity", {})
    immutable_core = variable_spec.get("immutable_core", {})
    canonical_representation = variable_spec.get("canonical_representation", {})
    variable_class = variable_spec.get("variable_class", {})
    ordinal_contract = variable_spec.get("ordinal_result_contract", {})
    standard_variable = mapping_spec.get("standard_variable", {})
    database_mapping = mapping_spec.get("database_mapping", {})
    ordinal_translation = mapping_spec.get("ordinal_result_build_translation", {})
    representation = mapping_spec.get("representation_and_normalization", {})
    validation_contract = mapping_spec.get("validation_contract", {})

    variable_id = str(variable_identity.get("variable_id", "")).strip()
    variable_class_id = str(variable_class.get("variable_class_id", "")).strip()
    add_check(
        checks,
        "ordinal_text_class_lock",
        variable_class_id in {ORDINAL_TEXT_SEMIQUANTITATIVE_RESULT_CLASS_ID, ""},
        f"variable is compatible with the ordinal/text semiquantitative result class for {variable_id or variable_dir.name}",
        "variable_class.variable_class_id conflicts with the ordinal/text semiquantitative wrapper",
    )
    add_check(
        checks,
        "variable_directory_alignment",
        variable_dir.name == variable_id,
        f"variable directory name matches variable_id {variable_id}",
        f"variable directory name {variable_dir.name!r} does not match variable_id {variable_id!r}",
    )
    add_check(
        checks,
        "ordinal_value_family_lock",
        immutable_core.get("value_family") in {"ordinal_result", "categorical_ordinal_result", "binary_ordinal_result"}
        and canonical_representation.get("value_type") in {"ordinal_result_event", "categorical_result_event"},
        "value family and representation are locked as ordinal/categorical result events",
        "ordinal/text class requires an ordinal/categorical result value family and result-event representation",
    )
    add_check(
        checks,
        "ordinal_source_class_lock",
        immutable_core.get("source_value_class") == "source_recorded_ordinal_text_result",
        "source_value_class is locked to source-recorded ordinal/text results",
        "ordinal/text class requires immutable_core.source_value_class = source_recorded_ordinal_text_result",
    )
    add_check(
        checks,
        "result_domain_present",
        isinstance(canonical_representation.get("result_domain"), list)
        and len(canonical_representation.get("result_domain", [])) >= 1,
        "canonical result_domain is explicitly locked",
        "ordinal/text class requires canonical_representation.result_domain",
    )
    for field_name in (
        "target_entity_grain",
        "anchor_family",
        "result_domain_rule",
        "raw_result_retention_rule",
        "normalization_rule",
        "no_row_interpretation",
    ):
        add_check(
            checks,
            f"ordinal_result_contract_{field_name}_present",
            isinstance(ordinal_contract.get(field_name), str)
            and str(ordinal_contract.get(field_name)).strip() != "",
            f"ordinal_result_contract.{field_name} is explicitly locked",
            f"ordinal/text variable_spec requires ordinal_result_contract.{field_name}",
        )
    for field_name in ("source_locator_mode", "source_table", "source_result_field", "source_grain", "target_grain"):
        add_check(
            checks,
            f"database_mapping_{field_name}_present",
            isinstance(database_mapping.get(field_name), str)
            and str(database_mapping.get(field_name)).strip() != "",
            f"database_mapping.{field_name} is explicitly locked",
            f"ordinal/text mapping_spec requires database_mapping.{field_name}",
        )
    add_check(
        checks,
        "source_itemids_present",
        isinstance(database_mapping.get("source_itemids"), list)
        and len(database_mapping.get("source_itemids", [])) >= 1,
        "mapping_spec locks at least one source itemid",
        "ordinal/text mapping_spec requires database_mapping.source_itemids",
    )
    for field_name in (
        "target_entity_grain",
        "anchor_family",
        "result_normalization_translation",
        "raw_result_retention_translation",
        "no_row_translation",
    ):
        add_check(
            checks,
            f"ordinal_result_translation_{field_name}_present",
            isinstance(ordinal_translation.get(field_name), str)
            and str(ordinal_translation.get(field_name)).strip() != "",
            f"ordinal_result_build_translation.{field_name} is explicitly locked",
            f"ordinal/text mapping_spec requires ordinal_result_build_translation.{field_name}",
        )
    add_check(
        checks,
        "target_entity_grain_match",
        ordinal_contract.get("target_entity_grain") == ordinal_translation.get("target_entity_grain"),
        "target_entity_grain matches across variable_spec and mapping_spec",
        "target_entity_grain mismatch between variable_spec and mapping_spec",
    )
    add_check(
        checks,
        "mapping_semantic_grain_match",
        standard_variable.get("semantic_grain") == immutable_core.get("semantic_grain"),
        "mapping_spec standard_variable.semantic_grain matches variable_spec immutable_core.semantic_grain",
        "ordinal/text semantic_grain mismatch between variable_spec and mapping_spec",
    )
    for field_name in ("normalization_rule_id", "primary_output_value_field", "source_result_output_field"):
        add_check(
            checks,
            f"representation_{field_name}_present",
            isinstance(representation.get(field_name), str)
            and str(representation.get(field_name)).strip() != "",
            f"representation_and_normalization.{field_name} is explicitly locked",
            f"ordinal/text mapping_spec requires representation_and_normalization.{field_name}",
        )
    add_check(
        checks,
        "required_non_null_fields_present",
        isinstance(validation_contract.get("required_non_null_fields"), list)
        and len(validation_contract.get("required_non_null_fields", [])) >= 1,
        "mapping_spec declares required_non_null_fields for validation",
        "ordinal/text mapping_spec requires validation_contract.required_non_null_fields",
    )


def validate_diagnosis_admin_demographic_id_map_contract(
    *,
    checks: list[dict[str, str]],
    variable_dir: Path,
    variable_spec: dict[str, Any],
    mapping_spec: dict[str, Any],
) -> None:
    variable_identity = variable_spec.get("variable_identity", {})
    immutable_core = variable_spec.get("immutable_core", {})
    canonical_representation = variable_spec.get("canonical_representation", {})
    variable_class = variable_spec.get("variable_class", {})
    admin_contract = variable_spec.get("admin_demographic_contract", {})
    standard_variable = mapping_spec.get("standard_variable", {})
    database_mapping = mapping_spec.get("database_mapping", {})
    admin_translation = mapping_spec.get("admin_demographic_build_translation", {})
    representation = mapping_spec.get("representation_and_normalization", {})
    validation_contract = mapping_spec.get("validation_contract", {})

    variable_id = str(variable_identity.get("variable_id", "")).strip()
    variable_class_id = str(variable_class.get("variable_class_id", "")).strip()
    add_check(
        checks,
        "admin_demographic_class_lock",
        variable_class_id in {DIAGNOSIS_ADMIN_DEMOGRAPHIC_ID_MAP_CLASS_ID, ""},
        f"variable is compatible with the diagnosis/admin/demographic/id-map class for {variable_id or variable_dir.name}",
        "variable_class.variable_class_id conflicts with the diagnosis/admin/demographic/id-map wrapper",
    )
    add_check(
        checks,
        "variable_directory_alignment",
        variable_dir.name == variable_id,
        f"variable directory name matches variable_id {variable_id}",
        f"variable directory name {variable_dir.name!r} does not match variable_id {variable_id!r}",
    )
    add_check(
        checks,
        "admin_value_family_lock",
        immutable_core.get("value_family") in {"demographic_category", "administrative_category", "identifier_map", "diagnosis_code_event"}
        and isinstance(canonical_representation.get("value_type"), str),
        "value family is locked to an administrative/demographic/id-map compatible family",
        "Class 7 requires an administrative, demographic, diagnosis, or id-map value family",
    )
    add_check(
        checks,
        "admin_source_class_present",
        isinstance(immutable_core.get("source_value_class"), str)
        and str(immutable_core.get("source_value_class")).strip() != "",
        "source_value_class is explicitly locked",
        "Class 7 requires immutable_core.source_value_class",
    )
    for field_name in (
        "target_entity_grain",
        "identifier_scope_rule",
        "source_authority_rule",
        "normalization_rule",
        "no_row_interpretation",
    ):
        add_check(
            checks,
            f"admin_demographic_contract_{field_name}_present",
            isinstance(admin_contract.get(field_name), str)
            and str(admin_contract.get(field_name)).strip() != "",
            f"admin_demographic_contract.{field_name} is explicitly locked",
            f"Class 7 variable_spec requires admin_demographic_contract.{field_name}",
        )
    for field_name in ("source_locator_mode", "source_table", "source_value_field", "source_grain", "target_grain"):
        add_check(
            checks,
            f"database_mapping_{field_name}_present",
            isinstance(database_mapping.get(field_name), str)
            and str(database_mapping.get(field_name)).strip() != "",
            f"database_mapping.{field_name} is explicitly locked",
            f"Class 7 mapping_spec requires database_mapping.{field_name}",
        )
    for field_name in (
        "target_entity_grain",
        "identifier_translation",
        "value_normalization_translation",
        "no_row_translation",
    ):
        add_check(
            checks,
            f"admin_demographic_translation_{field_name}_present",
            isinstance(admin_translation.get(field_name), str)
            and str(admin_translation.get(field_name)).strip() != "",
            f"admin_demographic_build_translation.{field_name} is explicitly locked",
            f"Class 7 mapping_spec requires admin_demographic_build_translation.{field_name}",
        )
    add_check(
        checks,
        "target_entity_grain_match",
        admin_contract.get("target_entity_grain") == admin_translation.get("target_entity_grain"),
        "target_entity_grain matches across variable_spec and mapping_spec",
        "target_entity_grain mismatch between variable_spec and mapping_spec",
    )
    add_check(
        checks,
        "mapping_semantic_grain_match",
        standard_variable.get("semantic_grain") == immutable_core.get("semantic_grain"),
        "mapping_spec standard_variable.semantic_grain matches variable_spec immutable_core.semantic_grain",
        "Class 7 semantic_grain mismatch between variable_spec and mapping_spec",
    )
    for field_name in ("normalization_rule_id", "primary_output_value_field"):
        add_check(
            checks,
            f"representation_{field_name}_present",
            isinstance(representation.get(field_name), str)
            and str(representation.get(field_name)).strip() != "",
            f"representation_and_normalization.{field_name} is explicitly locked",
            f"Class 7 mapping_spec requires representation_and_normalization.{field_name}",
        )
    add_check(
        checks,
        "required_non_null_fields_present",
        isinstance(validation_contract.get("required_non_null_fields"), list)
        and len(validation_contract.get("required_non_null_fields", [])) >= 1,
        "mapping_spec declares required_non_null_fields for validation",
        "Class 7 mapping_spec requires validation_contract.required_non_null_fields",
    )


def validate_score_phenotype_composite_derived_contract(
    *,
    checks: list[dict[str, str]],
    variable_dir: Path,
    variable_spec: dict[str, Any],
    mapping_spec: dict[str, Any],
) -> None:
    variable_identity = variable_spec.get("variable_identity", {})
    immutable_core = variable_spec.get("immutable_core", {})
    canonical_representation = variable_spec.get("canonical_representation", {})
    variable_class = variable_spec.get("variable_class", {})
    score_contract = variable_spec.get("score_phenotype_contract", {})
    standard_variable = mapping_spec.get("standard_variable", {})
    database_mapping = mapping_spec.get("database_mapping", {})
    score_translation = mapping_spec.get("score_phenotype_build_translation", {})
    representation = mapping_spec.get("representation_and_normalization", {})
    validation_contract = mapping_spec.get("validation_contract", {})

    variable_id = str(variable_identity.get("variable_id", "")).strip()
    variable_class_id = str(variable_class.get("variable_class_id", "")).strip()
    add_check(
        checks,
        "score_phenotype_class_lock",
        variable_class_id in {SCORE_PHENOTYPE_COMPOSITE_DERIVED_CLASS_ID, ""},
        f"variable is compatible with the score/phenotype/composite-derived class for {variable_id or variable_dir.name}",
        "variable_class.variable_class_id conflicts with the score/phenotype/composite-derived wrapper",
    )
    add_check(
        checks,
        "variable_directory_alignment",
        variable_dir.name == variable_id,
        f"variable directory name matches variable_id {variable_id}",
        f"variable directory name {variable_dir.name!r} does not match variable_id {variable_id!r}",
    )
    add_check(
        checks,
        "score_value_family_lock",
        immutable_core.get("value_family") in {"score_time_series", "score_summary", "phenotype_onset", "composite_derived"}
        and isinstance(canonical_representation.get("value_type"), str),
        "value family is locked to a score/phenotype/composite-compatible family",
        "Class 8 requires a score, phenotype, or composite-derived value family",
    )
    add_check(
        checks,
        "derived_source_class_lock",
        immutable_core.get("source_value_class") in {"source_supplied_composite_score", "derived_composite_score", "derived_phenotype"},
        "source_value_class is locked to a source-supplied or derived composite",
        "Class 8 requires source_value_class to be source-supplied/derived composite evidence",
    )
    for field_name in (
        "target_entity_grain",
        "time_basis_rule",
        "component_trace_rule",
        "score_value_rule",
        "no_row_interpretation",
    ):
        add_check(
            checks,
            f"score_phenotype_contract_{field_name}_present",
            isinstance(score_contract.get(field_name), str)
            and str(score_contract.get(field_name)).strip() != "",
            f"score_phenotype_contract.{field_name} is explicitly locked",
            f"Class 8 variable_spec requires score_phenotype_contract.{field_name}",
        )
    for field_name in ("source_locator_mode", "source_table", "source_value_field", "source_grain", "target_grain"):
        add_check(
            checks,
            f"database_mapping_{field_name}_present",
            isinstance(database_mapping.get(field_name), str)
            and str(database_mapping.get(field_name)).strip() != "",
            f"database_mapping.{field_name} is explicitly locked",
            f"Class 8 mapping_spec requires database_mapping.{field_name}",
        )
    for field_name in (
        "target_entity_grain",
        "time_basis_translation",
        "score_value_translation",
        "component_trace_translation",
        "no_row_translation",
    ):
        add_check(
            checks,
            f"score_phenotype_translation_{field_name}_present",
            isinstance(score_translation.get(field_name), str)
            and str(score_translation.get(field_name)).strip() != "",
            f"score_phenotype_build_translation.{field_name} is explicitly locked",
            f"Class 8 mapping_spec requires score_phenotype_build_translation.{field_name}",
        )
    add_check(
        checks,
        "target_entity_grain_match",
        score_contract.get("target_entity_grain") == score_translation.get("target_entity_grain"),
        "target_entity_grain matches across variable_spec and mapping_spec",
        "target_entity_grain mismatch between variable_spec and mapping_spec",
    )
    add_check(
        checks,
        "mapping_semantic_grain_match",
        standard_variable.get("semantic_grain") == immutable_core.get("semantic_grain"),
        "mapping_spec standard_variable.semantic_grain matches variable_spec immutable_core.semantic_grain",
        "Class 8 semantic_grain mismatch between variable_spec and mapping_spec",
    )
    for field_name in ("normalization_rule_id", "primary_output_value_field"):
        add_check(
            checks,
            f"representation_{field_name}_present",
            isinstance(representation.get(field_name), str)
            and str(representation.get(field_name)).strip() != "",
            f"representation_and_normalization.{field_name} is explicitly locked",
            f"Class 8 mapping_spec requires representation_and_normalization.{field_name}",
        )
    add_check(
        checks,
        "required_non_null_fields_present",
        isinstance(validation_contract.get("required_non_null_fields"), list)
        and len(validation_contract.get("required_non_null_fields", [])) >= 1,
        "mapping_spec declares required_non_null_fields for validation",
        "Class 8 mapping_spec requires validation_contract.required_non_null_fields",
    )


def validate_microbiology_multi_entity_family_contract(
    *,
    checks: list[dict[str, str]],
    variable_dir: Path,
    variable_spec: dict[str, Any],
    mapping_spec: dict[str, Any],
) -> None:
    variable_identity = variable_spec.get("variable_identity", {})
    immutable_core = variable_spec.get("immutable_core", {})
    canonical_representation = variable_spec.get("canonical_representation", {})
    variable_class = variable_spec.get("variable_class", {})
    microbiology_contract = variable_spec.get("microbiology_entity_contract", {})
    standard_variable = mapping_spec.get("standard_variable", {})
    database_mapping = mapping_spec.get("database_mapping", {})
    microbiology_translation = mapping_spec.get("microbiology_family_build_translation", {})
    representation = mapping_spec.get("representation_and_normalization", {})
    validation_contract = mapping_spec.get("validation_contract", {})

    variable_id = str(variable_identity.get("variable_id", "")).strip()
    variable_class_id = str(variable_class.get("variable_class_id", "")).strip()
    allowed_source_classes = {
        "microbiology_test_event",
        "microbiology_organism_branch",
        "microbiology_susceptibility_leaf",
    }
    allowed_value_types = {
        "microbiology_test_event",
        "microbiology_organism_branch",
        "microbiology_antibiotic_susceptibility_leaf",
    }
    add_check(
        checks,
        "microbiology_multi_entity_class_lock",
        variable_class_id in {MICROBIOLOGY_MULTI_ENTITY_FAMILY_CLASS_ID, ""},
        f"variable is compatible with the microbiology multi-entity family class for {variable_id or variable_dir.name}",
        "variable_class.variable_class_id conflicts with the microbiology multi-entity family wrapper",
    )
    add_check(
        checks,
        "variable_directory_alignment",
        variable_dir.name == variable_id,
        f"variable directory name matches variable_id {variable_id}",
        f"variable directory name {variable_dir.name!r} does not match variable_id {variable_id!r}",
    )
    add_check(
        checks,
        "microbiology_value_family_lock",
        immutable_core.get("value_family") == "microbiology_multi_entity"
        and canonical_representation.get("value_type") in allowed_value_types,
        "value family and representation are locked to microbiology multi-entity roles",
        "Class 9 requires immutable_core.value_family=microbiology_multi_entity and an approved microbiology value_type",
    )
    add_check(
        checks,
        "microbiology_source_class_lock",
        immutable_core.get("source_value_class") in allowed_source_classes,
        "source_value_class is locked to a microbiology entity role",
        "Class 9 requires source_value_class to be microbiology_test_event, microbiology_organism_branch, or microbiology_susceptibility_leaf",
    )
    for field_name in (
        "family_role",
        "entity_grain",
        "source_hierarchy_rule",
        "parent_child_rule",
        "raw_text_retention_rule",
        "no_row_interpretation",
    ):
        add_check(
            checks,
            f"microbiology_entity_contract_{field_name}_present",
            isinstance(microbiology_contract.get(field_name), str)
            and str(microbiology_contract.get(field_name)).strip() != "",
            f"microbiology_entity_contract.{field_name} is explicitly locked",
            f"Class 9 variable_spec requires microbiology_entity_contract.{field_name}",
        )
    for field_name in ("source_locator_mode", "source_table", "source_grain", "target_grain"):
        add_check(
            checks,
            f"database_mapping_{field_name}_present",
            isinstance(database_mapping.get(field_name), str)
            and str(database_mapping.get(field_name)).strip() != "",
            f"database_mapping.{field_name} is explicitly locked",
            f"Class 9 mapping_spec requires database_mapping.{field_name}",
        )
    add_check(
        checks,
        "source_entity_key_fields_present",
        isinstance(database_mapping.get("source_entity_key_fields"), list)
        and len(database_mapping.get("source_entity_key_fields", [])) >= 1,
        "mapping_spec locks source_entity_key_fields",
        "Class 9 mapping_spec requires database_mapping.source_entity_key_fields",
    )
    for field_name in (
        "family_role",
        "entity_grain_translation",
        "source_hierarchy_translation",
        "parent_child_translation",
        "raw_text_retention_translation",
        "no_row_translation",
    ):
        add_check(
            checks,
            f"microbiology_translation_{field_name}_present",
            isinstance(microbiology_translation.get(field_name), str)
            and str(microbiology_translation.get(field_name)).strip() != "",
            f"microbiology_family_build_translation.{field_name} is explicitly locked",
            f"Class 9 mapping_spec requires microbiology_family_build_translation.{field_name}",
        )
    add_check(
        checks,
        "family_role_match",
        microbiology_contract.get("family_role") == microbiology_translation.get("family_role"),
        "family_role matches across variable_spec and mapping_spec",
        "family_role mismatch between variable_spec and mapping_spec",
    )
    add_check(
        checks,
        "mapping_semantic_grain_match",
        standard_variable.get("semantic_grain") == immutable_core.get("semantic_grain"),
        "mapping_spec standard_variable.semantic_grain matches variable_spec immutable_core.semantic_grain",
        "Class 9 semantic_grain mismatch between variable_spec and mapping_spec",
    )
    for field_name in ("normalization_rule_id", "primary_entity_id_field"):
        add_check(
            checks,
            f"representation_{field_name}_present",
            isinstance(representation.get(field_name), str)
            and str(representation.get(field_name)).strip() != "",
            f"representation_and_normalization.{field_name} is explicitly locked",
            f"Class 9 mapping_spec requires representation_and_normalization.{field_name}",
        )
    add_check(
        checks,
        "required_non_null_fields_present",
        isinstance(validation_contract.get("required_non_null_fields"), list)
        and len(validation_contract.get("required_non_null_fields", [])) >= 1,
        "mapping_spec declares required_non_null_fields for validation",
        "Class 9 mapping_spec requires validation_contract.required_non_null_fields",
    )
    add_check(
        checks,
        "no_row_policy_present",
        isinstance(validation_contract.get("no_row_policy_check"), str)
        and str(validation_contract.get("no_row_policy_check")).strip() != "",
        "mapping_spec explicitly locks a no-row policy check",
        "Class 9 mapping_spec requires validation_contract.no_row_policy_check",
    )


def run_governed_standard_variable(
    *,
    variable_dir: Path,
    execution_entrypoint_path: Path,
    parser_description: str,
    class_contract_validator,
) -> int:
    parser = build_parser(parser_description)
    args = parser.parse_args()

    workspace_root = Path(args.workspace_root).resolve() if args.workspace_root else DEFAULT_WORKSPACE_ROOT.resolve()
    variable_spec_path = Path(args.variable_spec).resolve() if args.variable_spec else (variable_dir / "variable_spec.json").resolve()
    mapping_spec_path = Path(args.mapping_spec).resolve() if args.mapping_spec else build_default_mapping_spec_path(variable_dir, args.database_id).resolve()
    output_dir = Path(args.output_dir).resolve() if args.output_dir else None

    checks: list[dict[str, str]] = []
    if not variable_spec_path.exists():
        raise SystemExit(f"variable_spec.json not found: {variable_spec_path}")
    if not mapping_spec_path.exists():
        raise SystemExit(f"mapping_spec JSON not found: {mapping_spec_path}")

    variable_spec = load_json(variable_spec_path)
    mapping_spec = load_json(mapping_spec_path)

    variable_identity = variable_spec.get("variable_identity", {})
    immutable_core = variable_spec.get("immutable_core", {})
    canonical_representation = variable_spec.get("canonical_representation", {})
    mapping_standard_variable = mapping_spec.get("standard_variable", {})
    database_mapping = mapping_spec.get("database_mapping", {})
    execution_contract = mapping_spec.get("execution_contract", {})
    representation = mapping_spec.get("representation_and_normalization", {})

    variable_id = str(variable_identity.get("variable_id", "")).strip()
    mapping_variable_id = str(mapping_standard_variable.get("variable_id", "")).strip()
    expected_variable_spec_ref = repo_relative(variable_spec_path)
    actual_variable_spec_ref = str(mapping_spec.get("variable_spec_ref", "")).strip()

    add_check(
        checks,
        "variable_spec_artifact_type",
        variable_spec.get("artifact_type") == "variable_spec",
        "variable_spec artifact_type is variable_spec",
        f"unexpected variable_spec artifact_type: {variable_spec.get('artifact_type')!r}",
    )
    add_check(
        checks,
        "mapping_spec_artifact_type",
        mapping_spec.get("artifact_type") == "mapping_spec",
        "mapping_spec artifact_type is mapping_spec",
        f"unexpected mapping_spec artifact_type: {mapping_spec.get('artifact_type')!r}",
    )
    add_check(
        checks,
        "variable_id_match",
        bool(variable_id) and variable_id == mapping_variable_id,
        f"variable_id is consistently locked to {variable_id or '<missing>'}",
        "variable_id mismatch between variable_spec and mapping_spec",
    )
    add_check(
        checks,
        "variable_version_match",
        variable_identity.get("variable_version") == mapping_standard_variable.get("variable_version"),
        "variable_version matches across variable_spec and mapping_spec",
        "variable_version mismatch between variable_spec and mapping_spec",
    )
    add_check(
        checks,
        "database_id_match",
        database_mapping.get("database_id") == args.database_id,
        f"mapping_spec database_id matches requested database_id {args.database_id}",
        "mapping_spec database_id does not match the requested database_id",
    )
    add_check(
        checks,
        "variable_spec_ref_match",
        actual_variable_spec_ref == expected_variable_spec_ref,
        "mapping_spec variable_spec_ref points to the chosen variable_spec.json",
        (
            "mapping_spec variable_spec_ref does not match the chosen variable_spec.json: "
            f"{actual_variable_spec_ref!r} != {expected_variable_spec_ref!r}"
        ),
    )
    add_check(
        checks,
        "semantic_grain_match",
        immutable_core.get("semantic_grain") == mapping_standard_variable.get("semantic_grain"),
        "semantic_grain matches across variable_spec and mapping_spec",
        "semantic_grain mismatch between variable_spec and mapping_spec",
    )
    add_check(
        checks,
        "source_value_class_match",
        immutable_core.get("source_value_class") == mapping_standard_variable.get("source_value_class"),
        "source_value_class matches across variable_spec and mapping_spec",
        "source_value_class mismatch between variable_spec and mapping_spec",
    )
    add_check(
        checks,
        "canonical_unit_match",
        canonical_representation.get("canonical_unit") == mapping_standard_variable.get("canonical_unit"),
        "canonical_unit matches across variable_spec and mapping_spec",
        "canonical_unit mismatch between variable_spec and mapping_spec",
    )
    add_check(
        checks,
        "canonical_value_family_match",
        immutable_core.get("value_family") == mapping_standard_variable.get("canonical_value_family"),
        "value family matches across variable_spec and mapping_spec",
        "value family mismatch between variable_spec and mapping_spec",
    )
    add_check(
        checks,
        "representation_unit_match",
        canonical_representation.get("canonical_unit") == representation.get("canonical_unit"),
        "canonical_unit matches across variable_spec and representation_and_normalization",
        "canonical_unit mismatch between variable_spec and representation_and_normalization",
    )

    class_contract_validator(
        checks=checks,
        variable_dir=variable_dir,
        variable_spec=variable_spec,
        mapping_spec=mapping_spec,
    )

    reference_implementation_raw = str(execution_contract.get("current_reference_implementation", "")).strip()
    local_input_asset_raw = resolve_primary_local_input_asset_raw(database_mapping)
    missing_placeholder = workspace_root / "__missing_standard_system_mvp_path__"
    reference_implementation_path = (
        resolve_workspace_relative_path(workspace_root, reference_implementation_raw)
        if reference_implementation_raw
        else missing_placeholder
    )
    local_input_asset_path = (
        resolve_workspace_relative_path(workspace_root, local_input_asset_raw)
        if local_input_asset_raw
        else missing_placeholder
    )
    public_command = ["python", workspace_relative(reference_implementation_path, workspace_root)]

    add_check(
        checks,
        "governed_execution_entrypoint_declared",
        str(execution_contract.get("governed_execution_entrypoint", "")).strip() == repo_relative(execution_entrypoint_path),
        "mapping_spec governed_execution_entrypoint points to this execution.py",
        "mapping_spec governed_execution_entrypoint does not point to this execution.py",
    )
    add_check(
        checks,
        "reference_implementation_declared",
        bool(reference_implementation_raw),
        "mapping_spec declares current_reference_implementation",
        "mapping_spec execution_contract.current_reference_implementation is missing",
    )
    add_check(
        checks,
        "reference_implementation_exists",
        bool(reference_implementation_raw) and reference_implementation_path.exists(),
        f"current reference implementation exists: {workspace_relative(reference_implementation_path, workspace_root)}",
        f"current reference implementation not found: {reference_implementation_path}",
    )
    add_check(
        checks,
        "local_input_asset_declared",
        bool(local_input_asset_raw),
        "mapping_spec declares a primary local prepared input asset",
        "mapping_spec does not declare local_prepared_input_asset or a non-empty local_prepared_input_assets list",
    )
    add_check(
        checks,
        "local_input_asset_exists",
        bool(local_input_asset_raw) and local_input_asset_path.exists(),
        f"local prepared input asset exists: {workspace_relative(local_input_asset_path, workspace_root)}",
        f"local prepared input asset not found: {local_input_asset_path}",
    )
    evidence_refs = mapping_spec.get("evidence_refs", {})
    local_output_asset_raw = ""
    if isinstance(evidence_refs, dict):
        local_output_asset_raw = str(evidence_refs.get("local_output_asset_path", "")).strip()
    database_id_for_layout = str(database_mapping.get("database_id") or args.database_id).strip()
    layer3_path_ok, layer3_path_message = validate_layer3_output_path_for_database(
        local_output_asset_raw,
        database_id_for_layout,
    )
    add_check(
        checks,
        "layer3_output_path_layout",
        layer3_path_ok,
        layer3_path_message,
        layer3_path_message,
    )

    validation_report = build_validation_report(
        variable_spec_path=variable_spec_path,
        mapping_spec_path=mapping_spec_path,
        variable_spec=variable_spec,
        mapping_spec=mapping_spec,
        checks=checks,
    )
    print_validation_summary(validation_report)

    if validation_report["overall_status"] != "pass":
        blocked_manifest = build_execution_manifest(
            variable_spec_path=variable_spec_path,
            mapping_spec_path=mapping_spec_path,
            workspace_root=workspace_root,
            reference_implementation_path=reference_implementation_path,
            local_input_asset_path=local_input_asset_path,
            validation_report=validation_report,
            execution_mode="blocked_by_validation",
            command=public_command,
            process_batch_id=None,
            subprocess_return_code=None,
            started_at=None,
            finished_at=None,
            output_artifacts={},
            output_signatures={},
            build_summary={},
            execution_entrypoint_path=execution_entrypoint_path,
        )
        if output_dir is not None:
            write_runtime_artifacts(output_dir, validation_report, blocked_manifest)
        return 1

    command = [sys.executable, str(reference_implementation_path)]

    if args.validate_only:
        manifest = build_execution_manifest(
            variable_spec_path=variable_spec_path,
            mapping_spec_path=mapping_spec_path,
            workspace_root=workspace_root,
            reference_implementation_path=reference_implementation_path,
            local_input_asset_path=local_input_asset_path,
            validation_report=validation_report,
            execution_mode="validate_only",
            command=public_command,
            process_batch_id=None,
            subprocess_return_code=None,
            started_at=None,
            finished_at=None,
            output_artifacts={},
            output_signatures={},
            build_summary={},
            execution_entrypoint_path=execution_entrypoint_path,
        )
        if output_dir is not None:
            write_runtime_artifacts(output_dir, validation_report, manifest)
        print("Validation-only mode. Reference implementation not executed.")
        return 0

    if args.dry_run:
        manifest = build_execution_manifest(
            variable_spec_path=variable_spec_path,
            mapping_spec_path=mapping_spec_path,
            workspace_root=workspace_root,
            reference_implementation_path=reference_implementation_path,
            local_input_asset_path=local_input_asset_path,
            validation_report=validation_report,
            execution_mode="dry_run",
            command=public_command,
            process_batch_id=None,
            subprocess_return_code=None,
            started_at=None,
            finished_at=None,
            output_artifacts={},
            output_signatures={},
            build_summary={},
            execution_entrypoint_path=execution_entrypoint_path,
        )
        if output_dir is not None:
            write_runtime_artifacts(output_dir, validation_report, manifest)
        print("Governed command:")
        print(" ".join(public_command))
        print("Dry-run only. Reference implementation not executed.")
        return 0

    started_at = now_utc_iso()
    completed = subprocess.run(command, check=False, capture_output=True, text=True)
    finished_at = now_utc_iso()
    process_batch_id = parse_process_batch_id(completed.stdout)
    build_summary = sanitize_build_summary(
        parse_build_summary(completed.stdout),
        workspace_root,
    )

    if completed.stdout:
        print(completed.stdout, end="" if completed.stdout.endswith("\n") else "\n")
    if completed.stderr:
        print(completed.stderr, file=sys.stderr, end="" if completed.stderr.endswith("\n") else "\n")

    output_artifacts: dict[str, str] = {}
    output_signatures: dict[str, dict[str, Any]] = {}
    if completed.returncode == 0:
        if process_batch_id is None:
            print(
                "Governed execute-mode run finished without a process_batch_id in stdout; runtime evidence is incomplete.",
                file=sys.stderr,
            )
            completed = subprocess.CompletedProcess(
                args=completed.args,
                returncode=1,
                stdout=completed.stdout,
                stderr=completed.stderr,
            )
        else:
            try:
                output_artifacts = discover_output_artifacts(
                    mapping_spec=mapping_spec,
                    workspace_root=workspace_root,
                    process_batch_id=process_batch_id,
                )
                if output_dir is not None:
                    output_artifacts = capture_runtime_local_append_only_artifacts(
                        output_artifacts=output_artifacts,
                        workspace_root=workspace_root,
                        runtime_output_dir=output_dir,
                    )
                output_signatures = build_output_signatures(
                    output_artifacts=output_artifacts,
                    workspace_root=workspace_root,
                )
            except (FileNotFoundError, OSError) as exc:
                print(
                    "Governed execute-mode run finished but runtime evidence could not lock all output artifacts: "
                    f"{exc}",
                    file=sys.stderr,
                )
                completed = subprocess.CompletedProcess(
                    args=completed.args,
                    returncode=1,
                    stdout=completed.stdout,
                    stderr=completed.stderr,
                )

    manifest = build_execution_manifest(
        variable_spec_path=variable_spec_path,
        mapping_spec_path=mapping_spec_path,
        workspace_root=workspace_root,
        reference_implementation_path=reference_implementation_path,
        local_input_asset_path=local_input_asset_path,
        validation_report=validation_report,
        execution_mode="execute",
        command=public_command,
        process_batch_id=process_batch_id,
        subprocess_return_code=completed.returncode,
        started_at=started_at,
        finished_at=finished_at,
        output_artifacts=output_artifacts,
        output_signatures=output_signatures,
        build_summary=build_summary,
        execution_entrypoint_path=execution_entrypoint_path,
    )
    if output_dir is not None:
        public_stdout_text = render_public_stdout_log(
            variable_id=validation_report["variable_id"],
            process_batch_id=process_batch_id,
            build_summary=build_summary,
        )
        write_runtime_artifacts(
            output_dir,
            validation_report,
            manifest,
            stdout_text=public_stdout_text,
            stderr_text=completed.stderr,
        )
    return completed.returncode


def run_event_level_numeric_primary_source(
    *,
    variable_dir: Path,
    execution_entrypoint_path: Path,
) -> int:
    return run_governed_standard_variable(
        variable_dir=variable_dir,
        execution_entrypoint_path=execution_entrypoint_path,
        parser_description=(
            "Governed execution entrypoint for the reusable event-level numeric primary-source "
            "standard-system MVP class."
        ),
        class_contract_validator=validate_event_level_numeric_primary_source_contract,
    )


def run_baseline_summary_window_numeric(
    *,
    variable_dir: Path,
    execution_entrypoint_path: Path,
) -> int:
    return run_governed_standard_variable(
        variable_dir=variable_dir,
        execution_entrypoint_path=execution_entrypoint_path,
        parser_description=(
            "Governed execution entrypoint for the reusable baseline-summary-window numeric "
            "standard-system MVP class."
        ),
        class_contract_validator=validate_baseline_summary_window_numeric_contract,
    )


def run_binary_state_episode(
    *,
    variable_dir: Path,
    execution_entrypoint_path: Path,
) -> int:
    return run_governed_standard_variable(
        variable_dir=variable_dir,
        execution_entrypoint_path=execution_entrypoint_path,
        parser_description=(
            "Governed execution entrypoint for the reusable binary-state episode "
            "standard-system MVP class."
        ),
        class_contract_validator=validate_binary_state_episode_contract,
    )


def run_treatment_device_io_event_stream(
    *,
    variable_dir: Path,
    execution_entrypoint_path: Path,
) -> int:
    return run_governed_standard_variable(
        variable_dir=variable_dir,
        execution_entrypoint_path=execution_entrypoint_path,
        parser_description=(
            "Governed execution entrypoint for the reusable treatment/device/IO "
            "event-stream standard-system MVP class."
        ),
        class_contract_validator=validate_treatment_device_io_event_stream_contract,
    )


def run_episode_interval_bridge(
    *,
    variable_dir: Path,
    execution_entrypoint_path: Path,
) -> int:
    return run_governed_standard_variable(
        variable_dir=variable_dir,
        execution_entrypoint_path=execution_entrypoint_path,
        parser_description=(
            "Governed execution entrypoint for the reusable episode-interval bridge "
            "standard-system MVP class."
        ),
        class_contract_validator=validate_episode_interval_bridge_contract,
    )


def run_ordinal_text_semiquantitative_result(
    *,
    variable_dir: Path,
    execution_entrypoint_path: Path,
) -> int:
    return run_governed_standard_variable(
        variable_dir=variable_dir,
        execution_entrypoint_path=execution_entrypoint_path,
        parser_description=(
            "Governed execution entrypoint for the reusable ordinal/text/"
            "semiquantitative result standard-system MVP class."
        ),
        class_contract_validator=validate_ordinal_text_semiquantitative_result_contract,
    )


def run_diagnosis_admin_demographic_id_map(
    *,
    variable_dir: Path,
    execution_entrypoint_path: Path,
) -> int:
    return run_governed_standard_variable(
        variable_dir=variable_dir,
        execution_entrypoint_path=execution_entrypoint_path,
        parser_description=(
            "Governed execution entrypoint for the reusable diagnosis/admin/"
            "demographic/id-map standard-system MVP class."
        ),
        class_contract_validator=validate_diagnosis_admin_demographic_id_map_contract,
    )


def run_score_phenotype_composite_derived(
    *,
    variable_dir: Path,
    execution_entrypoint_path: Path,
) -> int:
    return run_governed_standard_variable(
        variable_dir=variable_dir,
        execution_entrypoint_path=execution_entrypoint_path,
        parser_description=(
            "Governed execution entrypoint for the reusable score/phenotype/"
            "composite-derived standard-system MVP class."
        ),
        class_contract_validator=validate_score_phenotype_composite_derived_contract,
    )


def run_microbiology_multi_entity_family(
    *,
    variable_dir: Path,
    execution_entrypoint_path: Path,
) -> int:
    return run_governed_standard_variable(
        variable_dir=variable_dir,
        execution_entrypoint_path=execution_entrypoint_path,
        parser_description=(
            "Governed execution entrypoint for the reusable microbiology "
            "multi-entity family standard-system MVP class."
        ),
        class_contract_validator=validate_microbiology_multi_entity_family_contract,
    )
