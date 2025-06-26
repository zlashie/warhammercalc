DROP TABLE IF EXISTS unit_type;
DROP TABLE IF EXISTS unit_stats;
DROP TABLE IF EXISTS attack;
DROP TABLE IF EXISTS ability;
DROP TABLE IF EXISTS unit;

-- Main unit table
CREATE TABLE unit (
    unit_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

-- Abilities 
CREATE TABLE ability (
    id SERIAL PRIMARY KEY,
    unit_id INT REFERENCES unit(unit_id) ON DELETE CASCADE,
    ability_text TEXT
);

-- Attacks / Weapons
CREATE TABLE attack (
    id SERIAL PRIMARY KEY,
    unit_id INT REFERENCES unit(unit_id) ON DELETE CASCADE,
    weapon_name TEXT,
    range TEXT,
    range_type TEXT, 
    attacks TEXT,
    weapon_skill TEXT,
    ballistic_skill TEXT,
    strength TEXT,
    ap TEXT,
    damage TEXT,
    keywords TEXT
);

-- Statline
CREATE TABLE unit_stats (
    unit_id INT PRIMARY KEY REFERENCES unit(unit_id) ON DELETE CASCADE,
    movement TEXT,
    toughness TEXT,
    save TEXT,
    wounds TEXT,
    leadership TEXT,
    objective_control TEXT,
    invuln_save TEXT,
    feel_no_pain TEXT
);

-- Unit type flags 
CREATE TABLE unit_type (
    unit_id INT PRIMARY KEY REFERENCES unit(unit_id) ON DELETE CASCADE,
    character BOOLEAN DEFAULT FALSE,
    vehicle BOOLEAN DEFAULT FALSE,
    infantry BOOLEAN DEFAULT FALSE,
    monster BOOLEAN DEFAULT FALSE,
    battleline BOOLEAN DEFAULT FALSE,
    fly BOOLEAN DEFAULT FALSE
);
