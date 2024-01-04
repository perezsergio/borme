from datetime import date, datetime
from logging import getLogger, FileHandler, StreamHandler, Handler, basicConfig
from os.path import isfile
from pathlib import Path

from requests.exceptions import RequestException


def set_up_root_logger() -> None:
    """Set up configuration of root logger"""

    # Set log file path.
    current_date = datetime.today().strftime("%Y%m%d")
    log_file = (
        Path(__file__).parent.parent.parent
        / "data"
        / "logs"
        / f"{current_date}_execution.log"
    )

    # If file does not exist, create and empty file at that path
    if not isfile(log_file):
        # Create parent directory if it does not exist
        log_file.parent.mkdir(parents=True, exist_ok=True)
        # create file
        open(log_file, "a", encoding="utf-8").close()

    # Handlers: write logs to file and print to stdout
    handlers: list[Handler] = [FileHandler(str(log_file)), StreamHandler()]

    # Apply config to root logger
    basicConfig(handlers=handlers, format="%(asctime)s: %(levelname)-8s: %(message)s")


def log_no_target_elements(url: str, day: date) -> None:
    """Log warning: no target elements found at url"""
    logger = getLogger()
    logger.warning(
        "Couldn't find any links to pdfs at url '%s'. No pdfs will be downloaded for the date '%s'.",
        url,
        day.strftime("%Y-%m-%d"),
    )


def log_non_200_status_code(status_code: int, url: str) -> None:
    """Log warning: received non 200 status code from url"""
    logger = getLogger()
    logger.warning(
        "Received status code '%s' from url '%s'.",
        status_code,
        url,
    )


def log_get_request_exception(e: RequestException, url: str) -> None:
    """Log warning: got exception after sending a get http request to a url"""
    logger = getLogger()
    logger.warning("Http get request to '%s' raised exception:\n'%s'", url, e)


def log_no_pdfs_for_date(day: date) -> None:
    """Log warning: no url for date."""
    logger = getLogger()
    logger.warning(
        "Could not find any pdfs for the date '%s'. Skipping this date.", day
    )


def log_dates_from_cl_and_file() -> None:
    """Log warning: reading dates from a file and passing them from the command line."""
    logger = getLogger()
    logger.warning(
        "When reading from a text file, the dates passed in directly through the command line will be ignored. Use --help to print usage statement."
    )


def log_no_dates_read() -> None:
    """Log warning: no dates where passed to the script"""
    logger = getLogger()
    logger.warning(
        "No dates where passed to the script. Use --help to print usage statement."
    )


def log_cannot_cast_str_to_date(my_date: str) -> None:
    """Log warning: no dates where passed to the script"""
    logger = getLogger()
    logger.warning(
        "Could not convert string '%s' to date. This element will be skipped",
        my_date,
    )


def log_duplicate_dates(dates: list[date]) -> None:
    """Log warning: no dates where passed to the script"""
    logger = getLogger()
    logger.warning(
        "The list of dates '%s' has duplicate elements. The duplicates will be dropped.",
        [e.strftime("%Y-%m-%d") for e in dates],
    )
