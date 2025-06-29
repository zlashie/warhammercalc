### Dependencies
import pytest
from unittest.mock import patch, MagicMock
from psycopg2 import OperationalError
from etl.helper_functions.db_connector import connect_to_db

### Definitions
"""
Test: test_connect_to_db

Description:
    Verifies that the database connector returns a valid connection
    or raises an appropriate exception on failure.

Input:
    - Valid and invalid connection parameters

Expected Outcome:
    - Valid connection returns object
    - Failed connection raises OperationalError

Edge Cases Covered:
    - Simulated connection failure
"""
@patch("psycopg2.connect")
def test_connect_to_db_success(mock_connect):
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn

    conn_params = {
        "dbname": "test",
        "user": "test_user",
        "password": "test_pass",
        "host": "localhost",
        "port": 5432
    }

    conn = connect_to_db(conn_params)
    assert conn == mock_conn
    mock_connect.assert_called_once_with(**conn_params)

@patch("psycopg2.connect")
def test_connect_to_db_failure(mock_connect):
    mock_connect.side_effect = OperationalError("Simulated failure")

    with pytest.raises(OperationalError) as excinfo:
        connect_to_db({
            "dbname": "wrong",
            "user": "none",
            "password": "nope",
            "host": "localhost",
            "port": 5432
        })

    assert "Database connection failed" in str(excinfo.value)
