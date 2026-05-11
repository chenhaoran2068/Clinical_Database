from __future__ import annotations

import argparse
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from validate_standard_system_runtime import (
    CONTRACT_REF,
    DEFAULT_WORKSPACE_ROOT,
    MACHINE_BOUND_ABSOLUTE_PATH_PATTERN,
    classify_output_artifact,
    load_json,
    repo_relative,
    validate_runtime_dir,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
ALLOWED_REPORT_STATUSES = {"pass", "fail"}
REQUIRED_REPORT_FIELDS: dict[str, type[Any]] = {
    "artifact_type": str,
    "artifact_version": str,
    "contract_ref": str,
    "generated_at": str,
    "comparison_scope": str,
    "overall_status": str,
    "variable_id": str,
    "database_id": str,
    "baseline_runtime_dir": str,
    "candidate_runtime_dir": str,
    "baseline_process_batch_id": str,
    "candidate_process_batch_id": str,
    "artifact_role_policy": dict,
    "stable_build_summary_fields": list,
    "checks": list,
    "artifact_comparisons": dict,
    "build_summary_comparisons": dict,
}
BUILD_SUMMARY_IGNORED_FIELDS = {"process_batch_id", "build_log_path"}
NUMERIC_BUILD_SUMMARY_ABS_TOLERANCE = 1e-6
NUMERIC_BUILD_SUMMARY_REL_TOLERANCE = 1e-12


def now_utc_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


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


def find_reproducibility_reports() -> list[Path]:
    reports: list[Path] = []
    runtime_root = REPO_ROOT / "docs" / "standard_system_mvp"
    if not runtime_root.exists():
        return reports
    for path in runtime_root.glob("*/runtime/*/reproducibility_report.json"):
        if path.is_file():
            reports.append(path)
    return sorted(reports, key=lambda item: repo_relative(item))


def load_runtime_manifest(runtime_dir: Path) -> dict[str, Any]:
    return load_json(runtime_dir / "manifest.json")


def build_artifact_role_policy(output_artifacts: dict[str, Any]) -> dict[str, list[str]]:
    policy = {
        "rerun_invariant_artifact_keys": [],
        "latest_state_mutable_artifact_keys": [],
        "run_scoped_append_only_artifact_keys": [],
    }
    for artifact_name in sorted(output_artifacts):
        role = classify_output_artifact(artifact_name)
        if role == "latest_state_mutable":
            policy["latest_state_mutable_artifact_keys"].append(artifact_name)
        elif role == "run_scoped_append_only":
            policy["run_scoped_append_only_artifact_keys"].append(artifact_name)
        else:
            policy["rerun_invariant_artifact_keys"].append(artifact_name)
    return policy


def stable_build_summary_fields(build_summary: dict[str, Any]) -> list[str]:
    return sorted(
        key for key in build_summary
        if key not in BUILD_SUMMARY_IGNORED_FIELDS
    )


def build_summary_values_equivalent(left: Any, right: Any) -> bool:
    if isinstance(left, bool) or isinstance(right, bool):
        return left == right
    if isinstance(left, (int, float)) and isinstance(right, (int, float)):
        return math.isclose(
            float(left),
            float(right),
            rel_tol=NUMERIC_BUILD_SUMMARY_REL_TOLERANCE,
            abs_tol=NUMERIC_BUILD_SUMMARY_ABS_TOLERANCE,
        )
    if isinstance(left, dict) and isinstance(right, dict):
        return (
            set(left) == set(right)
            and all(build_summary_values_equivalent(left[key], right[key]) for key in left)
        )
    if isinstance(left, list) and isinstance(right, list):
        return (
            len(left) == len(right)
            and all(build_summary_values_equivalent(item_left, item_right) for item_left, item_right in zip(left, right))
        )
    return left == right


def compare_runtime_dirs(
    *,
    baseline_runtime_dir: Path,
    candidate_runtime_dir: Path,
    workspace_root: Path,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    artifact_comparisons: dict[str, Any] = {}
    build_summary_comparisons: dict[str, Any] = {}

    baseline_errors = validate_runtime_dir(baseline_runtime_dir, workspace_root=workspace_root)
    candidate_errors = validate_runtime_dir(candidate_runtime_dir, workspace_root=workspace_root)
    add_check(
        checks,
        "baseline_runtime_validation",
        not baseline_errors,
        f"baseline runtime directory passes runtime validation: {repo_relative(baseline_runtime_dir)}",
        "baseline runtime directory failed runtime validation: " + "; ".join(baseline_errors),
    )
    add_check(
        checks,
        "candidate_runtime_validation",
        not candidate_errors,
        f"candidate runtime directory passes runtime validation: {repo_relative(candidate_runtime_dir)}",
        "candidate runtime directory failed runtime validation: " + "; ".join(candidate_errors),
    )

    baseline_manifest = load_runtime_manifest(baseline_runtime_dir)
    candidate_manifest = load_runtime_manifest(candidate_runtime_dir)
    baseline_build_summary = baseline_manifest.get("build_summary", {})
    candidate_build_summary = candidate_manifest.get("build_summary", {})
    policy = build_artifact_role_policy(candidate_manifest.get("output_artifacts", {}))

    equality_fields = (
        "variable_id",
        "database_id",
        "variable_spec_path",
        "mapping_spec_path",
        "execution_entrypoint_path",
        "reference_implementation_path",
        "local_input_asset_path",
        "command",
        "spec_hashes",
    )
    for field_name in equality_fields:
        add_check(
            checks,
            f"{field_name}_match",
            baseline_manifest.get(field_name) == candidate_manifest.get(field_name),
            f"{field_name} matches across baseline and candidate runtime evidence",
            f"{field_name} differs across baseline and candidate runtime evidence",
        )

    add_check(
        checks,
        "process_batch_id_distinct",
        baseline_manifest.get("process_batch_id") != candidate_manifest.get("process_batch_id"),
        "baseline and candidate process_batch_id are distinct as expected for a rerun",
        "baseline and candidate process_batch_id should differ for a rerun comparison",
    )

    baseline_artifacts = baseline_manifest.get("output_artifacts", {})
    candidate_artifacts = candidate_manifest.get("output_artifacts", {})
    add_check(
        checks,
        "output_artifact_keys_match",
        set(baseline_artifacts) == set(candidate_artifacts),
        "baseline and candidate output artifact keys match",
        "baseline and candidate output artifact keys do not match",
    )

    for artifact_name in sorted(set(baseline_artifacts) | set(candidate_artifacts)):
        baseline_path = baseline_artifacts.get(artifact_name)
        candidate_path = candidate_artifacts.get(artifact_name)
        baseline_signature = baseline_manifest.get("output_signatures", {}).get(artifact_name, {})
        candidate_signature = candidate_manifest.get("output_signatures", {}).get(artifact_name, {})
        role = classify_output_artifact(artifact_name)

        path_match = baseline_path == candidate_path
        signature_match = baseline_signature == candidate_signature
        comparison_status = "pass"
        comparison_note = ""
        if role == "rerun_invariant":
            comparison_status = "pass" if path_match and signature_match else "fail"
            comparison_note = "rerun-invariant artifact should keep the same path and signature across reruns"
        elif role == "latest_state_mutable":
            comparison_status = "pass" if path_match else "fail"
            comparison_note = "latest-state mutable artifact may change content across reruns but should keep the same live path"
        elif role == "run_scoped_append_only":
            comparison_status = "pass" if isinstance(baseline_path, str) and isinstance(candidate_path, str) and baseline_path != candidate_path else "fail"
            comparison_note = "run-scoped append-only artifact should usually differ by process_batch_id across reruns"

        artifact_comparisons[artifact_name] = {
            "artifact_role": role,
            "status": comparison_status,
            "baseline_path": baseline_path,
            "candidate_path": candidate_path,
            "baseline_signature": baseline_signature,
            "candidate_signature": candidate_signature,
            "comparison_note": comparison_note,
        }
        add_check(
            checks,
            f"{artifact_name}_{role}_comparison",
            comparison_status == "pass",
            f"{artifact_name} satisfies the {role} comparison rule",
            f"{artifact_name} failed the {role} comparison rule",
        )

    baseline_fields = stable_build_summary_fields(baseline_build_summary)
    candidate_fields = stable_build_summary_fields(candidate_build_summary)
    add_check(
        checks,
        "stable_build_summary_field_set_match",
        baseline_fields == candidate_fields,
        "stable build_summary field sets match",
        "stable build_summary field sets do not match",
    )
    shared_fields = sorted(set(baseline_fields) & set(candidate_fields))
    for field_name in shared_fields:
        baseline_value = baseline_build_summary.get(field_name)
        candidate_value = candidate_build_summary.get(field_name)
        status = "pass" if build_summary_values_equivalent(baseline_value, candidate_value) else "fail"
        build_summary_comparisons[field_name] = {
            "status": status,
            "baseline_value": baseline_value,
            "candidate_value": candidate_value,
        }
        add_check(
            checks,
            f"build_summary_{field_name}_match",
            status == "pass",
            f"build_summary field {field_name} matches across reruns",
            f"build_summary field {field_name} differs across reruns",
        )

    overall_status = "pass" if all(item["status"] == "pass" for item in checks) else "fail"
    return {
        "artifact_type": "reproducibility_report",
        "artifact_version": "v0_draft",
        "contract_ref": CONTRACT_REF,
        "generated_at": now_utc_iso(),
        "comparison_scope": "rerun_reproducibility_gate",
        "overall_status": overall_status,
        "variable_id": candidate_manifest["variable_id"],
        "database_id": candidate_manifest["database_id"],
        "baseline_runtime_dir": repo_relative(baseline_runtime_dir),
        "candidate_runtime_dir": repo_relative(candidate_runtime_dir),
        "baseline_process_batch_id": baseline_manifest["process_batch_id"],
        "candidate_process_batch_id": candidate_manifest["process_batch_id"],
        "artifact_role_policy": policy,
        "stable_build_summary_fields": shared_fields,
        "checks": checks,
        "artifact_comparisons": artifact_comparisons,
        "build_summary_comparisons": build_summary_comparisons,
    }


def write_report(path: Path, report: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def validate_required_fields(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field_name, expected_type in REQUIRED_REPORT_FIELDS.items():
        value = record.get(field_name)
        if not isinstance(value, expected_type):
            actual_type = type(value).__name__
            errors.append(f"reproducibility_report.{field_name} expected {expected_type.__name__}, got {actual_type}")
    return errors


def validate_reproducibility_report(
    report_path: Path,
    workspace_root: Path | None = None,
) -> list[str]:
    workspace_root = workspace_root or DEFAULT_WORKSPACE_ROOT.resolve()
    try:
        report = load_json(report_path)
    except json.JSONDecodeError as exc:
        return [f"{repo_relative(report_path)} is not valid JSON: {exc}"]

    errors = validate_required_fields(report)
    if errors:
        return errors

    if report["artifact_type"] != "reproducibility_report":
        errors.append("reproducibility_report.artifact_type must be `reproducibility_report`")
    if report["contract_ref"] != CONTRACT_REF:
        errors.append("reproducibility_report.contract_ref does not point to the runtime-evidence contract")
    if report["overall_status"] not in ALLOWED_REPORT_STATUSES:
        errors.append(f"reproducibility_report.overall_status must be one of {sorted(ALLOWED_REPORT_STATUSES)}")

    for field_name in ("baseline_runtime_dir", "candidate_runtime_dir"):
        raw_path = report[field_name]
        path = Path(raw_path)
        if path.is_absolute():
            errors.append(f"{field_name} must be repo-relative, got absolute path: {raw_path}")
            continue
        target = REPO_ROOT / path
        if not target.exists():
            errors.append(f"{field_name} points to a missing runtime directory: {raw_path}")
        else:
            errors.extend(validate_runtime_dir(target, workspace_root=workspace_root))

    checks = report["checks"]
    if not checks:
        errors.append("reproducibility_report.checks must be a non-empty list")
    else:
        all_pass = True
        for index, item in enumerate(checks, start=1):
            if not isinstance(item, dict):
                errors.append(f"reproducibility_report.checks[{index}] must be an object")
                continue
            for required_key in ("check_id", "status", "message"):
                value = item.get(required_key)
                if not isinstance(value, str) or not value.strip():
                    errors.append(f"reproducibility_report.checks[{index}].{required_key} must be a non-empty string")
            if item.get("status") not in ALLOWED_REPORT_STATUSES:
                errors.append(f"reproducibility_report.checks[{index}].status must be one of {sorted(ALLOWED_REPORT_STATUSES)}")
            if item.get("status") != "pass":
                all_pass = False
        if report["overall_status"] == "pass" and not all_pass:
            errors.append("reproducibility_report.overall_status is pass but not all checks passed")

    text = report_path.read_text(encoding="utf-8")
    match = MACHINE_BOUND_ABSOLUTE_PATH_PATTERN.search(text)
    if match:
        errors.append(f"{repo_relative(report_path)} contains a machine-bound absolute path example: {match.group(0)!r}")

    baseline_runtime_dir = REPO_ROOT / report["baseline_runtime_dir"]
    candidate_runtime_dir = REPO_ROOT / report["candidate_runtime_dir"]
    if baseline_runtime_dir.exists():
        baseline_manifest = load_runtime_manifest(baseline_runtime_dir)
        if baseline_manifest["process_batch_id"] != report["baseline_process_batch_id"]:
            errors.append("baseline_process_batch_id does not match the current baseline manifest")
    if candidate_runtime_dir.exists():
        candidate_manifest = load_runtime_manifest(candidate_runtime_dir)
        if candidate_manifest["process_batch_id"] != report["candidate_process_batch_id"]:
            errors.append("candidate_process_batch_id does not match the current candidate manifest")
        if candidate_manifest["variable_id"] != report["variable_id"]:
            errors.append("reproducibility_report.variable_id does not match the candidate manifest")
        if candidate_manifest["database_id"] != report["database_id"]:
            errors.append("reproducibility_report.database_id does not match the candidate manifest")
    return errors


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate or validate standard-system rerun reproducibility reports."
    )
    parser.add_argument("--baseline-runtime-dir", help="Repo path or absolute path to the baseline runtime directory.")
    parser.add_argument("--candidate-runtime-dir", help="Repo path or absolute path to the candidate rerun runtime directory.")
    parser.add_argument("--output", help="Optional output path for reproducibility_report.json.")
    parser.add_argument("--workspace-root", help="Optional workspace root containing Github/ and Methods/ as sibling directories.")
    parser.add_argument("--report-path", action="append", default=[], help="One reproducibility_report.json path to validate.")
    parser.add_argument("--all-reports", action="store_true", help="Validate all reproducibility_report.json files under docs/standard_system_mvp/*/runtime/*/.")
    return parser


def resolve_path(raw_path: str) -> Path:
    path = Path(raw_path)
    return path.resolve() if path.is_absolute() else (REPO_ROOT / path).resolve()


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    workspace_root = Path(args.workspace_root).resolve() if args.workspace_root else DEFAULT_WORKSPACE_ROOT.resolve()

    if args.baseline_runtime_dir and args.candidate_runtime_dir:
        baseline_runtime_dir = resolve_path(args.baseline_runtime_dir)
        candidate_runtime_dir = resolve_path(args.candidate_runtime_dir)
        output_path = resolve_path(args.output) if args.output else (candidate_runtime_dir / "reproducibility_report.json")
        report = compare_runtime_dirs(
            baseline_runtime_dir=baseline_runtime_dir,
            candidate_runtime_dir=candidate_runtime_dir,
            workspace_root=workspace_root,
        )
        write_report(output_path, report)
        print(f"Wrote reproducibility report: {output_path}")
        print(f"overall_status={report['overall_status']}")
        return 0 if report["overall_status"] == "pass" else 1

    report_paths = [resolve_path(item) for item in args.report_path]
    if args.all_reports or not report_paths:
        report_paths = find_reproducibility_reports()
    if not report_paths:
        raise SystemExit("no reproducibility reports found to validate")

    all_errors: list[str] = []
    for report_path in report_paths:
        errors = validate_reproducibility_report(report_path, workspace_root=workspace_root)
        print(f"Reproducibility report: {report_path}")
        if errors:
            for error in errors:
                print(f"- {error}")
            all_errors.extend(errors)
        else:
            print("- validation passed")
    return 1 if all_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
