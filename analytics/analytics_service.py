

from database.crud import create_video, create_video_insight, get_insight_by_youtube_id
from interfaces.interfaces import VideoBase, VideoCreate
from sqlalchemy.orm import Session
import concurrent.futures
import nltk
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import openai
from datetime import datetime

class Analytics_Service:

    nltk.download('punkt')
    nltk.download('stopwords')

    weightage_variables = {
        'likes': 30,
        'views': 35,
        'mostRecent': 10,
        'likesIncreaseRate': 12.5,
        'viewsIncreaseRate': 12.5,
    }


    raw_video_data:VideoCreate = []


    def calculate_trend_point(self,video_data):
        # Construct prompt for batch processing
        prompt = "Calculate trend points for the following YouTube videos:\n\n"
        
        for i, video in enumerate(video_data, start=1):
            prompt += f"Video {i}:\n"
            prompt += f"- Likes: {video['likes']}\n"
            prompt += f"- Views: {video['views']}\n"
            prompt += f"- Upload recency: {video['upload_recency']}\n"
            prompt += f"- Like increase rate: {video['like_increase_rate']}\n"
            prompt += f"- Views increase rate: {video['views_increase_rate']}\n\n"
        
        prompt += "Context:\n"
        prompt += "You are tasked with calculating trend points based on the given parameters and benchmarks.\n"
        prompt += "Provide the trend point as a value between 0 and 1 for each video.\n"
        
        # Call OpenAI API
        response = openai.Completion.create(
            engine="davinci",
            prompt=prompt,
            max_tokens=250,
            n=len(video_data),
            stop=None,
            temperature=0.5,
        )
        
        trend_points = [float(choice.text.strip()) for choice in response.choices]
        return trend_points


    def extract_keywords(self,texts:list[str]):
        keywords = []
        for text in texts:
            stop_words = set(stopwords.words('english'))
            words = word_tokenize(text)
            filtered_words = [w for w in words if w.isalnum() and w.lower() not in stop_words]
            keywords.append(Counter(filtered_words).most_common(10))

    def get_time_difference_in_days(self, date_string):
        date_format = "%Y-%m-%dT%H:%M:%SZ"
        date_time_obj = datetime.strptime(date_string, date_format)
        current_date_time = datetime.utcnow()
        difference = current_date_time - date_time_obj
        difference_in_days = difference.days

        return difference_in_days

    def analyze_engagement(self, likes, comments, views, published):
        return {
            'likes': likes,
            'views': views,
            'upload_recency': self.get_time_difference_in_days(),
            'like_to_view_ratio': likes / views if views else 0,
            'comment_to_view_ratio': comments / views if views else 0
        }
    
    def calculate_insights_data(self,video):
        current_insight = get_insight_by_youtube_id(video_id=video['video_id'])
        return {
            'like_increase_rate': (video['like_to_view_ratio'] - current_insight['like_to_view_ratio'])/100,
            'comment_increase_rate': (video['comment_to_view_ratio'] - current_insight['comment_to_view_ratio'])/100,
            'views_increase_rate': (video['total_viewes'] - current_insight['total_viewes'])/100,
            'upload_recency': self.get_time_difference_in_days(video['published_date']),
            'likes': video['likes'],
            'views': video['views'],
        }

    def create_video(self,videos:list[VideoCreate], insights:list[dict], db:Session):
        for i in range(list(videos)):
            try:
                self.raw_video_data.append(videos[i])
                create_video(db=db,video=videos[i])
                create_video_insight(db=db,insight=insights[i])
            except Exception as e:
                print(f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}")
    
    def process_video(self,videos:list[dict],db:Session):
        insight_data_list = []
        keywords_data = []
        for video in videos:
            insight_data_list.append(self.calculate_insights_data({
                'video_id': video['youtube_video_id'],
                'like_to_view_ratio' :  video['likes'] /  video['viewes'],
                'comment_to_view_ratio': video['comments'] /  video['viewes'],
                'total_viewes': video['viewes']
            }))
            keyword_data = video['title'] + video['desciption'] + ' '.join(video.get('tags',[]))
            keywords_data.append(keyword_data)
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            future1 = executor.submit(self.calculate_trend_point, insight_data_list)
            future2 = executor.submit(self.extract_keywords, keywords_data)
            trends = future1.result()
            keywords = future2.result()
            for i in range(len(insight_data_list)):
                insight_data_list[i]['trend'] = trends[i]
                insight_data_list[i]['keywords'] = keywords[i]
            executor.submit(self.create_video,videos,insight_data_list,db) # non-blocking

    def process_batch(self,batch):
        for video in batch:
            self.process_video(video)

    def handle_analytics(self,videos,db:Session):
        batches = [videos[i:i+10] for i in range(0, len(videos), 10)]

        with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
            executor.map(self.process_batch, batches,db)




