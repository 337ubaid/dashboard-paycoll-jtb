import pandas as pd
import streamlit as st
from utils.formatter import format_currency

def validate_dataframe_schema(df: pd.DataFrame, required_columns: dict) -> bool:
    """Validate that the dataframe contains all required columns."""
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        st.error(f"Missing columns: {', '.join(missing_cols)}")
        return False
    return True
