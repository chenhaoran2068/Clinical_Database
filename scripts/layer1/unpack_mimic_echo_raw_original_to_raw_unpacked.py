from __future__ import annotations

import argparse
import shutil
import zipfile
from pathlib import Path


CANONICAL_ECHO_ROOT = "ECHO-1.0"
REQUIRED_FILES = (
    "echo-record-list.csv",
    "echo-study-list.csv",
    "structured-measurement.csv.gz",
)
OPTIONAL_FILES = (
    "LICENSE.txt",
    "SHA256SUMS.txt",
    "README.txt",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Normalize staged MIMIC-IV-ECHO v1.0 source files into the canonical "
            "Layer 1 raw_unpacked/ECHO-1.0 layout."
        )
    )
    parser.add_argument(
        "--layer1-root",
        required=True,
        help="Path to Methods/Clinical_Database/local_work/Layer 1/MIMIC-IV-ECHO-1.0.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace any existing canonical raw_unpacked/ECHO-1.0 tree.",
    )
    return parser.parse_args()


def safe_rmtree(path: Path, parent: Path) -> None:
    path = path.resolve()
    parent = parent.resolve()
    if parent not in path.parents:
        raise SystemExit(f"Refusing to remove path outside parent: {path}")
    if path.exists():
        shutil.rmtree(path)


def extract_archives(raw_original_dir: Path, raw_unpacked_dir: Path, overwrite: bool) -> None:
    archives = sorted(raw_original_dir.glob("*.zip"))
    if not archives:
        return

    extraction_root = raw_unpacked_dir / "_archive_extract"
    if overwrite and extraction_root.exists():
        safe_rmtree(extraction_root, raw_unpacked_dir)
    extraction_root.mkdir(parents=True, exist_ok=True)

    for archive_path in archives:
        with zipfile.ZipFile(archive_path) as zf:
            zf.extractall(extraction_root)
        print(f"[extract] {archive_path.name} -> {extraction_root}")


def canonical_root_ready(canonical_root: Path) -> bool:
    return canonical_root.exists() and all((canonical_root / file_name).exists() for file_name in REQUIRED_FILES)


def discover_sources(search_roots: list[Path]) -> dict[str, Path]:
    discovered: dict[str, Path] = {}
    required_and_optional = set(REQUIRED_FILES) | set(OPTIONAL_FILES)

    for file_name in required_and_optional:
        matches: list[Path] = []
        for root in search_roots:
            if not root.exists():
                continue
            matches.extend(
                path
                for path in root.rglob(file_name)
                if CANONICAL_ECHO_ROOT not in path.parts[-2:]
            )
        if not matches:
            continue
        unique_matches = sorted({path.resolve() for path in matches})
        if len(unique_matches) > 1:
            raise SystemExit(
                f"Multiple candidate source files found for {file_name}: "
                + ", ".join(str(path) for path in unique_matches)
            )
        discovered[file_name] = unique_matches[0]

    missing = [file_name for file_name in REQUIRED_FILES if file_name not in discovered]
    if missing:
        raise SystemExit(
            "Could not discover all required MIMIC-IV-ECHO source files. Missing: "
            + ", ".join(missing)
        )

    return discovered


def stage_sources(canonical_root: Path, source_files: dict[str, Path], overwrite: bool) -> None:
    if canonical_root.exists() and overwrite:
        safe_rmtree(canonical_root, canonical_root.parent)
    canonical_root.mkdir(parents=True, exist_ok=True)

    for file_name, source_path in source_files.items():
        target_path = canonical_root / file_name
        if target_path.exists() and not overwrite:
            print(f"[skip] {target_path}")
            continue
        shutil.copy2(source_path, target_path)
        print(f"[stage] {source_path} -> {target_path}")


def main() -> int:
    args = parse_args()
    layer1_root = Path(args.layer1_root).resolve()
    raw_original_dir = layer1_root / "raw_original"
    raw_unpacked_dir = layer1_root / "raw_unpacked"
    canonical_root = raw_unpacked_dir / CANONICAL_ECHO_ROOT

    raw_unpacked_dir.mkdir(parents=True, exist_ok=True)
    if canonical_root_ready(canonical_root) and not args.overwrite:
        print(f"[ok] canonical MIMIC-IV-ECHO root already ready: {canonical_root}")
        return 0

    if raw_original_dir.exists():
        extract_archives(raw_original_dir, raw_unpacked_dir, args.overwrite)

    source_files = discover_sources([raw_original_dir, raw_unpacked_dir])
    stage_sources(canonical_root, source_files, args.overwrite)

    print(f"[ok] canonical MIMIC-IV-ECHO root ready: {canonical_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
