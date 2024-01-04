from os.path import isfile


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
