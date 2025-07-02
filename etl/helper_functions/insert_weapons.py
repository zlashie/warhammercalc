### Dependencies
from typing import List, Dict, Any
from .insert_weapon_keywords import insert_weapon_keywords

### Definitions
"""
Description:
  Inserts each weapon for a unit into the 'weapon' table,
  and links keywords using weapon_keyword table.
  Avoids duplicates via UNIQUE(unit_id, name).

Input:
  - cursor: psycopg2 DB cursor
  - unit_id: int
  - weapons: List of weapon dictionaries

Output:
  - None
"""
def insert_weapons(cursor, unit_id: int, weapons: List[Dict[str, Any]]) -> int:
    if not isinstance(weapons, list) or not all(isinstance(w, dict) for w in weapons):
        raise TypeError("Weapons must be a list of dictionaries.")

    inserted_count = 0

    for weapon in weapons:
        try:
            cursor.execute("""
                INSERT INTO weapon (
                    unit_id, name, range, range_type,
                    attacks, weapon_skill, ballistic_skill,
                    strength, ap, damage
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT ON CONSTRAINT unique_weapon_per_unit DO NOTHING
                RETURNING weapon_id
            """, (
                unit_id,
                weapon.get("name"),
                int(weapon.get("range", 0)),
                weapon.get("range_type"),
                int(weapon.get("attacks", 0)),
                int(weapon.get("weapon_skill")) if weapon.get("weapon_skill") is not None else None,
                int(weapon.get("ballistic_skill")) if weapon.get("ballistic_skill") is not None else None,
                int(weapon.get("strength", 0)),
                int(weapon.get("ap", 0)),
                weapon.get("damage") if weapon.get("damage") is not None else 0,
            ))

            result = cursor.fetchone()
            if result:
                weapon_id = result[0]
                inserted_count += 1
            else:
                cursor.execute("""
                    SELECT weapon_id FROM weapon
                    WHERE unit_id = %s AND name = %s
                """, (unit_id, weapon.get("name")))
                weapon_id = cursor.fetchone()[0]

            insert_weapon_keywords(cursor, weapon_id, weapon.get("keywords", []))

        except Exception as e:
            raise Exception(f"Failed to insert weapon '{weapon.get('name')}' for unit_id {unit_id}: {e}")
        
    return inserted_count
