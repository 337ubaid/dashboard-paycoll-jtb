import pandas as pd

from core.schema import REQUIRED_COLUMNS_MYBRAINS, SCHEMA_DATABASE_NONPOTS
from data.excel import load_mybrains_excel
from services.aging_service import compute_lama_tunggakan
from services.kuadran_service import assign_kuadran


def normalize_columns_name(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize dataframe columns: strip, lower, and replace spaces with underscores."""
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df


def sort_values(df: pd.DataFrame, sort_column: str = "saldo_akhir") -> pd.DataFrame:
    """Sort dataframe by column descending."""
    return df.sort_values(sort_column, ascending=False)


def reset_index(df: pd.DataFrame) -> pd.DataFrame:
    """Reset index to 1-based numbering."""
    df = df.reset_index(drop=True)
    df.index += 1
    return df


def convert_excel_mybrains_nonpots(file, segmen_target, tanggal):
    """Pipeline to convert and enrich MyBrains Excel data."""
    df = load_mybrains_excel(file)
    df = normalize_columns_name(df)
    df = df.reindex(columns=REQUIRED_COLUMNS_MYBRAINS.keys()).copy()

    # Add metadata and compute business logic fields
    df = add_metadata(df, segmen_target, tanggal)
    df = compute_lama_tunggakan(df)
    df = assign_kuadran(df)

    return df


def create_empty_df() -> pd.DataFrame:
    """Create an empty dataframe with standard schema."""
    cols = SCHEMA_DATABASE_NONPOTS.keys()
    df = pd.DataFrame([{col: "" for col in cols}] * 11)
    return df


def add_metadata(df: pd.DataFrame, segmen: str, tanggal: str) -> pd.DataFrame:
    """Add segment and date metadata to dataframe."""
    df = df.copy()
    df["segmen"] = segmen
    df["tanggal"] = tanggal
    return df
