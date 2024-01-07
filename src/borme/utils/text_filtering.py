"""
Util functions used for filtering strings based on a regex pattern.

Functions:
    drop_lines_with_pattern
    drop_pattern

"""
import re
from datetime import date

from logs import log_unexpected_num_of_matches


def drop_lines_with_pattern(
    input_string: str, pattern: str, expected_num_of_matches: int, date_: date, pdf: str
) -> str:
    """
    Drop the lines that contain a match to some pattern.
    If the number of lines dropped is not the expected, log it.
    """
    # filter lines that don't contain a match to the pattern
    lines = input_string.split("\n")
    filtered_lines = [line for line in lines if not re.search(pattern, line)]

    # check if the number of matches is not the expected
    num_of_matches = len(lines) - len(filtered_lines)
    if num_of_matches != expected_num_of_matches:
        log_unexpected_num_of_matches(
            pattern, num_of_matches, expected_num_of_matches, date_, pdf
        )

    # join filtered lines to a single string
    result_string = "\n".join(filtered_lines)

    return result_string


def drop_pattern(
    input_string: str, pattern: str, expected_num_of_matches: int, date_: date, pdf: str
) -> str:
    """
    Substitute the occurrences of the pattern with an empty string.
    If the number of occurrences is not the expected, log it.
    """
    # substitute matches with an empty string
    result_string = re.sub(pattern, "", input_string)

    # check num of matches is the expected number
    num_of_matches = len(re.findall(pattern, input_string))
    if num_of_matches != expected_num_of_matches:
        log_unexpected_num_of_matches(
            pattern, num_of_matches, expected_num_of_matches, date_, pdf
        )

    return result_string
