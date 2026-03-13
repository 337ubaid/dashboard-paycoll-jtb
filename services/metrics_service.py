from services.filters import filter_collection_data
from services.aggregations import sum_saldo_by_date, count_pelanggan_by_date
from utils.date_utils import get_reference_dates

today, yesterday, day6 = get_reference_dates()


def calculate_dashboard_metrics(df, segmen):

    df = filter_collection_data(df, segmen)

    val_today = sum_saldo_by_date(df, today)
    val_yesterday = sum_saldo_by_date(df, yesterday)
    val_day6 = sum_saldo_by_date(df, day6)

    pelanggan_today = count_pelanggan_by_date(df, today)
    pelanggan_yesterday = count_pelanggan_by_date(df, yesterday)
    pelanggan_day6 = count_pelanggan_by_date(df, day6)

    return (
        df,
        {
            "today": val_today,
            "delta_yesterday": val_today - val_yesterday,
            "delta_day6": val_today - val_day6,
            "day6": val_day6,
        },
        {
            "today": pelanggan_today,
            "delta_yesterday": pelanggan_today - pelanggan_yesterday,
            "delta_day6": pelanggan_today - pelanggan_day6,
            "day6": pelanggan_day6,
        },
    )
