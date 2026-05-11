from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_WORKSPACE_ROOT = REPO_ROOT.parent.parent
CONTRACT_REF = "Framework_Guideline/StandardSystem_RuntimeEvidence_Contract.md"
PROCESS_BATCH_ID_PATTERN = re.compile(r"^\d{8}T\d{6}Z_[A-Za-z0-9.\-]+_[A-Za-z0-9_]+$")
MACHINE_BOUND_ABSOLUTE_PATH_PATTERN = re.compile(r"(?<!`)\b[A-Za-z]:[\\/][^\s)>\"]*|`[A-Za-z]:[\\/][^`]+`")
ALLOWED_CHECK_STATUSES = {"pass", "fail"}
ALLOWED_VALIDATION_STATUSES = {"pass", "fail"}
ALLOWED_EXECUTION_MODES = {"validate_only", "dry_run", "execute", "blocked_by_validation"}
RERUN_INVARIANT_ARTIFACT_KEYS = {"primary_output_asset", "preview_csv"}
LATEST_STATE_MUTABLE_ARTIFACT_KEYS = {"asset_manifest", "knowledge_package"}
RUN_SCOPED_APPEND_ONLY_ARTIFACT_KEYS = {"build_log"}

REQUIRED_VALIDATION_REPORT_FIELDS: dict[str, type[Any]] = {
    "artifact_type": str,
    "artifact_version": str,
    "contract_ref": str,
    "generated_at": str,
    "validation_scope": str,
    "overall_status": str,
    "variable_id": str,
    "database_id": str,
    "variable_spec_path": str,
    "mapping_spec_path": str,
    "spec_hashes": dict,
    "checks": list,
}

