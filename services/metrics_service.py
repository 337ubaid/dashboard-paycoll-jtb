from dataclasses import dataclass
from datetime import date
from typing import Dict, Any, Tuple, Optional

import pandas as pd

from services.aggregations import count_pelanggan_by_date, sum_saldo_by_date
from services.filters import filter_collection_data
from utils.date_utils import get_reference_dates


@dataclass
class MetricSummary:
    today: float
    delta_yesterday: float
    delta_start_periode: float
    start_periode: float


@dataclass
class DashboardMetrics:
    saldo: MetricSummary
    pelanggan: MetricSummary
    different_days: int
    latest_date: Optional[date]


def calculate_dashboard_metrics(df: pd.DataFrame, segmen: str) -> Tuple[pd.DataFrame, DashboardMetrics]:
    """Calculate dashboard metrics for a given dataframe and segment."""
    df = filter_collection_data(df, segmen)

    start_periode, yesterday, latest_date, different_days = get_reference_dates(df)

    nominal_today = sum_saldo_by_date(df, latest_date)
    nominal_yesterday = sum_saldo_by_date(df, yesterday)
    nominal_start_periode = sum_saldo_by_date(df, start_periode)

    pelanggan_today = count_pelanggan_by_date(df, latest_date)
    pelanggan_yesterday = count_pelanggan_by_date(df, yesterday)
    pelanggan_start_periode = count_pelanggan_by_date(df, start_periode)

    metrics = DashboardMetrics(
        saldo=MetricSummary(
            today=nominal_today,
            delta_yesterday=nominal_today - nominal_yesterday,
            delta_start_periode=nominal_today - nominal_start_periode,
            start_periode=nominal_start_periode,
        ),
        pelanggan=MetricSummary(
            today=pelanggan_today,
            delta_yesterday=pelanggan_today - pelanggan_yesterday,
            delta_start_periode=pelanggan_today - pelanggan_start_periode,
            start_periode=pelanggan_start_periode,
        ),
        different_days=different_days,
        latest_date=latest_date,
    )

    return df, metrics


def calculate_dashboard_metrics_supabase(df: pd.DataFrame) -> DashboardMetrics:
    """Calculate dashboard metrics from Supabase data summary."""
    if len(df) == 0:
        empty_summary = MetricSummary(today=0, delta_yesterday=0, delta_start_periode=0, start_periode=0)
        return DashboardMetrics(
            saldo=empty_summary,
            pelanggan=empty_summary,
            different_days=0,
            latest_date=None,
        )

    latest_date = df.iloc[0]["tanggal"]
    nominal_today = df.iloc[0]["total_saldo"]
    pelanggan_today = df.iloc[0]["total_pelanggan"]

    if len(df) > 1:
        yesterday = df.iloc[1]["tanggal"]
        different_days = (latest_date - yesterday).days
        nominal_yesterday = df.iloc[1]["total_saldo"]
        pelanggan_yesterday = df.iloc[1]["total_pelanggan"]
    else:
        different_days = 0
        nominal_yesterday = nominal_today
        pelanggan_yesterday = pelanggan_today

    if len(df) > 2:
        nominal_start_periode = df.iloc[2]["total_saldo"]
        pelanggan_start_periode = df.iloc[2]["total_pelanggan"]
    else:
        nominal_start_periode = nominal_yesterday
        pelanggan_start_periode = pelanggan_yesterday

    return DashboardMetrics(
        saldo=MetricSummary(
            today=nominal_today,
            delta_yesterday=nominal_today - nominal_yesterday,
            delta_start_periode=nominal_today - nominal_start_periode,
            start_periode=nominal_start_periode,
        ),
        pelanggan=MetricSummary(
            today=pelanggan_today,
            delta_yesterday=pelanggan_today - pelanggan_yesterday,
            delta_start_periode=pelanggan_today - pelanggan_start_periode,
            start_periode=pelanggan_start_periode,
        ),
        different_days=different_days,
        latest_date=latest_date,
    )
