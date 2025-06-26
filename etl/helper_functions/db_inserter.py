### Dependencies
import psycopg2
from typing import Dict, Any
from psycopg2 import sql, OperationalError, Error

### Definition
"""
Inserts unit stats and weapon profiles into PostgreSQL.

Args:       data (Dict[str, Any]): A dictionary containing 'unit_stats' and 'weapon_profiles'.
            conn_params (Dict[str, str]): Database connection parameters.

Raises:     psycopg2.DatabaseError: If any database error occurs.
"""
def insert_unit_data(data: Dict[str, Any], conn_params: Dict[str, str]) -> None:
    try:
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()

        unit_stats = data["unit_stats"]
        weapon_profiles = data["weapon_profiles"]

        # Insert unit and get unit_id
        cursor.execute("""
            INSERT INTO unit (name) VALUES (%s) RETURNING unit_id
        """, (unit_stats["name"],))
        unit_id = cursor.fetchone()[0]

        # Insert unit stats
        cursor.execute("""
            INSERT INTO unit_stats (
                unit_id, movement, toughness, save, wounds, leadership, objective_control, invuln_save, feel_no_pain
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, NULL, NULL)
        """, (
            unit_id,
            unit_stats.get("movement"),
            unit_stats.get("toughness"),
            unit_stats.get("save"),
            unit_stats.get("wounds"),
            unit_stats.get("leadership"),
            unit_stats.get("oc"),  # mapped to column `objective_control`
        ))

        # Insert each weapon
        for wp in weapon_profiles:
            cursor.execute("""
                INSERT INTO attack (
                    unit_id, weapon_name, range, range_type, attacks,
                    weapon_skill, ballistic_skill, ap, damage
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                unit_id,
                wp.get("name"),
                wp.get("range"),
                "Melee" if wp.get("range") == "Melee" else "Ranged",
                wp.get("attacks"),
                wp.get("ws"),
                wp.get("bs"),
                wp.get("ap"),
                wp.get("damage"),
            ))

        conn.commit()
        print(f"Inserted unit '{unit_stats['name']}' and {len(weapon_profiles)} weapons into the database.")

    except OperationalError as e:
        print(f"Database connection failed: {e}")
    except Error as e:
        print(f"Database error: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
