### Dependencies
from typing import List, Dict, Optional
import psycopg2

### Definitions
"""
Description: Inserts all weapon profiles for a unit into the 'attack' table.
Input:
    - cursor (psycopg2.extensions.cursor): Active DB cursor
    - unit_id (int): ID of the unit owning these weapons
    - weapons (List[Dict[str, Any]]): List of weapon profiles

Output: None

Raises:
    KeyError: If any weapon is missing required fields
    Exception: For unexpected DB errors
"""
def insert_attacks(cursor, unit_id: int, weapons: List[Dict[str, Optional[str]]]) -> None:
    required_keys = [
        "name", "range", "range_type", "attacks", "ballistic_skill",
        "weapon_skill", "strength", "ap", "damage", "keywords"
    ]

    for weapon in weapons:
        for key in required_keys:
            if key not in weapon:
                raise KeyError(f"Missing '{key}' in weapon for unit_id {unit_id}: {weapon}")
        
        try:
            cursor.execute("""
                INSERT INTO attack (
                    unit_id, weapon_name, range, range_type, attacks,
                    weapon_skill, ballistic_skill, strength, ap, damage, keywords
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                unit_id,
                weapon["name"],
                weapon["range"],
                weapon["range_type"],
                weapon["attacks"],
                weapon["weapon_skill"],
                weapon["ballistic_skill"],
                weapon["strength"],
                weapon["ap"],
                weapon["damage"],
                ", ".join(weapon["keywords"]) if weapon.get("keywords") else ""
            ))
        except Exception as e:
            raise Exception(f"Failed to insert weapon for unit_id {unit_id}: {e}")
