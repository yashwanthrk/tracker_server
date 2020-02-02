from datetime import datetime


def timestamp_to_date_month_year(timestamp):
    if not timestamp:
        return None
    try:
        # dt_object = datetime.fromtimestamp(timestamp)
        return datetime.fromtimestamp(timestamp / 1000.0).strftime("%d/%m/%Y")

    except ValueError:
        return None


def timestamp_to_hour_min_secs(timestamp):
    if not timestamp:
        return None
    try:
        # dt_object = datetime.fromtimestamp(timestamp)
        return datetime.fromtimestamp(timestamp / 1000.0).strftime("%H:%M:%S")

    except ValueError:
        return None
