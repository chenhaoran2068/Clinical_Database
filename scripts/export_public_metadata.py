from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG_PATH = REPO_ROOT / "docs" / "database_catalog.json"
DEFAULT_RELEASE_SAFE_MANIFEST_PATH = REPO_ROOT / "docs" / "release_safe_manifest.json"
DEFAULT_PUBLIC_INVENTORY_PATH = REPO_ROOT / "docs" / "PUBLIC_INVENTORY.md"
DEFAULT_RELEASE_CHANGELOG_PATH = REPO_ROOT / "docs" / "RELEASE_CHANGELOG.md"
DEFAULT_PUBLIC_EXPORTS_DIR = REPO_ROOT / "docs" / "public_exports"
DEFAULT_RELEASES_DIR = REPO_ROOT / "docs" / "releases"

DEFAULT_PUBLIC_EXPORT_PATHS = {
    "repository-status-json": DEFAULT_PUBLIC_EXPORTS_DIR / "repository_status.json",
    "database-variable-coverage-json": DEFAULT_PUBLIC_EXPORTS_DIR / "database_variable_coverage.json",
    "family-variable-coverage-json": DEFAULT_PUBLIC_EXPORTS_DIR / "family_variable_coverage.json",
    "variable-coverage-summary-markdown": DEFAULT_PUBLIC_EXPORTS_DIR / "variable_coverage_summary.md",
}

FALLBACK_RELEASE_GOVERNANCE: dict[str, str] = {
    "release_contract_version": "v1",
    "release_series_id": "clinical_database_public_method_repository",
    "release_version": "0.1.0-dev",
    "release_tag": "public-method-foundation-2026-04-21",
    "release_label": "public-method-repository-foundation",
    "release_status": "working_tree_snapshot",
    "release_date": "2026-04-21",
    "changelog_path": "docs/RELEASE_CHANGELOG.md",
    "current_changelog_entry_heading": "## 0.1.0-dev - 2026-04-21",
    "versioning_rule": (
        "Use semantic-version style release_version strings, with -dev or other suffixes "
        "allowed for non-stable lines."
    ),
    "release_update_rule": (
        "Whenever the public release boundary changes, update release_safe_manifest.json, "
        "PUBLIC_INVENTORY.md, RELEASE_CHANGELOG.md, the current generated public exports under "
        "docs/public_exports/, and the current release note under docs/releases/ in the same change set."
    ),
    "release_notes_path": "docs/releases/public-method-foundation-2026-04-21.md",
    "release_notes_rule": (
        "Each release tag should have one matching public release note under docs/releases/ "
        "that summarizes scope, coverage, and related generated exports."
    ),
    "release_gate_rule": (
        "A release-ready snapshot should pass scripts/check_public_repository.py and have a "
        "matching changelog heading before a stable tag or release note is published."
    ),
}

REQUIRED_PUBLIC_CARD_HEADINGS = (
    "## Identity",
    "## Cross-Database Status",
    "## Current Approved Database Assets",
    "## Publication Rule",
)


def load_catalog(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def family_records(data: dict[str, Any]) -> list[dict[str, Any]]:
    families = data.get("families", [])
    if not isinstance(families, list):
        raise SystemExit(f"catalog families section is malformed: {DEFAULT_CATALOG_PATH}")
    return families


def database_records(data: dict[str, Any]) -> list[dict[str, Any]]:
    databases = data.get("databases", [])
    if not isinstance(databases, list):
        raise SystemExit(f"catalog databases section is malformed: {DEFAULT_CATALOG_PATH}")
    return databases


def find_family_record(data: dict[str, Any], family_id: str) -> dict[str, Any]:
    for record in family_records(data):
        if record.get("family_id") == family_id:
            return record
    raise SystemExit(f"family_id not found in catalog: {family_id}")


def databases_for_family(data: dict[str, Any], family_id: str) -> list[dict[str, Any]]:
    return [record for record in database_records(data) if record.get("family_id") == family_id]


def repo_relative(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT)).replace("\\", "/")


def sorted_relative_paths(paths: list[Path]) -> list[str]:
    return [repo_relative(path) for path in sorted(paths, key=lambda item: repo_relative(item))]


def files_from_glob(pattern: str) -> list[str]:
    return sorted_relative_paths([path for path in REPO_ROOT.glob(pattern) if path.is_file()])


def files_from_recursive(root_relative: str) -> list[str]:
    root = REPO_ROOT / root_relative
    if not root.exists():
        return []
    return sorted_relative_paths([path for path in root.rglob("*") if path.is_file()])


def public_card_paths() -> list[Path]:
    cards_dir = REPO_ROOT / "docs" / "std_variable_cards"
    return sorted(
        [path for path in cards_dir.glob("*.md") if path.name.lower() != "readme.md"],
        key=lambda item: item.name.lower(),
    )


def count_public_cards() -> int:
    return len(public_card_paths())


