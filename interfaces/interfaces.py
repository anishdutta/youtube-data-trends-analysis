from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class FetchVideosRequest(BaseModel):
    channelId: str

class VideoBase(BaseModel):
    title: str
    youtube_video_id: str
    description: Optional[str] = None
    view_count: Optional[int] = 0
    like_count: Optional[int] = 0
    comment_count: Optional[int] = 0
    published_at: Optional[datetime] = None
    tags: List[str] = []

class VideoCreate(VideoBase):
    pass

class Video(VideoBase):
    id: str

    class Config:
        orm_mode = True

class BulkVideoCreate(BaseModel):
    videos: List[VideoCreate]

class InsightBase(BaseModel):
    video_id :str
    trend : float
    keywords : str
    like_to_view_ratio : float
    comment_to_view_ratio = float

class Insight(InsightBase):
    id: str
    class Config:
        orm_mode = True

class CreateInsight(InsightBase):
    pass


