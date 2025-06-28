### Dependencies
from typing import List
import psycopg2

### Definitions
"""
Description: Inserts ability strings for a given unit into the 'ability' table.
Input:
    - cursor (psycopg2.extensions.cursor): Active DB cursor
    - unit_id (int): ID of the unit
    - abilities (List[str]): List of ability names

Output: None

Raises:
    TypeError: If abilities is not a list of strings
    Exception: For unexpected DB errors
"""
def insert_abilities(cursor, unit_id: int, abilities: List[str]) -> None:
    if not isinstance(abilities, list) or not all(isinstance(a, str) for a in abilities):
        raise TypeError(f"Abilities must be a list of strings. Got: {abilities}")

    for ability in abilities:
        try:
            cursor.execute("""
                INSERT INTO ability (unit_id, ability_text)
                VALUES (%s, %s)
            """, (unit_id, ability))
        except Exception as e:
            raise Exception(f"Failed to insert ability '{ability}' for unit_id {unit_id}: {e}")
