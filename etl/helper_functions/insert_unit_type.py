### Dependencies
from typing import List
import psycopg2

### Definitions
"""
Description: Inserts unit type flags into the 'unit_type' table based on keyword detection.
Input:
    - cursor (psycopg2.extensions.cursor): Active DB cursor
    - unit_id (int): ID of the unit
    - keywords (List[str]): List of keyword strings for the unit

Output: None

Raises:
    TypeError: If keywords is not a list of strings
    Exception: For unexpected DB errors
"""
def insert_unit_types(cursor, unit_id: int, keywords: List[str]) -> None:
    if not isinstance(keywords, list) or not all(isinstance(k, str) for k in keywords):
        raise TypeError(f"Keywords must be a list of strings. Got: {keywords}")

    type_flags = {
        "character": "Character",
        "vehicle": "Vehicle",
        "infantry": "Infantry",
        "monster": "Monster",
        "battleline": "Battleline",
        "fly": "Fly",
    }

    resolved_flags = {k: False for k in type_flags}
    for key in keywords:
        for db_field, match in type_flags.items():
            if match.lower() == key.lower():
                resolved_flags[db_field] = True

    try:
        cursor.execute("""
            INSERT INTO unit_type (
                unit_id, character, vehicle, infantry,
                monster, battleline, fly
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (unit_id) DO NOTHING
        """, (
            unit_id,
            resolved_flags["character"],
            resolved_flags["vehicle"],
            resolved_flags["infantry"],
            resolved_flags["monster"],
            resolved_flags["battleline"],
            resolved_flags["fly"]
        ))
    except Exception as e:
        raise Exception(f"Failed to insert unit type flags for unit_id {unit_id}: {e}")
