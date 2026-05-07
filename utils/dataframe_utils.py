import pandas as pd
from datetime import datetime

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


def _extract_segmen_from_subsegment(df: pd.DataFrame) -> pd.DataFrame:
    """Extract first 3 characters from sub_segment column to create segmen."""
    df = df.copy()
    for col in df.columns:
        if col.startswith("sub") and ("segment" in col or "segmen" in col):
            df["segmen"] = df[col].astype(str).str[:3]
            break
    return df


def convert_excel_mybrains_nonpots(file, segmen_target, tanggal):
    """Pipeline to convert and enrich MyBrains Excel data."""
    df = load_mybrains_excel(file)
    df = normalize_columns_name(df)
    df = _extract_segmen_from_subsegment(df)
    
    # Keep required columns + segmen
    required_cols = list(REQUIRED_COLUMNS_MYBRAINS.keys()) + ["segmen"]
    df = df.reindex(columns=required_cols).copy()

    # Apply transformations
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
    """
    Add date metadata and handle segment filtering.
    
    If segmen is "-Semua-", keep all rows with their extracted segment values.
    Otherwise, filter data to only include rows matching the selected segment.
    
    Also extracts billperiode (YYYYMM format) from tanggal (DD/MM/YYYY format).
    """
    df = df.copy()
    df["tanggal"] = tanggal
    
    # Extract billperiode from tanggal (DD/MM/YYYY format → YYYYMM)
    try:
        parsed_date = datetime.strptime(tanggal, "%d/%m/%Y")
        df["billperiode"] = int(parsed_date.strftime("%Y%m"))
    except Exception:
        # Fallback if date parsing fails
        df["billperiode"] = None
    
    # If -Semua- is selected, preserve all segments from extraction
    if segmen == "-Semua-":
        # Keep all data with their extracted segments
        if "segmen" not in df.columns:
            raise ValueError(
                "Kolom 'segmen' tidak ditemukan. "
                "Pastikan file Excel memiliki kolom 'Sub-segment' atau pilih segmen spesifik."
            )
    else:
        # Filter data to only include matching segment
        if "segmen" in df.columns:
            df = df[df["segmen"] == segmen].copy()
        else:
            # If no segmen column (edge case), set all to selected segment
            df["segmen"] = segmen
    
    return df
