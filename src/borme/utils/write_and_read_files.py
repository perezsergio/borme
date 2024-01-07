from functools import reduce
from os.path import isfile

import jsonlines  # type: ignore
from pypdf import PdfReader


def read_list_from_txt(path: str) -> list:
    """
    Read a txt file and return a list,
    where each line in the file corresponds to an element in the list.
    If the file does not exist return an empty list.
    """
    if not isfile(path):
        return []
    with open(path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file]


def write_txt_from_list(my_list: list, path: str) -> None:
    """
    Write a txt file from a list,
    such that each element of the list corresponds to a row in the csv file
    """
    with open(path, "w", encoding="utf-8") as file:
        for el in my_list:
            file.write(el + "\n")


def get_pages_in_pdf(path_to_pdf: str) -> int:
    """Return the number of pages in a pdf file."""
    reader = PdfReader(path_to_pdf)
    num_of_pages = len(reader.pages)
    return num_of_pages


def read_text_from_pdf(path_to_pdf: str) -> str:
    """Return the text content of a pdf file."""
    reader = PdfReader(path_to_pdf)
    pages_text = [page.extract_text() for page in reader.pages]

    pdf_text = reduce(lambda x, y: x + y, pages_text)
    return pdf_text


def write_list_of_dict_to_jsonl(
    file_path: str, arr_of_dicts: list[dict], verbose: bool = False
) -> None:
    """
    Write a jsonl file from a list of dictionaries.
    """
    with jsonlines.open(file_path, mode="w") as writer:
        writer.write_all(arr_of_dicts)  # pylint: disable=no-member

    if verbose:
        print(f"Exported list of dictionaries to {file_path}")
