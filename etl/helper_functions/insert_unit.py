### Dependencies
from typing import Dict, Any, Tuple
from .insert_unit_stats import insert_unit_stats
from .insert_weapons import insert_weapons
from .insert_abilities import insert_abilities
from .insert_unit_type import insert_unit_types
from .insert_unit_keywords import insert_unit_keywords

### Definitions
"""
Description: Inserts unit data into the 'unit' table and delegates all related inserts.
Avoids duplicates using a UNIQUE constraint on (name, faction_id).
Supports 'models_per_unit' as a string like "1" or "3,6".

Input:
    - cursor: psycopg2 cursor
    - unit_data: Dict containing unit attributes
    - faction_id: int, foreign key from faction table
Output:
    - None
"""
def insert_unit(cursor, unit_data: Dict[str, Any], faction_id: int) -> Tuple[bool, Dict[str, int]]:
    try:
        name = unit_data["unit_name"]
        models = str(unit_data.get("models_per_unit", "1"))  
    except KeyError as e:
        raise KeyError(f"Missing required field in unit data: {e}")

    cursor.execute(
        """
        INSERT INTO unit (name, models_pr_unit, faction_id)
        VALUES (%s, %s, %s)
        ON CONFLICT ON CONSTRAINT unique_unit_per_faction DO NOTHING
        RETURNING unit_id
        """,
        (name, models, faction_id)
    )
    result = cursor.fetchone()

    if result:
        unit_id = result[0]
        was_inserted = True
    else:
        cursor.execute("""
            SELECT unit_id FROM unit
            WHERE name = %s AND faction_id = %s
        """, (name, faction_id))
        unit_id = cursor.fetchone()[0]
        was_inserted = False

    counters = {"weapons": 0, "abilities": 0, "keywords": 0}

    insert_unit_stats(cursor, unit_id, unit_data.get("unit_stats", {}))
    insert_unit_types(cursor, unit_id, unit_data.get("keywords", []))
    counters["abilities"] += insert_abilities(cursor, unit_id, unit_data.get("abilities", []))
    counters["weapons"] += insert_weapons(cursor, unit_id, unit_data.get("weapons", []))
    counters["keywords"] += insert_unit_keywords(cursor, unit_id, unit_data.get("keywords", []))

    return was_inserted, counters
