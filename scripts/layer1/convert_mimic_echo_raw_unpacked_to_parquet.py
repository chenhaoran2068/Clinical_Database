from __future__ import annotations

import argparse
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path


CANONICAL_ECHO_ROOT = "ECHO-1.0"
IGNORED_SOURCE_FILES = {"LICENSE.txt", "SHA256SUMS.txt", "README.txt"}


@dataclass(frozen=True)
class SourceTask:
    source_path: Path
    output_path: Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Convert MIMIC-IV-ECHO v1.0 raw_unpacked source files into "
            "local_converted_parquet under the standalone sibling-module root."
        )
    )
    parser.add_argument(
        "--layer1-root",
        required=True,
        help="Path to Methods/Clinical_Database/local_work/Layer 1/MIMIC-IV-ECHO-1.0.",
    )
    parser.add_argument(
        "--compression",
        default="zstd",
        help="Parquet compression codec. Default: zstd.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing parquet outputs for files that are rebuilt from raw_unpacked.",
    )
    return parser.parse_args()


def require_duckdb():
    try:
        import duckdb  # type: ignore
    except ImportError as exc:  # pragma: no cover
        raise SystemExit(
            "DuckDB is required. Install it first, for example: `pip install duckdb`."
        ) from exc
    return duckdb


def quote_sql_path(path: Path) -> str:
    return str(path.resolve()).replace("'", "''")


def build_temp_output_path(output_path: Path) -> Path:
    return output_path.with_name(f"tmp_{output_path.name}")


def cleanup_path(path: Path) -> None:
    if path.is_dir():
        shutil.rmtree(path)
    elif path.exists():
        path.unlink()


def finalize_output(temp_output_path: Path, output_path: Path) -> None:
    if output_path.exists():
        output_path.unlink()
    temp_output_path.replace(output_path)


def build_duckdb_copy_sql_mode(
    csv_path: Path,
    temp_output_path: Path,
    compression: str,
    sample_all: bool,
    all_varchar: bool,
) -> str:
    sample_size_clause = "SAMPLE_SIZE = -1," if sample_all else ""
    return f"""
        COPY (
            SELECT *
            FROM read_csv_auto(
                '{quote_sql_path(csv_path)}',
                HEADER = TRUE,
                {sample_size_clause}
                NULLSTR = ['NULL'],
                ALL_VARCHAR = {'TRUE' if all_varchar else 'FALSE'}
            )
        )
        TO '{quote_sql_path(temp_output_path)}'
        (FORMAT PARQUET, COMPRESSION {compression.upper()});
    """


def duckdb_modes() -> list[tuple[bool, bool, str]]:
    return [
        (False, False, "default-sample / typed"),
        (True, False, "full-sample / typed"),
        (False, True, "default-sample / all-varchar"),
        (True, True, "full-sample / all-varchar"),
    ]


def normalize_table_stem(file_name: str) -> str:
    if file_name.endswith(".csv.gz"):
        return file_name[:-7]
    if file_name.endswith(".csv"):
        return file_name[:-4]
    return Path(file_name).stem


def discover_tasks(layer1_root: Path) -> tuple[list[SourceTask], list[str]]:
    source_root = layer1_root / "raw_unpacked" / CANONICAL_ECHO_ROOT
    output_root = layer1_root / "local_converted_parquet"
    notes: list[str] = []

    if not source_root.exists():
        raise SystemExit(f"canonical ECHO source root does not exist: {source_root}")

    tasks: list[SourceTask] = []
    for source_path in sorted(source_root.glob("*.csv*")):
        if source_path.name in IGNORED_SOURCE_FILES:
            continue
        if source_path.suffix not in {".csv", ".gz"}:
            continue
        tasks.append(
            SourceTask(
                source_path=source_path,
                output_path=output_root / f"{normalize_table_stem(source_path.name)}.parquet",
            )
        )

    if not tasks:
        notes.append("no convertible ECHO source files discovered under raw_unpacked/ECHO-1.0/")

    companion_summary_path = output_root / "full_echo_census_report.parquet"
    if companion_summary_path.exists():
        notes.append(
            "existing companion summary retained without rebuild: "
            f"{companion_summary_path}"
        )

    return tasks, notes


def convert_single_csv(con, task: SourceTask, compression: str, overwrite: bool) -> None:
    task.output_path.parent.mkdir(parents=True, exist_ok=True)
    if task.output_path.exists() and not overwrite:
        print(f"[skip] {task.output_path}", file=sys.stderr)
        return

    temp_output_path = build_temp_output_path(task.output_path)
    cleanup_path(temp_output_path)
    last_error = None
    for sample_all, all_varchar, label in duckdb_modes():
        cleanup_path(temp_output_path)
        sql = build_duckdb_copy_sql_mode(
            csv_path=task.source_path,
            temp_output_path=temp_output_path,
            compression=compression,
            sample_all=sample_all,
            all_varchar=all_varchar,
        )
        try:
            print(f"[convert] {task.source_path} -> {task.output_path} ({label})")
            con.execute(sql)
            finalize_output(temp_output_path, task.output_path)
            return
        except Exception as exc:
            last_error = exc
            print(f"[retry] {task.source_path.name} failed in mode: {label}", file=sys.stderr)
    raise last_error  # type: ignore[misc]


def main() -> int:
    args = parse_args()
    duckdb = require_duckdb()

    layer1_root = Path(args.layer1_root).resolve()
    output_root = layer1_root / "local_converted_parquet"
    output_root.mkdir(parents=True, exist_ok=True)

    tasks, notes = discover_tasks(layer1_root)
    for note in notes:
        print(f"[note] {note}")
    if not tasks:
        raise SystemExit("No convertible MIMIC-IV-ECHO source files were discovered.")

    con = duckdb.connect()
    try:
        for task in tasks:
            convert_single_csv(con, task, args.compression, args.overwrite)
    finally:
        con.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
