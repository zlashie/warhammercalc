### Dependencies
import pytest
from unittest.mock import patch, MagicMock
from etl import main

### Definitions
"""
Test: test_run_etl_integration_mocked

Description:
    Validates that run_etl() flows through schema loading,
    data loading, faction + unit inserts and DB commit,
    without actually hitting filesystem or DB.

Mocks:
    - os.getenv → returns test DB config
    - load_dotenv → suppressed
    - load_datasheets → returns mock data
    - load_all_schemas → returns minimal valid schemas
    - connect_to_db → returns mock cursor/connection

Expected Outcome:
    - All major stages of ETL flow run successfully
    - Validations and inserts are invoked
"""
@patch("etl.main.connect_to_db")
@patch("etl.main.insert_unit")
@patch("etl.main.insert_faction")
@patch("etl.main.validate_json_with_schema")
@patch("etl.main.load_datasheets")
@patch("etl.main.load_all_schemas")
@patch("etl.main.load_dotenv")
@patch("etl.main.os.getenv")
def test_run_etl_integration_mocked(
    mock_getenv,
    mock_dotenv,
    mock_load_schemas,
    mock_load_datasheets,
    mock_validate_json,
    mock_insert_faction,
    mock_insert_unit,
    mock_connect_to_db
):
    # Simulate environment variables
    mock_getenv.side_effect = lambda key, default=None: {
        "DB_NAME": "test",
        "DB_USER": "test_user",
        "DB_PASSWORD": "test_pass",
        "DB_HOST": "localhost",
        "DB_PORT": "5432"
    }.get(key, default)

    # Minimal schema and data structure
    mock_load_schemas.return_value = {
        "faction_schema": {},
        "unit_schema": {},
        "unit_stats_schema": {},
        "unit_type_schema": {},
        "weapon_schema": {},
        "ability_schema": {},
        "keyword_schema": {}
    }

    mock_load_datasheets.return_value = {
        "Test Faction": {
            "units": [
                {
                    "unit_name": "Test Unit",
                    "models_per_unit": "1",
                    "unit_stats": {
                        "movement": 6, "toughness": 4, "save": 3, "wounds": 2,
                        "leadership": 6, "objective_control": 1, "invulnerable_save": 5,
                        "feel_no_pain": None
                    },
                    "weapons": [{"name": "Bolter", "range": 24, "range_type": "ranged", "attacks": 2,
                                 "ballistic_skill": 3, "weapon_skill": None, "strength": 4,
                                 "ap": 1, "damage": 1, "keywords": []}],
                    "abilities": ["Rapid Fire"],
                    "keywords": ["Infantry"]
                }
            ]
        }
    }

    # Mock DB connection
    mock_cursor = MagicMock()
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect_to_db.return_value = mock_conn

    # Simulate faction insert returning ID
    mock_insert_faction.return_value = 1

    # Run
    main.run_etl()

    # Assertions
    mock_load_schemas.assert_called_once()
    mock_load_datasheets.assert_called_once()
    mock_insert_faction.assert_called_once_with(mock_cursor, "Test Faction")
    mock_insert_unit.assert_called_once()
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()
