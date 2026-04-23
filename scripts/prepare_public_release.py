from __future__ import annotations

import argparse
from pathlib import Path

from export_public_metadata import (
    DEFAULT_CATALOG_PATH,
    DEFAULT_RELEASE_CHANGELOG_PATH,
    build_generated_public_outputs,
    load_catalog,
    load_current_release_governance,
    normalize_release_governance,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def prepend_changelog_entry(
    changelog_path: Path,
    heading: str,
    release_label: str,
    release_tag: str,
    release_status: str,
    summary_lines: list[str],
) -> None:
    existing_text = changelog_path.read_text(encoding="utf-8") if changelog_path.exists() else ""
    if heading in existing_text:
        return

    entry_lines = [
        heading,
        "",
        f"Release label: `{release_label}`",
        "",
        f"Release tag: `{release_tag}`",
        "",
        f"Status: `{release_status}`",
        "",
        "Summary:",
        "",
    ]
    for line in summary_lines:
        entry_lines.append(f"- {line}")
    entry_lines.append("")

    if existing_text.startswith("# Release Changelog"):
        split_marker = "\n## "
        if split_marker in existing_text:
            prefix, suffix = existing_text.split(split_marker, 1)
            new_text = prefix.rstrip() + "\n\n" + "\n".join(entry_lines) + "\n## " + suffix
        else:
            new_text = existing_text.rstrip() + "\n\n" + "\n".join(entry_lines) + "\n"
    else:
        new_text = "\n".join(
            [
                "# Release Changelog",
                "",
                "This file records public-release-facing repository changes.",
                "",
                "Entry rule:",
                "",
                "- each release entry should start with `## <release_version> - <YYYY-MM-DD>`",
                "- the matching heading should also be referenced from `docs/release_safe_manifest.json`",
                "",
                *entry_lines,
            ]
        ).rstrip() + "\n"

    changelog_path.write_text(new_text, encoding="utf-8")


def build_release_overrides(args: argparse.Namespace) -> dict[str, str]:
    current = load_current_release_governance()
    overrides = {
        "release_version": args.release_version or current["release_version"],
        "release_tag": args.release_tag or current["release_tag"],
        "release_label": args.release_label or current["release_label"],
        "release_status": args.release_status or current["release_status"],
        "release_date": args.release_date or current["release_date"],
    }
    overrides["current_changelog_entry_heading"] = (
        args.current_changelog_entry_heading
        or f"## {overrides['release_version']} - {overrides['release_date']}"
    )
    if args.release_notes_path:
        overrides["release_notes_path"] = args.release_notes_path
    return overrides


def write_outputs(outputs: dict[Path, str], dry_run: bool) -> None:
    for output_path, content in outputs.items():
        if dry_run:
            print(f"[dry-run] would write: {output_path}")
            continue
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding="utf-8")
        print(f"Wrote: {output_path}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Prepare the public release-facing artifact set. "
            "This updates generated GitHub-safe outputs together."
        )
    )
    parser.add_argument(
        "--catalog",
        default=str(DEFAULT_CATALOG_PATH),
        help="Path to the public database catalog JSON file.",
    )
    parser.add_argument("--release-version", help="Target release_version.")
    parser.add_argument("--release-tag", help="Target release_tag.")
    parser.add_argument("--release-label", help="Target release_label.")
    parser.add_argument("--release-status", help="Target release_status.")
    parser.add_argument("--release-date", help="Target release_date in YYYY-MM-DD form.")
    parser.add_argument(
        "--current-changelog-entry-heading",
        help="Explicit changelog heading. Defaults to ## <release_version> - <release_date>.",
    )
    parser.add_argument(
        "--release-notes-path",
        help="Optional repo-relative release notes path. Defaults to docs/releases/<release_tag>.md.",
    )
    parser.add_argument(
        "--summary-line",
        action="append",
        default=[],
        help="Optional summary bullet to prepend into the changelog if the target heading is missing.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show the target outputs without writing files.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    catalog_path = Path(args.catalog).resolve()
    if not catalog_path.exists():
        raise SystemExit(f"catalog not found: {catalog_path}")

    release_overrides = normalize_release_governance(
        load_current_release_governance(),
        build_release_overrides(args),
    )

    if args.summary_line and not args.dry_run:
        prepend_changelog_entry(
            DEFAULT_RELEASE_CHANGELOG_PATH,
            release_overrides["current_changelog_entry_heading"],
            release_overrides["release_label"],
            release_overrides["release_tag"],
            release_overrides["release_status"],
            args.summary_line,
        )

    changelog_text = DEFAULT_RELEASE_CHANGELOG_PATH.read_text(encoding="utf-8")
    if release_overrides["current_changelog_entry_heading"] not in changelog_text:
        raise SystemExit(
            "Target changelog heading not found. "
            "Pass --summary-line to create it or update docs/RELEASE_CHANGELOG.md first."
        )

    data = load_catalog(catalog_path)
    outputs = build_generated_public_outputs(data, release_overrides)

    print("Public release preparation summary")
    print(f"- release version: {release_overrides['release_version']}")
    print(f"- release tag: {release_overrides['release_tag']}")
    print(f"- release label: {release_overrides['release_label']}")
    print(f"- release status: {release_overrides['release_status']}")
    print(f"- release date: {release_overrides['release_date']}")
    print(f"- changelog heading: {release_overrides['current_changelog_entry_heading']}")
    print(f"- release notes path: {release_overrides['release_notes_path']}")
    write_outputs(outputs, args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
