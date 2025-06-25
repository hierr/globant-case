import os
import sys
from pathlib import Path

# src root for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.api.config import settings
from src.api.connector import pool
from src.api.schemas import Base

# set environment variables
os.environ["DB_USER"] = settings.DB_USER
os.environ["DB_PASS_SECRET"] = settings.DB_PASS_SECRET
os.environ["DB_NAME"] = settings.DB_NAME
os.environ["INSTANCE_CONNECTION_NAME"] = settings.INSTANCE_CONNECTION_NAME


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
