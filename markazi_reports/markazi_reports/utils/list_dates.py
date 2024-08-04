import datetime
from datetime import date, timedelta


today = lambda: datetime.datetime.now().strftime("%Y-%m-%d")
week_ago = lambda: (datetime.datetime.now() - datetime.timedelta(days=7)).strftime(
    "%Y-%m-%d"
)


def list_dates(start_dt, end_dt):
    # convert both dates to datetime objects
    start_dt = datetime.datetime.strptime(start_dt, "%Y-%m-%d")
    end_dt = datetime.datetime.strptime(end_dt, "%Y-%m-%d")
    # difference between current and previous date
    delta = timedelta(days=1)

    # store the dates between two dates in a list
    dates = []

    while start_dt <= end_dt:
        # add current date to list by converting  it to iso format
        dates.append(start_dt.isoformat())
        # increment start date by timedelta
        start_dt += delta
    return dates
