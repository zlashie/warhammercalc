### Dependencies
from helper_functions.catalogue_loader import NS
from typing import Optional
from xml.etree.ElementTree import Element

### Definition
"""
Searches the Battlescribe XML tree for a <profile> element representing the specified unit.

This function looks for a global <profile> with typeName="Unit" and a name matching the provided unit name (case-insensitive).

Args:       root (Element): The root element of the parsed Battlescribe XML catalogue.
            unit_name (str): The exact name of the unit to find (case-insensitive).

Returns:    Element or None: The <profile> element for the unit, or None if not found.
"""
def find_unit_profile(root: Element, unit_name: str) -> Optional[Element]:
    try:
        for profile in root.findall(".//bs:profile", NS):
            if profile.get("typeName") == "Unit" and profile.get("name", "").lower() == unit_name.lower():
                return profile
    except Exception as e:
        print(f"[ERROR] Failed to find unit profile for '{unit_name}': {e}")
    return None