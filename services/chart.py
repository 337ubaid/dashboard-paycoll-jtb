import pandas as pd


def prepare_total_with_forecast(df, date_col="tanggal", value_col="saldo_akhir"):
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])

    # aggregate
    df_actual = (
        df.groupby(date_col)[value_col].sum().reset_index().sort_values(date_col)
    )

    # trend (avg diff 7 hari)
    trend = df_actual[value_col].diff().tail(7).mean()

    last_date = df_actual[date_col].max()

    # target tgl 5 bulan berikutnya
    next_month = last_date.month + 1 if last_date.month < 12 else 1
    year = last_date.year if last_date.month < 12 else last_date.year + 1
    target_date = pd.Timestamp(year, next_month, 5)

    future_dates = pd.date_range(last_date, target_date, freq="D")[1:]

    # forecast
    last_value = df_actual[value_col].iloc[-1]
    vals = []
    current = last_value
    for _ in future_dates:
        current += trend
        vals.append(current)

    df_forecast = pd.DataFrame({date_col: future_dates, value_col: vals})

    df_actual["type"] = "actual"
    df_forecast["type"] = "forecast"

    return pd.concat([df_actual, df_forecast])
