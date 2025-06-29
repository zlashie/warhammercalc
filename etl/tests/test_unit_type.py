### Dependencies
import psycopg2
from etl.helper_functions.insert_unit_type import insert_unit_types

### Definitions
"""
Test: test_insert_unit_types_basic

Description:
    Verifies that keyword-based type flags are inserted into the unit_type table.
    Ensures correct mapping from keywords to boolean flags.

Input:
    - unit_id of a test unit
    - Keyword list: ["Infantry", "Battleline", "Fly"]

Expected Outcome:
    - unit_type row is created with correct boolean flags
    - Other flags remain False
    - TypeError is raised for invalid input (non-list or non-string elements)

Edge Cases Covered:
    - Irregular capitalization in keywords
    - Invalid keyword types
"""
def test_insert_unit_types_basic(test_db):
    conn = psycopg2.connect(**test_db)
    cursor = conn.cursor()

    # Setup: Create unit
    cursor.execute("INSERT INTO faction (name) VALUES ('TypeFaction') RETURNING faction_id;")
    faction_id = cursor.fetchone()[0]
    cursor.execute("""
        INSERT INTO unit (name, models_pr_unit, faction_id)
        VALUES ('TypeUnit', '5', %s)
        RETURNING unit_id
    """, (faction_id,))
    unit_id = cursor.fetchone()[0]

    keywords = ["infantry", "BATTLELINE", "Fly"]
    insert_unit_types(cursor, unit_id, keywords)

    cursor.execute("SELECT * FROM unit_type WHERE unit_id = %s", (unit_id,))
    result = cursor.fetchone()

    assert result is not None
    flags = dict(zip(
        ["unit_id", "character", "vehicle", "infantry", "monster", "battleline", "epic_hero", "fly"],
        result
    ))

    assert flags["infantry"] is True
    assert flags["battleline"] is True
    assert flags["fly"] is True
    assert flags["character"] is False
    assert flags["vehicle"] is False
    assert flags["monster"] is False

    # TypeError test
    try:
        insert_unit_types(cursor, unit_id + 1, "Infantry")  # Not a list
        assert False, "Expected TypeError"
    except TypeError:
        pass

    cursor.close()
    conn.close()
