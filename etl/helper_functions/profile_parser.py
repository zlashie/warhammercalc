### Dependencies
from helper_functions.catalogue_loader import NS
from models import UnitStats
from xml.etree.ElementTree import Element
from typing import Optional

### Definition
"""
Parses a unit <profile> XML node and returns a UnitStats dataclass instance.

Args:       profile_node (Element): An XML <profile> element with typeName="Unit",
            containing characteristic child elements.

Returns:    UnitStats: A populated UnitStats object containing unit statistics such as
            movement, toughness, save, wounds, leadership, and objective control.
            Returns UnitStats with name="Unknown" and other fields as None if the node is invalid.
"""
def parse_unit_stats(profile_node: Optional[Element]) -> UnitStats:
    if profile_node is None:
        print("[WARNING] No profile node provided for unit stats parsing.")
        return UnitStats(name="Unknown")

    try:
        return UnitStats(
            name=profile_node.get("name", "Unknown"),
            movement=_get_char(profile_node, "M"),
            toughness=_get_char(profile_node, "T"),
            save=_get_char(profile_node, "SV"),
            wounds=_get_char(profile_node, "W"),
            leadership=_get_char(profile_node, "LD"),
            oc=_get_char(profile_node, "OC")
        )
    except Exception as e:
        print(f"[ERROR] Failed to parse unit stats: {e}")
        return UnitStats(name=profile_node.get("name", "Unknown"))

"""
Helper function to extract a specific characteristic value from a unit profile node.

Args:       profile_node (Element): The XML <profile> node to search within.
            name (str): The name of the characteristic to retrieve (e.g., "M", "W", "OC").

Returns:    Optional[str]: The trimmed text content of the characteristic if found, otherwise None.
"""
def _get_char(profile_node: Element, name: str) -> Optional[str]:
    try:
        char = profile_node.find(f".//bs:characteristic[@name='{name}']", NS)
        return char.text.strip() if char is not None and char.text else None
    except Exception as e:
        print(f"[ERROR] Failed to get characteristic '{name}': {e}")
        return None
