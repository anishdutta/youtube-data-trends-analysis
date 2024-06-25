from sqlalchemy import select
from models.database import Insight, Video
from interfaces.interfaces import CreateInsight, VideoCreate, BulkVideoCreate
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


def get_video(db: Session, video_id: str):
    return db.query(Video).filter(Video.id == video_id).first()

def create_video(db: Session, video: VideoCreate):
    try:
        db_video = Video(**video.dict())
        db.add(db_video)
        db.commit()
        db.refresh(db_video)
        return db_video
    except IntegrityError as e:
        db.rollback()
        if "UNIQUE constraint failed: videos.youtube_video_id" in str(e.orig):
            existing_video = db.query(Video).filter_by(youtube_video_id=video.youtube_video_id).first()
            if existing_video:
                for key, value in video.dict().items():
                    setattr(existing_video, key, value)
                db.commit()
                db.refresh(existing_video)
                return existing_video       
        print(f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}")
    except Exception as e:
        db.rollback()
        print(f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}")

def get_video_by_youtube_id(db:Session, video_id: str):
    query = select(Video).where('youtube_video_id' == video_id)
    result = db.execute(query).scalars().one()
    return result


# For postgres we can use on_conflict_do_update 
def create_videos_bulk(db: Session, videos: BulkVideoCreate):
    db_videos = [VideoCreate(**video.dict()) for video in videos.videos]
    db.on
    db.add_all(db_videos)
    db.commit()
    for db_video in db_videos:
        db.refresh(db_video)
    return db_videos

def get_insight_by_youtube_id(db:Session, video_id: str):
    query = select(Insight).where('video_id' == video_id)
    result = db.execute(query).scalars().one()
    return result

def create_video_insight(db: Session, insight: CreateInsight):
    try:
        db_video = Insight(**insight.dict())
        db.add(db_video)
        db.commit()
        db.refresh(db_video)
        return db_video
    except Exception as e:
        db.rollback()
        print(f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}")


