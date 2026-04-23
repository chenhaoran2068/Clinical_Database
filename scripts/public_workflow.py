from __future__ import annotations

import argparse
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any

from export_public_metadata import (
    build_variable_coverage_snapshot,
    load_catalog,
    load_current_release_governance,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG_PATH = REPO_ROOT / "docs" / "database_catalog.json"
DEFAULT_MASTER_INDEX_PATH = (
    REPO_ROOT.parent.parent
    / "Methods"
    / "Clinical_Database"
    / "local_work"
    / "Layer 5"
    / "Global"
    / "Layer5_StdVariable_MasterIndex.xlsx"
)

SUPPORTED_BUILD_LAYER1_DATABASE_IDS = (
    "MIMIC-IV-3.1",
    "MIMIC-IV-ECHO-1.0",
    "AmsterdamUMCdb-1.0.2",
)


def catalog_records(path: Path) -> list[dict[str, Any]]:
    data = load_catalog(path)
    databases = data.get("databases", [])
    if not isinstance(databases, list):
        raise SystemExit(f"database catalog is malformed: {path}")
    return databases


def family_records(path: Path) -> list[dict[str, Any]]:
    data = load_catalog(path)
    families = data.get("families", [])
    if not isinstance(families, list):
        raise SystemExit(f"database catalog is malformed: {path}")
    return families


def find_database_record(path: Path, database_id: str) -> dict[str, Any]:
    for record in catalog_records(path):
        if record.get("database_id") == database_id:
            return record
    raise SystemExit(f"database_id not found in catalog: {database_id}")


def find_family_record(path: Path, family_id: str) -> dict[str, Any]:
    for record in family_records(path):
        if record.get("family_id") == family_id:
            return record
    raise SystemExit(f"family_id not found in catalog: {family_id}")


def count_public_cards() -> int:
    cards_dir = REPO_ROOT / "docs" / "std_variable_cards"
    return sum(1 for path in cards_dir.glob("*.md") if path.name.lower() != "readme.md")


def run_command(command: list[str], dry_run: bool) -> int:
    print("Command:", flush=True)
    print(shlex.join(command), flush=True)
    if dry_run:
        print("Dry-run only. Command not executed.")
        return 0
    completed = subprocess.run(command, check=False)
    return completed.returncode


def build_layer1_command(args: argparse.Namespace) -> list[str]:
    layer1_root = Path(args.layer1_root).resolve()
    python = sys.executable

    if args.database_id == "MIMIC-IV-3.1":
        if args.action == "unpack":
            command = [
                python,
                str(REPO_ROOT / "scripts" / "layer1" / "unpack_mimic_raw_original_to_raw_unpacked.py"),
                "--layer1-root",
                str(layer1_root),
            ]
            if args.overwrite:
                command.append("--overwrite")
            return command

        if args.action == "convert":
            command = [
                python,
                str(REPO_ROOT / "scripts" / "layer1" / "convert_mimic_raw_unpacked_to_parquet.py"),
                "--layer1-root",
                str(layer1_root),
                "--compression",
                args.compression,
            ]
            if args.overwrite:
                command.append("--overwrite")
            if args.modules:
                command.extend(["--modules", *args.modules])
            return command

    if args.database_id == "MIMIC-IV-ECHO-1.0":
        if args.action == "unpack":
            command = [
                python,
                str(REPO_ROOT / "scripts" / "layer1" / "unpack_mimic_echo_raw_original_to_raw_unpacked.py"),
                "--layer1-root",
                str(layer1_root),
            ]
            if args.overwrite:
                command.append("--overwrite")
            return command

        if args.action == "convert":
            command = [
                python,
                str(REPO_ROOT / "scripts" / "layer1" / "convert_mimic_echo_raw_unpacked_to_parquet.py"),
                "--layer1-root",
                str(layer1_root),
                "--compression",
                args.compression,
            ]
            if args.overwrite:
                command.append("--overwrite")
            return command

    if args.database_id == "AmsterdamUMCdb-1.0.2" and args.action == "convert":
        command = [
            python,
            str(REPO_ROOT / "scripts" / "layer1" / "convert_amsterdam_raw_unpacked_to_parquet.py"),
            "--input-dir",
            str(layer1_root / "raw_unpacked"),
            "--output-dir",
            str(layer1_root / "local_converted_parquet"),
            "--compression",
            args.compression,
            "--encoding",
            args.encoding,
        ]
        if args.overwrite:
            command.append("--overwrite")
        return command

    raise SystemExit(
        f"Unsupported Layer 1 workflow for database_id={args.database_id!r}, action={args.action!r}"
    )


def command_status(args: argparse.Namespace) -> int:
    catalog_path = Path(args.catalog).resolve() if args.catalog else DEFAULT_CATALOG_PATH
    if not catalog_path.exists():
        raise SystemExit(f"catalog not found: {catalog_path}")

    data = load_catalog(catalog_path)
    release_governance = load_current_release_governance()
    coverage = build_variable_coverage_snapshot(data)
    databases = data.get("databases", [])
    families = data.get("families", [])

    if args.family_id:
        family = find_family_record(catalog_path, args.family_id)
        family_coverage = next(
            (
                item
                for item in coverage["family_coverage"]
                if item["family_id"] == args.family_id
            ),
            None,
        )
        print("Clinical_Database public repository family status")
        print(f"Catalog: {catalog_path}")
        print(f"Catalog version: {data.get('catalog_version', 'unknown')}")
        print(f"Release version: {release_governance['release_version']}")
        print(f"Release tag: {release_governance['release_tag']}")
        print(f"Family: {family['family_id']}")
        print(f"Display name: {family.get('display_name', '')}")
        print(f"Public family playbook: {family.get('public_family_playbook', '')}")
        if family_coverage:
            print(f"Family union public-card count: {family_coverage['family_union_public_card_count']}")
            print(f"Family shared public-card count: {family_coverage['family_shared_public_card_count']}")
        print("")
        print("Current members:")
        filtered = [record for record in databases if record.get("family_id") == args.family_id]
        for record in filtered:
            database_coverage = next(
                (
                    item
                    for item in coverage["database_coverage"]
                    if item["database_id"] == record["database_id"]
                ),
                {"public_card_count": 0},
            )
            print(f"- {record['database_id']} ({record.get('module_role', '')}, v{record.get('version', '')})")
            print(f"  layer1: {record.get('public_layer1_support_status', '')}")
            print(f"  layer4: {record.get('public_layer4_support_status', '')}")
            print(f"  layer5: {record.get('public_layer5_public_status', '')}")
            print(f"  public cards: {database_coverage['public_card_count']}")
        return 0

    if args.database_id:
        databases = [record for record in databases if record.get("database_id") == args.database_id]
    if not databases:
        raise SystemExit("no matching database record found")

    print("Clinical_Database public repository status")
    print(f"Catalog: {catalog_path}")
    print(f"Catalog version: {data.get('catalog_version', 'unknown')}")
    print(f"Release version: {release_governance['release_version']}")
    print(f"Release tag: {release_governance['release_tag']}")
    print(f"Release status: {release_governance['release_status']}")
    print(f"Family records: {len(families)}")
    print(f"Public std-variable cards: {count_public_cards()}")
    print(f"Cross-database public cards: {coverage['cross_database_public_card_count']}")
    print(f"Database records shown: {len(databases)}")
    print("")
    for record in databases:
        database_coverage = next(
            (
                item
                for item in coverage["database_coverage"]
                if item["database_id"] == record["database_id"]
            ),
            {"public_card_count": 0},
        )
        print(f"- {record['database_id']}")
        print(f"  display_name: {record.get('display_name', '')}")
        print(f"  family: {record.get('family_id', '')}")
        print(f"  role: {record.get('module_role', '')}")
        print(f"  version: {record.get('version', '')}")
        print(f"  layer1: {record.get('public_layer1_support_status', '')}")
        print(f"  layer4: {record.get('public_layer4_support_status', '')}")
        print(f"  layer5: {record.get('public_layer5_public_status', '')}")
        print(f"  public cards: {database_coverage['public_card_count']}")
    return 0


def command_build_layer1(args: argparse.Namespace) -> int:
    command = build_layer1_command(args)
    return run_command(command, args.dry_run)


def command_validate_registry(args: argparse.Namespace) -> int:
    command = [
        sys.executable,
        str(REPO_ROOT / "scripts" / "layer4" / "validate_policy_registry.py"),
        "--registry",
        str(Path(args.registry).resolve()),
    ]
    return run_command(command, args.dry_run)


def command_check_public_repository(args: argparse.Namespace) -> int:
    command = [
        sys.executable,
        str(REPO_ROOT / "scripts" / "check_public_repository.py"),
    ]
    return run_command(command, args.dry_run)


def command_check_local_id_semantics(args: argparse.Namespace) -> int:
    command = [
        sys.executable,
        str(REPO_ROOT / "scripts" / "layer5" / "check_local_id_semantics.py"),
        "--database-id",
        args.database_id,
    ]
    if args.workspace_root:
        command.extend(["--workspace-root", str(Path(args.workspace_root).resolve())])
    if args.database_root:
        command.extend(["--database-root", str(Path(args.database_root).resolve())])
    if args.include_non_approved:
        command.append("--include-non-approved")
    if args.warning_only:
        command.append("--warning-only")
    return run_command(command, args.dry_run)


def command_prepare_release(args: argparse.Namespace) -> int:
    command = [
        sys.executable,
        str(REPO_ROOT / "scripts" / "prepare_public_release.py"),
    ]
    if args.catalog:
        command.extend(["--catalog", str(Path(args.catalog).resolve())])
    if args.release_version:
        command.extend(["--release-version", args.release_version])
    if args.release_tag:
        command.extend(["--release-tag", args.release_tag])
    if args.release_label:
        command.extend(["--release-label", args.release_label])
    if args.release_status:
        command.extend(["--release-status", args.release_status])
    if args.release_date:
        command.extend(["--release-date", args.release_date])
    if args.current_changelog_entry_heading:
        command.extend(["--current-changelog-entry-heading", args.current_changelog_entry_heading])
    if args.release_notes_path:
        command.extend(["--release-notes-path", args.release_notes_path])
    for summary_line in args.summary_line:
        command.extend(["--summary-line", summary_line])
    if args.dry_run:
        command.append("--dry-run")
    return run_command(command, False)


def command_scaffold_public_database(args: argparse.Namespace) -> int:
    command = [
        sys.executable,
        str(REPO_ROOT / "scripts" / "scaffold_public_database.py"),
        "--database-id",
        args.database_id,
        "--family-id",
        args.family_id,
        "--module-role",
        args.module_role,
        "--version",
        args.version,
    ]
    if args.family_display_name:
        command.extend(["--family-display-name", args.family_display_name])
    if args.emit_catalog_snippets_dir:
        command.extend(["--emit-catalog-snippets-dir", str(Path(args.emit_catalog_snippets_dir).resolve())])
    if args.create_family_template_if_missing:
        command.append("--create-family-template-if-missing")
    if args.overwrite:
        command.append("--overwrite")
    if args.dry_run:
        command.append("--dry-run")
    return run_command(command, False)


def resolve_master_index_path(raw_path: str | None) -> Path:
    if raw_path:
        return Path(raw_path).resolve()
    if DEFAULT_MASTER_INDEX_PATH.exists():
        return DEFAULT_MASTER_INDEX_PATH
    raise SystemExit(
        "master index path not provided and default local-work path was not found. "
        "Pass --master-index explicitly."
    )


def command_export_public_artifacts(args: argparse.Namespace) -> int:
    if args.artifact == "variable-cards":
        if not args.std_variable_id and not args.all_reviewed_approved:
            raise SystemExit(
                "Choose one export scope: pass --std-variable-id or --all-reviewed-approved."
            )

        command = [
            sys.executable,
            str(REPO_ROOT / "scripts" / "layer5" / "export_public_variable_card.py"),
            "--master-index",
            str(resolve_master_index_path(args.master_index)),
        ]
        if args.std_variable_id:
            command.extend(["--std-variable-id", args.std_variable_id])
        if args.all_reviewed_approved:
            command.append("--all-reviewed-approved")
        if args.output:
            command.extend(["--output", str(Path(args.output).resolve())])
        if args.output_dir:
            command.extend(["--output-dir", str(Path(args.output_dir).resolve())])
        if args.cross_database:
            command.append("--cross-database")
        if args.only_missing:
            command.append("--only-missing")
        return run_command(command, args.dry_run)

    metadata_artifact_map = {
        "database-catalog": "database-catalog-json",
        "repository-status": "repository-status-json",
        "release-governance": "release-governance-json",
        "release-safe-manifest": "release-safe-manifest-json",
        "public-inventory": "public-inventory-markdown",
        "family-summary": "family-summary-markdown",
        "database-variable-coverage": "database-variable-coverage-json",
        "family-variable-coverage": "family-variable-coverage-json",
        "variable-coverage-summary": "variable-coverage-summary-markdown",
        "release-note": "release-note-markdown",
    }
    if args.artifact in metadata_artifact_map:
        command = [
            sys.executable,
            str(REPO_ROOT / "scripts" / "export_public_metadata.py"),
            "--artifact",
            metadata_artifact_map[args.artifact],
            "--catalog",
            str(DEFAULT_CATALOG_PATH),
        ]
        if args.family_id:
            command.extend(["--family-id", args.family_id])
        if args.output:
            command.extend(["--output", str(Path(args.output).resolve())])
        return run_command(command, args.dry_run)

    raise SystemExit(f"Unsupported artifact type: {args.artifact}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Public entrypoints for the Clinical_Database method repository."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    status_parser = subparsers.add_parser(
        "status",
        help="Show current public repository status from the database catalog.",
    )
    status_parser.add_argument(
        "--catalog",
        help="Optional path to a database catalog JSON file.",
    )
    status_parser.add_argument(
        "--database-id",
        help="Optional database_id filter.",
    )
    status_parser.add_argument(
        "--family-id",
        help="Optional family_id summary filter.",
    )
    status_parser.set_defaults(handler=command_status)

    build_parser_obj = subparsers.add_parser(
        "build-layer1",
        help="Run a public Layer 1 staging or conversion workflow for a supported database.",
    )
    build_parser_obj.add_argument(
        "--database-id",
        required=True,
        choices=SUPPORTED_BUILD_LAYER1_DATABASE_IDS,
        help="Database or module to build.",
    )
    build_parser_obj.add_argument(
        "--action",
        required=True,
        choices=("unpack", "convert"),
        help="Layer 1 action to run.",
    )
    build_parser_obj.add_argument(
        "--layer1-root",
        required=True,
        help="Path to the local-work Layer 1 database root.",
    )
    build_parser_obj.add_argument(
        "--compression",
        default="zstd",
        help="Compression to forward to conversion scripts when applicable.",
    )
    build_parser_obj.add_argument(
        "--encoding",
        default="auto",
        help="Encoding to forward to the Amsterdam converter when applicable.",
    )
    build_parser_obj.add_argument(
        "--modules",
        nargs="+",
        choices=("hosp", "icu", "ed", "note"),
        help="Optional MIMIC module subset for convert.",
    )
    build_parser_obj.add_argument(
        "--overwrite",
        action="store_true",
        help="Forward overwrite behavior to the underlying script.",
    )
    build_parser_obj.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the underlying command without executing it.",
    )
    build_parser_obj.set_defaults(handler=command_build_layer1)

    validate_parser = subparsers.add_parser(
        "validate-registry",
        help="Run the public Layer 4 policy-registry validator.",
    )
    validate_parser.add_argument(
        "--registry",
        required=True,
        help="Path to the policy registry JSON file.",
    )
    validate_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the underlying command without executing it.",
    )
    validate_parser.set_defaults(handler=command_validate_registry)

    check_parser = subparsers.add_parser(
        "check-public-repository",
        help="Run the public repository structural checker.",
    )
    check_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the underlying command without executing it.",
    )
    check_parser.set_defaults(handler=command_check_public_repository)

    local_id_parser = subparsers.add_parser(
        "check-local-id-semantics",
        help="Run a lightweight local Layer 5 ID-normalization wording check.",
    )
    local_id_parser.add_argument(
        "--database-id",
        required=True,
        help="Database id whose local Layer 5 assets should be inspected.",
    )
    local_id_parser.add_argument(
        "--workspace-root",
        help="Optional workspace root containing Methods/Clinical_Database/local_work/Layer 5.",
    )
    local_id_parser.add_argument(
        "--database-root",
        help="Optional direct path to the local Layer 5 database root.",
    )
    local_id_parser.add_argument(
        "--include-non-approved",
        action="store_true",
        help="Also inspect non-approved assets.",
    )
    local_id_parser.add_argument(
        "--warning-only",
        action="store_true",
        help="Print findings without failing the command.",
    )
    local_id_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the underlying command without executing it.",
    )
    local_id_parser.set_defaults(handler=command_check_local_id_semantics)

    prepare_release_parser = subparsers.add_parser(
        "prepare-release",
        help="Prepare the release-facing public outputs together.",
    )
    prepare_release_parser.add_argument("--catalog", help="Optional database catalog path.")
    prepare_release_parser.add_argument("--release-version", help="Target release_version.")
    prepare_release_parser.add_argument("--release-tag", help="Target release_tag.")
    prepare_release_parser.add_argument("--release-label", help="Target release_label.")
    prepare_release_parser.add_argument("--release-status", help="Target release_status.")
    prepare_release_parser.add_argument("--release-date", help="Target release_date.")
    prepare_release_parser.add_argument(
        "--current-changelog-entry-heading",
        help="Explicit changelog heading.",
    )
    prepare_release_parser.add_argument(
        "--release-notes-path",
        help="Optional repo-relative release notes path.",
    )
    prepare_release_parser.add_argument(
        "--summary-line",
        action="append",
        default=[],
        help="Optional summary bullet to prepend if a new changelog entry is needed.",
    )
    prepare_release_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the release preparation plan without writing files.",
    )
    prepare_release_parser.set_defaults(handler=command_prepare_release)

    scaffold_parser = subparsers.add_parser(
        "scaffold-public-database",
        help="Scaffold a public Layer 1 skeleton and onboarding draft for a new database, with optional family-draft and catalog-snippet outputs.",
    )
    scaffold_parser.add_argument("--database-id", required=True, help="New database_id to scaffold.")
    scaffold_parser.add_argument("--family-id", required=True, help="Family ID.")
    scaffold_parser.add_argument(
        "--family-display-name",
        help="Optional family display name if a new family template should be created.",
    )
    scaffold_parser.add_argument(
        "--module-role",
        default="core_database",
        help="Module role such as core_database or sibling_module.",
    )
    scaffold_parser.add_argument("--version", required=True, help="Version string.")
    scaffold_parser.add_argument(
        "--emit-catalog-snippets-dir",
        help="Optional output directory for draft catalog snippets.",
    )
    scaffold_parser.add_argument(
        "--create-family-template-if-missing",
        action="store_true",
        help="Create a family onboarding draft if it does not exist.",
    )
    scaffold_parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite scaffolded files if they already exist.",
    )
    scaffold_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the planned scaffold without writing files.",
    )
    scaffold_parser.set_defaults(handler=command_scaffold_public_database)

    export_parser = subparsers.add_parser(
        "export-public-artifacts",
        help="Export the current GitHub-safe publication artifact set.",
    )
    export_parser.add_argument(
        "--artifact",
        default="variable-cards",
        choices=(
            "variable-cards",
            "database-catalog",
            "repository-status",
            "release-governance",
            "release-safe-manifest",
            "public-inventory",
            "family-summary",
            "database-variable-coverage",
            "family-variable-coverage",
            "variable-coverage-summary",
            "release-note",
        ),
        help="Public artifact type to export. Current default: variable-cards.",
    )
    export_parser.add_argument(
        "--master-index",
        help="Path to the Layer 5 master index workbook. If omitted, the conventional local-work path is tried.",
    )
    export_parser.add_argument(
        "--std-variable-id",
        help="Single std_variable_id to export.",
    )
    export_parser.add_argument(
        "--family-id",
        help="Required for family-summary exports.",
    )
    export_parser.add_argument(
        "--all-reviewed-approved",
        action="store_true",
        help="Export all reviewed-approved public cards.",
    )
    export_parser.add_argument(
        "--output",
        help="Optional output path for a single card or metadata export.",
    )
    export_parser.add_argument(
        "--output-dir",
        help="Optional output directory for batch card exports.",
    )
    export_parser.add_argument(
        "--cross-database",
        action="store_true",
        help="Prefer cross-database approved assets when multiple assets exist.",
    )
    export_parser.add_argument(
        "--only-missing",
        action="store_true",
        help="Skip files that already exist in the output directory during batch export.",
    )
    export_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the underlying command without executing it.",
    )
    export_parser.set_defaults(handler=command_export_public_artifacts)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
