### Dependencies
import requests
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError

### Variables
NS = {'bs': 'http://www.battlescribe.net/schema/catalogueSchema'}

### Definition
"""
Downloads and parses a Battlescribe .cat file from the given URL.
Args:       url (str): The URL of the .cat file to download.
Returns:    ElementTree.Element: The root element of the parsed XML tree.
"""
def load_catalogue(url: str) -> ET.Element:
    try:
        response = requests.get(url)
        response.raise_for_status()
        return ET.fromstring(response.content)
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to fetch catalogue from URL: {url}\nReason: {e}")
    except ParseError as e:
        print(f"[ERROR] Failed to parse XML content from: {url}\nReason: {e}")
    return None