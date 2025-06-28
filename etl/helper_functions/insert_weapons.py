### Dependencies
from typing import List, Dict, Any
import psycopg2

### Definitions
"""
Description: Inserts weapon profiles into the 'attack' table for a given unit.
Input:
    - cursor (psycopg2.extensions.cursor): Active DB cursor
    - unit_id (int): ID of the unit
    - weapons (List[Dict[str, Any]]): List of weapon dictionaries

Output: None

Raises:
    TypeError: If weapons is not a list of dicts with expected structure
    Exception: For unexpected DB errors
"""
def insert_weapons(cursor, unit_id: int, weapons: List[Dict[str, Any]]) -> None:
    if not isinstance(weapons, list) or not all(isinstance(w, dict) for w in weapons):
        raise TypeError("Weapons must be a list of dictionaries.")

    for weapon in weapons:
        try:
            cursor.execute("""
                INSERT INTO weapon (
                    unit_id, name, range, range_type,
                    attacks, weapon_skill, ballistic_skill,
                    strength, ap, damage, keywords
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                unit_id,
                weapon.get("name"),
                str(weapon.get("range", "")),
                weapon.get("range_type"),
                str(weapon.get("attacks", "")),
                str(weapon.get("weapon_skill", "")) if weapon.get("weapon_skill") is not None else None,
                str(weapon.get("ballistic_skill", "")) if weapon.get("ballistic_skill") is not None else None,
                str(weapon.get("strength", "")),
                str(weapon.get("ap", "")),
                str(weapon.get("damage", "")),
                weapon.get("keywords", [])
            ))
        except Exception as e:
            raise Exception(f"Failed to insert weapon for unit_id {unit_id}: {e}")
