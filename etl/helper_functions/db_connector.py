### Dependencies
import psycopg2
from psycopg2 import OperationalError
from typing import Dict

### Definitions
"""
Description: Connects to PostgreSQL using provided connection parameters.
Input:       conn_params (dict) - DB credentials: dbname, user, password, host, port
Output:      connection (psycopg2 connection object)

Raises:
    OperationalError: If connection fails
"""
def connect_to_db(conn_params: Dict[str, str]):
    try:
        conn = psycopg2.connect(**conn_params)
        return conn
    except OperationalError as e:
        raise OperationalError(f"Database connection failed: {e}")
