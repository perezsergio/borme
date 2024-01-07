"""
Given a series of dates, read all the pdfs of the BORME registry webpage for each date,
and write one jsonl file per date with the information obtained from parsing the pdfs.
"""
from datetime import date
from pathlib import Path
import re
from os import listdir


from cli import dates_cli
from logs import (
    set_up_root_logger,
    log_no_dates_read,
    log_date_data_dir_does_not_exist,
    log_no_pdfs_in_dir,
    log_finished_daily_crawler,
)
from utils.type_casting import uniq_dates_in_list, flatten
from utils.text_filtering import drop_lines_with_pattern, drop_pattern
from utils.write_and_read_files import (
    get_pages_in_pdf,
    read_text_from_pdf,
    write_list_of_dict_to_jsonl,
)


def drop_headers_and_footnotes(
    pdf_text: str, num_of_pages: int, date_: date, pdf: str
) -> str:
    """
    Given the text content of a pdf of the BORME registry,
    use regex patterns to find the headers and footnotes inside of the pdf text,
    drop them.
    """
    # Define pattern, expected_num_of_matches for the filler texts that we want to remove
    final_footnote = (
        "https://www.boe.es BOLETÍN OFICIAL DEL REGISTRO MERCANTIL D.L.",
        1,
    )
    section_header = ("SECCIÓN PRIMERA\n Empresarios\n Actos inscritos\n", 1)
    header = ("BOLETÍN OFICIAL DEL REGISTRO MERCANTIL", num_of_pages)
    subheader = (r"Núm. \d+ [A-Za-z]+ \d+ de [A-Za-z]+ de \d+ Pág. \d+", num_of_pages)
    footnote_1 = (r"cve: BORME-[A-Za-z]-\d+-\d+-\d+", num_of_pages)
    footnote_2 = ("Verificable en https://www.boe.es", num_of_pages)

    # Remove lines that contain the specified patterns
    result_text = pdf_text
    for pattern, expected_num_of_matches in [
        final_footnote,
        header,
        subheader,
        footnote_1,
        footnote_2,
    ]:
        result_text = drop_lines_with_pattern(
            result_text, pattern, expected_num_of_matches, date_, pdf
        )

    # Remove occurrences of the specified pattern
    result_text = drop_pattern(result_text, *section_header, date_, pdf)

    return result_text.strip()


def split_text_by_acts(acts_text: str) -> list[str]:
    """
    Given a text from a pdf of the BORME registry,
    containing only the act information with no headers footnotes or region name,
    split text in a list, where each element of the list corresponds to a different act.
    """
    # Pattern: digit at the start of line followed by ' - ' and a word in all uppercase
    pattern = r"(\n\d+ - [A-Z]+)"
    # Split string by pattern, keep the separators.
    # The separators are kept because the pattern is wrapped in parenthesis.
    splitted_text = re.split(pattern, acts_text)
    # remove empty strings from splitted text
    splitted_text = [e for e in splitted_text if e != ""]

    # The splitted text has the form [pattern match, (...), pattern match, (...), ...]
    # we want to add the odd and even elements
    even_els = splitted_text[0::2]
    odd_els = splitted_text[1::2]
    assert len(even_els) == len(odd_els), "num of even and odd elements do not match"
    acts = [even_els[i] + odd_els[i] for i in range(len(even_els))]

    return acts


def parse_act(act: str, region_name: str, date_: date) -> dict:
    """
    Parse the string containing the information of a given act,
    return a dictionary with the structured information
    """
    lines = act.strip().split("\n")
    # id, company name are in the 1st line, separated by an '-' character
    act_id, company_name = lines[0].split("-", 1)
    clean_company_name = company_name.strip().replace(".", "")

    # store the rest of the text in the variable description
    # For more information about this design choice, consult the README
    description = "\n".join(lines[1:])

    return {
        "id": act_id,
        "company_name": clean_company_name,
        "region_name": region_name,
        "borme_date": date_.strftime("%Y-%m-%d"),
        "description": description,
    }


def parse_pdf(path: str, date_: date) -> list[dict]:
    """
    Given the path to a pdf of the BORME registry,
    parse pdf text and return a list of dictionaries,
    where each dictionary corresponds to the info of a single act listed in the pdf.
    """
    # get text and num of pages of pdf
    pdf_text = read_text_from_pdf(path)
    num_of_pages = get_pages_in_pdf(path)

    # Clean the pdf text by dropping headers and footnotes
    cleaned_pdf_text = drop_headers_and_footnotes(pdf_text, num_of_pages, date_, path)

    # The first line of the cleaned pdf text is the region name,
    # the rest is the text containing the act information
    region_name = cleaned_pdf_text.split("\n")[0]
    acts_text = cleaned_pdf_text.replace(region_name, "", 1)

    # Split the pdf text in act, parse each act to obtain a dict with the curated information
    acts = split_text_by_acts(acts_text)
    cleaned_acts = [parse_act(act, region_name, date_) for act in acts]

    return cleaned_acts


def daily_crawler(date_: date) -> None:
    """
    Read all the pdfs of the BORME registry for a given date,
    parse pdfs text and write a jsonl file, where each line of the jsonl file corresponds to
    the info of a single act listed in one of the pdfs.
    """
    # Path to directory where the pdfs for that date are stored
    data_dir = (
        Path(__file__).parent.parent.parent
        / "data"
        / "output"
        / date_.strftime("%Y-%m-%d")
    )

    # If the data dir does not exist, log warning and exit function
    if not data_dir.is_dir():
        log_date_data_dir_does_not_exist(str(data_dir), date_)
        return

    # List of pdf files inside the data dir
    pdf_files = [
        str(data_dir / f) for f in listdir(str(data_dir)) if f.endswith(".pdf")
    ]

    # If there are no pdf files, log warning and exit function
    if len(pdf_files) == 0:
        log_no_pdfs_in_dir(str(data_dir), date_)
        return

    # Parse every pdf file
    acts_per_pdf = [parse_pdf(pdf, date_) for pdf in pdf_files]

    # Flatten to get a single list containing the acts of all the pdfs
    acts = flatten(acts_per_pdf)

    # Write acts to jsonl file
    write_list_of_dict_to_jsonl(str(data_dir / "acts.jsonl"), acts)

    log_finished_daily_crawler(date_)


def main(input_dates: tuple[str, ...]) -> None:
    """
    For each date, read all the pdfs of the BORME registry webpage for that date,
    write a jsonl file with the information obtained from parsing the pdfs.
    """
    set_up_root_logger()

    uniq_dates: list[date] = uniq_dates_in_list(input_dates)

    if len(uniq_dates) == 0:
        log_no_dates_read()

    for date_ in uniq_dates:
        daily_crawler(date_)


if __name__ == "__main__":
    dates_cli(main)()  # pylint: disable=no-value-for-parameter
