from videos.videos_service import Video_Service
from sqlalchemy.orm import Session
from analytics.analytics_service import Analytics_Service

class Data_Pipeline_Service:

    channel_id_list = [
        'UCK8sQmJBp8GCxrOtXWBpyEA'
    ]

    def start_pipeline(self,db:Session):
        overall_analytics = {}
        for channel_id in self.channel_id_list:
            videos = Video_Service.fetch_video_details(channel_id=channel_id)
            Analytics_Service.handle_analytics(videos=videos,db=db)
            overall_analytics[channel_id] = videos
        return overall_analytics


