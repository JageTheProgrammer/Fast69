from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from googleapiclient.discovery import build
import os

app = FastAPI()

# Set your YouTube Data API key here
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# Allow all CORS (adjust in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/search")
async def search_youtube(query: str = Query(..., min_length=1)):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

    request = youtube.search().list(
        q=query + " music",
        part="snippet",
        maxResults=10,
        type="video"
    )
    response = request.execute()

    results = []
    for item in response.get("items", []):
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        results.append({
            "title": title,
            "videoId": video_id,
            "embedUrl": f"https://www.youtube.com/embed/{video_id}?autoplay=0"
        })

    return {"results": results}
