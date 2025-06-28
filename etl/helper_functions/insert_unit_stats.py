### Dependencies
from typing import Dict, Optional
import psycopg2

### Definitions
"""
Description: Inserts unit statline into the 'unit_stats' table.
Input:
    - cursor (psycopg2.extensions.cursor): Active DB cursor
    - unit_id (int): ID of the unit this statline belongs to
    - stats (Dict[str, Optional[int]]): Dictionary of unit stat values

Output: None

Raises:
    KeyError: If any required stat field is missing
    Exception: For any unexpected database errors
"""
def insert_unit_stats(cursor, unit_id: int, stats: Dict[str, Optional[int]]) -> None:
    required_keys = [
        "movement", "toughness", "save", "wounds", "leadership",
        "objective_control", "invulnerable_save", "feel_no_pain"
    ]

    for key in required_keys:
        if key not in stats:
            raise KeyError(f"Missing required stat '{key}' in unit_stats for unit_id {unit_id}")

    try:
        cursor.execute("""
            INSERT INTO unit_stats (
                unit_id, movement, toughness, save, wounds, leadership,
                objective_control, invulnerable_save, feel_no_pain
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (unit_id) DO NOTHING
        """, (
            unit_id,
            stats["movement"],
            stats["toughness"],
            stats["save"],
            stats["wounds"],
            stats["leadership"],
            stats["objective_control"],
            stats["invulnerable_save"],
            stats["feel_no_pain"]
        ))
    except Exception as e:
        raise Exception(f"Failed to insert unit_stats for unit_id {unit_id}: {e}")