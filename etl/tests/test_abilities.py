### Dependencies
import psycopg2
from etl.helper_functions.insert_abilities import insert_abilities

### Definitions
"""
Test: test_insert_abilities_basic

Description:
    Verifies that abilities are inserted into the 'ability' table
    and that duplicates are ignored due to the unique constraint.

Input:
    - unit_id for a test unit
    - List of abilities: ["Deep Strike", "Shield Wall", "Deep Strike"]

Expected Outcome:
    - Only unique abilities are inserted
    - Ability table contains "Deep Strike" and "Shield Wall"

Edge Cases Covered:
    - Duplicate ability names for same unit
"""
def test_insert_abilities_basic(test_db):
    conn = psycopg2.connect(**test_db)
    cursor = conn.cursor()

    # Setup: Insert a unit
    cursor.execute("INSERT INTO faction (name) VALUES ('AbilityTest') RETURNING faction_id;")
    faction_id = cursor.fetchone()[0]
    cursor.execute("""
        INSERT INTO unit (name, models_pr_unit, faction_id)
        VALUES ('Ability Unit', '1', %s)
        RETURNING unit_id
    """, (faction_id,))
    unit_id = cursor.fetchone()[0]

    abilities = ["Deep Strike", "Shield Wall", "Deep Strike"]  # Intentional duplicate

    insert_abilities(cursor, unit_id, abilities)

    cursor.execute("SELECT name FROM ability WHERE unit_id = %s", (unit_id,))
    rows = cursor.fetchall()

    assert len(rows) == 2
    names = [r[0] for r in rows]
    assert "Deep Strike" in names
    assert "Shield Wall" in names

    cursor.close()
    conn.close()