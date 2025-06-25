from pydantic import BaseModel, ConfigDict
from datetime import datetime

class Department(BaseModel):
    id: int
    department: str | None

    model_config = ConfigDict(from_attributes=True)


class Job(BaseModel):
    id: int
    job: str | None

    model_config = ConfigDict(from_attributes=True)


class HiredEmployee(BaseModel):
    id: int
    name: str | None
    datetime: datetime | None
    department_id: int | None   
    job_id: int | None

    model_config = ConfigDict(from_attributes=True)
