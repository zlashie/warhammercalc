### Dependencies
import json
from typing import Dict, Any
import os

### Definitions
"""
Description: Loads and validates the datasheet JSON file from the specified path.
Input:       filepath (str) - Path to the JSON file
Output:      data (Dict[str, Any]) - Parsed JSON data structured by faction

Raises:
    FileNotFoundError: If the JSON file doesn't exist
    json.JSONDecodeError: If the file is not valid JSON
    ValueError: If top-level structure is not a dict
"""
def load_datasheets(filepath: str) -> Dict[str, Any]:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    with open(filepath, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Invalid JSON in {filepath}: {e}", e.doc, e.pos)
    
    if not isinstance(data, dict):
        raise ValueError("Top-level structure must be a dictionary grouped by faction names.")
    
    return data
