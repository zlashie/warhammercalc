### Dependencies
from helper_functions.catalogue_loader import load_catalogue
from helper_functions.unit_finder import find_unit_profile
from helper_functions.profile_parser import parse_unit_stats
from models import UnitStats
from requests.exceptions import RequestException
from xml.etree.ElementTree import ParseError
import logging

### Variables
logger = logging.getLogger(__name__)

### Defintion

"""
Retrieves the parsed stat block for a specified unit from a Battlescribe .cat file.
Args:       url (str): The URL to the Battlescribe .cat file.
            unit_name (str): The exact name of the unit to retrieve stats for.
Returns:    A dictionary of unit statistics (e.g., Movement, Toughness, Save, etc.).
            Returns an empty dictionary if the unit or profile is not found.

"""
def get_unit_stats(url: str, unit_name: str) -> UnitStats:
    try:
        root = load_catalogue(url)
    except RequestException as e:
        logger.error(f"Failed to fetch catalogue from URL '{url}': {e}")
        return UnitStats(name=f"{unit_name} (Load Error)")

    except ParseError as e:
        logger.error(f"Failed to parse XML from catalogue: {e}")
        return UnitStats(name=f"{unit_name} (Parse Error)")

    try:
        profile_node = find_unit_profile(root, unit_name)
        if profile_node is None:
            logger.warning(f"Unit '{unit_name}' not found in the catalogue.")
            return UnitStats(name=f"{unit_name} (Not Found)")
        return parse_unit_stats(profile_node)

    except Exception as e:
        logger.exception(f"Unexpected error while processing unit '{unit_name}': {e}")
        return UnitStats(name=f"{unit_name} (Error)")