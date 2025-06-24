from pydantic import BaseModel, ConfigDict
from datetime import datetime

class Department(BaseModel):
    id: int
    department: str

    model_config = ConfigDict(from_attributes=True)


class Job(BaseModel):
    id: int
    job: str

    model_config = ConfigDict(from_attributes=True)


class HiredEmployee(BaseModel):
    id: int
    name: str
    datetime: datetime
    department_id: int
    job_id: int

    model_config = ConfigDict(from_attributes=True)
