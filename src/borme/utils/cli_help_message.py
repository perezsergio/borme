from os.path import basename
from sys import argv
from typing import Callable

from pyfiglet import figlet_format  # type: ignore


def construct_help_message(func: Callable) -> str:
    """Construct CLI help message."""

    # Get name of the script executed in the CL (not the name of the current script)
    script_name = basename(argv[0])
    # Get docstring of the function, remove indentation
    func_docstring = func.__doc__

    # Use figlet to create a fancy formatted title
    title = figlet_format(script_name.split(".")[0], font="rozzo")
    # String with Args help message
    args = "Arguments:\n" + "  DATE\t date with the format YYYYMMDD"
    # String with Options help message
    options = (
        "Options:\n"
        + "  -f --file \tRead dates from file."
        + "  Each line in the file must correspond to a date, with the format 'YYYYMMDD'"
    )
    # String with Usage help message
    usage = (
        "Usage:\n"
        + f"  {script_name} DATE ... \t(dates specified in command line)\n"
        + f"  {script_name} -f FILE \t(path to file containing dates)"
    )
    # String with Usage Examples help message
    usage_examples = (
        "Usage examples:\n"
        + f"  {script_name} 20231127 20231128 20231201\n"
        + f"  echo '20231127\\n20231128\\n20231201' > dates.txt ; {script_name} -f dates.txt "
    )
    # String with Notes help message
    notes = (
        "*Notes:\n"
        + "  When reading from a text file, "
        + "the dates passed in directly through the command line will be ignored.\n"
        + f"  For example: '{script_name} -f dates.txt 20010101' "
        + "only reads the dates from dates.txt and "
        + "ignores the date passed in the command line (20010101)."
    )

    # Use all the strings to construct a help message
    help_message = (
        ("\n" + title + "\n")
        + (
            func_docstring.replace("    ", "") + "\n"
            if func_docstring is not None
            else "\n"
        )
        + (usage + "\n\n")
        + (usage_examples + "\n\n")
        + (args + "\n\n")
        + (options + "\n\n")
        + (notes + "\n")
    )

    return help_message
