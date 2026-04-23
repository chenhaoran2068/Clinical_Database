from __future__ import annotations

import argparse
import gzip
import shutil
from pathlib import Path


NOTE_TABLES = (
    "discharge",
    "discharge_detail",
    "radiology",
    "radiology_detail",
)
PROXY_ROOT_NAME = "mimic-iv-note-2.2_local_reconstructed_from_parquet"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Reconstruct a local MIMIC note raw_unpacked proxy from existing "
            "local_converted_parquet note tables. This is a local source proxy, "
            "not an official PhysioNet raw delivery."
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
        help="Replace the existing reconstructed note proxy root if it exists.",
    )
    return parser.parse_args()


def require_pandas_pyarrow():
    try:
        import pandas as pd  # type: ignore
        import pyarrow.parquet as pq  # type: ignore
    except ImportError as exc:  # pragma: no cover
        raise SystemExit(
            "pandas and pyarrow are required. Install them first, for example: "
            "`pip install pandas pyarrow`."
        ) from exc
    return pd, pq


def safe_rmtree(path: Path, parent: Path) -> None:
    path = path.resolve()
    parent = parent.resolve()
    if parent not in path.parents:
        raise SystemExit(f"Refusing to remove path outside parent: {path}")
    if path.exists():
        shutil.rmtree(path)


def normalize_datetime_columns(df) -> None:
    for column in df.columns:
        series = df[column]
        if str(series.dtype).startswith("datetime64"):
            formatted = series.dt.strftime("%Y-%m-%d %H:%M:%S.%f")
            formatted = formatted.where(~series.isna(), "")
            formatted = formatted.str.replace(r"\.?0+$", "", regex=True)
            df[column] = formatted


def write_parquet_as_csv_gz(parquet_path: Path, csv_gz_path: Path) -> int:
    pd, pq = require_pandas_pyarrow()
    parquet_file = pq.ParquetFile(parquet_path)
    csv_gz_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = csv_gz_path.with_name(f"tmp_{csv_gz_path.name}")
    if temp_path.exists():
        temp_path.unlink()

    total_rows = 0
    with gzip.open(temp_path, "wt", encoding="utf-8", newline="") as handle:
        first = True
        for batch in parquet_file.iter_batches(batch_size=100_000):
            df = batch.to_pandas()
            normalize_datetime_columns(df)
            df.to_csv(
                handle,
                index=False,
                header=first,
                na_rep="",
                lineterminator="\n",
            )
            total_rows += len(df)
            first = False

    if csv_gz_path.exists():
        csv_gz_path.unlink()
    temp_path.replace(csv_gz_path)
    return total_rows


def main() -> int:
    args = parse_args()
    layer1_root = Path(args.layer1_root).resolve()
    note_parquet_dir = layer1_root / "local_converted_parquet" / "note"
    proxy_root = layer1_root / "raw_unpacked" / "note" / PROXY_ROOT_NAME
    proxy_note_dir = proxy_root / "note"

    if not note_parquet_dir.exists():
        raise SystemExit(f"Note parquet directory does not exist: {note_parquet_dir}")

    if proxy_root.exists():
        if not args.overwrite:
            raise SystemExit(
                f"Reconstructed note proxy already exists: {proxy_root}. Use --overwrite to replace it."
            )
        safe_rmtree(proxy_root, layer1_root / "raw_unpacked" / "note")

    proxy_note_dir.mkdir(parents=True, exist_ok=True)

    for table_name in NOTE_TABLES:
        parquet_path = note_parquet_dir / f"{table_name}.parquet"
        if not parquet_path.exists():
            raise SystemExit(f"Missing note parquet input: {parquet_path}")
        output_path = proxy_note_dir / f"{table_name}.csv.gz"
        rows = write_parquet_as_csv_gz(parquet_path, output_path)
        print(f"[reconstruct] {parquet_path.name} -> {output_path.name} ({rows} rows)")

    print(f"[done] reconstructed local note raw_unpacked proxy at {proxy_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
