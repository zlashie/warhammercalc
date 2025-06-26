### Dependencies
from dataclasses import dataclass
from typing import Optional

### Classes
@dataclass
class WeaponProfile:
    name: str
    range: Optional[str] = None
    attacks: Optional[str] = None
    bs: Optional[str] = None
    ws: Optional[str] = None
    strength: Optional[str] = None
    ap: Optional[str] = None
    damage: Optional[str] = None
    keywords: Optional[str] = None

@dataclass
class UnitStats:
    name: str
    movement: Optional[str] = None
    toughness: Optional[str] = None
    save: Optional[str] = None
    wounds: Optional[str] = None
    leadership: Optional[str] = None
    oc: Optional[str] = None
