### Dependencies
import psycopg2
from etl.helper_functions.insert_unit import insert_unit

### Definitions
"""
Test: test_insert_unit_basic

Description:
    Verifies that a unit can be inserted into the database correctly.
    Ensures that all fields are mapped and stored as expected.

Input:
    - unit_data with "models_per_unit" as string ("1")
    - Associated faction inserted into 'faction' table

Expected Outcome:
    - Unit is inserted
    - Unit fields match input (faction_id, name, models_pr_unit)

Edge Cases Covered:
    - None (baseline test only)
"""
def test_insert_unit_basic(test_db):
    conn = psycopg2.connect(**test_db)
    cursor = conn.cursor()

    faction_id = 1
    cursor.execute("INSERT INTO faction (name) VALUES ('Test Faction') RETURNING faction_id;")
    faction_id = cursor.fetchone()[0]

    test_unit = {
        "unit_name": "Test Unit",
        "models_per_unit": "1",
        "keywords": ["Infantry"],
        "unit_stats": {
            "movement": 6,
            "toughness": 4,
            "save": 3,
            "wounds": 2,
            "leadership": 6,
            "objective_control": 1,
            "invulnerable_save": 5,
            "feel_no_pain": None
        },
        "weapons": [],
        "abilities": []
    }

    insert_unit(cursor, test_unit, faction_id)
    cursor.execute("SELECT * FROM unit WHERE name = 'Test Unit'")
    result = cursor.fetchone()

    assert result is not None
    assert result[1] == faction_id
    assert result[2] == "Test Unit"
    assert result[3] == "1"

    cursor.close()
    conn.close()
