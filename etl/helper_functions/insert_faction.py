### Dependencies
from typing import Tuple

### Definitions
"""
Description: Inserts a faction into the 'faction' table if not already present.
Input:
    - cursor (psycopg2.extensions.cursor): Active DB cursor
    - name (str): Name of the faction
Output:
    - faction_id (int): ID of the inserted or existing faction
"""
def insert_faction(cursor, name: str) -> Tuple[int, bool]:
    try:
        cursor.execute("""
            INSERT INTO faction (name)
            VALUES (%s)
            ON CONFLICT (name) DO NOTHING
            RETURNING faction_id
        """, (name,))
        result = cursor.fetchone()
        if result:
            return result[0], True

        cursor.execute("SELECT faction_id FROM faction WHERE name = %s", (name,))
        return cursor.fetchone()[0], False
    except Exception as e:
        raise Exception(f"Failed to insert or fetch faction '{name}': {e}")
