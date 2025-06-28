### Dependencies
from typing import List
from .insert_keywords import insert_keywords

### Definitions
"""
Description:
  Links a weapon to its keywords using the weapon_keyword table.
  Ensures all keywords are inserted beforehand.

Input:
  - cursor: psycopg2 DB cursor
  - weapon_id: int
  - keywords: List[str]

Output:
  - None
"""
def insert_weapon_keywords(cursor, weapon_id: int, keywords: List[str]) -> None:
    if not keywords:
        return

    keyword_ids = insert_keywords(cursor, keywords)

    for keyword, keyword_id in keyword_ids.items():
        try:
            cursor.execute("""
                INSERT INTO weapon_keyword (weapon_id, keyword_id)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING
            """, (weapon_id, keyword_id))
        except Exception as e:
            raise Exception(f"Failed to link weapon_id {weapon_id} to keyword '{keyword}': {e}")
