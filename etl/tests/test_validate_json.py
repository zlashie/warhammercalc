### Dependencies
import os
import json
import pytest
from jsonschema import ValidationError, SchemaError
from etl.helper_functions.validate_json import (
    load_json_file,
    validate_json_with_schema,
    load_all_schemas,
)

### Definitions
"""
Test: test_validate_json_helpers

Description:
    Tests schema loading, JSON validation, and error handling for all validation helpers.

Input:
    - Valid and invalid JSON files
    - Valid and invalid schema files
    - Directory with schema files

Expected Outcome:
    - Valid JSON and schema pass silently
    - Invalid JSON or schema raise appropriate exceptions

Edge Cases Covered:
    - Non-existent file
    - Malformed schema
    - JSON fails validation
"""
def test_load_json_file_success(tmp_path):
    filepath = tmp_path / "data.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump({"key": "value"}, f)

    result = load_json_file(str(filepath))
    assert result == {"key": "value"}

def test_load_json_file_missing():
    with pytest.raises(FileNotFoundError):
        load_json_file("nonexistent.json")

def test_validate_json_with_valid_schema():
    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"}
        },
        "required": ["name"]
    }
    data = {"name": "Unit"}
    validate_json_with_schema(data, schema)  # Should not raise

def test_validate_json_with_invalid_data():
    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"}
        },
        "required": ["name"]
    }
    data = {"title": "Unit"}
    with pytest.raises(ValidationError):
        validate_json_with_schema(data, schema)

def test_validate_json_with_invalid_schema():
    schema = {
        "type": "invalid_type",  # Not a valid JSON Schema type
    }
    data = {"name": "test"}
    with pytest.raises(SchemaError):
        validate_json_with_schema(data, schema)

def test_load_all_schemas_success(tmp_path):
    filenames = [
        "unit_schema.json", "unit_stats_schema.json", "weapon_schema.json",
        "ability_schema.json", "faction_schema.json", "keyword_schema.json",
        "unit_keyword_schema.json", "unit_type_schema.json", "weapon_keyword_schema.json"
    ]
    for fname in filenames:
        with open(tmp_path / fname, "w", encoding="utf-8") as f:
            json.dump({"type": "object"}, f)

    result = load_all_schemas(str(tmp_path))
    assert len(result) == 9
    assert "unit_schema" in result
    assert result["unit_schema"]["type"] == "object"
