### Dependencies
from etl.helper_functions.insert_keywords import insert_keywords
import psycopg2

### Definitions
"""
Test: test_insert_keywords_basic

Description:
    Validates that keywords are inserted correctly into the 'keyword' table,
    and that their IDs are returned for linking.

Input:
    - List of new keywords: ["Fly", "Character", "Grenades"]

Expected Outcome:
    - All keywords inserted without error
    - Returned dictionary contains keyword → keyword_id mappings

Edge Cases Covered:
    - Re-inserting the same keywords should not duplicate entries
"""
def test_insert_keywords_basic(test_db):
    conn = psycopg2.connect(**test_db)
    cursor = conn.cursor()

    keywords = ["Fly", "Character", "Grenades"]
    keyword_ids, inserted = insert_keywords(cursor, keywords)

    assert len(keyword_ids) == 3
    assert inserted == 3
    for word in keywords:
        assert word in keyword_ids
        assert isinstance(keyword_ids[word], int)

    # Test re-insertion (no duplicates)
    keyword_ids_2, inserted_2 = insert_keywords(cursor, keywords)
    assert keyword_ids == keyword_ids_2
    assert inserted_2 == 0

    cursor.close()
    conn.close()
