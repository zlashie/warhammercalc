### Dependencies
from typing import List, Dict

### Definitions
"""
Description:
  Ensures all keywords are present in the 'keyword' table and returns a dict of keyword -> keyword_id.
  Uses ON CONFLICT DO NOTHING for idempotency.

Input:
  - cursor: psycopg2 DB cursor
  - keywords: List of keyword strings

Output:
  - Dict[str, int]: keyword name mapped to its database ID
"""
def insert_keywords(cursor, keywords: List[str]) -> Dict[str, int]:
    if not keywords:
        return {}

    keyword_ids = {}

    for keyword in keywords:
        try:
            cursor.execute("""
                INSERT INTO keyword (name)
                VALUES (%s)
                ON CONFLICT (name) DO NOTHING
                RETURNING keyword_id
            """, (keyword,))
            result = cursor.fetchone()
            if result:
                keyword_ids[keyword] = result[0]
            else:
                cursor.execute("SELECT keyword_id FROM keyword WHERE name = %s", (keyword,))
                keyword_ids[keyword] = cursor.fetchone()[0]
        except Exception as e:
            raise Exception(f"Failed to insert/fetch keyword '{keyword}': {e}")

    return keyword_ids
