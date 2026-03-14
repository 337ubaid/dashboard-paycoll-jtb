from core.schema import ALL_SCHEMAS


def format_currency(df):
    cols = get_currency_columns(df)
    return df.style.format({c: "{:,.0f}" for c in cols})


def get_currency_columns(df):
    return [col for col, t in ALL_SCHEMAS.items() if t == "currency"]
