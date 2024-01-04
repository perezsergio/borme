from datetime import date

import requests
from logs import log_get_request_exception, log_non_200_status_code
from requests.exceptions import RequestException


def download_pdf(url: str, path: str) -> None:
    """Download pdf from url to local path."""
    # send http get request to url
    try:
        response = requests.get(url, timeout=5)
    # if get request raises exception, log warning and return
    except RequestException as e:
        log_get_request_exception(e, url)
        return
    # if the status code is not 200, log warning and return
    if response.status_code != 200:
        log_non_200_status_code(response.status_code, url)
        return
    # write response contents to file
    with open(path, "wb") as file:
        file.write(response.content)


def construct_borme_daily_url(day: date) -> str:
    """
    Construct url for the 'Actos inscritos' section of the BORME registry for a given day.
    The url for a given day YYYYMMDD is https://www.boe.es/borme/dias/YYYY/MM/DD/index.php?s=a1
    """
    return (
        "https://www.boe.es/borme/dias/" + day.strftime("%Y/%m/%d") + "/index.php?s=a1"
    )
