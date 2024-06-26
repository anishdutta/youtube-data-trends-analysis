# YouTube Video Analytics Backend Service
## Overview
This project provides a backend service for a video analytics platform. It integrates with the YouTube Data API to fetch video data, processes the data to extract valuable insights, and stores the results in a MySQL database. The data is updated every hour through a scheduled pipeline.

## Features
### API Integration: 
Fetches detailed video information for specified channels from the YouTube Data API.
### Data Processing: 
Extracts insights such as view count trends, top keywords, and audience engagement metrics.
### Database Management: 
Uses SQLlite to store raw video data and processed insights.
### Data Pipeline: 
Updates data and recalculates insights hourly, handling API rate limits and retrying on failures.
### Insights Extraction: 
Provides additional insights like the most engaging videos and top trending videos.
## Technologies Used
Backend Framework: FastAPI
Programming Language: Python
Database: MySQL
ORM: SQLAlchemy
Task Scheduling: asyncio
Parallel Processing: ProcessPoolExecutor
Natural Language Processing: NLTK
Machine Learning: OpenAI's GPT-3.5
Getting Started
Prerequisites
Python 3.8+
MySQL 5.7+
YouTube Data API Key
Installation
Clone the repository:

```
git clone https://github.com/yourusername/yt-analytics-backend.git
cd yt-analytics-backend
```
Create a virtual environment:

```
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
Install the required packages:

```
pip install -r requirements.txt
```
Set up the MySQL database:

Create two databases: videos for raw data and insights for processed data.
Update config.py with your database credentials.
Set up environment variables:

Create a .env file with the following content:
```
YOUTUBE_API_KEY=your_youtube_api_key
DATABASE_URL=mysql+pymysql://user:password@localhost/videos
```
Run database migrations:

```
alembic upgrade head
```
Running the Service
Start the FastAPI server:

```
uvicorn app.main:app --reload
```

## Scheduled Data Pipeline
The data pipeline runs every hour using asyncio and ProcessPoolExecutor. It fetches video data in batches of 10, processes it in parallel, and stores the results in the MySQL database.
## Batch Processing Explained
### Batch Processing Architecture
Batch processing in this project is designed to efficiently handle large volumes of video data. The approach involves dividing the video data into manageable chunks and processing each chunk in parallel. This ensures that the system can handle high data throughput while maintaining performance.

### Batch Division:

The video data is divided into batches of 10 videos each. This batch size is chosen to balance the workload and ensure efficient use of system resources.
Parallel Processing with ProcessPoolExecutor:

Each batch is processed using a ProcessPoolExecutor, which allows the creation of multiple processes. In this setup, two processes are created at a time.
Each process is responsible for processing a batch of 10 videos. This parallel processing approach helps to utilize multiple CPU cores, speeding up data processing.
Thread Management:

Within each process, three worker threads are created to handle different aspects of data extraction and storage:
Thread 1: Fetches video data from the YouTube API.
Thread 2: Processes the data to extract insights such as trends and keywords.
Thread 3: Stores the processed data in the MySQL database.
###Task Execution:

Tasks are defined to handle specific functions like data fetching, processing, and storage.
Each task is designed to handle retries and error handling to ensure robustness against API rate limits and network issues.
Scalability:

The batch processing system is scalable. The number of batches, processes, and threads can be adjusted based on the system’s capabilities and data volume.
Benefits of Batch Processing
Efficient Resource Utilization: By dividing the workload, the system can make better use of available resources, leading to improved performance.
Reduced Latency: Parallel processing reduces the time taken to process large volumes of data, leading to faster data updates.
Scalability: The system can be scaled horizontally by increasing the number of processes and threads, allowing it to handle larger datasets.
##Project Structure
```
yt-analytics-backend/
│
├── app/
│   ├── main.py             # FastAPI application entry point
│   ├── config.py           # Configuration settings
│   ├── models.py           # SQLAlchemy models
│   ├── crud.py             # Database CRUD operations
│   ├── schemas.py          # Pydantic schemas
│   ├── api/
│   │   └── endpoints.py    # API endpoints
│   ├── utils/
│   │   ├── fetch_data.py   # Functions to fetch data from YouTube API
│   │   ├── process_data.py # Functions to process fetched data
│   │   ├── keywords.py     # Keyword extraction using NLTK
│   │   └── trends.py       # Trend analysis using GPT-3.5
│   └── db/
│       └── session.py      # Database session management
│
├── pipeline/
│   ├── run.py              # Data pipeline entry point
│   ├── tasks.py            # Task definitions
│   └── schedule.py         # Scheduling logic
│
├── migrations/             # Alembic migrations
│
└── README.md               # Project documentation
```

## Insights Calculation
### View Count Trends: Analyzed using predefined benchmarks and GPT-3.5.
### Top Keywords: Extracted from video titles, descriptions, and tags using NLTK.
### Engagement Metrics: Calculated based on likes and comments.
## Contributing
Fork the repository.
Create a new feature branch:
```
git checkout -b feature/new-feature
Commit your changes:
bash
Copy code
git commit -m 'Add new feature'
```
Push to the branch:
```
git push origin feature/new-feature
```
Open a pull request.
## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
YouTube Data API
FastAPI
SQLAlchemy
NLTK
OpenAI GPT-3.5
 
