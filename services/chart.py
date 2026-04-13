from datetime import date, timedelta

import pandas as pd


def get_available_billperiodes(df):
    """Get sorted list of available billperiodes from dataframe."""
    if "billperiode" in df.columns:
        billperiode = df["billperiode"].dropna().unique()
        return sorted(billperiode)
    return []


def prepare_forecast_nonpots(df, billperiode=None, value_col="saldo_akhir"):
    """
    Prepare forecast data grouped by billperiode or daily within a specific billperiode.

    Args:
        df: DataFrame with collection data
        billperiode: Optional specific billperiode to filter (e.g., 202604)
        value_col: Value column to aggregate

    Returns:
        DataFrame with:
        - If billperiode provided: daily progression within that period + forecast
        - If no billperiode: aggregated sums by billperiode + forecast to next period
    """
    df = df.copy()

    if billperiode is not None:
        # Filter to specific billperiode and show daily progression
        df_filtered = df[df["billperiode"] == billperiode].copy()

        if df_filtered.empty:
            return pd.DataFrame()

        # Convert tanggal to datetime for daily aggregation
        df_filtered["tanggal_dt"] = pd.to_datetime(
            df_filtered["tanggal"], format="%d/%m/%Y", errors="coerce"
        )

        # Aggregate by day within the billperiode
        df_actual = (
            df_filtered.groupby("tanggal_dt")[value_col]
            .sum()
            .reset_index()
            .sort_values("tanggal_dt")
        )
        df_actual.rename(columns={"tanggal_dt": "date"}, inplace=True)

        # Calculate trend (avg daily change)
        if len(df_actual) > 1:
            trend = df_actual[value_col].diff().tail(7).mean()
        else:
            trend = 0

        # Get last date and calculate forecast to end of period
        last_date = df_actual["date"].max()
        last_value = df_actual[value_col].iloc[-1]

        # Determine end of current billperiode (day 5 of next month)
        year = billperiode // 100
        month = billperiode % 100

        if month == 12:
            end_period = date(year + 1, 1, 5)
        else:
            end_period = date(year, month + 1, 5)

        # Generate future dates until end of period
        future_dates = pd.date_range(
            last_date + timedelta(days=1), end_period, freq="D"
        )

        # Forecast values
        vals = []
        current = last_value
        for _ in future_dates:
            current += trend
            vals.append(current)

        df_forecast = pd.DataFrame(
            {"date": future_dates, value_col: vals if vals else [last_value]}
        )

        df_actual["type"] = "actual"
        df_forecast["type"] = "forecast"

        return pd.concat([df_actual, df_forecast])

    else:
        # No specific billperiode - show aggregated by billperiode
        df_actual = (
            df.groupby("billperiode")[value_col]
            .sum()
            .reset_index()
            .sort_values("billperiode")
        )

        if df_actual.empty:
            return pd.DataFrame()

        # Calculate trend (avg period-to-period change)
        trend = df_actual[value_col].diff().tail(3).mean()

        # Get last billperiode
        last_bp = df_actual["billperiode"].max()
        last_value = df_actual[value_col].iloc[-1]

        # Calculate next billperiode
        month = last_bp % 100
        year = last_bp // 100

        if month == 12:
            next_bp = year * 100 + 1
        else:
            next_bp = year * 100 + month + 1

        # Forecast for next period
        forecast_value = last_value + trend

        df_forecast = pd.DataFrame(
            {"billperiode": [next_bp], value_col: [forecast_value]}
        )

        df_actual["type"] = "actual"
        df_forecast["type"] = "forecast"

        return pd.concat([df_actual, df_forecast])
