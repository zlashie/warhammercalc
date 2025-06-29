### Dependencies
import os
import sys
import time
import psycopg2
import pytest
import subprocess
import docker
from dotenv import load_dotenv

load_dotenv(dotenv_path='etl/tests/.env.test') 

### How to run test suite
# .\venv\Scripts\Activate.ps1
# pytest -v etl/tests/

### How to run test coverage report
# .\venv\Scripts\Activate.ps1
# pytest --cov=etl --cov-report=term-missing

# Add the root project folder to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

DB_CONFIG = {
    "dbname": os.environ.get("DB_NAME"),
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASSWORD"),
    "host": os.environ.get("DB_HOST"),
    "port": int(os.environ.get("DB_PORT", 5432))
}

### Helper to wait for container health
def wait_for_container_healthy(container_name: str, timeout: int = 60):
    client = docker.from_env()
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            container = client.containers.get(container_name)
            if container.attrs["State"]["Health"]["Status"] == "healthy":
                return True
        except Exception:
            pass
        time.sleep(1)
    raise RuntimeError(f"Container '{container_name}' did not become healthy in time.")

### Fixture
@pytest.fixture(scope="session")
def test_db():
    compose_file = "etl/tests/docker-compose.test.yml"
    container_name = "tests-test-db-1"

    print("🚀 Launching test DB container...")
    subprocess.run(["docker", "compose", "-f", compose_file, "up", "--build", "-d"], check=True)

    print("🩺 Waiting for container health...")
    wait_for_container_healthy(container_name)
    print("✅ Container is healthy.")

    print("🔧 DB_CONFIG in use:", DB_CONFIG)

    # Retry DB connection
    for i in range(60):
        try:
            print(f"⏳ Attempt {i+1}/60: Trying to connect to DB...")
            conn = psycopg2.connect(**DB_CONFIG)
            conn.close()
            print("✅ Connection to DB successful!")
            break
        except psycopg2.OperationalError as e:
            print(f"🚫 DB not ready yet: {e}")
            time.sleep(1)
    else:
        raise RuntimeError("Test DB did not become available in time")

    yield DB_CONFIG

    print("🧹 Tearing down test DB container...")
    subprocess.run(["docker", "compose", "-f", compose_file, "down"], check=True)

