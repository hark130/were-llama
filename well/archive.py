"""Functionality to retrieve and parse past Wordle answers."""

# Standard Imports
from typing import List
# Third Party Imports
from bs4 import BeautifulSoup
import requests
# Local Imports
from well.globals import ARCHIVE_NEEDLE, ARCHIVE_URL


def get_past_answers(archive_url: str = ARCHIVE_URL) -> List[str]:
    """Retrieve past Wordle answers.

    Args:
        archive_url: Optional; The URL to retrieve the answers from.

    Returns:
        List of five letter strings on success.
    """
    # LOCAL VARIABLES
    words = _get_all_items(url=archive_url, tag='h2')  # All of the li tag strings
    word_list = []                                     # List of Wordle-compliant words

    # PARSE IT
    for word in words:
        if 5 != len(word):
            raise RuntimeError(f'Found a non-Wordle word: {word}')
        word_list.append(word)

    # DONE
    return word_list


def _get_all_items(url: str, tag: str, needle: str = ARCHIVE_NEEDLE) -> List[str]:
    """Get all the li tags from the tag type with the needle text.

    Returns:
        A list of upper case words parsed from <tag>needle</tag> found at URL url on success.

    Raises:
        RuntimeError: The parser stubbed its toe.
    """
    # LOCAL VARIABLES
    raw_html = _get_raw_html(url=url)              # Raw HTML read from url
    soup = BeautifulSoup(raw_html, 'html.parser')  # Soup object
    target = soup.find(tag, string=needle)         # Target tag
    list_container = None                          # Container with all the items
    list_items = None                              # All the items

    # GET IT
    if target:
        list_container = target.find_next_sibling(['ul', 'ol'])
    else:
        raise RuntimeError(f'Unable to find tag "{tag}" / needle "{needle}" in URL "{url}"')

    if list_container:
        list_items = list_container.find_all('li')
    else:
        raise RuntimeError(f'No list found after the "{tag}" tag in URL "{url}"')

    if list_items:
        list_items = [item.text.strip().upper() for item in list_items]
    else:
        raise RuntimeError(f'No items found in the "{tag}" tag list for URL "{url}"?!')

    # DONE
    return list_items


def _get_raw_html(url: str) -> str:
    """Read the raw HTML from URL."""
    # LOCAL VARIABLES
    raw_html = None  # Raw HTML read from url

    # GET IT
    try:
        response = requests.get(url)
        response.raise_for_status()  # Bad status?
        raw_html = response.text
    except requests.exceptions.RequestException as err:
        print(f'Failed to fetch URL "{url}" with "{repr(err)}"')
        raise err from err

    # DONE
    return raw_html
