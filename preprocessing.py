# preprocess_unify.py
# One-shot pipeline:
# 1) Add surrogate IDs + snake-case columns into clean_<table> (from original tables)
# 2) Preprocess those clean_<table> tables
# 3) Export Parquet/CSV to ./data/clean

import os
import re
import sys
import sqlite3
from typing import Dict, List, Optional

import numpy as np
import pandas as pd


# =========================
# Helpers & small utilities
# =========================

DATE_HINTS = ("date", "dob", "created", "updated", "time")

def snake_case(name: str) -> str:
    """Convert column/table names to snake_case."""
    name = str(name).strip()
    name = re.sub(r"[^\w]+", "_", name)
    name = re.sub(r"__+", "_", name)
    return name.strip("_").lower()

def quote_ident(name: str) -> str:
    """Quote an SQLite identifier (table/column)."""
    return '"' + str(name).replace('"', '""') + '"'

def list_tables(conn: sqlite3.Connection, include_clean: bool = True) -> List[str]:
    """Return tables in the DB (optionally include/exclude clean_*)."""
    rows = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"
    ).fetchall()
    tables = [r[0] for r in rows]
    if not include_clean:
        tables = [t for t in tables if not t.startswith("clean_")]
    return sorted(tables)

def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def has_id_like_column(df: pd.DataFrame) -> bool:
    """Heuristic: does df have an ID-like column already?"""
    cols = [c.lower() for c in df.columns]
    if "id" in cols or "uuid" in cols or "guid" in cols:
        return True
    if any(c.endswith("_id") for c in cols):
        return True
    # avoid false positives like 'ssid' or 'grid'
    if "ssid" in cols or "grid" in cols:
        return False
    return False

def choose_surrogate_id_name(raw_table_name: str, existing_cols: List[str]) -> str:
    """Create a surrogate ID column name that doesn't collide."""
    base = f"{snake_case(raw_table_name)}_id"
    cand = base
    i = 2
    lower_cols = {c.lower() for c in existing_cols}
    while cand.lower() in lower_cols:
        cand = f"{base}_{i}"
        i += 1
    return cand


# =========================
# Preprocessing primitives
# =========================

def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [snake_case(c) for c in df.columns]
    return df

