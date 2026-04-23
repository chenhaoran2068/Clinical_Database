from __future__ import annotations

import argparse
import sys
from pathlib import Path


AUTO_ENCODING = "auto"
DUCKDB_ENCODINGS = ("utf-8", "latin-1")
PANDAS_ENCODINGS = ("utf-8", "latin-1", "cp1252")
FALLBACK_CHUNKSIZE = 250_000


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Convert AmsterdamUMCdb raw_unpacked CSV files into local_converted_parquet "
            "files using DuckDB first and a pandas/pyarrow fallback when needed."
        )
    )
    parser.add_argument(
        "--input-dir",
        required=True,
        help="Directory containing unpacked AmsterdamUMCdb CSV files.",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        help="Directory where parquet files should be written.",
    )
    parser.add_argument(
        "--compression",
        default="zstd",
        help="Parquet compression codec. Default: zstd.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing parquet files if they already exist.",
    )
    parser.add_argument(
        "--encoding",
        default=AUTO_ENCODING,
        help=(
            "CSV encoding to use. Default: auto, which tries utf-8 first and "
            "falls back to latin-1 in DuckDB, then utf-8/latin-1/cp1252 in pandas."
        ),
    )
    return parser.parse_args()


def require_duckdb():
    try:
        import duckdb  # type: ignore
    except ImportError as exc:  # pragma: no cover - dependency guard
        raise SystemExit(
            "DuckDB is required for this script. Install it first, for example: "
            "`pip install duckdb`."
        ) from exc
    return duckdb


def require_pandas_pyarrow():
    try:
        import pandas as pd  # type: ignore
        import pyarrow as pa  # type: ignore
        import pyarrow.parquet as pq  # type: ignore
    except ImportError as exc:  # pragma: no cover - dependency guard
        raise SystemExit(
            "pandas and pyarrow are required for the CSV fallback path. "
            "Install them first, for example: `pip install pandas pyarrow`."
        ) from exc
    return pd, pa, pq


def quote_sql_path(path: Path) -> str:
    return str(path.resolve()).replace("'", "''")


def build_temp_output_path(output_path: Path) -> Path:
    return output_path.with_name(f"tmp_{output_path.name}")


def cleanup_temp_output(path: Path) -> None:
    if path.exists():
        path.unlink()


def finalize_output(temp_output_path: Path, output_path: Path) -> None:
    if output_path.exists():
        output_path.unlink()
    temp_output_path.replace(output_path)


def build_duckdb_copy_sql(
    csv_path: Path,
    temp_output_path: Path,
    compression: str,
    encoding: str,
    all_varchar: bool,
) -> str:
    return f"""
        COPY (
            SELECT *
            FROM read_csv_auto(
                '{quote_sql_path(csv_path)}',
                HEADER = TRUE,
                IGNORE_ERRORS = FALSE,
                ENCODING = '{encoding}',
                ALL_VARCHAR = {'TRUE' if all_varchar else 'FALSE'}
            )
        )
        TO '{quote_sql_path(temp_output_path)}'
        (FORMAT PARQUET, COMPRESSION {compression.upper()});
    """


def duckdb_candidate_modes(requested_encoding: str) -> list[tuple[str, bool]]:
    if requested_encoding != AUTO_ENCODING:
        return [(requested_encoding, False), (requested_encoding, True)]

    modes: list[tuple[str, bool]] = []
    for encoding in DUCKDB_ENCODINGS:
        modes.append((encoding, False))
    for encoding in DUCKDB_ENCODINGS:
        modes.append((encoding, True))
    return modes


def pandas_candidate_encodings(requested_encoding: str) -> list[str]:
    if requested_encoding != AUTO_ENCODING:
        return [requested_encoding]
    return list(PANDAS_ENCODINGS)


