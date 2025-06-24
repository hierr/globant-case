from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase

class Base(DeclarativeBase):
    pass


class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True)
    department = Column(String)

    employees = relationship("HiredEmployee", back_populates="department")


class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True)
    job = Column(String)

    employees = relationship("HiredEmployee", back_populates="job")


class HiredEmployee(Base):
    __tablename__ = "hired_employees"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    datetime = Column(DateTime)

    department_id = Column(Integer, ForeignKey("departments.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))

    department = relationship("Department", back_populates="employees")
    job = relationship("Job", back_populates="employees")
