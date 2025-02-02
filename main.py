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
async def query_jobs(db: db_dependency):
    all_jobs = db.query(models.Job)
    if all_jobs is None:
        raise HTTPException(status_code=404, detail='Jobs not found')
    return all_jobs

@app.get("/jobs/{name}", status_code=status.HTTP_200_OK)
async def query_jobs_by_name(name: str, db: db_dependency):
    jobs = db.query(models.Job).filter(models.Job.name == name)
    if jobs is None:
        raise HTTPException(status_code=404, detail='Job name not found')
    return jobs

@app.get("/jobs/{customer}", status_code=status.HTTP_200_OK)
async def query_jobs_by_customer(customer: str, db: db_dependency):
    jobs = db.query(models.Job).filter(models.Job.customer == customer)
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
