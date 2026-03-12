from datetime import date, timedelta

def get_reference_dates():

    today = date.today()
    yesterday = today - timedelta(days=3) # kemarin = today - 3
    day6 = today.replace(day=6)

    return today, yesterday, day6