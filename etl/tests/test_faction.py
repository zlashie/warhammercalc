### Dependencies
import psycopg2
from etl.helper_functions.insert_faction import insert_faction

### Definitions
"""
Test: test_insert_faction_basic

Description:
    Verifies that a faction is inserted into the 'faction' table correctly.
    Also ensures that duplicate inserts do not create multiple entries.

Input:
    - Faction name: "Space Marines"

Expected Outcome:
    - A single faction is inserted
    - Re-inserting returns the same faction_id
    - No duplicates are created

Edge Cases Covered:
    - Duplicate name insertions
"""
def test_insert_faction_basic(test_db):
    conn = psycopg2.connect(**test_db)
    cursor = conn.cursor()

    name = "Space Marines"
    faction_id_1 = insert_faction(cursor, name)
    faction_id_2 = insert_faction(cursor, name)

    assert isinstance(faction_id_1, int)
    assert faction_id_1 == faction_id_2

    cursor.execute("SELECT COUNT(*) FROM faction WHERE name = %s", (name,))
    count = cursor.fetchone()[0]
    assert count == 1

    cursor.close()
    conn.close()
