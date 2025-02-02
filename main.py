"""
api.py
This module defines a FastAPI-based REST API for managing job records in a database. 
It provides CRUD endpoints for job and worker management.
"""

from fastapi import FastAPI, HTTPException, Depends, status, Query
from pydantic import BaseModel
from typing import Annotated, Optional
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from datetime import date
from sqlalchemy import asc, desc


app = FastAPI()
models.Base.metadata.create_all(bind = engine)


class JobBase(BaseModel):
    name : Optional[str] = None
    customer : Optional[str] = None
    startDate : Optional[date] = None
    endDate : Optional[date] = None
    status : Optional[models.Status] = None

class WorkerBase(BaseModel):
    name : str
    role : str
    jobId : int


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]



"""
Description: Creates Job in Jobs table
Params:
    job - a job object we will add to the jobs row

Returns: created job if successful. We also check if job contains all required fields (name, customer) and return 400 if not
"""
@app.post("/jobs/", status_code=status.HTTP_201_CREATED)
async def create_job(job: JobBase, db: db_dependency):
    db_job = models.Job(**job.dict())
    if not db_job.name:
        raise HTTPException(status_code=400, detail="Name field required")
    if not db_job.customer:
        raise HTTPException(status_code=400, detail="Customer field required")
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


"""
Description: Queries Jobs table with addtional optional parameters
Params:
    name - Filter jobs based on name (optional)
    customer - Fitler jobs based on customer (optional)
    startAfter - Filter jobs starting after this date (optional)
    endBefore - Filter jobs ending before this date (optional)
    status - Filter jobs by status (optional)
    page - Page number for pagination (optional)
    limit - Number of jobs per page (optional)
    sort_by - Field to sort by (optional)
    sort_order - Sort order (optional)
Returns: All jobs matching criteria. We also check if criteria is valid and return 400 if not
"""
@app.get("/jobs/", status_code=status.HTTP_200_OK)
async def query_jobs(
    db: db_dependency, 
    name : str = Query(None, description="Filter jobs starting based on name"),
    customer : str = Query(None, description="Filter jobs starting based on customer"),
    startAfter: date = Query(None, description="Filter jobs starting after this date"),
    endBefore: date = Query(None, description="Filter jobs ending before this date"),
    status: models.Status = Query(None, description="Filter jobs by status"),
    page: int = Query(1, description="Page number for pagination"),
    limit: int = Query(100, description="Number of jobs per page"),
    sort_by: str = Query("startDate", description="Field to sort by ('name', 'customer', 'startDate', 'endDate', 'status')"),
    sort_order: str = Query("asc", description="Sort order ('asc' for ascending, 'desc' for descending)"),
):
    all_jobs = db.query(models.Job)

    if name:
        all_jobs = all_jobs.filter(models.Job.name == name)
    if customer:
        all_jobs = all_jobs.filter(models.Job.customer == customer)

    # Handle date filtering
    if startAfter and endBefore and startAfter >= endBefore:
        raise HTTPException(status_code=400, detail="startAfter must be before endBefore")
    if startAfter:
        all_jobs = all_jobs.filter(models.Job.startDate and models.Job.startDate >= startAfter)
    if endBefore:
        all_jobs = all_jobs.filter(models.Job.endDate and models.Job.endDate <= endBefore)
    if status:
        all_jobs = all_jobs.filter(models.Job.status == status)

    # Handle sorting
    if sort_by not in ["name", "customer", "startDate", "endDate", "status"]:
        raise HTTPException(status_code=400, detail="Invalid sort field")
    if sort_order == "asc":
        order_by = asc(getattr(models.Job, sort_by))
    elif sort_order == "desc":
        order_by = desc(getattr(models.Job, sort_by))
    else:
        raise HTTPException(status_code=400, detail="Invalid sort order. Use 'asc' or 'desc'.")


    skip = (page - 1) * limit
    return all_jobs.order_by(order_by).offset(skip).limit(limit).all()




"""
Description: Deletes Job from job table based on id
Params:
    jobId - jobId to be deleted from 
Returns: Deleted job if successful. We also check if jobId exists and returns 404 if not
"""
@app.delete("/jobs/{jobId}", status_code=status.HTTP_200_OK)
async def query_jobs_by_customer(jobId: int, db: db_dependency):
    job = db.query(models.Job).filter(models.Job.id == jobId).first()
    if job is None:
        raise HTTPException(status_code=404, detail='Job not found')
    db.delete(job)
    db.commit()
    return job


