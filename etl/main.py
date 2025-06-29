### Dependencies
from helper_functions.db_connector import connect_to_db
from helper_functions.load_datasheets import load_datasheets
from helper_functions.insert_unit import insert_unit
from helper_functions.insert_faction import insert_faction
from helper_functions.validate_json import load_json_file, validate_json_with_schema, load_all_schemas
import os
from dotenv import load_dotenv

### Main ETL
"""
Description:    
Main ETL (Extract-Transform-Load) execution function. 
It loads datasheet information from a JSON file, establishes a PostgreSQL database connection,
and inserts each unit's structured data (faction, stats, weapons, abilities, keywords) into normalized tables.

Input:          
Environment variables for database configuration (DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT).
Local file path: 'data/datasheets.json' — structured JSON containing faction->units->attributes.

Output:         
Populates PostgreSQL database tables with datasheet content.
Commits all insertions in a single transaction. Raises exceptions if any stage fails.
"""
def run_etl():
    load_dotenv()

    conn_params = {
        "dbname": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "host": os.getenv("DB_HOST"),
        "port": int(os.getenv("DB_PORT", 5432)),
    }

    schemas = load_all_schemas("schemas")
    data = load_datasheets("data/datasheets.json")
    conn = connect_to_db(conn_params)
    cursor = conn.cursor()

    # Counters
    faction_count = 0
    unit_count = 0
    weapon_count = 0

    for faction_name, faction_data in data.items():
        validate_json_with_schema(faction_name, schemas["faction_schema"])
        faction_id = insert_faction(cursor, faction_name)
        faction_count += 1

        for unit in faction_data.get("units", []):
            validate_json_with_schema(unit, schemas["unit_schema"])

            if "unit_stats" in unit:
                validate_json_with_schema(unit["unit_stats"], schemas["unit_stats_schema"])

            if "unit_type" in unit:
                validate_json_with_schema(unit["unit_type"], schemas["unit_type_schema"])

            for weapon in unit.get("weapons", []):
                validate_json_with_schema(weapon, schemas["weapon_schema"])

            for ability in unit.get("abilities", []):
                validate_json_with_schema({"name": ability}, schemas["ability_schema"])

            for keyword in unit.get("keywords", []):
                validate_json_with_schema({"name": keyword}, schemas["keyword_schema"])

            insert_unit(cursor, unit, faction_id)
            unit_count += 1
            weapon_count += len(unit.get("weapons", []))

    conn.commit()
    cursor.close()
    conn.close()

    print("ETL Summary")
    print(f" - Factions inserted: {faction_count}")
    print(f" - Units inserted:    {unit_count}")
    print(f" - Weapons inserted:  {weapon_count}")

if __name__ == "__main__":
    run_etl()