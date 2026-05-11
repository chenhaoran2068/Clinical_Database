from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_POLICY_PATH = REPO_ROOT / "docs" / "layer3_directory_policy.json"
DEFAULT_CATALOG_PATH = REPO_ROOT / "docs" / "database_catalog.json"
DEFAULT_SCAN_ROOTS = (
    REPO_ROOT / "docs" / "standard_system_mvp",
    REPO_ROOT / "scripts",
)
TEXT_FILE_SUFFIXES = {".json", ".md", ".py", ".txt", ".yml", ".yaml"}
LAYER3_PATH_PATTERN = re.compile(
    r"Methods/Clinical_Database/local_work/Layer 3/(?P<suffix>[^`\"'\]\)\}\r\n,]+)"
)


def slugify(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_").lower()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def catalog_database_ids(catalog_path: Path) -> set[str]:
    catalog = load_json(catalog_path)
    databases = catalog.get("databases", [])
    if not isinstance(databases, list):
        raise ValueError(f"catalog databases field must be a list: {catalog_path}")
    ids: set[str] = set()
    for record in databases:
        if isinstance(record, dict) and isinstance(record.get("database_id"), str):
            ids.add(record["database_id"])
    return ids


def infer_database_id(path: Path, text: str, database_ids: set[str]) -> str | None:
    if path.suffix.lower() == ".json":
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            payload = None
        if isinstance(payload, dict):
            direct = payload.get("database_id")
            if isinstance(direct, str) and direct in database_ids:
                return direct
            database_mapping = payload.get("database_mapping")
            if isinstance(database_mapping, dict):
                mapped = database_mapping.get("database_id")
                if isinstance(mapped, str) and mapped in database_ids:
                    return mapped

    database_match = re.search(r'"database_id"\s*:\s*"([^"]+)"', text)
    if database_match and database_match.group(1) in database_ids:
        return database_match.group(1)

    relative_text = path.as_posix().lower()
    for database_id in database_ids:
        if slugify(database_id) in relative_text:
            return database_id
    return None


def normalize_layer3_suffix(raw_suffix: str) -> str:
    suffix = raw_suffix.replace("\\", "/").strip()
    while suffix and suffix[-1] in ".;:":
        suffix = suffix[:-1]
    return suffix.strip("/")


def path_context_has_mimic(text: str, start: int, end: int) -> bool:
    window = text[max(0, start - 500) : min(len(text), end + 500)]
    return "MIMIC-IV-3.1" in window or "mimic_iv_3_1" in window.lower()


def validate_policy_shape(policy: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expected = {
        "artifact_type": "layer3_directory_policy",
        "contract_ref": "Framework_Guideline/Layer3_Directory_Contract.md",
    }
    for key, expected_value in expected.items():
        if policy.get(key) != expected_value:
            errors.append(f"docs/layer3_directory_policy.json {key} must be {expected_value!r}")
    if "canonical_layer3_asset_pattern" not in policy:
        errors.append("docs/layer3_directory_policy.json is missing canonical_layer3_asset_pattern")
    if policy.get("database_scoped_required_for_new_assets") is not True:
        errors.append("docs/layer3_directory_policy.json must require database-scoped new assets")
    legacy = policy.get("legacy_root_level_exception")
    if not isinstance(legacy, dict):
        errors.append("docs/layer3_directory_policy.json legacy_root_level_exception must be an object")
    elif legacy.get("status") != "legacy_do_not_extend":
        errors.append("docs/layer3_directory_policy.json legacy exception must be legacy_do_not_extend")
    return errors


def iter_scan_files(scan_roots: list[Path]) -> list[Path]:
    files: list[Path] = []
    for scan_root in scan_roots:
        if scan_root.is_file():
            if scan_root.suffix.lower() in TEXT_FILE_SUFFIXES:
                files.append(scan_root)
            continue
        if not scan_root.exists():
            continue
        for path in scan_root.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix.lower() not in TEXT_FILE_SUFFIXES:
                continue
            if ".git" in path.parts or "__pycache__" in path.parts:
                continue
            files.append(path)
    return sorted(set(files))


def validate_layer3_layout_policy(
    repo_root: Path = REPO_ROOT,
    policy_path: Path | None = None,
    catalog_path: Path | None = None,
    scan_roots: list[Path] | None = None,
    strict_legacy: bool = False,
) -> dict[str, Any]:
    policy_path = policy_path or repo_root / "docs" / "layer3_directory_policy.json"
    catalog_path = catalog_path or repo_root / "docs" / "database_catalog.json"
    scan_roots = scan_roots or [
        repo_root / "docs" / "standard_system_mvp",
        repo_root / "scripts",
    ]

    errors: list[str] = []
    warnings: list[str] = []
    summary = {
        "files_scanned": 0,
        "layer3_references_seen": 0,
        "template_references_skipped": 0,
        "database_scoped_references": 0,
        "legacy_mimic_root_references": 0,
        "unknown_root_references": 0,
    }

    if not policy_path.exists():
        errors.append(f"missing Layer 3 policy file: {policy_path.relative_to(repo_root)}")
        return {"errors": errors, "warnings": warnings, "summary": summary}
    if not catalog_path.exists():
        errors.append(f"missing database catalog file: {catalog_path.relative_to(repo_root)}")
        return {"errors": errors, "warnings": warnings, "summary": summary}

    policy = load_json(policy_path)
    errors.extend(validate_policy_shape(policy))
    database_ids = catalog_database_ids(catalog_path)
    legacy_database_ids = set(
        policy.get("legacy_root_level_exception", {}).get("allowed_database_ids", [])
    )

    scan_files = iter_scan_files(scan_roots)
    summary["files_scanned"] = len(scan_files)
    for path in scan_files:
        text = path.read_text(encoding="utf-8")
        inferred_database_id = infer_database_id(path, text, database_ids)
        relative_path = path.relative_to(repo_root).as_posix()
        legacy_file_context = any(
            legacy_id in text or slugify(legacy_id) in text.lower()
            for legacy_id in legacy_database_ids
        )

        for match in LAYER3_PATH_PATTERN.finditer(text):
            summary["layer3_references_seen"] += 1
            suffix = normalize_layer3_suffix(match.group("suffix"))
            if any(token in suffix for token in ("<", ">", "{", "}")) or "__" in suffix:
                summary["template_references_skipped"] += 1
                continue

            parts = [part for part in suffix.split("/") if part]
            if not parts:
                continue

            first_segment = parts[0]
            if first_segment in database_ids:
                summary["database_scoped_references"] += 1
                if inferred_database_id and inferred_database_id != first_segment and path.suffix.lower() == ".json":
                    errors.append(
                        f"{relative_path}: Layer 3 path database_id {first_segment!r} does not match "
                        f"the JSON database_id {inferred_database_id!r}"
                    )
                continue

            legacy_context = (
                inferred_database_id in legacy_database_ids
                or legacy_file_context
                or path_context_has_mimic(text, match.start(), match.end())
                or "mimic_iv_3_1" in relative_path.lower()
            )
            if legacy_context:
                summary["legacy_mimic_root_references"] += 1
                if strict_legacy:
                    errors.append(
                        f"{relative_path}: legacy root-level MIMIC Layer 3 reference is present: "
                        f"Methods/Clinical_Database/local_work/Layer 3/{suffix}"
                    )
                continue

            summary["unknown_root_references"] += 1
            message = (
                f"{relative_path}: non-database-scoped Layer 3 reference is not allowed for new assets: "
                f"Methods/Clinical_Database/local_work/Layer 3/{suffix}"
            )
            if inferred_database_id and inferred_database_id not in legacy_database_ids:
                errors.append(message)
            else:
                warnings.append(message)

    return {"errors": errors, "warnings": warnings, "summary": summary}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate public Layer 3 path references against the database-scoped layout policy."
    )
    parser.add_argument(
        "--policy",
        default=str(DEFAULT_POLICY_PATH),
        help="Path to docs/layer3_directory_policy.json.",
    )
    parser.add_argument(
        "--catalog",
        default=str(DEFAULT_CATALOG_PATH),
        help="Path to docs/database_catalog.json.",
    )
    parser.add_argument(
        "--scan-root",
        action="append",
        default=[],
        help="File or directory to scan. Defaults to docs/standard_system_mvp and scripts.",
    )
    parser.add_argument(
        "--strict-legacy",
        action="store_true",
        help="Fail even on known legacy MIMIC root-level Layer 3 references.",
    )
    parser.add_argument(
        "--show-warnings",
        action="store_true",
        help="Print warning-level unknown-context root references.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    scan_roots = [Path(value).resolve() for value in args.scan_root]
    if not scan_roots:
        scan_roots = [path.resolve() for path in DEFAULT_SCAN_ROOTS]

    result = validate_layer3_layout_policy(
        repo_root=REPO_ROOT,
        policy_path=Path(args.policy).resolve(),
        catalog_path=Path(args.catalog).resolve(),
        scan_roots=scan_roots,
        strict_legacy=args.strict_legacy,
    )
    errors = result["errors"]
    warnings = result["warnings"]
    summary = result["summary"]

    if errors:
        print("Layer 3 layout policy check failed:")
        for error in errors:
            print(f"- {error}")
        if warnings and args.show_warnings:
            print("Warnings:")
            for warning in warnings:
                print(f"- {warning}")
        return 1

    print("Layer 3 layout policy check passed.")
    print(f"Files scanned: {summary['files_scanned']}")
    print(f"Layer 3 references seen: {summary['layer3_references_seen']}")
    print(f"Database-scoped references: {summary['database_scoped_references']}")
    print(f"Legacy MIMIC root-level references: {summary['legacy_mimic_root_references']}")
    print(f"Template references skipped: {summary['template_references_skipped']}")
    print(f"Unknown-context root references: {summary['unknown_root_references']}")
    if warnings and args.show_warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"- {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
