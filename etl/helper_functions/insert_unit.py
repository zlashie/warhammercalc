### Dependencies
from typing import Dict, Any
from helper_functions.insert_unit_stats import insert_unit_stats
from helper_functions.insert_weapons import insert_weapons
from helper_functions.insert_abilities import insert_abilities
from helper_functions.insert_unit_type import insert_unit_types

### Definitions
"""
Description: Inserts unit data into the 'unit' table and delegates insertion of stats, weapons, abilities, and unit types.
Input:       cursor (psycopg2 cursor) - Active DB cursor
             unit_data (dict) - Unit dictionary containing all stats, weapons, etc.
             faction (str) - The faction name to tag this unit with
Output:      None

Raises:
    KeyError: If required fields are missing in unit_data
"""
def insert_unit(cursor, unit_data: Dict[str, Any], faction: str) -> None:
    try:
        name = unit_data["unit_name"]
    except KeyError:
        raise KeyError("Missing 'unit_name' in unit data")

    cursor.execute(
        """
        INSERT INTO unit (name, faction) VALUES (%s, %s)
        RETURNING unit_id
        """,
        (name, faction)
    )
    unit_id = cursor.fetchone()[0]

    insert_unit_stats(cursor, unit_id, unit_data.get("unit_stats", {}))
    insert_weapons(cursor, unit_id, unit_data.get("weapons", []))
    insert_abilities(cursor, unit_id, unit_data.get("abilities", []))
    insert_unit_types(cursor, unit_id, unit_data.get("keywords", []))