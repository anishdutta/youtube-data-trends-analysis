import ssl
from fastapi import FastAPI, Depends
from dotenv import load_dotenv
from videos.videos_service import Video_Service
from interfaces.interfaces import FetchVideosRequest
from sqlalchemy.orm import Session
from database.db import get_db
from data_pipeline.data_pipeline import Data_Pipeline_Service
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.memory import MemoryJobStore
import os
# Load environment variables from .env file
load_dotenv()

# Disable SSL verification
ssl._create_default_https_context = ssl._create_unverified_context

app = FastAPI()

jobstores = {
    'default': MemoryJobStore()
}
scheduler = AsyncIOScheduler(jobstores=jobstores, timezone='Asia/Kolkata') 

# This is a scheduled job that will run every 1 hour.
@scheduler.scheduled_job('interval', seconds=3600)
def scheduled_job(db: Session = Depends(get_db)):
    response = Data_Pipeline_Service.start_pipeline(db=db)
    print("scheduled_job",response)

@app.on_event("startup")
async def startup_event():
    scheduler.start()

@app.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown()

@app.get("/")
async def root():
    return {
        "success": True
    }



@app.post("/start_pipeline")
async def search(request:FetchVideosRequest,db: Session = Depends(get_db)):
    print("here",request)
    response = Data_Pipeline_Service.start_pipeline(db=db)
    return response
