from __future__ import annotations

import re
from typing import Any


LOCAL_ONLY_RULES: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("source itemid or concept code", re.compile(r"\b(?:itemid|concept[_ ](?:code|id))s?\b", re.IGNORECASE)),
    ("source table or source field wording", re.compile(r"\bsource (?:table|tables|column|columns|field|fields|itemids?|items?)\b", re.IGNORECASE)),
    ("raw source field token", re.compile(r"\bsource_[a-z0-9_]+\b", re.IGNORECASE)),
    ("raw table reference", re.compile(r"\b(?:hosp|icu)\.[a-z0-9_]+\b", re.IGNORECASE)),
    ("source relation table name", re.compile(r"\b(?:chartevents|labevents|omr|d_labitems|d_items|admissions_core)\b", re.IGNORECASE)),
    ("derived-table implementation detail", re.compile(r"\bderived table\b", re.IGNORECASE)),
    ("operational id field", re.compile(r"\b(?:hadm_id|stay_id|subject_id|admissionid)\b", re.IGNORECASE)),
    (
        "operational linkage or source-status field",
        re.compile(
            r"\b(?:stay_link_status|cleaning_status|source_rule_summary|source_label_raw|source_itemid_raw|"
            r"source_hadm_id_raw|source_specimen_raw|specimen_class|default_baseline_eligibility|"
            r"route_to_child_asset|hospital_only_no_icu_overlap|inferred_unique_stay)\b",
            re.IGNORECASE,
        ),
    ),
    ("local field token", re.compile(r"\b[a-z0-9]+(?:_[a-z0-9]+){1,}_(?:raw|status|flag)\b", re.IGNORECASE)),
    (
        "build or review artifact",
        re.compile(
            r"\b(?:query_summary|query summaries|extract_code|build log|grouped review|rerun assessment|"
            r"preview output|preview outputs|completeness backfill)\b",
            re.IGNORECASE,
        ),
    ),
    ("local file-format detail", re.compile(r"\bparquet\b", re.IGNORECASE)),
    ("raw-source implementation detail", re.compile(r"\b(?:raw[- ]source|raw-vs-official|official comparison column)\b", re.IGNORECASE)),
    (
        "local threshold or outlier detail",
        re.compile(
            r"\b(?:kept range|cleaned threshold|threshold decisions?|outlier columns?|normalized and outlier columns?)\b",
            re.IGNORECASE,
        ),
    ),
    ("study-layer workflow note", re.compile(r"\b(?:study-specific|study layer|grouped user review|retained threshold)\b", re.IGNORECASE)),
)


def normalize_public_card_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def find_local_only_match_labels(text: Any, limit: int = 5) -> list[str]:
    normalized = normalize_public_card_text(text)
    if not normalized:
        return []

    labels: list[str] = []
    for label, pattern in LOCAL_ONLY_RULES:
        if pattern.search(normalized):
            labels.append(label)
            if len(labels) >= limit:
                break
    return labels


def contains_local_only_detail(text: Any) -> bool:
    return bool(find_local_only_match_labels(text, limit=1))
