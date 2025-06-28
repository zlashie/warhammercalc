### Dependencies
from typing import List
from .insert_keywords import insert_keywords

### Definitions
"""
Description:
  Links a unit to its keywords using the unit_keyword table.
  Ensures all keywords exist beforehand.

Input:
  - cursor: psycopg2 DB cursor
  - unit_id: ID of the unit
  - keywords: List of keyword strings

Output:
  - None
"""
def insert_unit_keywords(cursor, unit_id: int, keywords: List[str]) -> None:
    if not keywords:
        return

    keyword_ids = insert_keywords(cursor, keywords)

    for keyword, keyword_id in keyword_ids.items():
        try:
            cursor.execute("""
                INSERT INTO unit_keyword (unit_id, keyword_id)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING
            """, (unit_id, keyword_id))
        except Exception as e:
            raise Exception(f"Failed to insert unit_keyword link for unit {unit_id} and keyword '{keyword}': {e}")