def trim_and_normalize_strings(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    obj_cols = df.select_dtypes(include=["object", "string"]).columns
    for col in obj_cols:
        df[col] = (
            df[col]
            .astype("string")
            .str.strip()
            .replace({"": pd.NA})
        )
    return df

def coerce_dates(df: pd.DataFrame, date_cols: Optional[List[str]] = None) -> pd.DataFrame:
    df = df.copy()
    candidates = set(date_cols or [])
    for c in df.columns:
        if any(h in c for h in DATE_HINTS):
            candidates.add(c)
    for c in candidates:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce", infer_datetime_format=True, utc=False)
    return df

def coerce_numeric(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for col in df.columns:
        if df[col].dtype == "object":
            # try numeric conversion accounting for $, %, commas, spaces
            converted = pd.to_numeric(df[col].astype(str).str.replace(r"[,$% ]", "", regex=True), errors="coerce")
            if converted.notna().mean() >= 0.7:  # adopt if 70%+ rows convert
                df[col] = converted
    return df

def basic_missing_value_fill(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for col in df.columns:
        s = df[col]
        if pd.api.types.is_numeric_dtype(s):
            if s.isna().any():
                df[col] = s.fillna(s.median())
        elif pd.api.types.is_datetime64_any_dtype(s):
            # often better to leave as NaT; customize if you want forward-fill per group
            pass
        else:
            if s.isna().any():
                mode = s.mode(dropna=True)
                if not mode.empty:
                    df[col] = s.fillna(mode.iloc[0])
    return df

def drop_exact_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop_duplicates(ignore_index=True)

def remove_outliers_iqr(df: pd.DataFrame, cols: Optional[List[str]] = None, k: float = 1.5) -> pd.DataFrame:
    """Optional: filter numeric outliers via IQR for provided cols or all numeric cols."""
    df = df.copy()
    target_cols = cols or list(df.select_dtypes(include=[np.number]).columns)
    if not target_cols:
        return df
    mask = pd.Series(True, index=df.index)
    for c in target_cols:
        q1 = df[c].quantile(0.25)
        q3 = df[c].quantile(0.75)
        iqr = q3 - q1
        if pd.isna(iqr) or iqr == 0:
            continue
        lo = q1 - k * iqr
        hi = q3 + k * iqr
        mask &= df[c].between(lo, hi) | df[c].isna()
    return df[mask].reset_index(drop=True)

def preprocess_df(df: pd.DataFrame,
                  date_cols: Optional[List[str]] = None,
                  outlier_cols: Optional[List[str]] = None) -> pd.DataFrame:
    df = standardize_columns(df)               # idempotent
    df = trim_and_normalize_strings(df)
    df = coerce_dates(df, date_cols=date_cols)
    df = coerce_numeric(df)
    df = basic_missing_value_fill(df)
    df = drop_exact_duplicates(df)
    if outlier_cols:
        df = remove_outliers_iqr(df, cols=outlier_cols, k=1.5)
    return df


# =========================
# Phase A: Create clean_* with surrogate IDs when needed
# =========================

def bootstrap_clean_tables_with_ids(conn: sqlite3.Connection) -> List[str]:
    """
    From all non-clean tables:
      - read each table,
      - snake-case column names,
      - add surrogate <table>_id if no id-like col,
      - write to clean_<snake_table>.
    Returns the list of clean table names created/updated.
    """
    original_tables = list_tables(conn, include_clean=False)
    clean_tables = []

    for t in original_tables:
        # read original table
        df = pd.read_sql_query(f'SELECT * FROM {quote_ident(t)};', conn)
        # standardize column names once
        df = standardize_columns(df)

        # add surrogate ID if no existing id-like
        if not has_id_like_column(df):
            id_col = choose_surrogate_id_name(t, list(df.columns))
            df.insert(0, id_col, range(1, len(df) + 1))

        # destination table name
        clean_name = f"clean_{snake_case(t)}"
        df.to_sql(clean_name, conn, if_exists="replace", index=False)

        # index any *_id columns
        for col in df.columns:
            if col.lower().endswith("_id"):
                idx_name = f"idx_{clean_name}_{snake_case(col)}"
                conn.execute(
                    f"CREATE INDEX IF NOT EXISTS {quote_ident(idx_name)} "
                    f"ON {quote_ident(clean_name)}({quote_ident(col)});"
                )

        clean_tables.append(clean_name)

    conn.commit()
    return clean_tables


# =========================
# Phase B: Preprocess clean_* tables in place
# =========================

def preprocess_clean_tables(conn: sqlite3.Connection,
                            export_dir: str = "./data/clean",
                            date_cols_by_table: Optional[Dict[str, List[str]]] = None,
                            outlier_cols_by_table: Optional[Dict[str, List[str]]] = None,
                            index_id_suffix: str = "_id") -> None:
    """
    Load all clean_* tables, run preprocessing, rewrite same table, create *_id indexes,
    and export Parquet/CSV to export_dir.
    """
    tables = [t for t in list_tables(conn, include_clean=True) if t.startswith("clean_")]
    if not tables:
        print("[warn] No clean_* tables found to preprocess.")
        return

    ensure_dir(export_dir)

    for t in tables:
        print(f"[info] preprocessing table: {t}")
        df = pd.read_sql_query(f"SELECT * FROM {quote_ident(t)};", conn)

        # per-table hints (optional)
        dcols = (date_cols_by_table or {}).get(t, None)
        ocols = (outlier_cols_by_table or {}).get(t, None)

        clean = preprocess_df(df, date_cols=dcols, outlier_cols=ocols)
        clean.to_sql(t, conn, if_exists="replace", index=False)
        print(f"[info] wrote cleaned table → {t}")

        # index any *_id columns (simple heuristic)
        for col in clean.columns:
            if col.lower().endswith(index_id_suffix):
                idx_name = f"idx_{snake_case(t)}_{snake_case(col)}"
                try:
                    conn.execute(
                        f"CREATE INDEX IF NOT EXISTS {quote_ident(idx_name)} "
                        f"ON {quote_ident(t)}({quote_ident(col)});"
                    )
                except Exception as e:
                    print(f"[warn] could not create index on {t}({col}): {e}")

        # export
        base = os.path.join(export_dir, t)
        clean.to_parquet(base + ".parquet", index=False)
        clean.to_csv(base + ".csv", index=False)
        print(f"[info] exported → {base}.parquet and .csv")

    conn.commit()
    print("[done] preprocessing complete.")


# =========================
# CLI
# =========================

def main():
    if len(sys.argv) < 2:
        print("Usage: python preprocess_unify.py /path/to/Unify.db")
        sys.exit(1)

    db_path = sys.argv[1]
    if not os.path.exists(db_path):
        print(f"[error] DB not found: {db_path}")
        sys.exit(2)

    print(f"[info] opening SQLite: {os.path.abspath(db_path)}")
    conn = sqlite3.connect(db_path)

    try:
        # Phase A: build/refresh clean_* tables from originals, add surrogate IDs if needed
        created = bootstrap_clean_tables_with_ids(conn)
        if created:
            print(f"[info] created/updated clean tables: {created}")
        else:
            print("[warn] no source tables found (excluding sqlite_*).")

        # Phase B: preprocess clean_* tables in place and export
        preprocess_clean_tables(
            conn,
            export_dir="./data/clean",
            # Customize with real hints if you know them:
            date_cols_by_table={
                # "clean_student_info": ["dob", "application_date"],
                # "clean_user_input": ["submitted_at"],
            },
            outlier_cols_by_table={
                # "clean_scores": ["gpa", "sat_total"],
            },
            index_id_suffix="_id",
        )

    finally:
        conn.close()


if __name__ == "__main__":
    main()
