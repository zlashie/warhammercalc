### Dependencies
from helper_functions.catalogue_loader import load_catalogue
from helper_functions.unit_finder import find_unit_profile
from helper_functions.unit_entry_finder import find_unit_entry
from helper_functions.profile_parser import parse_unit_stats
from helper_functions.weapon_entry_links import get_linked_entry_ids
from helper_functions.weapon_parser import extract_weapons
from models import UnitStats, WeaponProfile
from requests.exceptions import RequestException
from xml.etree.ElementTree import ParseError, Element
from typing import Dict, Any, List
import logging

### Variables
logger = logging.getLogger(__name__)

### Definition
"""
Extracts and formats unit data for database insertion from a Battlescribe .cat file.

Args:
    url (str): The URL to the Battlescribe .cat file.
    unit_name (str): The exact name of the unit to retrieve.

Returns:    dict: A dictionary with keys:
            - 'unit_stats': Dict[str, str] of core stats.
            - 'weapon_profiles': List[Dict[str, str]] of weapon profile entries.
"""
def extract_unit_data(url: str, unit_name: str) -> Dict[str, Any]:
    try:
        root = load_catalogue(url)
    except RequestException as e:
        logger.error(f"Failed to fetch catalogue from URL '{url}': {e}")
        return {
            "unit_stats": {"name": f"{unit_name} (Load Error)"},
            "weapon_profiles": []
        }
    except ParseError as e:
        logger.error(f"Failed to parse XML from catalogue: {e}")
        return {
            "unit_stats": {"name": f"{unit_name} (Parse Error)"},
            "weapon_profiles": []
        }

    try:
        profile_node = find_unit_profile(root, unit_name)
        unit_stats: UnitStats = parse_unit_stats(profile_node) if profile_node else UnitStats(name=f"{unit_name} (Not Found)")
    except Exception as e:
        logger.exception(f"Unexpected error while processing stats for '{unit_name}': {e}")
        unit_stats = UnitStats(name=f"{unit_name} (Error)")

    try:
        unit_entry = find_unit_entry(root, unit_name)
        if not unit_entry:
            logger.warning(f"Unit entry for '{unit_name}' not found. No weapons returned.")
            weapon_profiles: List[WeaponProfile] = []
        else:
            linked_ids = get_linked_entry_ids(unit_entry)
            weapon_profiles: List[WeaponProfile] = extract_weapons(root, linked_ids)
    except Exception as e:
        logger.exception(f"Unexpected error while extracting weapons for '{unit_name}': {e}")
        weapon_profiles = []

    unit_stats_record = {
        "name": unit_stats.name,
        "movement": unit_stats.movement,
        "toughness": unit_stats.toughness,
        "save": unit_stats.save,
        "wounds": unit_stats.wounds,
        "leadership": unit_stats.leadership,
        "oc": unit_stats.oc,
    }

    weapon_records = [
        {
            "unit_name": unit_stats.name,
            "name": wp.name,
            "range": wp.range,
            "attacks": wp.attacks,
            "ws": wp.ws,
            "bs": wp.bs,
            "strength": wp.strength,
            "ap": wp.ap,
            "damage": wp.damage,
            "keywords": wp.keywords,
        }
        for wp in weapon_profiles
    ]

    return {
        "unit_stats": unit_stats_record,
        "weapon_profiles": weapon_records,
    }