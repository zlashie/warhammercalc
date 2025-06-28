### Dependencies
from typing import Dict, Any
from helper_functions.insert_unit_stats import insert_unit_stats
from helper_functions.insert_weapons import insert_weapons
from helper_functions.insert_abilities import insert_abilities
from helper_functions.insert_unit_type import insert_unit_types
from helper_functions.insert_unit_keywords import insert_unit_keywords

### Definitions
"""
Description: Inserts unit data into the 'unit' table and delegates all related inserts.
Input:
    - cursor: psycopg2 cursor
    - unit_data: Dict containing unit attributes
    - faction_id: int, foreign key from faction table
Output:
    - None
"""
def insert_unit(cursor, unit_data: Dict[str, Any], faction_id: int) -> None:
    try:
        name = unit_data["unit_name"]
        models = unit_data.get("models_pr_unit", 1)
    except KeyError as e:
        raise KeyError(f"Missing required field in unit data: {e}")

    cursor.execute(
        """
        INSERT INTO unit (name, models_pr_unit, faction_id)
        VALUES (%s, %s, %s)
        RETURNING unit_id
        """,
        (name, models, faction_id)
    )
    unit_id = cursor.fetchone()[0]

    insert_unit_stats(cursor, unit_id, unit_data.get("unit_stats", {}))
    insert_unit_types(cursor, unit_id, unit_data.get("keywords", []))
    insert_abilities(cursor, unit_id, unit_data.get("abilities", []))
    insert_weapons(cursor, unit_id, unit_data.get("weapons", [])) 
    insert_unit_keywords(cursor, unit_id, unit_data.get("keywords", []))
