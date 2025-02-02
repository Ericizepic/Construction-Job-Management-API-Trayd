"""
api.py
This module defines a FastAPI-based REST API for managing job records in a database. 
It provides CRUD endpoints for job and worker management.
"""

from fastapi import FastAPI, HTTPException, Depends, status, Query
from pydantic import BaseModel
from typing import Annotated, Optional, List
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
    name : Optional[str] = None
    role : Optional[str] = None
    jobId : Optional[int] = None

class WorkerAssignment(BaseModel):
    workerIds: List[int]


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
    job - a job object we will add to the jobs table

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
Description: Bulk creates Job in Jobs table
Params:
    jobs - a list of job objects we will add to the jobs table

Returns: a success message if successful. We also check if job contains all required fields (name, customer) and return 400 if not
"""
@app.post("/jobs/bulk/", status_code=status.HTTP_201_CREATED)
async def create_jobs_bulk(jobs: List[JobBase], db: db_dependency):
    db_jobs = []
    
    for job in jobs:
        db_job = models.Job(**job.dict())
        if not db_job.name:
            raise HTTPException(status_code=400, detail="Name field required for all jobs")
        if not db_job.customer:
            raise HTTPException(status_code=400, detail="Customer field required for all jobs")
        db_jobs.append(db_job)

    db.add_all(db_jobs)
    db.commit()
    return {"message": f"{len(db_jobs)} jobs created successfully"}



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



"""
Description: Creates Worker in Workers table. Note we let the jobid be optional as those can change
Params:
    worker - a worker object we will add to the workers table

Returns: created worker if successful. We also check if worker contains all required fields (name) and return 400 if not
"""
@app.post("/workers/", status_code=status.HTTP_201_CREATED)
async def create_worker(worker: WorkerBase, db: db_dependency):
    db_worker = models.Worker(**worker.dict())
    if db_worker.jobId and db.query(models.Job).filter(models.Job.id == db_worker.jobId).first() is None:
        raise HTTPException(status_code=400, detail="Job not found")
    if not db_worker.name:
        raise HTTPException(status_code=400, detail="Name field required")
    if not db_worker.role:
        raise HTTPException(status_code=400, detail="Role field required")
    db.add(db_worker)
    db.commit()
    db.refresh(db_worker)
    return db_worker




"""
Description: Bulk creates Workers in Workers table. Note we let the jobid be optional as those can change
Params:
    workers - a list of worker objects we will add to the workers table

Returns: a success message if successful. We also check if job contains all required fields (name) and return 400 if not
"""
@app.post("/workers/bulk/", status_code=status.HTTP_201_CREATED)
async def create_workers_bulk(workers: List[WorkerBase], db: db_dependency):
    db_workers = []
    
    for worker in workers:
        db_worker = models.Worker(**worker.dict())
        if db_worker.jobId and db.query(models.Job).filter(models.Job.id == db_worker.jobId).first() is None:
            raise HTTPException(status_code=400, detail="Job not found")
        if not db_worker.name:
            raise HTTPException(status_code=400, detail="Name field required")
        if not db_worker.role:
            raise HTTPException(status_code=400, detail="Role field required")
        db_workers.append(db_worker)

    db.add_all(db_workers)
    db.commit()
    return {"message": f"{len(db_workers)} workers created successfully"}




"""
Description: Assigns workers to jobId in Workers table
Params:
    jobId - id of job workers will be assigned to
    workerIds - a list of worker id we will try assigning to jobId

Returns: a success message if successful. We also check if job contains all required fields (name, customer) and return 400 if not
"""
# @app.put("/workers/assign/{jobId}", status_code=status.HTTP_200_OK)
# async def assign_workers(jobId : int, workerIds: List[int], db: db_dependency):   
#     if jobId is None:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="jobId is required")
#     if db.query(models.Job).filter(models.Job.id == jobId).first() is None:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="no job with jobId was found")

#     db_workers = db.query(models.Worker).filter(models.Worker.id.in_(workerIds)).all()
#     for worker in db_workers:
#         worker.jobId = jobId

#     db.commit()
#     return {"message": f"The following worker ids were assigned to job {jobId}: {str([worker.id for worker in db_workers])}"}




"""
Description: Queries Workers table with addtional optional parameters
Params:
    name - Filter workers based on name (optional)
    role - Filter workers based on role (optional)
    jobId - Filter workers based on Job (optional)
    page - Page number for pagination (optional)
    limit - Number of workers per page (optional)
Returns: All workers matching criteria. We also check if criteria is valid and return 400 if not
"""
@app.get("/jobs/", status_code=status.HTTP_200_OK)
async def query_jobs(
    db: db_dependency, 
    name : str = Query(None, description="Filter workers starting based on name"),
    role : str = Query(None, description="Filter workers starting based on role"),
    jobId : int = Query(None, description="Filter workers starting based on Job"),
    page: int = Query(1, description="Page number for pagination"),
    limit: int = Query(100, description="Number of workers per page"),
):
    all_workers = db.query(models.Worker)

    if name:
        all_jobs = all_workers.filter(models.Worker.name == name)
    if role:
        all_jobs = all_workers.filter(models.Worker.role == role)
    if jobId:
        job = db.query(models.Job).filter(models.Job.id == jobId).first()
        if job is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="no job with jobId was found")
        all_jobs = all_workers.filter(models.Worker.jobId == jobId)

    skip = (page - 1) * limit
    return all_jobs.offset(skip).limit(limit).all()

