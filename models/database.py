# models.py
from sqlalchemy import Column, Float, Integer, String, Text, DateTime, JSON
from database.db import Base


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    youtube_video_id = Column(String(255), nullable=False, unique=True)
    description = Column(Text)
    view_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    published_at = Column(DateTime)
    tags = Column(JSON, default=[])

class Insight(Base):
    __tablename__ = 'insights'
    id = Column(Integer, primary_key=True, autoincrement=True)
    video_id = Column(String)
    trend = Column(Float)
    keywords = Column(Text)
    like_to_view_ratio = Column(Float)
    comment_to_view_ratio = Column(Float)
    total_viewes = Column(Float)
