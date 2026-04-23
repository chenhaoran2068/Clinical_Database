from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Query-first numeric summary for a retained Layer 3 parquet asset.",
    )
    parser.add_argument("--input", required=True, help="Path to the Layer 3 parquet file.")
    parser.add_argument("--value-col", required=True, help="Numeric value column to summarize.")
    parser.add_argument(
        "--filter",
        action="append",
        default=[],
        help="Filter rule in the form column:op:value. Supported ops: eq, ne, lt, le, gt, ge, in, isnull, notnull.",
    )
    parser.add_argument(
        "--quantiles",
        default="0.01,0.05,0.50,0.95,0.99",
        help="Comma-separated quantiles to report. Default: 0.01,0.05,0.50,0.95,0.99",
    )
    parser.add_argument(
        "--count-rule",
        action="append",
        default=[],
        help="Extra count rule in the form label:op:value, applied to the value column.",
    )
    parser.add_argument(
        "--output-json",
        help="Optional JSON output path. If omitted, JSON is printed to stdout.",
    )
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


def apply_count_rule(series: pd.Series, rule: str) -> tuple[str, int]:
    label, op, raw_value = split_rule(rule, 3)
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
        raise ValueError(f"Unsupported count-rule operator: {op}")
    return label, int(operations[op].sum())


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)
    if not input_path.exists():
        raise FileNotFoundError(f"Input parquet not found: {input_path}")

    parsed_filters = [parse_filter_rule(rule) for rule in args.filter]
    filter_columns = [column for column, _, _ in parsed_filters]
    read_columns = sorted({args.value_col, *filter_columns})

    df = pd.read_parquet(input_path, columns=read_columns)
    for rule in args.filter:
        df = apply_filter(df, rule)

    value_series = pd.to_numeric(df[args.value_col], errors="coerce")
    quantiles = [float(item.strip()) for item in args.quantiles.split(",") if item.strip()]
    quantile_map = {str(q): None for q in quantiles}
    non_null = value_series.dropna()
    if not non_null.empty:
        quantile_map = {str(q): float(non_null.quantile(q)) for q in quantiles}

    count_rules = {}
    for rule in args.count_rule:
        label, count = apply_count_rule(value_series, rule)
        count_rules[label] = count

    result = {
        "input_path": str(input_path),
        "value_col": args.value_col,
        "applied_filters": args.filter,
        "row_count_after_filter": int(len(df)),
        "value_non_null_count": int(value_series.notna().sum()),
        "value_null_count": int(value_series.isna().sum()),
        "value_unique_non_null_count": int(non_null.nunique()),
        "min": None if non_null.empty else float(non_null.min()),
        "max": None if non_null.empty else float(non_null.max()),
        "mean": None if non_null.empty else float(non_null.mean()),
        "quantiles": quantile_map,
        "count_rules": count_rules,
    }

    output_text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output_json:
        Path(args.output_json).write_text(output_text + "\n", encoding="utf-8")
    else:
        print(output_text)


if __name__ == "__main__":
    main()
