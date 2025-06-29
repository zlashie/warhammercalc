### Dependencies
import os
import json
import pytest
from etl.helper_functions.load_datasheets import load_datasheets

### Definitions
"""
Test: test_load_datasheets_variants

Description:
    Verifies that JSON files are loaded correctly, and that error cases
    such as invalid JSON, missing files, and incorrect structure are caught.

Input:
    - Valid file with dict root
    - Invalid JSON file
    - File with wrong top-level structure (e.g., list)

Expected Outcome:
    - Correct dict returned from valid file
    - FileNotFoundError, JSONDecodeError, or ValueError thrown when appropriate

Edge Cases Covered:
    - Empty file
    - File exists but is not valid JSON
"""
def test_load_datasheets_success(tmp_path):
    valid_json_path = tmp_path / "valid.json"
    with open(valid_json_path, "w", encoding="utf-8") as f:
        json.dump({"Space Marines": []}, f)
    
    result = load_datasheets(str(valid_json_path))
    assert isinstance(result, dict)
    assert "Space Marines" in result

def test_load_datasheets_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_datasheets("nonexistent_file.json")

def test_load_datasheets_invalid_json(tmp_path):
    invalid_json_path = tmp_path / "invalid.json"
    with open(invalid_json_path, "w", encoding="utf-8") as f:
        f.write("{ invalid json ")

    with pytest.raises(json.JSONDecodeError):
        load_datasheets(str(invalid_json_path))

def test_load_datasheets_wrong_structure(tmp_path):
    list_json_path = tmp_path / "list.json"
    with open(list_json_path, "w", encoding="utf-8") as f:
        json.dump(["bad", "structure"], f)

    with pytest.raises(ValueError, match="Top-level structure must be a dictionary"):
        load_datasheets(str(list_json_path))
