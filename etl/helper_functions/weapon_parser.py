### Dependencies
from .catalogue_loader import NS
from models import WeaponProfile
from xml.etree.ElementTree import Element
from typing import List

### Variables
WEAPON_TYPES = {"Weapon", "Melee Weapons", "Ranged Weapons"}

### Definition
"""
Extracts weapon profiles from a Battlescribe catalogue based on linked entry IDs.

This function searches both <selectionEntry> and <sharedSelectionEntry> elements
for profiles of type "Weapon", "Melee Weapons", or "Ranged Weapons" that match
the provided linked IDs. Each matching weapon is parsed into a dictionary of
its characteristics.

Args:       root (Element): The root element of the parsed Battlescribe XML catalogue.
            linked_ids (list[str]): A list of entry IDs that are associated with the unit.

Returns:    list[dict]: A list of weapon profiles, where each profile is a dictionary
            containing the weapon name and its stats (e.g., Range, A, S, AP).
            Returns an empty list if no matching weapons are found.
"""
def extract_weapons(root: Element, linked_ids: List[str]) -> List[WeaponProfile]:
    weapon_profiles: List[WeaponProfile] = []

    try:
        all_entries = root.findall(".//bs:selectionEntry", NS) + root.findall(".//bs:sharedSelectionEntry", NS)

        for entry in all_entries:
            if entry.get("id") in linked_ids:
                for profile in entry.findall(".//bs:profile", NS):
                    if profile.get("typeName") in WEAPON_TYPES:
                        try:
                            profile_data = {
                                (char.get("name") or "").lower(): (char.text or "").strip()
                                for char in profile.findall("bs:characteristics/bs:characteristic", NS)
                            }
                            weapon_profiles.append(
                                WeaponProfile(
                                    name=profile.get("name", "Unnamed Weapon"),
                                    range=profile_data.get("range"),
                                    attacks=profile_data.get("a"),
                                    bs=profile_data.get("bs"),
                                    ws=profile_data.get("ws"),
                                    strength=profile_data.get("s"),
                                    ap=profile_data.get("ap"),
                                    damage=profile_data.get("d"),
                                    keywords=profile_data.get("keywords")
                                )
                            )
                        except Exception as e:
                            print(f"[WARNING] Skipped a weapon profile due to parsing error: {e}")

    except Exception as e:
        print(f"[ERROR] Failed to extract weapon profiles: {e}")

    return weapon_profiles
