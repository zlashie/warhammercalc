### Dependencies
import psycopg2
from etl.helper_functions.insert_weapon_keywords import insert_weapon_keywords

### Definitions
"""
Test: test_insert_weapon_keywords_basic

Description:
    Verifies that weapon keywords are linked correctly in the weapon_keyword table.
    Ensures proper keyword creation and no duplicate links.

Input:
    - weapon_id for a test weapon
    - Keywords list: ["Anti-Vehicle", "Melta"]

Expected Outcome:
    - Keywords inserted via insert_keywords()
    - weapon_keyword contains correct (weapon_id, keyword_id) mappings

Edge Cases Covered:
    - Empty keyword list (should skip insert)
    - Repeated keyword (should not duplicate)
"""
def test_insert_weapon_keywords_basic(test_db):
    conn = psycopg2.connect(**test_db)
    cursor = conn.cursor()

    # Setup: Create faction/unit/weapon
    cursor.execute("INSERT INTO faction (name) VALUES ('WeaponKeywordFaction') RETURNING faction_id;")
    faction_id = cursor.fetchone()[0]
    cursor.execute("""
        INSERT INTO unit (name, models_pr_unit, faction_id)
        VALUES ('WeaponKeywordUnit', '1', %s)
        RETURNING unit_id
    """, (faction_id,))
    unit_id = cursor.fetchone()[0]
    cursor.execute("""
        INSERT INTO weapon (name, unit_id, range, range_type, attacks, weapon_skill,
                            ballistic_skill, strength, ap, damage)
        VALUES ('Flamer', %s, 12, 'ranged', 1, NULL, 3, 4, 1, 1)
        RETURNING weapon_id
    """, (unit_id,))
    weapon_id = cursor.fetchone()[0]

    keywords = ["Anti-Vehicle", "Melta"]
    insert_weapon_keywords(cursor, weapon_id, keywords)

    # Validate links
    cursor.execute("SELECT COUNT(*) FROM weapon_keyword WHERE weapon_id = %s", (weapon_id,))
    count = cursor.fetchone()[0]
    assert count == 2

    # Edge case: empty list
    insert_weapon_keywords(cursor, weapon_id, [])
    cursor.execute("SELECT COUNT(*) FROM weapon_keyword WHERE weapon_id = %s", (weapon_id,))
    count_after = cursor.fetchone()[0]
    assert count_after == 2  # No change

    cursor.close()
    conn.close()
