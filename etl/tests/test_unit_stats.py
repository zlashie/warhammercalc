### Dependencies
import psycopg2
from etl.helper_functions.insert_unit_stats import insert_unit_stats

### Definitions
"""
Test: test_insert_unit_stats_basic

Description:
    Verifies that the unit statline is inserted into the unit_stats table
    and that all values are correctly stored.

Input:
    - A unit_id for a test unit
    - A full dictionary of stats with valid values

Expected Outcome:
    - All stat fields are inserted correctly
    - No errors raised for full input
    - KeyError is raised if a required stat is missing

Edge Cases Covered:
    - Missing one stat value
    - Null value in optional field (feel_no_pain)
"""
def test_insert_unit_stats_basic(test_db):
    conn = psycopg2.connect(**test_db)
    cursor = conn.cursor()

    # Setup: Create faction and unit
    cursor.execute("INSERT INTO faction (name) VALUES ('StatFaction') RETURNING faction_id;")
    faction_id = cursor.fetchone()[0]
    cursor.execute("""
        INSERT INTO unit (name, models_pr_unit, faction_id)
        VALUES ('StatUnit', '3', %s)
        RETURNING unit_id
    """, (faction_id,))
    unit_id = cursor.fetchone()[0]

    stats = {
        "movement": 6,
        "toughness": 5,
        "save": 3,
        "wounds": 4,
        "leadership": 7,
        "objective_control": 2,
        "invulnerable_save": 4,
        "feel_no_pain": None
    }

    insert_unit_stats(cursor, unit_id, stats)

    # Validate insertion
    cursor.execute("SELECT * FROM unit_stats WHERE unit_id = %s", (unit_id,))
    result = cursor.fetchone()
    assert result is not None
    assert result[1:] == (
        stats["movement"],
        stats["toughness"],
        stats["save"],
        stats["wounds"],
        stats["leadership"],
        stats["objective_control"],
        stats["invulnerable_save"],
        stats["feel_no_pain"],
    )

    # Edge Case: Missing field
    stats_missing = stats.copy()
    del stats_missing["save"]
    try:
        insert_unit_stats(cursor, unit_id + 1, stats_missing)
        assert False, "Expected KeyError for missing 'save'"
    except KeyError as e:
        assert "save" in str(e)

    cursor.close()
    conn.close()
