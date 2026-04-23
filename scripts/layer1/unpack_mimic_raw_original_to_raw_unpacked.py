from __future__ import annotations

import argparse
import shutil
import zipfile
from pathlib import Path


CORE_ARCHIVE = "mimic-iv-3.1.zip"
ED_ARCHIVE = "mimic-iv-ed-2.2.zip"
NOTE_ARCHIVE_GLOB = "mimic-iv-note*.zip"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Unpack MIMIC raw_original archives into the canonical Layer 1 "
            "raw_unpacked module layout."
        )
    )
    parser.add_argument(
        "--layer1-root",
        required=True,
        help="Path to Methods/Clinical_Database/local_work/Layer 1/MIMIC-IV-3.1.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Re-extract known module deliveries if they already exist.",
    )
    return parser.parse_args()


def safe_rmtree(path: Path, parent: Path) -> None:
    path = path.resolve()
    parent = parent.resolve()
    if parent not in path.parents:
        raise SystemExit(f"Refusing to remove path outside parent: {path}")
    if path.exists():
        shutil.rmtree(path)


def ensure_module_dirs(raw_unpacked_dir: Path) -> None:
    for name in ("core", "ed", "note"):
        (raw_unpacked_dir / name).mkdir(parents=True, exist_ok=True)


def zip_root_names(archive_path: Path) -> list[str]:
    with zipfile.ZipFile(archive_path) as zf:
        roots = sorted({name.split("/", 1)[0] for name in zf.namelist() if name and not name.endswith("/")})
    return roots


def extract_archive(archive_path: Path, destination_dir: Path, overwrite: bool) -> list[Path]:
    roots = [destination_dir / root for root in zip_root_names(archive_path)]
    if overwrite:
        for root in roots:
            if root.exists():
                safe_rmtree(root, destination_dir)
    with zipfile.ZipFile(archive_path) as zf:
        zf.extractall(destination_dir)
    return roots


def main() -> int:
    args = parse_args()
    layer1_root = Path(args.layer1_root).resolve()
    raw_original_dir = layer1_root / "raw_original"
    raw_unpacked_dir = layer1_root / "raw_unpacked"

    if not raw_original_dir.exists():
        raise SystemExit(f"raw_original does not exist: {raw_original_dir}")

    raw_unpacked_dir.mkdir(parents=True, exist_ok=True)
    ensure_module_dirs(raw_unpacked_dir)

    core_archive = raw_original_dir / CORE_ARCHIVE
    if core_archive.exists():
        extracted = extract_archive(core_archive, raw_unpacked_dir / "core", args.overwrite)
        print(f"[unpack] core: {core_archive.name} -> {raw_unpacked_dir / 'core'}")
        for root in extracted:
            print(f"  [root] {root}")
    else:
        print(f"[skip] core archive not found: {core_archive}")

    ed_archive = raw_original_dir / ED_ARCHIVE
    if ed_archive.exists():
        extracted = extract_archive(ed_archive, raw_unpacked_dir / "ed", args.overwrite)
        print(f"[unpack] ed: {ed_archive.name} -> {raw_unpacked_dir / 'ed'}")
        for root in extracted:
            print(f"  [root] {root}")
    else:
        print(f"[skip] ed archive not found: {ed_archive}")

    note_archives = sorted(raw_original_dir.glob(NOTE_ARCHIVE_GLOB))
    if note_archives:
        for note_archive in note_archives:
            extracted = extract_archive(note_archive, raw_unpacked_dir / "note", args.overwrite)
            print(f"[unpack] note: {note_archive.name} -> {raw_unpacked_dir / 'note'}")
            for root in extracted:
                print(f"  [root] {root}")
    else:
        print("[skip] no note archive found under raw_original/")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
