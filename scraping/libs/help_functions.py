import datetime as dt

def get_current_time_string():
    return dt.datetime.now().strftime('%Y%m%d%H%M%S')