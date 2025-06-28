# WARHAMMERCALC – Warhammer 40K Unit Efficiency Analyzer

This project is a full-stack tool for evaluating Warhammer 40K unit efficiency. It uses a Python-based ETL pipeline to load unit data into a PostgreSQL database and enables analysis of unit stats, damage profiles, keywords, and abilities.

---

## 🧱 Data Model

The PostgreSQL database schema is fully normalized and includes the following tables:

- **faction**: List of all factions.
- **unit**: Core unit table with name, faction, and models per unit.
- **unit_stats**: Movement, toughness, wounds, save, etc.
- **unit_type**: Flags such as character, vehicle, infantry.
- **ability**: Special rules or traits attached to units.
- **weapon**: Weapon profiles per unit (range, attacks, AP, etc.).
- **unit_keyword**: Mapping table linking units to keywords.
- **weapon_keyword**: Mapping table linking weapons to keywords.
- **keyword**: Canonical set of keywords.

ER Diagram (Simplified):
```
faction --< unit >-- unit_stats
                    >-- unit_type
                    >-- ability
                    >-- weapon >-- weapon_keyword >-- keyword
                    >-- unit_keyword >-- keyword
```

---

## 🐳 Docker Test Setup

For testing, a separate Docker Compose environment is defined:

- Located in: `etl/tests/docker-compose.test.yml`
- Starts a PostgreSQL 16 container with:
  - `warhammer_test` database
  - Test user + password
  - Preloaded schema from `etl/tests/init-test.sql`
- Includes a **health check** to wait for DB readiness

To run the test environment:

```bash
docker compose -f etl/tests/docker-compose.test.yml up --build -d
```

To shut it down:

```bash
docker compose -f etl/tests/docker-compose.test.yml down -v
```

---

## 🔄 ETL Pipeline

Main ETL script: `etl/main.py`

**Steps:**
1. **Fetch Data** `.json` data from datasheets.json
2. **Insert Order**:
   - `faction` → `unit` → `unit_stats` → `unit_type`
   - `ability`, `weapon`, `keywords`, `unit_keyword`, `weapon_keyword`
3. Each insert is modularized into `etl/helper_functions/`
4. Designed to be **idempotent**: re-running it skips already-inserted data.

Example:

```bash
python etl/main.py
```

---

## 🧪 Tests

Run integration tests against the Docker test DB:

```bash
pytest -v etl/tests/
```

Tests cover:
- Insertion of core units
- Weapon profiles
- Keyword handling


---

## ✅ Goals

- Analyze unit efficiency using damage/point ratios and survivability
- Support full-stack UI for damage simulation and comparisons
- Enable continuous development via Docker, PostgreSQL, and CI tools like Jenkins

---