from helper_functions.extract_unit_data import extract_unit_data
from helper_functions.db_inserter import insert_unit_data
import os
from dotenv import load_dotenv

url = "https://raw.githubusercontent.com/BSData/wh40k-10e/main/Imperium%20-%20Space%20Marines.cat"
unit_name = "Assault Intercessors with Jump Packs"

data = extract_unit_data(url, unit_name)

# PostgreSQL connection parameters
load_dotenv()

conn_params = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", 5432)),
}

insert_unit_data(data, conn_params)