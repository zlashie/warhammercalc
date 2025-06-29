erDiagram

  faction ||--o{ unit : "has"
  unit ||--|| unit_stats : "has"
  unit ||--|| unit_type : "has"
  unit ||--o{ weapon : "has"
  unit ||--o{ ability : "has"
  unit ||--o{ unit_keyword : "tags"
  keyword ||--o{ unit_keyword : "is in"
  weapon ||--o{ weapon_keyword : "has"
  keyword ||--o{ weapon_keyword : "is in"

  faction {
    int faction_id PK
    string name
  }

  unit {
    int unit_id PK
    int faction_id FK
    string name
    int models_pr_unit
  }

  unit_stats {
    int unit_id PK, FK
    int movement
    int toughness
    int save
    int wounds
    int leadership
    int objective_control
    int invulnerable_save
    int feel_no_pain
  }

  unit_type {
    int unit_id PK, FK
    bool character
    bool vehicle
    bool infantry
    bool monster
    bool battleline
    bool epic_hero
    bool fly
  }

  weapon {
    int weapon_id PK
    int unit_id FK
    string name
    int range
    string range_type
    int attacks
    int ballistic_skill
    int weapon_skill
    int strength
    int ap
    string damage
  }

  ability {
    int ability_id PK
    int unit_id FK
    string name
  }

  keyword {
    int keyword_id PK
    string name
  }

  unit_keyword {
    int unit_id PK, FK
    int keyword_id PK, FK
  }

  weapon_keyword {
    int weapon_id PK, FK
    int keyword_id PK, FK
  }
