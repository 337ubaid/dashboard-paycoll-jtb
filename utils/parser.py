import pandas as pd

from core.schema import SCHEMA_MAP

# def parse_date_column(df, df_type, date_format="%d/%m/%Y"):

#     schema = get_schema(df_type)

#     for col in date_columns(schema):
#         if col in df.columns:
#             df[col] = pd.to_datetime(
#                 df[col], format=date_format, errors="coerce"
#             ).dt.date

#     return df


def parse_dataframe(df, df_type, date_format="%d/%m/%Y"):

    schema = SCHEMA_MAP[df_type]

    parser = DataSpreadsheetParser(schema)

    return parser.parse(df)


# def date_columns(schema):
#     return [col for col, dtype in schema.items() if dtype == "date"]


## next time pakai parser
class DataSpreadsheetParser:

    def __init__(self, schema):
        self.schema = schema

    def parse(self, df):
        df = self._parse_dates(df)
        df = self._parse_ints(df)
        return df

    def _parse_dates(self, df, date_format="%d/%m/%Y"):
        for col in self._date_columns():
            if col in df.columns:
                df[col] = pd.to_datetime(
                    df[col], format=date_format, errors="coerce"
                ).dt.date
        return df

    def _parse_ints(self, df):
        for col in self._int_columns():
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
        return df

    def _date_columns(self):
        return [c for c, t in self.schema.items() if t == "date"]

    def _int_columns(self):
        return [c for c, t in self.schema.items() if t in ["int", "id", "currency"]]
