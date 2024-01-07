from datetime import date, datetime
from logging import getLogger, FileHandler, StreamHandler, Handler, basicConfig, INFO
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
    basicConfig(
        handlers=handlers,
        format="%(asctime)s: %(levelname)-8s: %(message)s",
        level=INFO,
    )


def log_no_target_elements(url: str, date_: date) -> None:
    """Log warning: no target elements found at url"""
    logger = getLogger()
    logger.warning(
        "'%s' : Couldn't find any links to pdfs at url '%s'. No pdfs will be downloaded for the date '%s'.",
        date_.strftime("%Y-%m-%d"),
        url,
        date_.strftime("%Y-%m-%d"),
    )


def log_non_200_status_code(status_code: int, url: str, date_: date) -> None:
    """Log warning: received non 200 status code from url"""
    logger = getLogger()
    logger.warning(
        "'%s' : Received status code '%s' from url '%s'.",
        date_.strftime("%Y-%m-%d"),
        status_code,
        url,
    )


def log_get_request_exception(e: RequestException, url: str, date_: date) -> None:
    """Log warning: got exception after sending a get http request to a url"""
    logger = getLogger()
    logger.warning(
        "'%s' : Http get request to '%s' raised exception: '%s'",
        date_.strftime("%Y-%m-%d"),
        url,
        e,
    )


def log_no_pdfs_for_date(date_: date) -> None:
    """Log warning: no url for date."""
    logger = getLogger()
    logger.warning(
        "'%s' : Could not find any pdfs for the date '%s'. Skipping this date.",
        date_.strftime("%Y-%m-%d"),
        date_.strftime("%Y-%m-%d"),
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


def log_unexpected_num_of_matches(
    pattern: str,
    num_of_matches: int,
    expected_num_of_matches: int,
    date_: date,
    pdf: str,
) -> None:
    """Log warning: got an unexpected num of matches"""
    logger = getLogger()
    logger.warning(
        "'%s' : '%s' : The pattern '%s' has '%s' matches, expected '%s'.",
        date_.strftime("%Y-%m-%d"),
        pdf.split("/")[-1],
        pattern,
        num_of_matches,
        expected_num_of_matches,
    )


def log_date_data_dir_does_not_exist(path: str, date_: date) -> None:
    """Log warning: there is not an existing data dir for the date"""
    logger = getLogger()
    logger.warning(
        "'%s' : When attempting to read the pdfs for the date '%s', expected a directory containing all the pdfs at the path '%s', but this directory does not exist.",
        date_.strftime("%Y-%m-%d"),
        date_.strftime("%Y-%m-%d"),
        path,
    )


def log_no_pdfs_in_dir(path: str, date_: date) -> None:
    """Log warning: there are no pdfs in the directory."""
    logger = getLogger()
    logger.warning(
        "'%s' : When attempting to read the pdfs for the date '%s', expected a directory containing all the pdfs at the path '%s', but this directory does not contain any pdfs.",
        date_.strftime("%Y-%m-%d"),
        date_.strftime("%Y-%m-%d"),
        path,
    )


def log_finished_daily_crawler(date_: date) -> None:
    """Log info: finished execution of the daily crawler."""
    logger = getLogger()
    logger.info(
        "'%s' : Daily crawler finished execution. Parsed all the pdfs for the date '%s'.",
        date_.strftime("%Y-%m-%d"),
        date_.strftime("%Y-%m-%d"),
    )


def log_finished_daily_spyder(date_: date) -> None:
    """Log info: finished execution of the daily spyder."""
    logger = getLogger()
    logger.info(
        "'%s' : Daily spyder finished execution. Downloaded all the pdfs for the date '%s'.",
        date_.strftime("%Y-%m-%d"),
        date_.strftime("%Y-%m-%d"),
    )
