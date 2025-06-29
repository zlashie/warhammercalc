### Dependencies
import psycopg2
from etl.helper_functions.insert_unit_keywords import insert_unit_keywords

### Definitions
"""
Test: test_insert_unit_keywords_basic

Description:
    Verifies that keywords are properly linked to a unit via the unit_keyword table.

Input:
    - A unit_id for a test unit
    - Keywords list: ["Infantry", "Battleline"]

Expected Outcome:
    - Keywords inserted via insert_keywords()
    - unit_keyword table contains correct (unit_id, keyword_id) mappings

Edge Cases Covered:
    - Empty keyword list (should not insert anything)
"""
def test_insert_unit_keywords_basic(test_db):
    conn = psycopg2.connect(**test_db)
    cursor = conn.cursor()

    # Setup: Create unit and faction
    cursor.execute("INSERT INTO faction (name) VALUES ('KeywordFaction') RETURNING faction_id;")
    faction_id = cursor.fetchone()[0]
    cursor.execute("""
        INSERT INTO unit (name, models_pr_unit, faction_id)
        VALUES ('KeywordUnit', '5', %s)
        RETURNING unit_id
    """, (faction_id,))
    unit_id = cursor.fetchone()[0]

    keywords = ["Infantry", "Battleline"]
    insert_unit_keywords(cursor, unit_id, keywords)

    # Validate links
    cursor.execute("SELECT COUNT(*) FROM unit_keyword WHERE unit_id = %s", (unit_id,))
    count = cursor.fetchone()[0]
    assert count == 2

    # Edge case: Empty list
    insert_unit_keywords(cursor, unit_id, [])
    cursor.execute("SELECT COUNT(*) FROM unit_keyword WHERE unit_id = %s", (unit_id,))
    new_count = cursor.fetchone()[0]
    assert new_count == 2  # Still 2, nothing new inserted

    cursor.close()
    conn.close()
