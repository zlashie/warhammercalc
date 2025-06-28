-- Drop in reverse dependency order
DROP TABLE IF EXISTS weapon_keyword;
DROP TABLE IF EXISTS weapon;
DROP TABLE IF EXISTS ability;
DROP TABLE IF EXISTS unit_keyword;
DROP TABLE IF EXISTS keyword;
DROP TABLE IF EXISTS unit_stats;
DROP TABLE IF EXISTS unit;
DROP TABLE IF EXISTS faction;

-- 1. Factions
CREATE TABLE faction (
    faction_id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

-- 2. Units
CREATE TABLE unit (
    unit_id SERIAL PRIMARY KEY,
    faction_id INT REFERENCES faction(faction_id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    faction TEXT NOT NULL,
    models_per_unit INT[]  -- Array of valid model counts (e.g. [1] or [3, 6])
);

-- 3. Unit Stats
CREATE TABLE unit_stats (
    unit_id INT PRIMARY KEY REFERENCES unit(unit_id) ON DELETE CASCADE,
    movement INT,
    toughness INT,
    save INT,
    wounds INT,
    leadership INT,
    objective_control INT,
    invulnerable_save INT,
    feel_no_pain INT
);

-- 4. Keywords (Many-to-Many)
CREATE TABLE keyword (
    keyword_id SERIAL PRIMARY KEY,
    keyword TEXT UNIQUE NOT NULL
);

CREATE TABLE unit_keyword (
    unit_id INT REFERENCES unit(unit_id) ON DELETE CASCADE,
    keyword_id INT REFERENCES keyword(keyword_id) ON DELETE CASCADE,
    PRIMARY KEY (unit_id, keyword_id)
);

-- 5. Abilities (One-to-Many)
CREATE TABLE ability (
    ability_id SERIAL PRIMARY KEY,
    unit_id INT REFERENCES unit(unit_id) ON DELETE CASCADE,
    name TEXT NOT NULL
);

-- 6. Weapons (One-to-Many)
CREATE TABLE weapon (
    weapon_id SERIAL PRIMARY KEY,
    unit_id INT REFERENCES unit(unit_id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    range INT,  -- NULL for melee
    range_type TEXT CHECK (range_type IN ('melee', 'ranged')),
    attacks INT,
    ballistic_skill INT,
    weapon_skill INT,
    strength INT,
    ap INT,
    damage INT,
    keywords TEXT[]
);

-- 7. Weapon Keywords (Many-to-Many)
CREATE TABLE weapon_keyword (
    weapon_id INT REFERENCES weapon(weapon_id) ON DELETE CASCADE,
    keyword TEXT NOT NULL,
    PRIMARY KEY (weapon_id, keyword)
);

-- 8. Unit Type Flags (One-to-One)
CREATE TABLE unit_type (
    unit_id INT PRIMARY KEY REFERENCES unit(unit_id) ON DELETE CASCADE,
    character BOOLEAN DEFAULT FALSE,
    vehicle BOOLEAN DEFAULT FALSE,
    infantry BOOLEAN DEFAULT FALSE,
    monster BOOLEAN DEFAULT FALSE,
    battleline BOOLEAN DEFAULT FALSE,
    epic_hero BOOLEAN DEFAULT FALSE,
    fly BOOLEAN DEFAULT FALSE
);