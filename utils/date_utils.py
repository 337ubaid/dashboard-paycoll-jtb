from datetime import date, timedelta


def get_reference_dates():
    today = date.today()
    yesterday = today - timedelta(days=1)

    if today.day >= 6:
        start_period = today.replace(day=6)
    else:
        # mundur ke bulan sebelumnya
        if today.month == 1:
            start_period = date(today.year - 1, 12, 6)
        else:
            start_period = date(today.year, today.month - 1, 6)

    return today, yesterday, start_period
