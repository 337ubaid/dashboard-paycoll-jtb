from datetime import date, timedelta


def get_reference_dates(df):
    today = date.today()

    if today.day >= 6:
        start_period = today.replace(day=6)
    else:
        # mundur ke bulan sebelumnya
        if today.month == 1:
            start_period = date(today.year - 1, 12, 6)
        else:
            start_period = date(today.year, today.month - 1, 6)

    dates = df["tanggal"].drop_duplicates().sort_values(ascending=False)

    latest_date = dates.iloc[0]
    yesterday = dates.iloc[1]

    different_days = (latest_date - yesterday).days

    return start_period, yesterday, latest_date, different_days
