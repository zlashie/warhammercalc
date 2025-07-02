### Dependencies
import psycopg2
import pytest
from unittest.mock import MagicMock
from etl.helper_functions.insert_faction import insert_faction

### Definitions
"""
Test: test_insert_faction_basic + failure handling

Description:
    Covers successful insert, duplicate insert, and DB exception handling.

Expected Outcome:
    - Valid insert works
    - Duplicate insert returns same ID
    - DB failure raises correct exception

Edge Cases Covered:
    - Duplicate names
    - DB insert failure
"""
def test_insert_faction_basic(test_db):
    conn = psycopg2.connect(**test_db)
    cursor = conn.cursor()

    name = "Space Marines"
    faction_id_1, _ = insert_faction(cursor, name)
    faction_id_2, _ = insert_faction(cursor, name)

    assert isinstance(faction_id_1, int)
    assert faction_id_1 == faction_id_2

    cursor.execute("SELECT COUNT(*) FROM faction WHERE name = %s", (name,))
    count = cursor.fetchone()[0]
    assert count == 1

    cursor.close()
    conn.close()

def test_insert_faction_db_failure():
    mock_cursor = MagicMock()
    mock_cursor.execute.side_effect = Exception("DB error")

    with pytest.raises(Exception) as excinfo:
        insert_faction(mock_cursor, "Chaos Marines")

    assert "Failed to insert or fetch faction 'Chaos Marines'" in str(excinfo.value)
