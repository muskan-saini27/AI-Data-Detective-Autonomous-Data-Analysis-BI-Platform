from __future__ import annotations
import re
from typing import Any
import pandas as pd


def normalize_name(v: Any) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(v).strip().lower()).strip()


def explicit_identifier_name(col: Any) -> bool:
    n = normalize_name(col)
    compact = n.replace(" ", "_")
    exact = {"id", "identifier", "uuid", "code", "key"}
    if n in exact:
        return True
    if any(x in n for x in [" id", " identifier", " uuid"]):
        return True
    if compact.endswith(("_id", "_uuid", "_code", "_key")):
        return True
    return False


def looks_like_identifier(col: Any, s: pd.Series) -> bool:
    # Prefer explicit naming. We deliberately do NOT classify numeric columns
    # as IDs merely because most values are unique (salary, score, price, etc.).
    if explicit_identifier_name(col):
        return True
    non = s.dropna()
    if len(non) < 15:
        return False
    # High-cardinality text can be an implicit record key, but only for
    # simple short values. Date-like values are handled before this function.
    if pd.api.types.is_numeric_dtype(s) or pd.api.types.is_datetime64_any_dtype(s):
        return False
    uniq = non.nunique() / len(non)
    if uniq >= 0.995:
        sample = non.astype(str).head(100)
        return bool(sample.str.len().median() <= 32 and sample.str.contains(r"\s", regex=True).mean() < 0.5)
    return False


def try_datetime(series: pd.Series):
    if pd.api.types.is_datetime64_any_dtype(series):
        return True, pd.to_datetime(series, errors="coerce")
    if pd.api.types.is_numeric_dtype(series):
        return False, None
    non = series.dropna()
    if len(non) < 5:
        return False, None
    # pandas >=2 supports format='mixed'; fall back for older versions.
    try:
        converted = pd.to_datetime(non, errors="coerce", format="mixed")
    except TypeError:
        converted = pd.to_datetime(non, errors="coerce")
    if converted.notna().mean() >= 0.8:
        try:
            full = pd.to_datetime(series, errors="coerce", format="mixed")
        except TypeError:
            full = pd.to_datetime(series, errors="coerce")
        return True, full
    return False, None


def infer_schema(df: pd.DataFrame) -> dict[str, Any]:
    numeric, categorical, dates, ids, text, booleans = [], [], [], [], [], []

    for c in df.columns:
        s = df[c]

        # Explicit ID/code columns first.
        if explicit_identifier_name(c):
            ids.append(c)
            continue

        # Date detection before high-cardinality text detection.
        is_dt, _ = try_datetime(s)
        if is_dt:
            dates.append(c)
            continue

        if pd.api.types.is_bool_dtype(s):
            booleans.append(c)
            categorical.append(c)
            continue

        if pd.api.types.is_numeric_dtype(s):
            numeric.append(c)
            continue

        if looks_like_identifier(c, s):
            ids.append(c)
            continue

        nunique = s.nunique(dropna=True)
        if nunique <= max(20, min(50, max(len(df) * 0.2, 1))):
            categorical.append(c)
        else:
            text.append(c)

    metric_preference = [
        "revenue", "sales", "sale", "amount", "profit", "income", "price",
        "cost", "salary", "score", "marks", "grade", "quantity", "units",
        "count", "total", "value", "balance", "rate", "percentage", "percent"
    ]

    def metric_score(c):
        n = normalize_name(c)
        priority = sum(4 for term in metric_preference if term in n)
        s = pd.to_numeric(df[c], errors="coerce").dropna()
        var = float(s.var()) if len(s) > 1 else 0.0
        return (priority, var, int(len(s)))

    metrics = sorted(numeric, key=metric_score, reverse=True)

    dimension_preference = [
        "category", "region", "department", "segment", "class", "type", "group",
        "status", "gender", "country", "state", "city", "product", "channel", "source"
    ]

    def dimension_score(c):
        n = normalize_name(c)
        priority = sum(4 for term in dimension_preference if term in n)
        cardinality = df[c].nunique(dropna=True)
        return (priority, -cardinality)

    dimensions = sorted(categorical, key=dimension_score, reverse=True)

    return {
        "numeric_columns": numeric,
        "metric_columns": metrics,
        "categorical_columns": categorical,
        "dimension_columns": dimensions,
        "datetime_columns": dates,
        "identifier_columns": ids,
        "text_columns": text,
        "boolean_columns": booleans,
        "primary_metric": metrics[0] if metrics else None,
        "primary_dimension": dimensions[0] if dimensions else None,
        "date_column": dates[0] if dates else None,
    }
