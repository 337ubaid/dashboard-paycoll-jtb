from services.aggregations import count_pelanggan_by_date, sum_saldo_by_date
from services.filters import filter_collection_data
from utils.date_utils import get_reference_dates


def calculate_dashboard_metrics(df, segmen):

    df = filter_collection_data(df, segmen)

    start_periode, yesterday, latest_date, different_days = get_reference_dates(df)

    nominal_today = sum_saldo_by_date(df, latest_date)
    nominal_yesterday = sum_saldo_by_date(df, yesterday)
    nominal_start_periode = sum_saldo_by_date(df, start_periode)

    pelanggan_today = count_pelanggan_by_date(df, latest_date)
    pelanggan_yesterday = count_pelanggan_by_date(df, yesterday)
    pelanggan_start_periode = count_pelanggan_by_date(df, start_periode)

    return (
        df,
        {
            "today": nominal_today,
            "delta_yesterday": nominal_today - nominal_yesterday,
            "delta_start_periode": nominal_today - nominal_start_periode,
            "start_periode": nominal_start_periode,
        },
        {
            "today": pelanggan_today,
            "delta_yesterday": pelanggan_today - pelanggan_yesterday,
            "delta_start_periode": pelanggan_today - pelanggan_start_periode,
            "start_periode": pelanggan_start_periode,
        },
        different_days,
        latest_date,
    )
