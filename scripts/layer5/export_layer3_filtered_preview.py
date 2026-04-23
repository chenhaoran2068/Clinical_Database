from __future__ import annotations

import argparse
from pathlib import Path
import sys

import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export a small filtered preview from a retained Layer 3 parquet asset.",
    )
    parser.add_argument("--input", required=True, help="Path to the Layer 3 parquet file.")
    parser.add_argument(
        "--columns",
        required=True,
        help="Comma-separated columns to return.",
    )
    parser.add_argument(
        "--filter",
        action="append",
        default=[],
        help="Filter rule in the form column:op:value. Supported ops: eq, ne, lt, le, gt, ge, in, isnull, notnull.",
    )
    parser.add_argument("--sort-by", help="Optional sort column.")
    parser.add_argument("--descending", action="store_true", help="Sort descending if --sort-by is used.")
    parser.add_argument("--limit", type=int, default=50, help="Maximum number of rows to return.")
    parser.add_argument("--output-csv", help="Optional CSV output path. If omitted, CSV is printed to stdout.")
    return parser.parse_args()


def split_rule(rule: str, expected_parts: int) -> list[str]:
    parts = rule.split(":", expected_parts - 1)
    if len(parts) != expected_parts:
        raise ValueError(f"Invalid rule: {rule}")
    return parts


def parse_filter_rule(rule: str) -> tuple[str, str, str | None]:
    parts = rule.split(":", 2)
    if len(parts) == 2 and parts[1] in {"isnull", "notnull"}:
        return parts[0], parts[1], None
    if len(parts) == 3:
        return parts[0], parts[1], parts[2]
    raise ValueError(f"Invalid filter rule: {rule}")


def coerce_scalar(series: pd.Series, raw_value: str):
    if pd.api.types.is_datetime64_any_dtype(series):
        return pd.to_datetime(raw_value)
    if pd.api.types.is_bool_dtype(series):
        lowered = raw_value.strip().lower()
        if lowered in {"true", "1", "yes"}:
            return True
        if lowered in {"false", "0", "no"}:
            return False
        raise ValueError(f"Cannot parse boolean value: {raw_value}")
    if pd.api.types.is_integer_dtype(series) or pd.api.types.is_float_dtype(series):
        return pd.to_numeric(raw_value)
    return raw_value


def apply_filter(df: pd.DataFrame, rule: str) -> pd.DataFrame:
    column, op, raw_value = parse_filter_rule(rule)
    if column not in df.columns:
        raise KeyError(f"Filter column not found: {column}")

    series = df[column]
    if op == "isnull":
        return df[series.isna()]
    if op == "notnull":
        return df[series.notna()]

    if op == "in":
        values = [coerce_scalar(series, value.strip()) for value in raw_value.split(",")]
        return df[series.isin(values)]

    value = coerce_scalar(series, raw_value)
    operations = {
        "eq": series == value,
        "ne": series != value,
        "lt": series < value,
        "le": series <= value,
        "gt": series > value,
        "ge": series >= value,
    }
    if op not in operations:
        raise ValueError(f"Unsupported operator: {op}")
    return df[operations[op]]


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)
    if not input_path.exists():
        raise FileNotFoundError(f"Input parquet not found: {input_path}")

    requested_columns = [column.strip() for column in args.columns.split(",") if column.strip()]
    parsed_filters = [parse_filter_rule(rule) for rule in args.filter]
    filter_columns = [column for column, _, _ in parsed_filters]
    read_columns = sorted({*requested_columns, *filter_columns, *( [args.sort_by] if args.sort_by else [] )})

    df = pd.read_parquet(input_path, columns=read_columns)
    for rule in args.filter:
        df = apply_filter(df, rule)

    if args.sort_by:
        df = df.sort_values(args.sort_by, ascending=not args.descending, kind="stable")

    preview = df[requested_columns].head(args.limit)
    if args.output_csv:
        Path(args.output_csv).parent.mkdir(parents=True, exist_ok=True)
        preview.to_csv(args.output_csv, index=False)
    else:
        preview.to_csv(sys.stdout, index=False)


if __name__ == "__main__":
    main()
