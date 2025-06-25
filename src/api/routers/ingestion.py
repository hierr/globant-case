from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException, status
import traceback
from sqlalchemy import insert
from src.api.connector import pool
from src.api import models
from src.api import schemas

router = APIRouter(prefix="/ingest", tags=["Ingestion"])

TABLES = {
    "departments": schemas.Department.__table__,
    "jobs": schemas.Job.__table__,
    "hired_employees": schemas.HiredEmployee.__table__,
}

MODELS = {
    "departments": models.Department,
    "jobs": models.Job,
    "hired_employees": models.HiredEmployee,
}


@router.post("/{table_name}", status_code=status.HTTP_201_CREATED)
def batch_insert(table_name: str, payload: List[Dict[str, Any]]) -> Dict[str, str]:
    """
    Receives a batch of up to 1000 rows and inserts them into the specified table.

    Args:
        table_name: The name of the table to insert the data into.
        payload: A list of dictionaries, where each dictionary represents a row to insert into the table.

    Returns:
        A dictionary with a message indicating the number of rows inserted.
    """
    
    # Validate table name
    if table_name not in TABLES:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Table '{table_name}' not found.")

    # Validate payload size
    if not 1 <= len(payload) <= 1000:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Payload must contain between 1 and 1000 rows.")

    table = TABLES[table_name]
    model = MODELS[table_name]

    # Validate payload records
    validated_rows = [model.model_validate(row) for row in payload]
    rows_to_insert = [row.model_dump() for row in validated_rows]


    # Insert rows
    try:
        with pool.begin() as conn:
            conn.execute(insert(table).values(rows_to_insert))
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred during database insertion: {e}"
        )

    return {"message": f"Successfully inserted {len(rows_to_insert)} records into '{table_name}'."}
