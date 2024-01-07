import re
from datetime import date
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from cli import dates_cli
from logs import (
    set_up_root_logger,
    log_get_request_exception,
    log_no_pdfs_for_date,
    log_no_target_elements,
    log_non_200_status_code,
    log_no_dates_read,
    log_finished_daily_spyder,
)
from requests.exceptions import RequestException
from utils.borme_website import construct_borme_daily_url, download_pdf
from utils.type_casting import uniq_dates_in_list
from utils.write_and_read_files import write_txt_from_list


def get_pdf_urls(date_: date, skip_first_and_last=True) -> list:
    """
    Parse the 'Actos inscritos' section of the BORME registry webpage for a given day,
    return a list with the links to all the pdfs of the webpage.
    """
    url = construct_borme_daily_url(date_)
    try:
        response = requests.get(url, timeout=5)
    # if get request raises exception, log warning and return
    except RequestException as e:
        log_get_request_exception(e, url, date_)
        return []

    # If status code is not 200, log warning and return empty list
    if response.status_code != 200:
        log_non_200_status_code(response.status_code, url, date_)
        return []

    # Load html from url to soup
    soup = BeautifulSoup(response.content, "html.parser")
    # Find all html <a> elements with an href, and a title including the word 'PDF'
    target_elements = soup.find_all(
        "a", attrs={"title": re.compile("PDF"), "href": True}
    )
    # If no elements were found, log warning and return empty list
    if len(target_elements) == 0:
        log_no_target_elements(url, date_)
        return []

    # The pdf urls are the href of the target elements
    pdf_urls = ["https://www.boe.es" + el["href"] for el in target_elements]

    if skip_first_and_last and len(pdf_urls) > 2:
        return pdf_urls[1:-1]

    return pdf_urls


def daily_spyder(date_: date) -> None:
    """
    Parse the 'Actos inscritos' section of the BORME registry webpage for a given day,
    write a txt file with the links to all the pdfs of the webpage,
    download all the pdfs.
    """
    # Set directory to store the output data for that day
    data_dir = (
        Path(__file__).parent.parent.parent
        / "data"
        / "output"
        / date_.strftime("%Y-%m-%d")
    )
    data_dir.mkdir(parents=True, exist_ok=True)  # mkdir will be ignored if dir exists

    # We do not care about the first and last pdfs: they are just indices for the rest of the pdfs
    pdf_urls = get_pdf_urls(date_, skip_first_and_last=True)

    # if there are no pdfs urls for the date, log warning and exit function
    if len(pdf_urls) == 0:
        log_no_pdfs_for_date(date_)
        return

    # Write pdf urls to txt file
    write_txt_from_list(pdf_urls, path=str(data_dir / "pdf_urls.txt"))

    # Download the contents from every url to a pdf file
    for url in pdf_urls:
        # pdf from foo.es/wp/name.pdf will be saved as name.pdf
        pdf_name = url.split("/")[-1]
        download_pdf(url=url, path=str(data_dir / pdf_name))

    log_finished_daily_spyder(date_)


def main(input_dates: tuple[str, ...]) -> None:
    """
    For each date, parse the BORME registry webpage for that date,
    write a txt file with the links to all the pdfs of the webpage, and download all the pdfs.
    """
    set_up_root_logger()

    uniq_dates: list[date] = uniq_dates_in_list(input_dates)

    if len(uniq_dates) == 0:
        log_no_dates_read()

    for date_ in uniq_dates:
        daily_spyder(date_)


if __name__ == "__main__":
    dates_cli(main)()  # pylint: disable=no-value-for-parameter
