### Dependencies
import json
import os
from jsonschema import validate, ValidationError, SchemaError
from typing import Any, Dict

### Definitions
"""
Load a JSON file from the specified path.
"""
def load_json_file(path: str) -> Dict[str, Any]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)

"""
Validate a JSON object against a schema.

Raises:
    ValidationError: if the data does not conform to the schema
    SchemaError: if the schema itself is invalid
"""
def validate_json_with_schema(data: Dict[str, Any], schema: Dict[str, Any]) -> None:
    try:
        validate(instance=data, schema=schema)
    except ValidationError as ve:
        raise ValidationError(f"JSON validation error: {ve.message}")
    except SchemaError as se:
        raise SchemaError(f"Schema definition error: {se.message}")
    
"""
Loads and returns all predefined JSON schemas from a specified directory.

This function expects a fixed set of schema filenames corresponding to the data model
(e.g., unit, weapon, faction, etc.). It reads each schema file from disk and loads its
content into a dictionary keyed by the schema's base filename (without extension).

Args:
    schema_dir (str): Path to the directory containing JSON schema files.

Returns:
    Dict[str, Dict[str, Any]]: A dictionary where each key is a schema name (e.g., "unit_schema")
    and the value is the loaded JSON schema as a dictionary.

Raises:
    FileNotFoundError: If any schema file is missing.
    json.JSONDecodeError: If a schema file is not valid JSON.
"""
def load_all_schemas(schema_dir: str) -> Dict[str, Dict[str, Any]]:
    schema_files = [
        "unit_schema.json",
        "unit_stats_schema.json",
        "weapon_schema.json",
        "ability_schema.json",
        "faction_schema.json",
        "keyword_schema.json",
        "unit_keyword_schema.json",
        "unit_type_schema.json",
        "weapon_keyword_schema.json"
    ]
    return {
        os.path.splitext(f)[0]: load_json_file(os.path.join(schema_dir, f))
        for f in schema_files
    }