from datetime import date
from logs import log_cannot_cast_str_to_date, log_duplicate_dates


def cast_str_to_date(my_date: str) -> date | None:
    """Convert str with format YYYYMMDD to date, return None if conversion is impossible"""
    if len(my_date) != 8:
        return None
    year = my_date[:4]
    month = my_date[4:6]
    day = my_date[6:8]
    try:
        return date(int(year), int(month), int(day))
    except ValueError:
        log_cannot_cast_str_to_date(my_date)
        return None


def uniq_dates_in_list(input_dates: tuple[str, ...]) -> list[date]:
    """
    Convert list of strings to list of dates,
    drop repeated elements and elements that cannot be converted to a date
    """
    # cast dates from str to date, drop dates that cannot be converted
    dates = [e for e in map(cast_str_to_date, input_dates) if e is not None]
    # Drop duplicates
    uniq_dates = list(set(dates))

    # Log warning if there are any duplicates
    if len(dates) != len(uniq_dates):
        log_duplicate_dates(dates)

    return uniq_dates
