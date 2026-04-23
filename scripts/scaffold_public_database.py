from __future__ import annotations

import argparse
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
ONBOARDING_TEMPLATE_PATH = REPO_ROOT / "docs" / "onboarding" / "ONBOARDING_TEMPLATE.md"
FAMILY_TEMPLATE_PATH = REPO_ROOT / "docs" / "onboarding" / "families" / "FAMILY_TEMPLATE.md"


def build_layer1_bucket_status_csv(database_id: str) -> str:
    return "\n".join(
        [
            "bucket,status,notes",
            f"raw_original,pending_fill,Stage official source packages for {database_id} here.",
            f"raw_unpacked,pending_fill,Stage unpacked source files for {database_id} here.",
            "source_supplied_derived,pending_fill,Use only for provider-supplied derived source assets.",
            "local_converted_parquet,pending_fill,Git-ignored local source-faithful parquet conversions live here.",
        ]
    ) + "\n"


def build_docs_manifest_readme(database_id: str, family_id: str, version: str) -> str:
    return "\n".join(
        [
            f"# Layer 1 Skeleton: {database_id}",
            "",
            f"- family: `{family_id}`",
            f"- version: `{version}`",
            "",
            "This is the committed GitHub-safe Layer 1 skeleton.",
            "",
            "Expected buckets:",
            "",
            "- `raw_original/`",
            "- `raw_unpacked/`",
            "- `source_supplied_derived/`",
            "- `local_converted_parquet/`",
            "- `docs_manifest/`",
        ]
    ) + "\n"


def build_onboarding_doc(
    database_id: str,
    family_id: str,
    module_role: str,
    version: str,
) -> str:
    template = ONBOARDING_TEMPLATE_PATH.read_text(encoding="utf-8")
    return (
        template.replace("- database ID:", f"- database ID: `{database_id}`")
        .replace("- family:", f"- family: `{family_id}`")
        .replace("- module role:", f"- module role: `{module_role}`")
        .replace("- version:", f"- version: `{version}`")
    )


def build_family_doc(family_id: str, display_name: str) -> str:
    template = FAMILY_TEMPLATE_PATH.read_text(encoding="utf-8")
    return (
        template.replace("- family ID:", f"- family ID: `{family_id}`")
        .replace("- display name:", f"- display name: `{display_name}`")
    )


def plan_paths(
    database_id: str,
    family_id: str,
    *,
    include_family_template: bool,
    emit_catalog_snippets_dir: str | None,
) -> dict[Path, str]:
    layer1_root = REPO_ROOT / "Data" / "Layer 1" / database_id
    docs_manifest_root = layer1_root / "docs_manifest"
    planned: dict[Path, str] = {
        docs_manifest_root / "README.md": "",
        docs_manifest_root / "LAYER1_BUCKET_STATUS.csv": "",
        layer1_root / "raw_original" / ".gitkeep": "",
        layer1_root / "raw_unpacked" / ".gitkeep": "",
        layer1_root / "source_supplied_derived" / ".gitkeep": "",
        layer1_root / "local_converted_parquet" / ".gitkeep": "",
        REPO_ROOT / "docs" / "onboarding" / f"{database_id}.md": "",
    }
    if include_family_template:
        planned[REPO_ROOT / "docs" / "onboarding" / "families" / f"{family_id}.md"] = ""
    if emit_catalog_snippets_dir:
        output_dir = Path(emit_catalog_snippets_dir).resolve()
        planned[output_dir / f"{database_id}_database_row.json"] = ""
        if include_family_template:
            planned[output_dir / f"{family_id}_family_row.json"] = ""
    return planned


