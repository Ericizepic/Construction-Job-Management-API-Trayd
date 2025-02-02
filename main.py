"""
api.py
This module defines a FastAPI-based REST API for managing job records in a database. 
It provides CRUD endpoints for job management.

API Endpoints:
    - POST /jobs/:
        Creates a new job record in the database.
        Request Body: JobBase (name, customer, startDate, endDate, status)
        Response: 201 Created

    - GET /jobs/:
        Retrieves a list of job records (limited to 500 by default).
        Response: 200 OK, List of Jobs

    - GET /jobs/name/{name}:
        Retrieves job records by job name.
        Response: 200 OK, List of Jobs or 404 Not Found

    - GET /jobs/customer/{customer}:
        Retrieves job records by customer name.
        Response: 200 OK, List of Jobs or 404 Not Found

    - DELETE /jobs/{jobId}:
        Deletes a job record by its ID.
        Response: 200 OK if successful, or 404 Not Found
"""

from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from datetime import date


app = FastAPI()
models.Base.metadata.create_all(bind = engine)


class JobBase(BaseModel):
    name : str
    customer : str
    startDate : date
    endDate : date
    status : models.Status


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


# Basic Crud Operations
@app.post("/jobs/", status_code=status.HTTP_201_CREATED)
async def create_job(job: JobBase, db: db_dependency):
    db_job = models.Job(**job.dict())
    db.add(db_job)
    db.commit()

@app.get("/jobs/", status_code=status.HTTP_200_OK)
async def query_jobs(db: db_dependency, lim = 500):
    return db.query(models.Job).limit(lim).all()


@app.get("/jobs/name/{name}", status_code=status.HTTP_200_OK)
async def query_jobs_by_name(name: str, db: db_dependency):
    jobs = db.query(models.Job).filter(models.Job.name == name).all()
    if jobs is None:
        raise HTTPException(status_code=404, detail='Job name not found')
    return jobs

@app.get("/jobs/customer/{customer}", status_code=status.HTTP_200_OK)
async def query_jobs_by_customer(customer: str, db: db_dependency):
    jobs = db.query(models.Job).filter(models.Job.customer == customer).all()
    if jobs is None:
        raise HTTPException(status_code=404, detail='Customer not found')
    return jobs


@app.delete("/jobs/{jobId}", status_code=status.HTTP_200_OK)
async def query_jobs_by_customer(jobId: int, db: db_dependency):
    job = db.query(models.Job).filter(models.Job.id == jobId).first()
    if job is None:
        raise HTTPException(status_code=404, detail='Job not found')
    db.delete(job)
    db.commit()
