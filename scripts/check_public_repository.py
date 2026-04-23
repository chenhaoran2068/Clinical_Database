from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from export_public_metadata import (
    DEFAULT_PUBLIC_INVENTORY_PATH,
    DEFAULT_RELEASE_CHANGELOG_PATH,
    DEFAULT_RELEASE_SAFE_MANIFEST_PATH,
    REQUIRED_PUBLIC_CARD_HEADINGS,
    build_variable_coverage_snapshot,
    build_generated_public_outputs,
    changelog_headings,
    load_catalog,
    parse_public_variable_card_path,
    render_artifact,
)
from layer5.public_card_safety import find_local_only_match_labels


REPO_ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = REPO_ROOT / "docs" / "database_catalog.json"
FIXTURE_PUBLIC_CARD_PATH = REPO_ROOT / "tests" / "fixtures" / "public_cards" / "std_fixture_demo.md"

REQUIRED_TOP_LEVEL_FILES = (
    "README.md",
    "requirements.txt",
    "docs/GETTING_STARTED.md",
    "docs/DATABASE_LINEAGE_AND_VERSION_MATRIX.md",
    "docs/RELEASE_CHANGELOG.md",
    "docs/release_safe_manifest.json",
    "docs/PUBLIC_INVENTORY.md",
    "docs/PUBLIC_REPOSITORY_DETAILED_REVIEW_CHECKLIST.md",
    "docs/public_exports/README.md",
    "docs/releases/README.md",
    "docs/onboarding/README.md",
    "docs/onboarding/families/README.md",
    "docs/tutorials/README.md",
    "docs/std_variable_cards/README.md",
    "Framework_Guideline/Layer1_Directory_Contract.md",
    "Framework_Guideline/CrossDatabase_Variable_Harmonization_Contract.md",
    "Framework_Guideline/Database_Critical_Semantics_Contract.md",
    "Framework_Guideline/Database_Family_NewVersion_Admission_Contract.md",
    "Framework_Guideline/Layer5_PublicVariableCard_Contract.md",
    "Framework_Guideline/PolicyRegistry_Contract.md",
    "Framework_Guideline/ReleaseSafe_Manifest_ReleaseGovernance_Contract.md",
    "Framework_Guideline/Script_Placement_Contract.md",
    "scripts/public_workflow.py",
    "scripts/check_public_repository.py",
    "scripts/export_public_metadata.py",
    "scripts/prepare_public_release.py",
    "scripts/scaffold_public_database.py",
    ".github/workflows/public-smoke.yml",
    "tests/README.md",
    "tests/fixtures/public_cards/std_fixture_demo.md",
)

REQUIRED_REFERENCE_STRINGS: dict[str, tuple[str, ...]] = {
    "README.md": (
        "docs/GETTING_STARTED.md",
        "docs/release_safe_manifest.json",
        "docs/PUBLIC_REPOSITORY_DETAILED_REVIEW_CHECKLIST.md",
        "scripts/public_workflow.py",
    ),
    "docs/GETTING_STARTED.md": (
        "Framework_Guideline/Database_Family_NewVersion_Admission_Contract.md",
        "python scripts/public_workflow.py prepare-release",
        "python scripts/public_workflow.py scaffold-public-database",
        "docs/public_exports/README.md",
    ),
    "scripts/README.md": (
        "prepare_public_release.py",
        "scaffold_public_database.py",
        "public_workflow.py prepare-release",
    ),
    "docs/tutorials/README.md": (
        "database_family_and_version_admission_walkthrough.md",
        "public_release_governance_and_inventory_workflow.md",
    ),
}

REQUIRED_FAMILY_KEYS: dict[str, type[Any]] = {
    "family_id": str,
    "display_name": str,
    "description": str,
    "public_family_playbook": str,
    "current_database_ids": list,
    "future_member_rule": str,
    "alignment_rule": str,
}

