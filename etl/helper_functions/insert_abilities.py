### Dependencies
from typing import List
import psycopg2

### Definitions
"""
Description: Inserts all abilities for a unit into the 'ability' table.
Avoids duplicates using a UNIQUE constraint on (unit_id, name).

Input:
    - cursor (psycopg2.extensions.cursor): Active DB cursor
    - unit_id (int): ID of the unit this ability belongs to
    - abilities (List[str]): List of ability names or descriptions

Output: None

Raises:
    Exception: For any unexpected database errors
"""
def insert_abilities(cursor, unit_id: int, abilities: List[str]) -> None:
    for ability in abilities:
        try:
            cursor.execute("""
                INSERT INTO ability (unit_id, name)
                VALUES (%s, %s)
                ON CONFLICT ON CONSTRAINT unique_ability_per_unit DO NOTHING
            """, (unit_id, ability))
        except Exception as e:
            raise Exception(f"Failed to insert ability '{ability}' for unit_id {unit_id}: {e}")
