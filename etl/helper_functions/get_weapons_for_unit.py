### Dependencies
from helper_functions.catalogue_loader import load_catalogue
from helper_functions.unit_entry_finder import find_unit_entry
from helper_functions.weapon_entry_links import get_linked_entry_ids
from helper_functions.weapon_parser import extract_weapons
from typing import List
from models import WeaponProfile

### Definition
"""
Retrieves all weapon profiles associated with a specific unit from a Battlescribe .cat file.

This function:
- Loads the catalogue from the provided URL
- Locates the specified unit's selection entry
- Collects all linked entry IDs (typically referencing wargear)
- Extracts and returns all weapon profiles found in those linked entries

Args:       url (str): The URL of the Battlescribe .cat file.
            unit_name (str): The name of the unit to retrieve weapons for.

Returns:    list[dict]: A list of dictionaries, each representing a weapon profile
            (e.g., name, range, attacks, strength, AP, damage).
            Returns an empty list if no weapons are found or the unit is missing.
"""
def get_weapons_for_unit(url: str, unit_name: str) -> List[WeaponProfile]:
    root = load_catalogue(url)
    if root is None:
        print(f"[ERROR] Could not load catalogue from URL: {url}")
        return []

    unit_entry = find_unit_entry(root, unit_name)
    if unit_entry is None:
        print(f"[WARNING] Unit '{unit_name}' not found in catalogue.")
        return []

    try:
        linked_ids = get_linked_entry_ids(unit_entry)
        return extract_weapons(root, linked_ids)
    except Exception as e:
        print(f"[ERROR] Failed to extract weapons for '{unit_name}': {e}")
        return []