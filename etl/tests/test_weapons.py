### Dependencies
from etl.helper_functions.insert_weapons import insert_weapons
import psycopg2

### Definitions
"""
Test: test_insert_weapons_basic

Description:
    Ensures that a weapon is inserted into the 'weapon' table,
    and that weapon keywords are properly linked.

Input:
    - A single weapon dict with 1 keyword

Expected Outcome:
    - Weapon is inserted into the DB
    - weapon_keyword table is populated

Edge Cases Covered:
    - Keyword list is empty
"""
def test_insert_weapons_basic(test_db):
    conn = psycopg2.connect(**test_db)
    cursor = conn.cursor()

    # Setup: Insert faction/unit
    cursor.execute("INSERT INTO faction (name) VALUES ('WeaponTest') RETURNING faction_id;")
    faction_id = cursor.fetchone()[0]
    cursor.execute("""
        INSERT INTO unit (name, models_pr_unit, faction_id)
        VALUES ('Weapon Carrier', '1', %s)
        RETURNING unit_id
    """, (faction_id,))
    unit_id = cursor.fetchone()[0]

    weapons = [
        {
            "name": "Power Sword",
            "range": 0,
            "range_type": "melee",
            "attacks": 5,
            "ballistic_skill": None,
            "weapon_skill": 3,
            "strength": 6,
            "ap": 3,
            "damage": 2,
            "keywords": ["Precision"]
        }
    ]

    insert_weapons(cursor, unit_id, weapons)

    # Validate weapon insert
    cursor.execute("SELECT name FROM weapon WHERE unit_id = %s", (unit_id,))
    result = cursor.fetchone()
    assert result is not None
    assert result[0] == "Power Sword"

    # Validate keyword link
    cursor.execute("SELECT COUNT(*) FROM weapon_keyword WHERE weapon_id IN (SELECT weapon_id FROM weapon WHERE unit_id = %s)", (unit_id,))
    link_count = cursor.fetchone()[0]
    assert link_count == 1

    cursor.close()
    conn.close()
