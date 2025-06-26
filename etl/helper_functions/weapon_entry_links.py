### Dependencies
from helper_functions.catalogue_loader import NS
from xml.etree.ElementTree import Element
from typing import List

### Definition
"""
Extracts all linked entry IDs from a unit's <selectionEntry> element.

These IDs typically point to other entries in the catalogue such as weapons,
abilities, or wargear that are associated with the unit.

Args:       unit_entry (Element): The <selectionEntry> XML element representing a unit.

Returns:    list[str]: A list of targetId strings from all <entryLink> elements within the unit entry.
            Returns an empty list if no entryLinks are found.
"""
def get_linked_entry_ids(unit_entry: Element) -> List[str]:
    try:
        return [
            el.get("targetId")
            for el in unit_entry.findall(".//bs:entryLink", NS)
            if el.get("targetId") is not None
        ]
    except Exception as e:
        print(f"[ERROR] Failed to extract linked entry IDs: {e}")
        return []