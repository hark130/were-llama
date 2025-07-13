"""Parse the command line arguments on behalf of the package."""
# Standard
from typing import Any
import argparse
# Third Party
# Local
from well.argvals import ArgVals
from well.globals import DEBUG_ARG, SKIP_ARCHIVE_ARG


def parse_args() -> ArgVals:
    """Parse the command line arguments.

    Returns:
        A ArgVals data class containing all parsed values.
    """
    # LOCAL VARIABLES
    parser = None         # ArgumentParser object
    args = None           # Parsed argument Namespace
    skip_archive = False  # Skip loading the archived Wordle answers
    debug = False         # Enable DEBUG mode

    # SETUP
    parser = argparse.ArgumentParser(prog='well',
                                     description='WERE LLAMA (WELL): "Cheating" at NYT Wordle')
    parser.add_argument(f'-{SKIP_ARCHIVE_ARG[0]}', f'--{SKIP_ARCHIVE_ARG}', action='store_true',
                        help='Ignore past Wordle answers by not loading the archive',
                        required=False)
    parser.add_argument(f'-{DEBUG_ARG[0]}', f'--{DEBUG_ARG}', action='store_true',
                        help='NOT IMPLEMENTED', required=False)

    # PARSE IT
    args = parser.parse_args()
    if _get_eafp_attr(args, SKIP_ARCHIVE_ARG):
        skip_archive = True
    if _get_eafp_attr(args, DEBUG_ARG):
        debug = True

    # DONE
    return ArgVals(use_archive=not skip_archive, debug=debug)


def use_archive() -> bool:
    """Parses the arguments to control archive use."""
    argvals = parse_args()
    return argvals.use_archive


def _get_eafp_attr(args: argparse.Namespace, attr: str) -> Any:
    """Safely retrieve values from a Namespace (if they exist)."""
    # LOCAL VARIABLES
    value = None  # Retrieved value

    # GET IT
    try:
        value = getattr(args, attr)
    except AttributeError:
        pass  # Easier to ask for forgiveness than permission (EAFP)

    # DONE
    return value
