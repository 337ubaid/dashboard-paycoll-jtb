import pandas as pd

from core.schema import SCHEMA_MAP


def parse_dataframe(df, df_type, date_format="%d/%m/%Y"):

    schema = SCHEMA_MAP[df_type]

    parser = DataSpreadsheetParser(schema)

    return parser.parse(df)


class DataSpreadsheetParser:

    def __init__(self, schema):
        self.schema = schema

    def parse(self, df):
        df = self._parse_dates(df)
        df = self._parse_numbers(df)
        return df

    def _normalize_number(self, val):
        if pd.isna(val):
            return val

        if isinstance(val, str):
            # hapus spasi
            val = val.strip()

            # hapus pemisah ribuan (.)
            val = val.replace(".", "")

            # ubah koma jadi titik
            val = val.replace(",", ".")

        return val

    def _parse_dates(self, df, date_format="%d/%m/%Y"):
        for col in self._date_columns():
            if col in df.columns:
                df[col] = pd.to_datetime(
                    df[col], format=date_format, errors="coerce"
                ).dt.date
        return df

    def _parse_numbers(self, df):
        for col in self._number_columns():
            if col in df.columns:
                df[col] = df[col].apply(self._normalize_number)
                df[col] = pd.to_numeric(df[col], errors="coerce")
        return df

    def _date_columns(self):
        return [c for c, t in self.schema.items() if t == "date"]

    def _number_columns(self):
        return [
            c
            for c, t in self.schema.items()
            if t in ["int", "id", "currency", "percentage", "number"]
        ]
