### Dependencies
from helper_functions.db_connector import connect_to_db
from helper_functions.load_datasheets import load_datasheets
from helper_functions.insert_unit import insert_unit
import os
from dotenv import load_dotenv

### Definitions
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

    data = load_datasheets("data/datasheets.json")
    conn = connect_to_db(conn_params)
    cursor = conn.cursor()

    for faction, faction_data in data.items():
        for unit in faction_data.get("units", []):
            insert_unit(cursor, unit, faction)

    conn.commit()
    cursor.close()
    conn.close()

### Run
if __name__ == "__main__":
    run_etl()
