### Dependencies
from helper_functions.catalogue_loader import NS
from xml.etree.ElementTree import Element
from typing import Optional

### Definition
"""
Searches the Battlescribe XML tree for a <selectionEntry> corresponding to a specific unit.
Args:       root (Element): The root element of the parsed Battlescribe XML catalogue.
            unit_name (str): The exact name of the unit to search for (case-insensitive).

Returns:    Element or None: The <selectionEntry> element with type="unit" and matching name,
            or None if not found.
"""
def find_unit_entry(root: Element, unit_name: str) -> Optional[Element]:
    try:
        for entry in root.findall(".//bs:selectionEntry", NS):
            if entry.get("type") == "unit" and entry.get("name", "").lower() == unit_name.lower():
                return entry
    except Exception as e:
        print(f"[ERROR] Failed to find unit entry for '{unit_name}': {e}")
    return None
