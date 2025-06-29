### Dependencies
import psycopg2
import pytest
from unittest.mock import MagicMock
from etl.helper_functions.insert_abilities import insert_abilities

### Definitions
"""
Test: test_insert_abilities_basic + failure injection

Description:
    Covers normal inserts, duplicate handling, and failure during DB insert.

Expected Outcome:
    - Unique abilities inserted correctly
    - Duplicate ignored
    - Simulated DB failure triggers exception

Edge Cases Covered:
    - Duplicate names
    - DB insert failure (mocked)
"""
def test_insert_abilities_basic(test_db):
    conn = psycopg2.connect(**test_db)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO faction (name) VALUES ('AbilityTest') RETURNING faction_id;")
    faction_id = cursor.fetchone()[0]
    cursor.execute("""
        INSERT INTO unit (name, models_pr_unit, faction_id)
        VALUES ('Ability Unit', '1', %s)
        RETURNING unit_id
    """, (faction_id,))
    unit_id = cursor.fetchone()[0]

    abilities = ["Deep Strike", "Shield Wall", "Deep Strike"]

    insert_abilities(cursor, unit_id, abilities)

    cursor.execute("SELECT name FROM ability WHERE unit_id = %s", (unit_id,))
    rows = cursor.fetchall()

    assert len(rows) == 2
    names = [r[0] for r in rows]
    assert "Deep Strike" in names
    assert "Shield Wall" in names

    cursor.close()
    conn.close()

def test_insert_abilities_db_failure():
    mock_cursor = MagicMock()
    mock_cursor.execute.side_effect = Exception("DB insert failed")

    with pytest.raises(Exception) as excinfo:
        insert_abilities(mock_cursor, 42, ["Failsafe"])

    assert "Failed to insert ability 'Failsafe'" in str(excinfo.value)