REQUIRED_DATABASE_KEYS: dict[str, type[Any]] = {
    "database_id": str,
    "display_name": str,
    "family_id": str,
    "module_role": str,
    "version": str,
    "relationship_note": str,
    "public_layer1_skeleton_path": str,
    "public_onboarding_playbook": str,
    "public_script_entrypoints": list,
    "special_semantics_contracts": list,
    "public_layer1_support_status": str,
    "public_layer4_support_status": str,
    "public_layer5_public_status": str,
    "current_local_stage": str,
    "public_tutorials": list,
}

TEXT_FILE_SUFFIXES = {
    ".md",
    ".py",
    ".json",
    ".yml",
    ".yaml",
    ".txt",
    ".csv",
}


def load_catalog_data() -> dict[str, Any]:
    return load_catalog(CATALOG_PATH)


def validate_catalog_structure(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(data.get("catalog_version"), str):
        errors.append("catalog_version must be a string")
    if not isinstance(data.get("repository_scope"), str):
        errors.append("repository_scope must be a string")

    families = data.get("families")
    if not isinstance(families, list) or not families:
        errors.append("families must be a non-empty list")
    else:
        seen_family_ids: set[str] = set()
        for index, record in enumerate(families, start=1):
            label = f"families[{index}]"
            if not isinstance(record, dict):
                errors.append(f"{label} must be an object")
                continue
            for key, expected_type in REQUIRED_FAMILY_KEYS.items():
                value = record.get(key)
                if not isinstance(value, expected_type):
                    actual = type(value).__name__
                    errors.append(f"{label}.{key} expected {expected_type.__name__}, got {actual}")
            family_id = record.get("family_id")
            if isinstance(family_id, str):
                if family_id in seen_family_ids:
                    errors.append(f"duplicate family_id: {family_id}")
                seen_family_ids.add(family_id)

    databases = data.get("databases")
    if not isinstance(databases, list) or not databases:
        errors.append("databases must be a non-empty list")
        return errors

    seen_database_ids: set[str] = set()
    for index, record in enumerate(databases, start=1):
        label = f"databases[{index}]"
        if not isinstance(record, dict):
            errors.append(f"{label} must be an object")
            continue
        for key, expected_type in REQUIRED_DATABASE_KEYS.items():
            value = record.get(key)
            if not isinstance(value, expected_type):
                actual = type(value).__name__
                errors.append(f"{label}.{key} expected {expected_type.__name__}, got {actual}")
        database_id = record.get("database_id")
        if isinstance(database_id, str):
            if database_id in seen_database_ids:
                errors.append(f"duplicate database_id: {database_id}")
            seen_database_ids.add(database_id)
    return errors


def validate_required_files() -> list[str]:
    errors: list[str] = []
    for relative_path in REQUIRED_TOP_LEVEL_FILES:
        full_path = REPO_ROOT / relative_path
        if not full_path.exists():
            errors.append(f"missing required file: {relative_path}")
    return errors


def validate_reference_strings() -> list[str]:
    errors: list[str] = []
    for relative_path, required_snippets in REQUIRED_REFERENCE_STRINGS.items():
        full_path = REPO_ROOT / relative_path
        if not full_path.exists():
            continue
        text = full_path.read_text(encoding="utf-8")
        for snippet in required_snippets:
            if snippet not in text:
                errors.append(f"{relative_path}: missing reference snippet {snippet!r}")
    return errors


def validate_no_machine_bound_absolute_paths() -> list[str]:
    errors: list[str] = []
    absolute_path_pattern = re.compile(r"(?<!`)\b[A-Za-z]:[\\/][^\s)>\"]*|`[A-Za-z]:[\\/][^`]+`")

    for path in REPO_ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in TEXT_FILE_SUFFIXES:
            continue
        if ".git" in path.parts or "__pycache__" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        match = absolute_path_pattern.search(text)
        if match:
            errors.append(
                f"{path.relative_to(REPO_ROOT)} contains a machine-bound absolute path example: {match.group(0)!r}"
            )
    return errors


def validate_tutorial_readme() -> list[str]:
    readme_path = REPO_ROOT / "docs" / "tutorials" / "README.md"
    if not readme_path.exists():
        return []
    readme_text = readme_path.read_text(encoding="utf-8")
    errors: list[str] = []
    tutorial_files = [
        path.name
        for path in (REPO_ROOT / "docs" / "tutorials").glob("*.md")
        if path.name.lower() != "readme.md"
    ]
    for tutorial_name in tutorial_files:
        if tutorial_name not in readme_text:
            errors.append(f"docs/tutorials/README.md does not mention {tutorial_name}")
    return errors


def validate_layer1_skeleton(path: Path, database_id: str) -> list[str]:
    errors: list[str] = []
    required_paths = (
        path / "docs_manifest" / "README.md",
        path / "docs_manifest" / "LAYER1_BUCKET_STATUS.csv",
        path / "raw_original" / ".gitkeep",
        path / "raw_unpacked" / ".gitkeep",
        path / "source_supplied_derived" / ".gitkeep",
        path / "local_converted_parquet" / ".gitkeep",
    )
    for required_path in required_paths:
        if not required_path.exists():
            errors.append(
                f"{database_id}: missing Layer 1 skeleton component {required_path.relative_to(REPO_ROOT)}"
            )
    return errors


def validate_catalog_references(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    family_ids = {record["family_id"] for record in data["families"]}

    for record in data["families"]:
        family_id = record["family_id"]
        playbook_path = REPO_ROOT / record["public_family_playbook"]
        if not playbook_path.exists():
            errors.append(f"{family_id}: missing family playbook {record['public_family_playbook']}")

        member_ids = set(record["current_database_ids"])
        known_database_ids = {db["database_id"] for db in data["databases"] if db["family_id"] == family_id}
        if member_ids != known_database_ids:
            errors.append(
                f"{family_id}: current_database_ids mismatch. family lists {sorted(member_ids)}, "
                f"catalog databases show {sorted(known_database_ids)}"
            )

    for record in data["databases"]:
        database_id = record["database_id"]
        if record["family_id"] not in family_ids:
            errors.append(f"{database_id}: unknown family_id {record['family_id']}")

        layer1_path = REPO_ROOT / record["public_layer1_skeleton_path"]
        if not layer1_path.exists():
            errors.append(f"{database_id}: missing public Layer 1 skeleton path {record['public_layer1_skeleton_path']}")
        else:
            errors.extend(validate_layer1_skeleton(layer1_path, database_id))

        onboarding_path = REPO_ROOT / record["public_onboarding_playbook"]
        if not onboarding_path.exists():
            errors.append(f"{database_id}: missing onboarding playbook {record['public_onboarding_playbook']}")

        for relative_path in record["public_script_entrypoints"]:
            full_path = REPO_ROOT / relative_path
            if not full_path.exists():
                errors.append(f"{database_id}: missing script entrypoint {relative_path}")

        for relative_path in record["special_semantics_contracts"]:
            full_path = REPO_ROOT / relative_path
            if not full_path.exists():
                errors.append(f"{database_id}: missing special semantics contract {relative_path}")

        for relative_path in record["public_tutorials"]:
            full_path = REPO_ROOT / relative_path
            if not full_path.exists():
                errors.append(f"{database_id}: missing public tutorial {relative_path}")

    return errors


def validate_database_specific_semantics_contracts(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    coverage = build_variable_coverage_snapshot(data)
    coverage_by_database = {
        item["database_id"]: int(item.get("public_card_count", 0))
        for item in coverage["database_coverage"]
    }

    for record in data["databases"]:
        database_id = record["database_id"]
        public_card_count = coverage_by_database.get(database_id, 0)
        special_contracts = record.get("special_semantics_contracts", [])
        if public_card_count > 0 and not special_contracts:
            errors.append(
                f"{database_id}: public retained-variable coverage exists but special_semantics_contracts is empty"
            )
    return errors


def validate_public_cards() -> list[str]:
    cards_dir = REPO_ROOT / "docs" / "std_variable_cards"
    cards = [path for path in cards_dir.glob("*.md") if path.name.lower() != "readme.md"]
    if not cards:
        return ["docs/std_variable_cards does not contain any public variable cards"]

    errors: list[str] = []
    for card_path in cards:
        parsed = parse_public_variable_card_path(card_path)
        card_text = card_path.read_text(encoding="utf-8")
        if not parsed["std_variable_id"]:
            errors.append(f"{card_path.relative_to(REPO_ROOT)}: missing std_variable_id field")
        if parsed["missing_headings"]:
            errors.append(
                f"{card_path.relative_to(REPO_ROOT)}: missing required headings {parsed['missing_headings']}"
            )
        if (
            "## Standard Definition" not in card_text
            and "## Cross-Database Standard Definition" not in card_text
        ):
            errors.append(
                f"{card_path.relative_to(REPO_ROOT)}: missing a standard-definition section"
            )
        if (
            "## Default Presentation" not in card_text
            and "## Approved Database Implementations" not in card_text
        ):
            errors.append(
                f"{card_path.relative_to(REPO_ROOT)}: missing a presentation or implementation section"
            )
        if not parsed["current_asset_rows"]:
            errors.append(
                f"{card_path.relative_to(REPO_ROOT)}: missing current approved database assets table rows"
            )
        if not parsed["approved_database_ids"]:
            errors.append(
                f"{card_path.relative_to(REPO_ROOT)}: no approved database_ids could be parsed"
            )
        errors.extend(validate_public_card_boundary(card_path, card_text))
    return errors


def validate_public_card_boundary(card_path: Path, card_text: str) -> list[str]:
    errors: list[str] = []
    current_section = ""
    checked_sections = {
        "## Standard Definition",
        "## Cross-Database Standard Definition",
        "## Global Warnings",
        "## Shared Current Contract",
        "## Database-Specific Notes",
    }

    for line_number, line in enumerate(card_text.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("## "):
            current_section = stripped
            continue

        if not stripped:
            continue

        if current_section not in checked_sections:
            continue

        labels = find_local_only_match_labels(stripped)
        if not labels:
            continue

        excerpt = stripped
        if len(excerpt) > 140:
            excerpt = excerpt[:137] + "..."
        errors.append(
            f"{card_path.relative_to(REPO_ROOT)}:{line_number} contains local-only implementation detail "
            f"markers {labels}: {excerpt!r}"
        )

    return errors


def validate_fixture_card() -> list[str]:
    if not FIXTURE_PUBLIC_CARD_PATH.exists():
        return [f"fixture card not found: {FIXTURE_PUBLIC_CARD_PATH.relative_to(REPO_ROOT)}"]

    parsed = parse_public_variable_card_path(FIXTURE_PUBLIC_CARD_PATH)
    errors: list[str] = []
    if parsed["std_variable_id"] != "std_fixture_demo":
        errors.append("fixture card parser did not recover std_fixture_demo as the std_variable_id")
    expected_databases = ["AmsterdamUMCdb-1.0.2", "MIMIC-IV-3.1"]
    if parsed["approved_database_ids"] != expected_databases:
        errors.append(
            f"fixture card parser mismatch. expected {expected_databases}, got {parsed['approved_database_ids']}"
        )
    if parsed["missing_headings"]:
        errors.append(f"fixture card missing required headings: {parsed['missing_headings']}")
    return errors


def validate_release_governance_sync() -> list[str]:
    errors: list[str] = []
    if not DEFAULT_RELEASE_SAFE_MANIFEST_PATH.exists():
        return errors

    manifest = json.loads(DEFAULT_RELEASE_SAFE_MANIFEST_PATH.read_text(encoding="utf-8"))
    release_governance = manifest.get("release_governance", {})
    if not isinstance(release_governance, dict):
        return ["release_governance block missing or malformed in docs/release_safe_manifest.json"]

    heading = str(release_governance.get("current_changelog_entry_heading", ""))
    release_notes_path = str(release_governance.get("release_notes_path", ""))
    changelog = DEFAULT_RELEASE_CHANGELOG_PATH.read_text(encoding="utf-8")

    if heading and heading not in changelog_headings(changelog):
        errors.append(
            "docs/release_safe_manifest.json current_changelog_entry_heading does not exist in docs/RELEASE_CHANGELOG.md"
        )
    headings = changelog_headings(changelog)
    if headings and heading and headings[0] != heading:
        errors.append(
            "docs/RELEASE_CHANGELOG.md latest heading does not match docs/release_safe_manifest.json current_changelog_entry_heading"
        )
    if release_notes_path:
        release_notes_full_path = REPO_ROOT / release_notes_path
        if not release_notes_full_path.exists():
            errors.append(
                f"release notes path from manifest does not exist: {release_notes_path}"
            )
    release_update_rule = str(release_governance.get("release_update_rule", ""))
    required_release_update_references = (
        "release_safe_manifest.json",
        "PUBLIC_INVENTORY.md",
        "RELEASE_CHANGELOG.md",
        "docs/public_exports/",
        "docs/releases/",
    )
    for snippet in required_release_update_references:
        if snippet not in release_update_rule:
            errors.append(
                "docs/release_safe_manifest.json release_update_rule is missing required "
                f"release-surface reference {snippet!r}"
            )
    return errors


def validate_generated_snapshots(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expected_outputs = build_generated_public_outputs(data)
    for output_path, expected_content in expected_outputs.items():
        if not output_path.exists():
            errors.append(f"missing generated public output: {output_path.relative_to(REPO_ROOT)}")
            continue
        current_content = output_path.read_text(encoding="utf-8")
        if current_content != expected_content:
            errors.append(
                f"{output_path.relative_to(REPO_ROOT)} does not match the current generated public output"
            )

    expected_manifest = render_artifact(data, "release-safe-manifest-json", None, None)
    if DEFAULT_RELEASE_SAFE_MANIFEST_PATH.read_text(encoding="utf-8") != expected_manifest:
        errors.append(
            "docs/release_safe_manifest.json does not match the current generated release-safe manifest"
        )

    expected_inventory = render_artifact(data, "public-inventory-markdown", None, None)
    if DEFAULT_PUBLIC_INVENTORY_PATH.read_text(encoding="utf-8") != expected_inventory:
        errors.append(
            "docs/PUBLIC_INVENTORY.md does not match the current generated public inventory"
        )

    return errors


def main() -> int:
    errors: list[str] = []

    if not CATALOG_PATH.exists():
        raise SystemExit(f"database catalog not found: {CATALOG_PATH}")

    errors.extend(validate_required_files())
    errors.extend(validate_reference_strings())
    errors.extend(validate_no_machine_bound_absolute_paths())
    errors.extend(validate_tutorial_readme())
    catalog_data = load_catalog_data()
    errors.extend(validate_catalog_structure(catalog_data))
    if not errors:
        errors.extend(validate_catalog_references(catalog_data))
        errors.extend(validate_database_specific_semantics_contracts(catalog_data))
    errors.extend(validate_public_cards())
    errors.extend(validate_fixture_card())
    errors.extend(validate_release_governance_sync())
    if not errors:
        errors.extend(validate_generated_snapshots(catalog_data))

    if errors:
        print("Public repository check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Public repository check passed.")
    print(f"Catalog: {CATALOG_PATH}")
    print(f"Families: {len(catalog_data['families'])}")
    print(f"Databases: {len(catalog_data['databases'])}")
    print("Required public-card headings:")
    for heading in REQUIRED_PUBLIC_CARD_HEADINGS:
        print(f"- {heading}")
    print("Family IDs:")
    for record in catalog_data["families"]:
        print(f"- {record['family_id']}")
    print("Database IDs:")
    for record in catalog_data["databases"]:
        print(f"- {record['database_id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