def write_if_missing(path: Path, content: str, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Scaffold the public-safe database onboarding surface for a new database or module. "
            "This writes a Layer 1 skeleton and onboarding draft by default, with optional family-draft "
            "and catalog-snippet outputs when explicitly requested."
        )
    )
    parser.add_argument("--database-id", required=True, help="New database_id to scaffold.")
    parser.add_argument("--family-id", required=True, help="Family ID for the new database.")
    parser.add_argument(
        "--family-display-name",
        default="",
        help="Optional family display name if a new family playbook draft should be created.",
    )
    parser.add_argument(
        "--module-role",
        default="core_database",
        help="Module role such as core_database or sibling_module.",
    )
    parser.add_argument("--version", required=True, help="Version string.")
    parser.add_argument(
        "--emit-catalog-snippets-dir",
        help="Optional output directory for draft catalog JSON snippets.",
    )
    parser.add_argument(
        "--create-family-template-if-missing",
        action="store_true",
        help="Create docs/onboarding/families/<family>.md when it does not already exist.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite generated scaffold files if they already exist.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show the planned paths without writing files.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    planned = plan_paths(
        args.database_id,
        args.family_id,
        include_family_template=args.create_family_template_if_missing,
        emit_catalog_snippets_dir=args.emit_catalog_snippets_dir,
    )
    family_path = REPO_ROOT / "docs" / "onboarding" / "families" / f"{args.family_id}.md"

    print("Public database scaffold plan")
    print(f"- database_id: {args.database_id}")
    print(f"- family_id: {args.family_id}")
    print(f"- module_role: {args.module_role}")
    print(f"- version: {args.version}")
    for path in planned:
        print(f"  - {path}")

    if args.dry_run:
        return 0

    layer1_root = REPO_ROOT / "Data" / "Layer 1" / args.database_id
    docs_manifest_root = layer1_root / "docs_manifest"

    write_if_missing(
        docs_manifest_root / "README.md",
        build_docs_manifest_readme(args.database_id, args.family_id, args.version),
        args.overwrite,
    )
    write_if_missing(
        docs_manifest_root / "LAYER1_BUCKET_STATUS.csv",
        build_layer1_bucket_status_csv(args.database_id),
        args.overwrite,
    )
    for bucket in (
        layer1_root / "raw_original" / ".gitkeep",
        layer1_root / "raw_unpacked" / ".gitkeep",
        layer1_root / "source_supplied_derived" / ".gitkeep",
        layer1_root / "local_converted_parquet" / ".gitkeep",
    ):
        write_if_missing(bucket, "", args.overwrite)

    write_if_missing(
        REPO_ROOT / "docs" / "onboarding" / f"{args.database_id}.md",
        build_onboarding_doc(args.database_id, args.family_id, args.module_role, args.version),
        args.overwrite,
    )

    if args.create_family_template_if_missing and (args.overwrite or not family_path.exists()):
        display_name = args.family_display_name or f"{args.family_id} family"
        write_if_missing(
            family_path,
            build_family_doc(args.family_id, display_name),
            args.overwrite,
        )

    if args.emit_catalog_snippets_dir:
        output_dir = Path(args.emit_catalog_snippets_dir).resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        database_row = {
            "database_id": args.database_id,
            "display_name": args.database_id,
            "family_id": args.family_id,
            "module_role": args.module_role,
            "version": args.version,
            "relationship_note": "TODO: fill relationship note",
            "public_layer1_skeleton_path": f"Data/Layer 1/{args.database_id}",
            "public_onboarding_playbook": f"docs/onboarding/{args.database_id}.md",
            "public_script_entrypoints": [
                "scripts/public_workflow.py",
            ],
            "special_semantics_contracts": [],
            "public_layer1_support_status": "published_skeleton_only_pending_scripts",
            "public_layer4_support_status": "not_yet_published",
            "public_layer5_public_status": "not_yet_published",
            "current_local_stage": "planning_only",
            "public_tutorials": [],
        }
        (output_dir / f"{args.database_id}_database_row.json").write_text(
            json.dumps(database_row, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        if args.create_family_template_if_missing:
            family_row = {
                "family_id": args.family_id,
                "display_name": args.family_display_name or f"{args.family_id} family",
                "description": "TODO: fill family description",
                "public_family_playbook": f"docs/onboarding/families/{args.family_id}.md",
                "current_database_ids": [args.database_id],
                "future_member_rule": "TODO: fill future member rule",
                "alignment_rule": "TODO: fill alignment rule",
            }
            (output_dir / f"{args.family_id}_family_row.json").write_text(
                json.dumps(family_row, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
        print(f"Wrote scaffold catalog snippets to: {output_dir}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