def markdown_section(text: str, heading: str) -> str:
    pattern = re.compile(
        rf"^{re.escape(heading)}\n(?P<body>.*?)(?=^## |\Z)",
        flags=re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(text)
    if not match:
        return ""
    return match.group("body").strip()


def parse_markdown_table(table_lines: list[str]) -> list[dict[str, str]]:
    if len(table_lines) < 2:
        return []
    headers = [cell.strip() for cell in table_lines[0].strip().strip("|").split("|")]
    rows: list[dict[str, str]] = []
    for line in table_lines[2:]:
        if not line.startswith("|"):
            continue
        values = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(values) != len(headers):
            continue
        rows.append(dict(zip(headers, values)))
    return rows


def table_from_section(text: str, heading: str) -> list[dict[str, str]]:
    section = markdown_section(text, heading)
    if not section:
        return []
    table_lines: list[str] = []
    for raw_line in section.splitlines():
        line = raw_line.rstrip()
        if line.startswith("|"):
            table_lines.append(line)
            continue
        if table_lines:
            break
    return parse_markdown_table(table_lines)


def clean_inline_code(value: str) -> str:
    return value.strip().strip("`").strip()


def parse_public_variable_card_text(text: str, relative_path: str) -> dict[str, Any]:
    missing_headings = [heading for heading in REQUIRED_PUBLIC_CARD_HEADINGS if heading not in text]

    std_variable_match = re.search(
        r"std_variable_id`:\s*`(?P<value>[^`]+)`",
        text,
    )
    std_variable_id = std_variable_match.group("value") if std_variable_match else ""

    approved_line_match = re.search(
        r"Currently approved in:\s*(?P<value>.+?)\.",
        text,
    )
    approved_database_ids: list[str] = []
    if approved_line_match:
        raw_value = approved_line_match.group("value").strip()
        if raw_value.lower() != "none":
            approved_database_ids = [
                item.strip()
                for item in raw_value.split(",")
                if item.strip()
            ]

    implementation_rows = table_from_section(text, "## Approved Database Implementations")
    current_asset_rows = table_from_section(text, "## Current Approved Database Assets")

    current_asset_database_ids = [
        clean_inline_code(row.get("database_id", ""))
        for row in current_asset_rows
        if row.get("database_id")
    ]
    if current_asset_database_ids:
        approved_database_ids = current_asset_database_ids

    publication_basis_match = re.search(
        r"current publication basis:\s*(?P<value>.+)",
        markdown_section(text, "## Cross-Database Status"),
        flags=re.IGNORECASE,
    )

    return {
        "path": relative_path,
        "std_variable_id": std_variable_id,
        "approved_database_ids": sorted(set(approved_database_ids)),
        "approved_database_count": len(set(approved_database_ids)),
        "implementation_rows": implementation_rows,
        "current_asset_rows": current_asset_rows,
        "publication_basis": (
            publication_basis_match.group("value").strip() if publication_basis_match else ""
        ),
        "missing_headings": missing_headings,
    }


def parse_public_variable_card_path(card_path: Path) -> dict[str, Any]:
    return parse_public_variable_card_text(
        card_path.read_text(encoding="utf-8"),
        repo_relative(card_path),
    )


def load_current_release_governance() -> dict[str, str]:
    if DEFAULT_RELEASE_SAFE_MANIFEST_PATH.exists():
        try:
            manifest = json.loads(DEFAULT_RELEASE_SAFE_MANIFEST_PATH.read_text(encoding="utf-8"))
            raw_governance = manifest.get("release_governance", {})
            if isinstance(raw_governance, dict):
                return normalize_release_governance(raw_governance)
        except json.JSONDecodeError:
            pass
    return normalize_release_governance({})


def normalize_release_governance(
    raw_governance: dict[str, Any] | None,
    overrides: dict[str, Any] | None = None,
) -> dict[str, str]:
    governance = dict(FALLBACK_RELEASE_GOVERNANCE)

    for source in (raw_governance or {}, overrides or {}):
        for key, value in source.items():
            if value is None:
                continue
            governance[key] = str(value)

    if not governance.get("current_changelog_entry_heading"):
        governance["current_changelog_entry_heading"] = (
            f"## {governance['release_version']} - {governance['release_date']}"
        )
    if not governance.get("release_notes_path"):
        governance["release_notes_path"] = (
            f"docs/releases/{governance['release_tag']}.md"
        )
    return governance


def changelog_text(path: Path = DEFAULT_RELEASE_CHANGELOG_PATH) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def changelog_headings(text: str) -> list[str]:
    return re.findall(r"^## .+$", text, flags=re.MULTILINE)


def extract_changelog_entry_body(text: str, heading: str) -> str:
    pattern = re.compile(
        rf"^{re.escape(heading)}\n(?P<body>.*?)(?=^## |\Z)",
        flags=re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(text)
    if not match:
        return ""
    return match.group("body").strip()


def extract_changelog_summary_bullets(text: str, heading: str) -> list[str]:
    body = extract_changelog_entry_body(text, heading)
    if not body:
        return []
    bullet_lines: list[str] = []
    capture = False
    for raw_line in body.splitlines():
        line = raw_line.rstrip()
        if line.strip() == "Summary:":
            capture = True
            continue
        if capture and line.startswith("- "):
            bullet_lines.append(line[2:].strip())
            continue
        if capture and bullet_lines and line.strip():
            break
    return bullet_lines


def build_variable_coverage_snapshot(data: dict[str, Any]) -> dict[str, Any]:
    database_lookup = {
        record["database_id"]: record for record in database_records(data)
    }

    coverage_by_database: dict[str, set[str]] = {
        database_id: set() for database_id in database_lookup
    }
    card_records: list[dict[str, Any]] = []

    for card_path in public_card_paths():
        record = parse_public_variable_card_path(card_path)
        approved_database_ids = [
            database_id
            for database_id in record["approved_database_ids"]
            if database_id in database_lookup
        ]
        for database_id in approved_database_ids:
            coverage_by_database.setdefault(database_id, set()).add(record["std_variable_id"])
        card_records.append(
            {
                "std_variable_id": record["std_variable_id"],
                "card_path": record["path"],
                "approved_database_ids": approved_database_ids,
                "approved_database_count": len(approved_database_ids),
                "publication_basis": record["publication_basis"],
            }
        )

    database_coverage: list[dict[str, Any]] = []
    for database in database_records(data):
        variable_ids = sorted(coverage_by_database.get(database["database_id"], set()))
        database_coverage.append(
            {
                "database_id": database["database_id"],
                "family_id": database["family_id"],
                "module_role": database["module_role"],
                "version": database["version"],
                "public_card_count": len(variable_ids),
                "example_variable_ids": variable_ids[:15],
                "variable_ids": variable_ids,
            }
        )

    family_coverage: list[dict[str, Any]] = []
    for family in family_records(data):
        member_ids = family["current_database_ids"]
        member_sets = [coverage_by_database.get(database_id, set()) for database_id in member_ids]
        union_ids = sorted(set().union(*member_sets)) if member_sets else []
        shared_ids = sorted(set.intersection(*member_sets)) if member_sets else []
        family_coverage.append(
            {
                "family_id": family["family_id"],
                "display_name": family["display_name"],
                "member_database_ids": member_ids,
                "family_union_public_card_count": len(union_ids),
                "family_shared_public_card_count": len(shared_ids),
                "example_union_variable_ids": union_ids[:15],
                "example_shared_variable_ids": shared_ids[:15],
                "union_variable_ids": union_ids,
                "shared_variable_ids": shared_ids,
            }
        )

    cross_database_variable_ids = sorted(
        record["std_variable_id"]
        for record in card_records
        if record["approved_database_count"] > 1
    )

    return {
        "catalog_version": data.get("catalog_version", ""),
        "public_std_variable_card_count": len(card_records),
        "cross_database_public_card_count": len(cross_database_variable_ids),
        "cross_database_variable_ids": cross_database_variable_ids,
        "database_coverage": database_coverage,
        "family_coverage": family_coverage,
        "cards": card_records,
    }


def build_database_variable_coverage_snapshot(data: dict[str, Any]) -> dict[str, Any]:
    coverage = build_variable_coverage_snapshot(data)
    return {
        "catalog_version": coverage["catalog_version"],
        "public_std_variable_card_count": coverage["public_std_variable_card_count"],
        "cross_database_public_card_count": coverage["cross_database_public_card_count"],
        "cross_database_variable_ids": coverage["cross_database_variable_ids"],
        "database_coverage": coverage["database_coverage"],
    }


def build_family_variable_coverage_snapshot(data: dict[str, Any]) -> dict[str, Any]:
    coverage = build_variable_coverage_snapshot(data)
    return {
        "catalog_version": coverage["catalog_version"],
        "public_std_variable_card_count": coverage["public_std_variable_card_count"],
        "family_coverage": coverage["family_coverage"],
    }


def build_repository_status_snapshot(
    data: dict[str, Any],
    release_overrides: dict[str, Any] | None = None,
) -> dict[str, Any]:
    families = family_records(data)
    databases = database_records(data)
    coverage = build_variable_coverage_snapshot(data)
    release_governance = normalize_release_governance(
        load_current_release_governance(),
        release_overrides,
    )
    return {
        "catalog_version": data.get("catalog_version", ""),
        "repository_scope": data.get("repository_scope", ""),
        "family_count": len(families),
        "database_count": len(databases),
        "public_std_variable_card_count": count_public_cards(),
        "cross_database_public_card_count": coverage["cross_database_public_card_count"],
        "release_governance": {
            "release_version": release_governance["release_version"],
            "release_tag": release_governance["release_tag"],
            "release_status": release_governance["release_status"],
            "release_date": release_governance["release_date"],
        },
        "families": [
            {
                "family_id": family["family_id"],
                "display_name": family["display_name"],
                "current_database_ids": family["current_database_ids"],
            }
            for family in families
        ],
        "databases": [
            {
                "database_id": database["database_id"],
                "family_id": database["family_id"],
                "version": database["version"],
                "module_role": database["module_role"],
                "public_layer1_support_status": database["public_layer1_support_status"],
                "public_layer4_support_status": database["public_layer4_support_status"],
                "public_layer5_public_status": database["public_layer5_public_status"],
                "public_card_count": next(
                    (
                        item["public_card_count"]
                        for item in coverage["database_coverage"]
                        if item["database_id"] == database["database_id"]
                    ),
                    0,
                ),
            }
            for database in databases
        ],
    }


def build_release_safe_categories() -> dict[str, list[str]]:
    release_note_docs = [
        path
        for path in files_from_glob("docs/releases/*.md")
        if path != "docs/releases/README.md"
    ]
    public_export_docs = [
        path
        for path in files_from_recursive("docs/public_exports")
        if path != "docs/public_exports/README.md"
    ]
    return {
        "root_files": sorted(
            [
                "README.md",
                "requirements.txt",
            ]
        ),
        "framework_contracts": files_from_glob("Framework_Guideline/*.md"),
        "docs_core": sorted(
            [
                "docs/DATABASE_LINEAGE_AND_VERSION_MATRIX.md",
                "docs/GETTING_STARTED.md",
                "docs/NEXT_STAGE_PUBLIC_METHOD_REPOSITORY_CHECKLIST.md",
                "docs/PUBLIC_INVENTORY.md",
                "docs/PUBLIC_REPOSITORY_DETAILED_REVIEW_CHECKLIST.md",
                "docs/database_catalog.json",
                "docs/release_safe_manifest.json",
            ]
        ),
        "release_docs": sorted(
            [
                "docs/RELEASE_CHANGELOG.md",
                "docs/releases/README.md",
            ]
        ),
        "release_note_docs": release_note_docs,
        "public_export_support_files": sorted(
            [
                "docs/public_exports/README.md",
            ]
        ),
        "public_export_docs": public_export_docs,
        "onboarding_support_files": sorted(
            [
                "docs/onboarding/README.md",
                "docs/onboarding/ONBOARDING_TEMPLATE.md",
                "docs/onboarding/families/README.md",
                "docs/onboarding/families/FAMILY_TEMPLATE.md",
            ]
        ),
        "family_playbooks": sorted(
            [
                "docs/onboarding/families/MIMIC-IV.md",
                "docs/onboarding/families/AmsterdamUMCdb.md",
            ]
        ),
        "database_playbooks": sorted(
            [
                "docs/onboarding/AmsterdamUMCdb-1.0.2.md",
                "docs/onboarding/MIMIC-IV-3.1.md",
                "docs/onboarding/MIMIC-IV-ECHO-1.0.md",
            ]
        ),
        "tutorial_docs": files_from_glob("docs/tutorials/*.md"),
        "github_workflows": files_from_glob(".github/workflows/*.yml"),
        "public_scripts": files_from_glob("scripts/*.py")
        + files_from_glob("scripts/layer1/*.py")
        + files_from_glob("scripts/layer4/*.py")
        + files_from_glob("scripts/layer5/*.py"),
        "public_script_support_files": sorted(
            [
                "scripts/README.md",
            ]
        ),
        "layer1_skeleton_files": files_from_recursive("Data/Layer 1"),
        "public_variable_card_support_files": sorted(
            [
                "docs/std_variable_cards/README.md",
            ]
        ),
        "public_variable_cards": files_from_glob("docs/std_variable_cards/*.md"),
        "test_support_files": files_from_recursive("tests"),
    }


def build_release_safe_manifest(
    data: dict[str, Any],
    release_overrides: dict[str, Any] | None = None,
) -> dict[str, Any]:
    families = family_records(data)
    databases = database_records(data)
    categories = build_release_safe_categories()
    std_cards = [
        path
        for path in categories["public_variable_cards"]
        if path != "docs/std_variable_cards/README.md"
    ]
    categories["public_variable_cards"] = std_cards
    total_files = sum(len(paths) for paths in categories.values())
    release_governance = normalize_release_governance(
        load_current_release_governance(),
        release_overrides,
    )
    return {
        "manifest_type": "release_safe_manifest",
        "manifest_version": "v1",
        "catalog_version": data.get("catalog_version", ""),
        "repository_scope": data.get("repository_scope", ""),
        "release_safe_definition": (
            "GitHub-safe repository snapshot. Includes public contracts, scripts, docs, "
            "Layer 1 skeletons, workflows, public exports, release notes, and public "
            "variable cards. Excludes restricted raw data, local parquet copies, and "
            "patient-level Layer 2-5 outputs."
        ),
        "default_manifest_path": repo_relative(DEFAULT_RELEASE_SAFE_MANIFEST_PATH),
        "default_inventory_path": repo_relative(DEFAULT_PUBLIC_INVENTORY_PATH),
        "release_governance": release_governance,
        "counts": {
            "family_count": len(families),
            "database_count": len(databases),
            "public_std_variable_card_count": len(std_cards),
            "release_safe_file_count": total_files,
            "category_counts": {
                category_name: len(paths)
                for category_name, paths in categories.items()
            },
        },
        "coverage": {
            "family_ids": [family["family_id"] for family in families],
            "database_ids": [database["database_id"] for database in databases],
            "database_statuses": [
                {
                    "database_id": database["database_id"],
                    "family_id": database["family_id"],
                    "module_role": database["module_role"],
                    "version": database["version"],
                    "public_layer1_support_status": database["public_layer1_support_status"],
                    "public_layer4_support_status": database["public_layer4_support_status"],
                    "public_layer5_public_status": database["public_layer5_public_status"],
                }
                for database in databases
            ],
        },
        "categories": categories,
    }


def build_family_summary_markdown(data: dict[str, Any], family_id: str) -> str:
    family = find_family_record(data, family_id)
    databases = databases_for_family(data, family_id)
    coverage = build_variable_coverage_snapshot(data)
    family_coverage = next(
        (item for item in coverage["family_coverage"] if item["family_id"] == family_id),
        None,
    )

    lines: list[str] = []
    lines.append(f"# Public Family Summary: {family['display_name']}")
    lines.append("")
    lines.append(f"- `family_id`: `{family['family_id']}`")
    lines.append(f"- display name: `{family['display_name']}`")
    lines.append(f"- current member count: `{len(databases)}`")
    if family_coverage:
        lines.append(
            f"- public-card union count across family members: `{family_coverage['family_union_public_card_count']}`"
        )
        lines.append(
            f"- public-card shared count across all family members: `{family_coverage['family_shared_public_card_count']}`"
        )
    lines.append("")
    lines.append("## Description")
    lines.append("")
    lines.append(family["description"])
    lines.append("")
    lines.append("## Governance")
    lines.append("")
    lines.append(f"- family playbook: `{family['public_family_playbook']}`")
    lines.append(f"- future member rule: {family['future_member_rule']}")
    lines.append(f"- alignment rule: {family['alignment_rule']}")
    lines.append("")
    lines.append("## Current members")
    lines.append("")
    lines.append("| database_id | role | version | layer1 status | layer4 status | layer5 status | public card count |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for database in databases:
        database_coverage = next(
            (
                item
                for item in coverage["database_coverage"]
                if item["database_id"] == database["database_id"]
            ),
            {"public_card_count": 0},
        )
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{database['database_id']}`",
                    database["module_role"],
                    f"`{database['version']}`",
                    database["public_layer1_support_status"],
                    database["public_layer4_support_status"],
                    database["public_layer5_public_status"],
                    f"`{database_coverage['public_card_count']}`",
                ]
            )
            + " |"
        )
    if family_coverage:
        lines.append("")
        lines.append("## Public-card coverage examples")
        lines.append("")
        lines.append(
            "- family union examples: "
            + ", ".join(f"`{item}`" for item in family_coverage["example_union_variable_ids"])
        )
        lines.append(
            "- family shared examples: "
            + ", ".join(f"`{item}`" for item in family_coverage["example_shared_variable_ids"])
        )
    lines.append("")
    lines.append("## Related public files")
    lines.append("")
    lines.append("- `docs/DATABASE_LINEAGE_AND_VERSION_MATRIX.md`")
    lines.append("- `docs/database_catalog.json`")
    lines.append(f"- `{family['public_family_playbook']}`")
    for database in databases:
        lines.append(f"- `{database['public_onboarding_playbook']}`")
    return "\n".join(lines) + "\n"


def build_variable_coverage_summary_markdown(data: dict[str, Any]) -> str:
    coverage = build_variable_coverage_snapshot(data)

    lines: list[str] = []
    lines.append("# Public Variable Coverage Summary")
    lines.append("")
    lines.append("This file is the human-readable coverage summary derived from the current public variable-card layer.")
    lines.append("")
    lines.append("## Snapshot")
    lines.append("")
    lines.append(f"- catalog version: `{coverage['catalog_version']}`")
    lines.append(f"- public std-variable cards: `{coverage['public_std_variable_card_count']}`")
    lines.append(f"- cross-database public cards: `{coverage['cross_database_public_card_count']}`")
    lines.append("")
    lines.append("## Coverage by database")
    lines.append("")
    lines.append("| database_id | family_id | role | public card count | example variable ids |")
    lines.append("| --- | --- | --- | --- | --- |")
    for record in coverage["database_coverage"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{record['database_id']}`",
                    f"`{record['family_id']}`",
                    record["module_role"],
                    f"`{record['public_card_count']}`",
                    ", ".join(f"`{item}`" for item in record["example_variable_ids"]),
                ]
            )
            + " |"
        )
    lines.append("")
    lines.append("## Coverage by family")
    lines.append("")
    lines.append("| family_id | family union count | family shared count | example shared variable ids |")
    lines.append("| --- | --- | --- | --- |")
    for record in coverage["family_coverage"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{record['family_id']}`",
                    f"`{record['family_union_public_card_count']}`",
                    f"`{record['family_shared_public_card_count']}`",
                    ", ".join(f"`{item}`" for item in record["example_shared_variable_ids"]),
                ]
            )
            + " |"
        )
    lines.append("")
    lines.append("## Cross-database examples")
    lines.append("")
    lines.append(
        ", ".join(f"`{item}`" for item in coverage["cross_database_variable_ids"][:30])
        if coverage["cross_database_variable_ids"]
        else "No current cross-database public cards."
    )
    return "\n".join(lines) + "\n"


def build_public_inventory_markdown(
    data: dict[str, Any],
    release_overrides: dict[str, Any] | None = None,
) -> str:
    manifest = build_release_safe_manifest(data, release_overrides)
    categories: dict[str, list[str]] = manifest["categories"]
    families = family_records(data)
    databases = database_records(data)
    coverage = build_variable_coverage_snapshot(data)

    lines: list[str] = []
    lines.append("# Public Inventory")
    lines.append("")
    lines.append("## What this file is")
    lines.append("")
    lines.append(
        "This is the human-readable inventory of the current GitHub-safe public repository surface."
    )
    lines.append(
        "The machine-readable counterpart is [`docs/release_safe_manifest.json`](release_safe_manifest.json)."
    )
    lines.append("")
    lines.append("## Snapshot summary")
    lines.append("")
    lines.append(f"- catalog version: `{data.get('catalog_version', '')}`")
    lines.append(f"- family count: `{len(families)}`")
    lines.append(f"- database count: `{len(databases)}`")
    lines.append(
        f"- public std-variable cards: `{manifest['counts']['public_std_variable_card_count']}`"
    )
    lines.append(
        f"- cross-database public cards: `{coverage['cross_database_public_card_count']}`"
    )
    lines.append(
        f"- total release-safe files listed in the manifest: `{manifest['counts']['release_safe_file_count']}`"
    )
    lines.append(f"- release version: `{manifest['release_governance']['release_version']}`")
    lines.append(f"- release tag: `{manifest['release_governance']['release_tag']}`")
    lines.append(f"- release status: `{manifest['release_governance']['release_status']}`")
    lines.append("")
    lines.append("## Release governance")
    lines.append("")
    lines.append(
        f"- release version: `{manifest['release_governance']['release_version']}`"
    )
    lines.append(
        f"- release tag: `{manifest['release_governance']['release_tag']}`"
    )
    lines.append(
        f"- release label: `{manifest['release_governance']['release_label']}`"
    )
    lines.append(
        f"- release status: `{manifest['release_governance']['release_status']}`"
    )
    lines.append(
        f"- release date: `{manifest['release_governance']['release_date']}`"
    )
    lines.append(
        f"- changelog: `{manifest['release_governance']['changelog_path']}`"
    )
    lines.append(
        f"- current changelog heading: `{manifest['release_governance']['current_changelog_entry_heading']}`"
    )
    lines.append(
        f"- release notes: `{manifest['release_governance']['release_notes_path']}`"
    )
    lines.append("")
    lines.append("## Coverage by family")
    lines.append("")
    lines.append("| family_id | display_name | current database_ids | family playbook | family union count | family shared count |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for family in families:
        family_coverage = next(
            (
                item
                for item in coverage["family_coverage"]
                if item["family_id"] == family["family_id"]
            ),
            {
                "family_union_public_card_count": 0,
                "family_shared_public_card_count": 0,
            },
        )
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{family['family_id']}`",
                    family["display_name"],
                    ", ".join(f"`{database_id}`" for database_id in family["current_database_ids"]),
                    f"`{family['public_family_playbook']}`",
                    f"`{family_coverage['family_union_public_card_count']}`",
                    f"`{family_coverage['family_shared_public_card_count']}`",
                ]
            )
            + " |"
        )
    lines.append("")
    lines.append("## Coverage by database/module")
    lines.append("")
    lines.append("| database_id | family | role | version | layer1 | layer4 | layer5 | public cards | onboarding |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for database in databases:
        database_coverage = next(
            (
                item
                for item in coverage["database_coverage"]
                if item["database_id"] == database["database_id"]
            ),
            {"public_card_count": 0},
        )
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{database['database_id']}`",
                    f"`{database['family_id']}`",
                    database["module_role"],
                    f"`{database['version']}`",
                    database["public_layer1_support_status"],
                    database["public_layer4_support_status"],
                    database["public_layer5_public_status"],
                    f"`{database_coverage['public_card_count']}`",
                    f"`{database['public_onboarding_playbook']}`",
                ]
            )
            + " |"
        )
    lines.append("")
    lines.append("## Public asset classes")
    lines.append("")
    lines.append("| asset class | count | notes |")
    lines.append("| --- | --- | --- |")
    lines.append(
        f"| root files | `{len(categories['root_files'])}` | repository-level public entry files |"
    )
    lines.append(
        f"| framework contracts | `{len(categories['framework_contracts'])}` | governing public contracts in `Framework_Guideline/` |"
    )
    lines.append(
        f"| core docs | `{len(categories['docs_core'])}` | matrix, inventory, review checklist, and other core public notes |"
    )
    lines.append(
        f"| release docs | `{len(categories['release_docs'])}` | changelog and release-process support docs |"
    )
    lines.append(
        f"| release note docs | `{len(categories['release_note_docs'])}` | one release note per public release tag |"
    )
    lines.append(
        f"| public export support files | `{len(categories['public_export_support_files'])}` | README for generated public export artifacts |"
    )
    lines.append(
        f"| public export docs | `{len(categories['public_export_docs'])}` | generated repository status and variable-coverage exports |"
    )
    lines.append(
        f"| onboarding support files | `{len(categories['onboarding_support_files'])}` | README and templates for onboarding layers |"
    )
    lines.append(
        f"| family playbooks | `{len(categories['family_playbooks'])}` | family-level governance docs |"
    )
    lines.append(
        f"| database playbooks | `{len(categories['database_playbooks'])}` | per-database onboarding docs |"
    )
    lines.append(
        f"| tutorials | `{len(categories['tutorial_docs'])}` | public-safe walkthroughs |"
    )
    lines.append(
        f"| GitHub workflows | `{len(categories['github_workflows'])}` | public CI/smoke workflows |"
    )
    lines.append(
        f"| public scripts | `{len(categories['public_scripts'])}` | GitHub-safe Python scripts under `scripts/` |"
    )
    lines.append(
        f"| Layer 1 skeleton files | `{len(categories['layer1_skeleton_files'])}` | committed public Layer 1 skeleton contents across supported databases |"
    )
    lines.append(
        f"| std-variable card support files | `{len(categories['public_variable_card_support_files'])}` | shared README for public cards |"
    )
    lines.append(
        f"| public std-variable cards | `{len(categories['public_variable_cards'])}` | variable-level public documentation cards |"
    )
    lines.append(
        f"| test support files | `{len(categories['test_support_files'])}` | public-safe fixtures and repository test notes |"
    )
    lines.append("")
    lines.append("## Key entrypoints")
    lines.append("")
    lines.append("- `python scripts/public_workflow.py status`")
    lines.append("- `python scripts/public_workflow.py status --family-id MIMIC-IV`")
    lines.append("- `python scripts/public_workflow.py build-layer1 ...`")
    lines.append("- `python scripts/public_workflow.py validate-registry ...`")
    lines.append("- `python scripts/public_workflow.py check-public-repository`")
    lines.append("- `python scripts/public_workflow.py prepare-release --dry-run`")
    lines.append("- `python scripts/public_workflow.py scaffold-public-database --help`")
    lines.append(
        "- `python scripts/public_workflow.py export-public-artifacts --artifact release-safe-manifest`"
    )
    lines.append(
        "- `python scripts/public_workflow.py export-public-artifacts --artifact public-inventory`"
    )
    lines.append(
        "- `python scripts/public_workflow.py export-public-artifacts --artifact release-governance`"
    )
    lines.append(
        "- `python scripts/public_workflow.py export-public-artifacts --artifact database-variable-coverage`"
    )
    lines.append(
        "- `python scripts/public_workflow.py export-public-artifacts --artifact family-variable-coverage`"
    )
    lines.append(
        "- `python scripts/public_workflow.py export-public-artifacts --artifact variable-coverage-summary`"
    )
    lines.append("")
    lines.append("## Full machine-readable inventory")
    lines.append("")
    lines.append(
        "For the complete file-level release-safe list, use [`docs/release_safe_manifest.json`](release_safe_manifest.json)."
    )
    lines.append("")
    lines.append("For public variable-coverage exports, use the generated files under [`docs/public_exports`](public_exports/README.md).")
    return "\n".join(lines) + "\n"


def build_release_note_markdown(
    data: dict[str, Any],
    release_overrides: dict[str, Any] | None = None,
) -> str:
    release_governance = normalize_release_governance(
        load_current_release_governance(),
        release_overrides,
    )
    coverage = build_variable_coverage_snapshot(data)
    manifest = build_release_safe_manifest(data, release_overrides)
    changelog = changelog_text()
    summary_bullets = extract_changelog_summary_bullets(
        changelog,
        release_governance["current_changelog_entry_heading"],
    )

    lines: list[str] = []
    lines.append(f"# Public Release Note: {release_governance['release_tag']}")
    lines.append("")
    lines.append(f"- release version: `{release_governance['release_version']}`")
    lines.append(f"- release tag: `{release_governance['release_tag']}`")
    lines.append(f"- release label: `{release_governance['release_label']}`")
    lines.append(f"- release status: `{release_governance['release_status']}`")
    lines.append(f"- release date: `{release_governance['release_date']}`")
    lines.append(f"- changelog heading: `{release_governance['current_changelog_entry_heading']}`")
    lines.append("")
    lines.append("## Release summary")
    lines.append("")
    if summary_bullets:
        for bullet in summary_bullets:
            lines.append(f"- {bullet}")
    else:
        lines.append("- See the linked changelog entry for the human-written release summary.")
    lines.append("")
    lines.append("## Snapshot counts")
    lines.append("")
    lines.append(f"- family count: `{manifest['counts']['family_count']}`")
    lines.append(f"- database count: `{manifest['counts']['database_count']}`")
    lines.append(
        f"- public std-variable cards: `{manifest['counts']['public_std_variable_card_count']}`"
    )
    lines.append(
        f"- cross-database public cards: `{coverage['cross_database_public_card_count']}`"
    )
    lines.append(
        f"- release-safe file count: `{manifest['counts']['release_safe_file_count']}`"
    )
    lines.append("")
    lines.append("## Coverage by database")
    lines.append("")
    lines.append("| database_id | role | public card count |")
    lines.append("| --- | --- | --- |")
    for record in coverage["database_coverage"]:
        lines.append(
            f"| `{record['database_id']}` | {record['module_role']} | `{record['public_card_count']}` |"
        )
    lines.append("")
    lines.append("## Generated companion artifacts")
    lines.append("")
    lines.append("- `docs/release_safe_manifest.json`")
    lines.append("- `docs/PUBLIC_INVENTORY.md`")
    for path in DEFAULT_PUBLIC_EXPORT_PATHS.values():
        lines.append(f"- `{repo_relative(path)}`")
    lines.append("")
    lines.append("## Release boundary")
    lines.append("")
    lines.append(
        "This release note describes only the GitHub-safe public method repository surface. "
        "It does not enumerate restricted raw data, local parquet copies, or patient-level "
        "Layer 2-5 outputs."
    )
    return "\n".join(lines) + "\n"


def build_generated_public_outputs(
    data: dict[str, Any],
    release_overrides: dict[str, Any] | None = None,
) -> dict[Path, str]:
    release_governance = normalize_release_governance(
        load_current_release_governance(),
        release_overrides,
    )
    outputs: dict[Path, str] = {
        DEFAULT_RELEASE_SAFE_MANIFEST_PATH: render_artifact(
            data,
            "release-safe-manifest-json",
            None,
            release_governance,
        ),
        DEFAULT_PUBLIC_INVENTORY_PATH: render_artifact(
            data,
            "public-inventory-markdown",
            None,
            release_governance,
        ),
        DEFAULT_PUBLIC_EXPORT_PATHS["repository-status-json"]: render_artifact(
            data,
            "repository-status-json",
            None,
            release_governance,
        ),
        DEFAULT_PUBLIC_EXPORT_PATHS["database-variable-coverage-json"]: render_artifact(
            data,
            "database-variable-coverage-json",
            None,
            release_governance,
        ),
        DEFAULT_PUBLIC_EXPORT_PATHS["family-variable-coverage-json"]: render_artifact(
            data,
            "family-variable-coverage-json",
            None,
            release_governance,
        ),
        DEFAULT_PUBLIC_EXPORT_PATHS["variable-coverage-summary-markdown"]: render_artifact(
            data,
            "variable-coverage-summary-markdown",
            None,
            release_governance,
        ),
        REPO_ROOT / Path(release_governance["release_notes_path"]): render_artifact(
            data,
            "release-note-markdown",
            None,
            release_governance,
        ),
    }
    return outputs


def render_artifact(
    data: dict[str, Any],
    artifact: str,
    family_id: str | None,
    release_overrides: dict[str, Any] | None = None,
) -> str:
    if artifact == "database-catalog-json":
        return json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    if artifact == "repository-status-json":
        snapshot = build_repository_status_snapshot(data, release_overrides)
        return json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n"
    if artifact == "release-governance-json":
        manifest = build_release_safe_manifest(data, release_overrides)
        return json.dumps(manifest["release_governance"], ensure_ascii=False, indent=2) + "\n"
    if artifact == "release-safe-manifest-json":
        manifest = build_release_safe_manifest(data, release_overrides)
        return json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    if artifact == "public-inventory-markdown":
        return build_public_inventory_markdown(data, release_overrides)
    if artifact == "family-summary-markdown":
        if not family_id:
            raise SystemExit("--family-id is required for family-summary-markdown")
        return build_family_summary_markdown(data, family_id)
    if artifact == "database-variable-coverage-json":
        coverage = build_database_variable_coverage_snapshot(data)
        return json.dumps(coverage, ensure_ascii=False, indent=2) + "\n"
    if artifact == "family-variable-coverage-json":
        coverage = build_family_variable_coverage_snapshot(data)
        return json.dumps(coverage, ensure_ascii=False, indent=2) + "\n"
    if artifact == "variable-coverage-summary-markdown":
        return build_variable_coverage_summary_markdown(data)
    if artifact == "release-note-markdown":
        return build_release_note_markdown(data, release_overrides)
    raise SystemExit(f"Unsupported artifact: {artifact}")


def write_output(content: str, output_path: Path | None) -> None:
    if output_path is None:
        print(content, end="")
        return
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")
    print(f"Wrote: {output_path}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Export GitHub-safe repository metadata derived from the public database catalog."
    )
    parser.add_argument(
        "--artifact",
        required=True,
        choices=(
            "database-catalog-json",
            "repository-status-json",
            "release-governance-json",
            "release-safe-manifest-json",
            "public-inventory-markdown",
            "family-summary-markdown",
            "database-variable-coverage-json",
            "family-variable-coverage-json",
            "variable-coverage-summary-markdown",
            "release-note-markdown",
        ),
        help="Metadata artifact to export.",
    )
    parser.add_argument(
        "--catalog",
        default=str(DEFAULT_CATALOG_PATH),
        help="Path to the public database catalog JSON file.",
    )
    parser.add_argument(
        "--family-id",
        help="Required for family-summary-markdown.",
    )
    parser.add_argument(
        "--output",
        help="Optional output file path. If omitted, content is printed to stdout.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    catalog_path = Path(args.catalog).resolve()
    if not catalog_path.exists():
        raise SystemExit(f"catalog not found: {catalog_path}")

    data = load_catalog(catalog_path)
    content = render_artifact(data, args.artifact, args.family_id, None)
    output_path = Path(args.output).resolve() if args.output else None
    write_output(content, output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
