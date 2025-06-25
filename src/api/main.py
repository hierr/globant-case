from fastapi import FastAPI
from .routers import ingestion, reports

app = FastAPI(
    title="Globant Data Engineering Challenge API",
    description="An API for ingesting and querying historical employee data.",
    version="1.0.0",
)

app.include_router(ingestion.router)
app.include_router(reports.router)


@app.get("/", tags=["Status"])
async def heartbeat():
    return {"status": "ok"}