def convert_with_duckdb(
    con,
    csv_path: Path,
    output_path: Path,
    compression: str,
    requested_encoding: str,
) -> Exception | None:
    temp_output_path = build_temp_output_path(output_path)
    last_error: Exception | None = None

    for encoding, all_varchar in duckdb_candidate_modes(requested_encoding):
        cleanup_temp_output(temp_output_path)
        mode_desc = f"encoding={encoding}, all_varchar={all_varchar}"
        sql = build_duckdb_copy_sql(
            csv_path=csv_path,
            temp_output_path=temp_output_path,
            compression=compression,
            encoding=encoding,
            all_varchar=all_varchar,
        )
        try:
            print(
                f"[convert] {csv_path.name} -> {output_path.name} "
                f"(duckdb; {mode_desc})"
            )
            con.execute(sql)
            finalize_output(temp_output_path, output_path)
            return None
        except Exception as exc:  # pragma: no cover - runtime fallback
            last_error = exc
            print(
                f"[retry] {csv_path.name} failed with duckdb {mode_desc}",
                file=sys.stderr,
            )

    cleanup_temp_output(temp_output_path)
    return last_error


def convert_with_pandas(
    csv_path: Path,
    output_path: Path,
    compression: str,
    requested_encoding: str,
) -> Exception | None:
    pd, pa, pq = require_pandas_pyarrow()
    temp_output_path = build_temp_output_path(output_path)
    last_error: Exception | None = None

    for encoding in pandas_candidate_encodings(requested_encoding):
        cleanup_temp_output(temp_output_path)
        writer = None
        try:
            print(
                f"[fallback] {csv_path.name} -> {output_path.name} "
                f"(pandas; encoding={encoding}, dtype=str)"
            )
            for chunk in pd.read_csv(
                csv_path,
                encoding=encoding,
                encoding_errors="replace",
                dtype=str,
                keep_default_na=False,
                na_filter=False,
                chunksize=FALLBACK_CHUNKSIZE,
                low_memory=False,
            ):
                table = pa.Table.from_pandas(chunk, preserve_index=False)
                if writer is None:
                    writer = pq.ParquetWriter(
                        temp_output_path,
                        table.schema,
                        compression=compression,
                    )
                writer.write_table(table)

            if writer is None:
                table = pa.Table.from_pydict({})
                writer = pq.ParquetWriter(temp_output_path, table.schema, compression=compression)
            writer.close()
            finalize_output(temp_output_path, output_path)
            return None
        except Exception as exc:  # pragma: no cover - runtime fallback
            last_error = exc
            print(
                f"[retry] {csv_path.name} failed with pandas encoding={encoding}",
                file=sys.stderr,
            )
            if writer is not None:
                writer.close()
        finally:
            cleanup_temp_output(temp_output_path)

    return last_error


def main() -> int:
    args = parse_args()
    duckdb = require_duckdb()

    input_dir = Path(args.input_dir).resolve()
    output_dir = Path(args.output_dir).resolve()

    if not input_dir.exists():
        raise SystemExit(f"Input directory does not exist: {input_dir}")
    if not input_dir.is_dir():
        raise SystemExit(f"Input path is not a directory: {input_dir}")

    csv_files = sorted(input_dir.glob("*.csv"))
    if not csv_files:
        raise SystemExit(f"No CSV files found in input directory: {input_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect()
    try:
        for csv_path in csv_files:
            output_path = output_dir / f"{csv_path.stem}.parquet"
            if output_path.exists() and not args.overwrite:
                print(f"[skip] {output_path.name} already exists", file=sys.stderr)
                continue

            duckdb_error = convert_with_duckdb(
                con=con,
                csv_path=csv_path,
                output_path=output_path,
                compression=args.compression,
                requested_encoding=args.encoding,
            )
            if duckdb_error is None:
                continue

            pandas_error = convert_with_pandas(
                csv_path=csv_path,
                output_path=output_path,
                compression=args.compression,
                requested_encoding=args.encoding,
            )
            if pandas_error is None:
                continue

            print(
                f"[error] {csv_path.name} failed in both DuckDB and pandas fallback",
                file=sys.stderr,
            )
            print(f"[error] last duckdb error: {duckdb_error}", file=sys.stderr)
            print(f"[error] last pandas error: {pandas_error}", file=sys.stderr)
            raise pandas_error
    finally:
        con.close()

    print(f"[done] wrote parquet files to {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
