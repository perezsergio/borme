"""Given a series of dates, execute the daily spyder and daily crawler for each one."""
from datetime import date

from spyder import daily_spyder
from crawler import daily_crawler
from cli import dates_cli
from logs import set_up_root_logger, log_no_dates_read
from utils.type_casting import uniq_dates_in_list


def main(input_dates: tuple[str, ...]) -> None:
    """
    For each date, parse the BORME registry webpage for that date,
    download all the relevant pdfs of the webpage,
    then parse the text in the pdfs and write one jsonl file per date with the parsed data.
    """
    set_up_root_logger()

    uniq_dates: list[date] = uniq_dates_in_list(input_dates)

    if len(uniq_dates) == 0:
        log_no_dates_read()

    for date_ in uniq_dates:
        daily_spyder(date_)
        daily_crawler(date_)


if __name__ == "__main__":
    dates_cli(main)()  # pylint: disable=no-value-for-parameter
