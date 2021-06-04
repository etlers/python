import datetime
from datetime import datetime
from datetime import timedelta

datetime_format = "%Y-%m-%d %H:%M:%S"

def get_now_datetime_string():
    return get_datetime_string(datetime.today())

def get_now_datetime():
    return datetime.today()

def get_datetime(datetime_string):
    return datetime.strptime(datetime_string, datetime_format)

def get_until_datetime(end_string):
    return datetime.strptime(end_string, datetime_format) - timedelta(seconds=1)

def get_datetime_string(datetime_value):
    return datetime_value.strftime(datetime_format)

def get_normalized_datetime(datetime_value, delta):
    return datetime_value.replace(minute=(datetime_value.minute - datetime_value.minute % delta), second=0, microsecond=0)

def get_datetime_list_between(start_string, end_string, delta):
    from_time = get_normalized_datetime(get_datetime(start_string), delta)
    until_time = get_normalized_datetime(get_datetime(end_string) - timedelta(secons=1), delta)
    between_datetime = until_time - from_time
    minutes = int((between_datetime.days * 1440) + (between_datetime.seconds / 60))
    between_datetime_list = []
    for m in range(0, minutes + delta, delta):
        between_datetime_list.append(from_time + timedelta(minutes=m))
    return between_datetime_list

def get_date_list_between(start_string, end_string):
    from_time = get_datetime(start_string).replace(hour=0, minute=0, second=0)
    until_time = get_datetime(end_string).replace(hour=0, minute=0, second=0) - timedelta(days=1)
    between_date = until_time - from_time
    days = int(between_date.days)
    between_date_list = []
    for d in range(0, days + 1, 1):
        between_date_list.append(from_time + timedelta(days=d))
    return between_date_list

def get_before_datetime(datetime_string, days=0, hours=0):
    return get_datetime_string(get_datetime(datetime_string) - timedelta(days=days, hours=hours))

def get_seconds_diff_between(start_datetime, end_datetime):
    from_time = get_datetime(start_datetime)
    to_time = get_datetime(end_datetime)
    between_time = to_time - from_time
    seconds = (between_time * 1440 * 60) + between_time.seconds
    return seconds

def get_datetime_from_epochtime(epochtime):
    return datetime.utcfromtimestamp(epochtime).strftime(datetime_format)

def seconds_operation_for_datetime_series(datetime_series, delta):
    return datetime_series.apply(lambda x: get_datetime(x) + timedelta(seconds=delta))