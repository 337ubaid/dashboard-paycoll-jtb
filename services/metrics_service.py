from services.aggregations import count_pelanggan_by_date, sum_saldo_by_date
from services.filters import filter_collection_data
from utils.date_utils import get_reference_dates

today, yesterday, start_periode = get_reference_dates()


def calculate_dashboard_metrics(df, segmen):

    df = filter_collection_data(df, segmen)
    latest_date = df["tanggal"].max()

    val_today = sum_saldo_by_date(df, latest_date)
    val_yesterday = sum_saldo_by_date(df, yesterday)
    val_start_periode = sum_saldo_by_date(df, start_periode)

    pelanggan_today = count_pelanggan_by_date(df, latest_date)
    pelanggan_yesterday = count_pelanggan_by_date(df, yesterday)
    pelanggan_start_periode = count_pelanggan_by_date(df, start_periode)

    return (
        df,
        {
            "today": val_today,
            "delta_yesterday": val_today - val_yesterday,
            "delta_start_periode": val_today - val_start_periode,
            "start_periode": val_start_periode,
        },
        {
            "today": pelanggan_today,
            "delta_yesterday": pelanggan_today - pelanggan_yesterday,
            "delta_start_periode": pelanggan_today - pelanggan_start_periode,
            "start_periode": pelanggan_start_periode,
        },
    )
