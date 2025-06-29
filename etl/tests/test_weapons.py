### Dependencies
from etl.helper_functions.insert_weapons import insert_weapons
import psycopg2
import pytest

### Definitions
"""
Test: test_insert_weapons_full_coverage

Description:
    Expands testing to cover all branches in insert_weapons:
    - Successful insert with keywords
    - Insert with empty keyword list
    - Duplicate weapon insert (ON CONFLICT logic)
    - Missing required field (triggers exception)

Input:
    - Various weapon dicts with different edge cases

Expected Outcome:
    - Inserts behave as expected
    - Duplicates do not cause failure
    - Missing field raises KeyError or fails validation

Edge Cases Covered:
    - Empty keywords list
    - Duplicate weapon name
    - Missing weapon field
"""
def test_insert_weapons_full_coverage(test_db):
    conn = psycopg2.connect(**test_db)
    cursor = conn.cursor()

    # Setup: Insert faction/unit
    cursor.execute("INSERT INTO faction (name) VALUES ('FullWeaponTest') RETURNING faction_id;")
    faction_id = cursor.fetchone()[0]
    cursor.execute("""
        INSERT INTO unit (name, models_pr_unit, faction_id)
        VALUES ('Unit A', '1', %s)
        RETURNING unit_id
    """, (faction_id,))
    unit_id = cursor.fetchone()[0]

    # 1. Standard weapon with keyword
    weapons = [{
        "name": "Flamer",
        "range": 12,
        "range_type": "ranged",
        "attacks": 3,
        "ballistic_skill": 4,
        "weapon_skill": None,
        "strength": 4,
        "ap": 1,
        "damage": 1,
        "keywords": ["Burn"]
    }]
    insert_weapons(cursor, unit_id, weapons)

    # 2. Weapon without keywords
    weapons_no_keywords = [{
        "name": "Lasgun",
        "range": 24,
        "range_type": "ranged",
        "attacks": 2,
        "ballistic_skill": 3,
        "weapon_skill": None,
        "strength": 3,
        "ap": 0,
        "damage": 1,
        "keywords": []
    }]
    insert_weapons(cursor, unit_id, weapons_no_keywords)
    
    # 3. Weapon with string damage (e.g., "D6")
    weapons_dice_damage = [{
        "name": "Plasma Cannon",
        "range": 36,
        "range_type": "ranged",
        "attacks": 1,
        "ballistic_skill": 3,
        "weapon_skill": None,
        "strength": 8,
        "ap": -3,
        "damage": "D6",
        "keywords": ["Blast"]
    }]
    insert_weapons(cursor, unit_id, weapons_dice_damage)

    # Assert it was added
    cursor.execute("SELECT damage FROM weapon WHERE name = 'Plasma Cannon' AND unit_id = %s", (unit_id,))
    result = cursor.fetchone()
    assert result is not None
    assert result[0] == "D6"

    # 4. Duplicate weapon (ON CONFLICT DO NOTHING)
    insert_weapons(cursor, unit_id, weapons_no_keywords)

    cursor.execute("SELECT COUNT(*) FROM weapon WHERE unit_id = %s", (unit_id,))
    count = cursor.fetchone()[0]
    assert count == 3  # Flamer + Lasgun + Plasma Cannon (duplicate ignored)

    # 5. Invalid weapon (missing 'name') – should raise KeyError or general Exception
    broken_weapons = [{
        # "name": "Broken",
        "range": 0,
        "range_type": "melee",
        "attacks": 1,
        "ballistic_skill": None,
        "weapon_skill": 3,
        "strength": 5,
        "ap": 2,
        "damage": 2,
        "keywords": []
    }]
    with pytest.raises(Exception):
        insert_weapons(cursor, unit_id, broken_weapons)

    cursor.close()
    conn.close()
