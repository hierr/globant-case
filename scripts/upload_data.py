import requests
import pandas as pd
from pathlib import Path
from requests.exceptions import HTTPError
from typing import List

API_BASE_URL = "http://127.0.0.1:8000"
BATCH_SIZE = 1000
TABLES = {
    "departments": ["id", "department"],
    "jobs": ["id", "job"],
    "hired_employees": ["id", "name", "datetime", "department_id", "job_id"],
}


def upload_csv_in_batches(file_path: Path, table_name: str, columns: List[str]):
    print(f"Uploading {file_path.name} to table '{table_name}'...")

    try:
        batch_iter = pd.read_csv(file_path, chunksize=BATCH_SIZE, header=None, names=columns, sep=",")
        
        batch_num = 1
        for batch in batch_iter:
            batch = batch.astype(object).where(pd.notna(batch), None)
            rows = batch.to_dict(orient="records")

            print(f"Uploading batch {batch_num} ({len(rows)} rows)...")
            response = requests.post(f"{API_BASE_URL}/ingest/{table_name}", json=rows)
            response.raise_for_status()

            print(f"Success: {response.json().get('message')}")
            batch_num += 1

    except (FileNotFoundError, HTTPError, Exception) as e:
        raise e


if __name__ == "__main__":
    data_dir = Path("data")

    for table_name, columns in TABLES.items():
        file_path = data_dir / f"{table_name}.csv"
        upload_csv_in_batches(file_path=file_path, table_name=table_name, columns=columns)