REQUIRED_MANIFEST_FIELDS: dict[str, type[Any]] = {
    "artifact_type": str,
    "artifact_version": str,
    "contract_ref": str,
    "generated_at": str,
    "variable_id": str,
    "database_id": str,
    "execution_mode": str,
    "validation_status": str,
    "variable_spec_path": str,
    "mapping_spec_path": str,
    "execution_entrypoint_path": str,
    "reference_implementation_path": str,
    "local_input_asset_path": str,
    "command": list,
    "spec_hashes": dict,
    "output_artifacts": dict,
    "output_signatures": dict,
    "build_summary": dict,
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_path(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def repo_relative(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT).as_posix()


def find_runtime_dirs() -> list[Path]:
    runtime_root = REPO_ROOT / "docs" / "standard_system_mvp"
    if not runtime_root.exists():
        return []
    runtime_dirs: list[Path] = []
    for path in runtime_root.glob("*/runtime/*"):
        if path.is_dir() and (path / "validation_report.json").exists() and (path / "manifest.json").exists():
            runtime_dirs.append(path)
    return sorted(runtime_dirs, key=lambda item: repo_relative(item))


def validate_required_fields(record: dict[str, Any], required_fields: dict[str, type[Any]], label: str) -> list[str]:
    errors: list[str] = []
    for field_name, expected_type in required_fields.items():
        value = record.get(field_name)
        if not isinstance(value, expected_type):
            actual_type = type(value).__name__
            errors.append(f"{label}.{field_name} expected {expected_type.__name__}, got {actual_type}")
    return errors


def validate_no_machine_bound_absolute_paths(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    match = MACHINE_BOUND_ABSOLUTE_PATH_PATTERN.search(text)
    if not match:
        return []
    return [f"{repo_relative(path)} contains a machine-bound absolute path example: {match.group(0)!r}"]


def validate_repo_relative_path(raw_path: str, field_name: str) -> list[str]:
    errors: list[str] = []
    path = Path(raw_path)
    if path.is_absolute():
        errors.append(f"{field_name} must be repo-relative, got absolute path: {raw_path}")
        return errors
    target = REPO_ROOT / path
    if not target.exists():
        errors.append(f"{field_name} points to a missing repo file: {raw_path}")
    return errors


def validate_workspace_relative_path(raw_path: str, field_name: str, workspace_root: Path) -> list[str]:
    errors: list[str] = []
    path = Path(raw_path)
    if path.is_absolute():
        errors.append(f"{field_name} must be workspace-relative, got absolute path: {raw_path}")
        return errors
    target = (workspace_root / path).resolve()
    if not target.exists():
        errors.append(f"{field_name} points to a missing workspace file: {raw_path}")
    return errors


def validate_spec_hashes(
    validation_report: dict[str, Any],
    manifest: dict[str, Any],
) -> list[str]:
    errors: list[str] = []
    validation_hashes = validation_report.get("spec_hashes", {})
    manifest_hashes = manifest.get("spec_hashes", {})
    if validation_hashes != manifest_hashes:
        errors.append("validation_report.spec_hashes does not match manifest.spec_hashes")

    variable_spec_path = REPO_ROOT / validation_report["variable_spec_path"]
    mapping_spec_path = REPO_ROOT / validation_report["mapping_spec_path"]
    actual_variable_hash = sha256_path(variable_spec_path)
    actual_mapping_hash = sha256_path(mapping_spec_path)

    if validation_hashes.get("variable_spec_sha256") != actual_variable_hash:
        errors.append("validation_report variable_spec_sha256 does not match the current referenced variable_spec.json")
    if validation_hashes.get("mapping_spec_sha256") != actual_mapping_hash:
        errors.append("validation_report mapping_spec_sha256 does not match the current referenced mapping_spec.json")
    return errors


def validate_checks_block(validation_report: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    checks = validation_report["checks"]
    if not checks:
        errors.append("validation_report.checks must be a non-empty list")
        return errors
    all_pass = True
    for index, item in enumerate(checks, start=1):
        if not isinstance(item, dict):
            errors.append(f"validation_report.checks[{index}] must be an object")
            continue
        for required_key in ("check_id", "status", "message"):
            value = item.get(required_key)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"validation_report.checks[{index}].{required_key} must be a non-empty string")
        status = item.get("status")
        if isinstance(status, str) and status not in ALLOWED_CHECK_STATUSES:
            errors.append(f"validation_report.checks[{index}].status must be one of {sorted(ALLOWED_CHECK_STATUSES)}")
        if status != "pass":
            all_pass = False
    overall_status = validation_report["overall_status"]
    if overall_status not in ALLOWED_VALIDATION_STATUSES:
        errors.append(f"validation_report.overall_status must be one of {sorted(ALLOWED_VALIDATION_STATUSES)}")
    if overall_status == "pass" and not all_pass:
        errors.append("validation_report.overall_status is pass but not all checks passed")
    return errors


def validate_manifest_command(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    command = manifest["command"]
    if not command:
        errors.append("manifest.command must be a non-empty list")
        return errors
    if not all(isinstance(item, str) and item.strip() for item in command):
        errors.append("manifest.command must contain only non-empty strings")
        return errors
    if command[0] != "python":
        errors.append("manifest.command[0] should be the public-safe launcher token `python`")
    if len(command) >= 2 and command[1] != manifest["reference_implementation_path"]:
        errors.append("manifest.command[1] should match manifest.reference_implementation_path")
    return errors


def classify_output_artifact(artifact_name: str) -> str:
    if artifact_name in RERUN_INVARIANT_ARTIFACT_KEYS:
        return "rerun_invariant"
    if artifact_name in LATEST_STATE_MUTABLE_ARTIFACT_KEYS:
        return "latest_state_mutable"
    if artifact_name in RUN_SCOPED_APPEND_ONLY_ARTIFACT_KEYS:
        return "run_scoped_append_only"
    return "rerun_invariant"


def validate_output_artifacts(manifest: dict[str, Any], workspace_root: Path) -> list[str]:
    errors: list[str] = []
    output_artifacts = manifest.get("output_artifacts", {})
    output_signatures = manifest.get("output_signatures", {})
    if not isinstance(output_artifacts, dict) or not output_artifacts:
        return ["manifest.output_artifacts must be a non-empty object for execute-mode runtime evidence"]
    if not isinstance(output_signatures, dict) or not output_signatures:
        return ["manifest.output_signatures must be a non-empty object for execute-mode runtime evidence"]

    artifact_names = set(output_artifacts)
    signature_names = set(output_signatures)
    if artifact_names != signature_names:
        errors.append(
            "manifest.output_artifacts keys must exactly match manifest.output_signatures keys"
        )

    for artifact_name, raw_path in output_artifacts.items():
        if not isinstance(artifact_name, str) or not artifact_name.strip():
            errors.append("manifest.output_artifacts contains a blank artifact key")
            continue
        if not isinstance(raw_path, str) or not raw_path.strip():
            errors.append(f"manifest.output_artifacts.{artifact_name} must be a non-empty string path")
            continue
        errors.extend(
            validate_workspace_relative_path(
                raw_path,
                f"manifest.output_artifacts.{artifact_name}",
                workspace_root,
            )
        )
        resolved_path = (workspace_root / raw_path).resolve()
        signature = output_signatures.get(artifact_name)
        if not isinstance(signature, dict):
            errors.append(f"manifest.output_signatures.{artifact_name} must be an object")
            continue
        sha256_value = signature.get("sha256")
        size_bytes = signature.get("size_bytes")
        if not isinstance(sha256_value, str) or not re.fullmatch(r"[0-9a-f]{64}", sha256_value):
            errors.append(
                f"manifest.output_signatures.{artifact_name}.sha256 must be a 64-character lowercase hex string"
            )
        if not isinstance(size_bytes, int) or size_bytes < 0:
            errors.append(f"manifest.output_signatures.{artifact_name}.size_bytes must be a non-negative integer")
        if resolved_path.exists():
            artifact_role = classify_output_artifact(artifact_name)
            if artifact_role != "latest_state_mutable":
                actual_sha256 = sha256_path(resolved_path)
                actual_size = resolved_path.stat().st_size
                if sha256_value != actual_sha256:
                    errors.append(
                        f"manifest.output_signatures.{artifact_name}.sha256 does not match the current file hash"
                    )
                if size_bytes != actual_size:
                    errors.append(
                        f"manifest.output_signatures.{artifact_name}.size_bytes does not match the current file size"
                    )
    return errors


def validate_execute_mode(
    runtime_dir: Path,
    manifest: dict[str, Any],
    validation_report: dict[str, Any],
    workspace_root: Path,
) -> list[str]:
    errors: list[str] = []
    stdout_path = runtime_dir / "execution_stdout.log"
    stderr_path = runtime_dir / "execution_stderr.log"

    if validation_report["overall_status"] != "pass":
        errors.append("execute-mode runtime evidence requires validation_report.overall_status = pass")
    if manifest["validation_status"] != "pass":
        errors.append("execute-mode runtime evidence requires manifest.validation_status = pass")

    process_batch_id = manifest.get("process_batch_id")
    if not isinstance(process_batch_id, str) or not PROCESS_BATCH_ID_PATTERN.fullmatch(process_batch_id):
        errors.append("manifest.process_batch_id is missing or does not match the required batch-id pattern")

    subprocess_return_code = manifest.get("subprocess_return_code")
    if subprocess_return_code != 0:
        errors.append("execute-mode runtime evidence requires manifest.subprocess_return_code = 0")

    for field_name in ("started_at", "finished_at"):
        value = manifest.get(field_name)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"execute-mode runtime evidence requires manifest.{field_name}")

    build_summary = manifest.get("build_summary")
    if not isinstance(build_summary, dict) or not build_summary:
        errors.append("execute-mode runtime evidence requires a non-empty manifest.build_summary")
    elif build_summary.get("process_batch_id") != process_batch_id:
        errors.append("manifest.build_summary.process_batch_id must match manifest.process_batch_id")
    else:
        stable_summary_fields = [key for key in build_summary if key != "process_batch_id"]
        if not stable_summary_fields:
            errors.append(
                "execute-mode runtime evidence requires manifest.build_summary to contain at least one stable machine-readable field beyond process_batch_id"
            )

    if not stdout_path.exists():
        errors.append(f"missing execute-mode stdout log: {repo_relative(stdout_path)}")
    else:
        stdout_text = stdout_path.read_text(encoding="utf-8")
        if process_batch_id and f"process_batch_id={process_batch_id}" not in stdout_text:
            errors.append("execution_stdout.log does not contain the manifest.process_batch_id line")
        if f"Built {manifest['variable_id']}" not in stdout_text:
            errors.append("execution_stdout.log does not contain the expected built-variable confirmation line")

    if not stderr_path.exists():
        errors.append(f"missing execute-mode stderr log: {repo_relative(stderr_path)}")
    else:
        stderr_text = stderr_path.read_text(encoding="utf-8")
        if stderr_text.strip():
            errors.append("execution_stderr.log should be empty for the current passing execute-mode runtime evidence")

    errors.extend(validate_output_artifacts(manifest, workspace_root))
    return errors


def validate_runtime_dir(runtime_dir: Path, workspace_root: Path | None = None) -> list[str]:
    workspace_root = workspace_root or DEFAULT_WORKSPACE_ROOT.resolve()
    errors: list[str] = []
    validation_path = runtime_dir / "validation_report.json"
    manifest_path = runtime_dir / "manifest.json"

    for path in (validation_path, manifest_path):
        if not path.exists():
            errors.append(f"missing required runtime evidence file: {repo_relative(path)}")
    if errors:
        return errors

    try:
        validation_report = load_json(validation_path)
    except json.JSONDecodeError as exc:
        return [f"{repo_relative(validation_path)} is not valid JSON: {exc}"]
    try:
        manifest = load_json(manifest_path)
    except json.JSONDecodeError as exc:
        return [f"{repo_relative(manifest_path)} is not valid JSON: {exc}"]

    errors.extend(validate_required_fields(validation_report, REQUIRED_VALIDATION_REPORT_FIELDS, "validation_report"))
    errors.extend(validate_required_fields(manifest, REQUIRED_MANIFEST_FIELDS, "manifest"))
    if errors:
        return errors

    if validation_report["artifact_type"] != "validation_report":
        errors.append("validation_report.artifact_type must be `validation_report`")
    if manifest["artifact_type"] != "execution_manifest":
        errors.append("manifest.artifact_type must be `execution_manifest`")
    if validation_report["contract_ref"] != CONTRACT_REF:
        errors.append("validation_report.contract_ref does not point to the current runtime-evidence contract")
    if manifest["contract_ref"] != CONTRACT_REF:
        errors.append("manifest.contract_ref does not point to the current runtime-evidence contract")
    if manifest["execution_mode"] not in ALLOWED_EXECUTION_MODES:
        errors.append(f"manifest.execution_mode must be one of {sorted(ALLOWED_EXECUTION_MODES)}")
    if manifest["validation_status"] not in ALLOWED_VALIDATION_STATUSES:
        errors.append(f"manifest.validation_status must be one of {sorted(ALLOWED_VALIDATION_STATUSES)}")

    shared_fields = (
        "variable_id",
        "database_id",
        "variable_spec_path",
        "mapping_spec_path",
    )
    for field_name in shared_fields:
        if validation_report[field_name] != manifest[field_name]:
            errors.append(f"validation_report.{field_name} does not match manifest.{field_name}")
    if validation_report["overall_status"] != manifest["validation_status"]:
        errors.append("validation_report.overall_status does not match manifest.validation_status")

    errors.extend(validate_checks_block(validation_report))
    errors.extend(validate_repo_relative_path(validation_report["variable_spec_path"], "validation_report.variable_spec_path"))
    errors.extend(validate_repo_relative_path(validation_report["mapping_spec_path"], "validation_report.mapping_spec_path"))
    errors.extend(validate_repo_relative_path(manifest["execution_entrypoint_path"], "manifest.execution_entrypoint_path"))
    errors.extend(validate_workspace_relative_path(manifest["reference_implementation_path"], "manifest.reference_implementation_path", workspace_root))
    errors.extend(validate_workspace_relative_path(manifest["local_input_asset_path"], "manifest.local_input_asset_path", workspace_root))
    errors.extend(validate_spec_hashes(validation_report, manifest))
    errors.extend(validate_manifest_command(manifest))

    for text_path in (validation_path, manifest_path, runtime_dir / "execution_stdout.log", runtime_dir / "execution_stderr.log"):
        if text_path.exists():
            errors.extend(validate_no_machine_bound_absolute_paths(text_path))

    if manifest["execution_mode"] == "execute":
        errors.extend(validate_execute_mode(runtime_dir, manifest, validation_report, workspace_root))
    return errors


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate public standard-system runtime evidence artifacts."
    )
    parser.add_argument(
        "--runtime-dir",
        action="append",
        default=[],
        help="One runtime evidence directory to validate. May be passed multiple times.",
    )
    parser.add_argument(
        "--workspace-root",
        help="Optional workspace root containing Github/ and Methods/ as sibling directories.",
    )
    parser.add_argument(
        "--all-runtime-dirs",
        action="store_true",
        help="Validate all runtime evidence directories under docs/standard_system_mvp/*/runtime/*.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    workspace_root = Path(args.workspace_root).resolve() if args.workspace_root else DEFAULT_WORKSPACE_ROOT.resolve()

    runtime_dirs = [Path(item).resolve() for item in args.runtime_dir]
    if args.all_runtime_dirs or not runtime_dirs:
        runtime_dirs = find_runtime_dirs()
    if not runtime_dirs:
        raise SystemExit("no runtime directories found to validate")

    all_errors: list[str] = []
    for runtime_dir in runtime_dirs:
        errors = validate_runtime_dir(runtime_dir, workspace_root=workspace_root)
        print(f"Runtime directory: {runtime_dir}")
        if errors:
            for error in errors:
                print(f"- {error}")
            all_errors.extend(errors)
        else:
            print("- validation passed")

    return 1 if all_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
