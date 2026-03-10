import pandas as pd
import numpy as np

def read_excel_mybrains(file):
    try:
        df = pd.read_excel(file, header=None)

        # gabungkan 2 baris header
        header1 = df.iloc[1]
        header2 = df.iloc[2]

        header2 = header2.fillna(header1)
        header2 = header2.replace("", pd.NA).fillna(header1)

        df.columns = header2

        df = df.iloc[3:].reset_index(drop=True)

        # hapus baris terakhir
        df = df.iloc[:-1]
        return df

    except Exception as e:
        raise ValueError(f"Error reading Excel file: {e}")