import os
import sys
from pathlib import Path

# src root for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# set environment variables
os.environ["DB_USER"] = "gbc-api-user"
os.environ["DB_PASS_SECRET"] = "xxxx"  # REPLACE BEFORE COMMIT
os.environ["DB_NAME"] = "gbc_employment_db"
os.environ["INSTANCE_CONNECTION_NAME"] = (
    "xxxx"  # REPLACE BEFORE COMMIT
)

from src.api.connector import pool
from src.api.schemas import Base


def main():
    """Connects to the database and creates tables"""
    print("Connecting to the database and creating tables...")
    try:
        Base.metadata.create_all(bind=pool)
        print("Tables created")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
