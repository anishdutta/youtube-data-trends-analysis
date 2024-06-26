import os
from googleapiclient.discovery import build
from interfaces.interfaces import VideoCreate
from googleapiclient.errors import HttpError
import time

class Video_Service:

    API_KEY = os.getenv('YOUTUBE_API_KEY')

    def get_youtube_service(self):
        return build('youtube', 'v3', developerKey=API_KEY)

    def fetch_playlist_items(self,youtube, playlist_id):
        results = []
        next_page_token = None
        retry_count = 0 
        max_retry_count = 100
        while True and retry_count<max_retry_count:
            try:
                request = youtube.playlistItems().list(
                    part='snippet,contentDetails',
                    playlistId=playlist_id,
                    maxResults=50,
                    pageToken=next_page_token
                )
                response = request.execute()

                results.extend(response.get('items', []))
                next_page_token = response.get('nextPageToken')
                break #Testing
                if not next_page_token:
                    break
            except HttpError as e:
                if e.resp.status in [403, 500, 503]:
                    print(f"Error occurred: {e.resp.status}. Retrying after a pause...")
                    time.sleep(5)  # Wait before retrying
                    retry_count+=1
                else:
                    print(f"An HTTP error {e.resp.status} occurred:\n{e.content}")
                    break
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                break

        return results
    
    def fetch_single_video_details(self,youtube,video_id):
        retry_count = 0 
        max_retry_count = 10
        while True and retry_count < max_retry_count:
            try:
                request = youtube.videos().list(
                    part='snippet,statistics',
                    id=video_id
                )
                response = request.execute()
                return response
            except HttpError as e:
                if e.resp.status in [403, 500, 503]:
                    print(f"Error occurred: {e.resp.status}. Retrying after a pause...")
                    time.sleep(5)  # Wait before retrying
                    retry_count+=1
                else:
                    print(f"An HTTP error {e.resp.status} occurred:\n{e.content}")
                    break
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                break

        return {}



    def fetch_video_details(self,channel_id)->list[VideoCreate]:
        youtube = self.get_youtube_service()
        request = youtube.channels().list(
            part='contentDetails',
            id=channel_id
        )
        response = request.execute()
        print(response)
        uploads_playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        
        response = self.fetch_playlist_items(youtube,uploads_playlist_id)
        print(response)
        video_ids = [item['contentDetails']['videoId'] for item in response]
        video_create_requests = []
        print(video_ids)
        for video_id in video_ids:
            request = self.fetch_single_video_details(youtube=youtube,video_id=video_id)
            response = request.execute()
            snippet = response['items'][0]['snippet']
            statistics = response['items'][0]['statistics']
            video = VideoCreate(
                    title=snippet.get('title', 'Untitled'),  
                    description=snippet.get('description', ''),  
                    view_count=statistics.get('viewCount', 0), 
                    like_count=statistics.get('likeCount', 0),  
                    comment_count=statistics.get('commentCount', 0),  
                    published_at=snippet.get('publishedAt'),  
                    youtube_video_id=response['items'][0]['id'],  
                    tags=snippet.get('tags', []) 
            )
            video_create_requests.append(video)
        return video_create_requests
