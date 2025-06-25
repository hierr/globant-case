from fastapi import APIRouter, HTTPException, status
from sqlalchemy import text

from src.api.connector import pool

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/hires_by_quarter_2021")
def get_hires_by_quarter():
    """
    Returns the number of employees hired for each job and department in 2021,
    divided by quarter. The table is ordered alphabetically by department and job.
    """
    sql_query = text("""
        SELECT
            d.department,
            j.job,
            COUNT(CASE WHEN EXTRACT(QUARTER FROM h.datetime) = 1 THEN h.id END) AS "Q1",
            COUNT(CASE WHEN EXTRACT(QUARTER FROM h.datetime) = 2 THEN h.id END) AS "Q2",
            COUNT(CASE WHEN EXTRACT(QUARTER FROM h.datetime) = 3 THEN h.id END) AS "Q3",
            COUNT(CASE WHEN EXTRACT(QUARTER FROM h.datetime) = 4 THEN h.id END) AS "Q4"
        FROM hired_employees h
        JOIN departments d ON h.department_id = d.id
        JOIN jobs j ON h.job_id = j.id
        WHERE EXTRACT(YEAR FROM h.datetime) = 2021
        GROUP BY d.department, j.job
        ORDER BY d.department, j.job
    """)

    try:
        with pool.connect() as conn:
            data = conn.execute(sql_query).mappings().all()
            return data if data else []
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred while querying the database: {e}"
        )


@router.get("/departments_hiring_above_average_2021")
def get_departments_above_average():
    """
    Lists departments that hired more employees than the average for all
    departments in 2021, ordered by the number of hires.
    """
    sql_query = text("""
        WITH department_hires AS (
            SELECT
                d.id,
                d.department,
                COUNT(h.id) AS hired_count
            FROM departments d
            JOIN hired_employees h ON d.id = h.department_id
            WHERE EXTRACT(YEAR FROM h.datetime) = 2021
            GROUP BY d.id, d.department
        ),
        avg_hires AS (SELECT AVG(hired_count) as avg_hired FROM department_hires)
                     
        SELECT
            dh.id,
            dh.department,
            dh.hired_count AS hired
        FROM department_hires dh, avg_hires ah
        WHERE dh.hired_count > ah.avg_hired
        ORDER BY hired DESC
    """)

    try:
        with pool.connect() as conn:
            data = conn.execute(sql_query).mappings().all()
            return data if data else []
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred while querying the database: {e}"
        )