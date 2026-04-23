from __future__ import annotations

import argparse
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path


LARGE_TABLE_ROWS_PER_PART = 10_000_000
REGULAR_MODULES = ("hosp", "icu", "ed", "note")


@dataclass(frozen=True)
class SourceTask:
    module: str
    source_path: Path
    output_dir: Path
    output_name: str
    split_prefix: str | None = None
    split_rows_per_part: int | None = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Convert MIMIC raw_unpacked source files into local_converted_parquet "
            "using stable Layer 1 module rules."
        )
    )
    parser.add_argument(
        "--layer1-root",
        required=True,
        help="Path to Methods/Clinical_Database/local_work/Layer 1/MIMIC-IV-3.1.",
    )
    parser.add_argument(
        "--compression",
        default="zstd",
        help="Parquet compression codec. Default: zstd.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing parquet outputs.",
    )
    parser.add_argument(
        "--modules",
        nargs="+",
        choices=REGULAR_MODULES,
        help="Optional subset of modules to convert. Default: all modules.",
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


def require_pyarrow():
    try:
        import pyarrow as pa  # type: ignore
        import pyarrow.parquet as pq  # type: ignore
    except ImportError as exc:  # pragma: no cover
        raise SystemExit(
            "pyarrow is required. Install it first, for example: `pip install pyarrow`."
        ) from exc
    return pa, pq


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


def build_duckdb_copy_sql(csv_path: Path, temp_output_path: Path, compression: str) -> str:
    return build_duckdb_copy_sql_mode(
        csv_path=csv_path,
        temp_output_path=temp_output_path,
        compression=compression,
        sample_all=False,
        all_varchar=False,
    )


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


def single_parquet_task(module: str, source_path: Path, output_root: Path) -> SourceTask:
    output_dir = output_root / module
    return SourceTask(
        module=module,
        source_path=source_path,
        output_dir=output_dir,
        output_name=f"{normalize_table_stem(source_path.name)}.parquet",
    )


def discover_tasks(layer1_root: Path, selected_modules: set[str]) -> tuple[list[SourceTask], list[str]]:
    raw_unpacked = layer1_root / "raw_unpacked"
    output_root = layer1_root / "local_converted_parquet"
    tasks: list[SourceTask] = []
    notes: list[str] = []

    core_hosp_dirs = sorted(raw_unpacked.glob("core/mimic-iv-*/hosp")) if "hosp" in selected_modules else []
    core_icu_dirs = sorted(raw_unpacked.glob("core/mimic-iv-*/icu")) if "icu" in selected_modules else []
    ed_dirs = sorted(raw_unpacked.glob("ed/mimic-iv-ed-*/ed")) if "ed" in selected_modules else []
    note_dirs = sorted(raw_unpacked.glob("note/*/note")) if "note" in selected_modules else []

    if "hosp" in selected_modules and not core_hosp_dirs:
        notes.append("missing core hosp source under raw_unpacked/core/")
    if "icu" in selected_modules and not core_icu_dirs:
        notes.append("missing core icu source under raw_unpacked/core/")
    if "ed" in selected_modules and not ed_dirs:
        notes.append("missing ed source under raw_unpacked/ed/")
    if "note" in selected_modules and not note_dirs:
        notes.append("missing note source under raw_unpacked/note/")

    for hosp_dir in core_hosp_dirs:
        for source_path in sorted(hosp_dir.glob("*.csv.gz")):
            stem = normalize_table_stem(source_path.name)
            if stem == "labevents":
                tasks.append(
                    SourceTask(
                        module="hosp",
                        source_path=source_path,
                        output_dir=output_root / "hosp",
                        output_name="",
                        split_prefix="labevents_part",
                        split_rows_per_part=LARGE_TABLE_ROWS_PER_PART,
                    )
                )
            else:
                tasks.append(single_parquet_task("hosp", source_path, output_root))

    for icu_dir in core_icu_dirs:
        for source_path in sorted(icu_dir.glob("*.csv.gz")):
            stem = normalize_table_stem(source_path.name)
            if stem == "chartevents":
                tasks.append(
                    SourceTask(
                        module="icu",
                        source_path=source_path,
                        output_dir=output_root / "icu",
                        output_name="",
                        split_prefix="chartevents_part",
                        split_rows_per_part=LARGE_TABLE_ROWS_PER_PART,
                    )
                )
            else:
                tasks.append(single_parquet_task("icu", source_path, output_root))

    for ed_dir in ed_dirs:
        for source_path in sorted(ed_dir.glob("*.csv.gz")):
            tasks.append(single_parquet_task("ed", source_path, output_root))

    for note_dir in note_dirs:
        for source_path in sorted(note_dir.glob("*.csv.gz")):
            tasks.append(single_parquet_task("note", source_path, output_root))

    return tasks, notes


def convert_single_csv(con, task: SourceTask, compression: str, overwrite: bool) -> None:
    task.output_dir.mkdir(parents=True, exist_ok=True)
    output_path = task.output_dir / task.output_name
    if output_path.exists() and not overwrite:
        print(f"[skip] {output_path}", file=sys.stderr)
        return

    temp_output_path = build_temp_output_path(output_path)
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
            print(f"[convert] {task.source_path} -> {output_path} ({label})")
            con.execute(sql)
            finalize_output(temp_output_path, output_path)
            return
        except Exception as exc:
            last_error = exc
            print(f"[retry] {task.source_path.name} failed in mode: {label}", file=sys.stderr)
    raise last_error  # type: ignore[misc]


def split_large_parquet(
    full_parquet_path: Path,
    staging_dir: Path,
    prefix: str,
    rows_per_part: int,
    compression: str,
) -> int:
    pa, pq = require_pyarrow()
    staging_dir.mkdir(parents=True, exist_ok=True)
    parquet_file = pq.ParquetFile(full_parquet_path)
    part_index = 0
    current_rows = 0
    writer = None
    schema = parquet_file.schema_arrow

    def open_writer(index: int):
        part_path = staging_dir / f"{prefix}_{index:03d}.parquet"
        return pq.ParquetWriter(part_path, schema, compression=compression)

    try:
        for batch in parquet_file.iter_batches(batch_size=250_000):
            remaining_offset = 0
            while remaining_offset < batch.num_rows:
                if writer is None:
                    writer = open_writer(part_index)
                remaining_capacity = rows_per_part - current_rows
                slice_length = min(remaining_capacity, batch.num_rows - remaining_offset)
                table = pa.Table.from_batches([batch.slice(remaining_offset, slice_length)], schema=schema)
                writer.write_table(table)
                current_rows += slice_length
                remaining_offset += slice_length

                if current_rows == rows_per_part:
                    writer.close()
                    writer = None
                    current_rows = 0
                    part_index += 1

        if writer is not None:
            writer.close()
            writer = None
            part_index += 1
    finally:
        if writer is not None:
            writer.close()

    return part_index


def convert_large_split_csv(con, task: SourceTask, compression: str, overwrite: bool) -> None:
    if task.split_prefix is None or task.split_rows_per_part is None:
        raise ValueError("Large split task is missing split configuration.")

    task.output_dir.mkdir(parents=True, exist_ok=True)
    existing_outputs = sorted(task.output_dir.glob(f"{task.split_prefix}_*.parquet"))
    if existing_outputs and not overwrite:
        print(f"[skip] {task.split_prefix} already exists under {task.output_dir}", file=sys.stderr)
        return

    temp_full_path = task.output_dir / f"tmp_{task.split_prefix}_full.parquet"
    staging_dir = task.output_dir / f"tmp_{task.split_prefix}_staging"
    cleanup_path(temp_full_path)
    cleanup_path(staging_dir)

    last_error = None
    for sample_all, all_varchar, label in duckdb_modes():
        cleanup_path(temp_full_path)
        sql = build_duckdb_copy_sql_mode(
            csv_path=task.source_path,
            temp_output_path=temp_full_path,
            compression=compression,
            sample_all=sample_all,
            all_varchar=all_varchar,
        )
        try:
            print(f"[convert-full] {task.source_path} -> {temp_full_path} ({label})")
            con.execute(sql)
            break
        except Exception as exc:
            last_error = exc
            print(f"[retry] {task.source_path.name} failed in mode: {label}", file=sys.stderr)
    else:
        raise last_error  # type: ignore[misc]

    print(f"[split] {temp_full_path} -> {task.output_dir / (task.split_prefix + '_*.parquet')}")
    part_count = split_large_parquet(
        full_parquet_path=temp_full_path,
        staging_dir=staging_dir,
        prefix=task.split_prefix,
        rows_per_part=task.split_rows_per_part,
        compression=compression,
    )

    for old_path in existing_outputs:
        old_path.unlink()
    for staged_path in sorted(staging_dir.glob("*.parquet")):
        final_path = task.output_dir / staged_path.name
        if final_path.exists():
            final_path.unlink()
        staged_path.replace(final_path)
    cleanup_path(staging_dir)
    cleanup_path(temp_full_path)
    print(f"[done] {task.split_prefix}: {part_count} parquet parts")


def main() -> int:
    args = parse_args()
    duckdb = require_duckdb()

    layer1_root = Path(args.layer1_root).resolve()
    raw_unpacked = layer1_root / "raw_unpacked"
    output_root = layer1_root / "local_converted_parquet"

    if not raw_unpacked.exists():
        raise SystemExit(f"raw_unpacked does not exist: {raw_unpacked}")

    selected_modules = set(args.modules or REGULAR_MODULES)

    output_root.mkdir(parents=True, exist_ok=True)
    for module in selected_modules:
        (output_root / module).mkdir(parents=True, exist_ok=True)

    tasks, notes = discover_tasks(layer1_root, selected_modules)
    if notes:
        for note in notes:
            print(f"[note] {note}")
    if not tasks:
        raise SystemExit("No convertible MIMIC source files were discovered under raw_unpacked.")

    con = duckdb.connect()
    try:
        for task in tasks:
            if task.split_prefix is not None:
                convert_large_split_csv(con, task, args.compression, args.overwrite)
            else:
                convert_single_csv(con, task, args.compression, args.overwrite)
    finally:
        con.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
