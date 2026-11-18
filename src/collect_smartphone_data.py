
import pandas as pd
import requests
import os
import time
from dotenv import load_dotenv

# ==========================================
# 1. LOAD API KEY
# ==========================================

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

if not YOUTUBE_API_KEY:
    raise ValueError("YouTube API key not found in .env file")

print("API key available:", bool(YOUTUBE_API_KEY))


# ==========================================
# 2. PROJECT CONFIGURATION
# ==========================================

PROJECT_NAME = "Smartphone Market Analysis"
COUNTRY = "India"

BRANDS = [
    "Apple",
    "Samsung",
    "Xiaomi",
    "OnePlus",
    "Vivo",
    "Oppo",
    "Realme",
    "Motorola"
]

BASE_URL = "https://www.googleapis.com/youtube/v3"

session = requests.Session()


# ==========================================
# 3. API REQUEST WITH RETRIES
# ==========================================

def youtube_request(endpoint, params):

    url = f"{BASE_URL}/{endpoint}"

    for attempt in range(1, 4):

        try:
            response = session.get(
                url,
                params=params,
                timeout=(15, 60)
            )

            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as error:

            print(f"Request attempt {attempt} failed: {error}")

            if attempt < 3:
                time.sleep(5)

    return None


# ==========================================
# 4. COLLECT VIDEOS
# ==========================================

print("\nProject:", PROJECT_NAME)
print("Market:", COUNTRY)

video_data = []

for brand in BRANDS:

    print(f"\nCollecting data for {brand}...")

    params = {
        "part": "snippet",
        "q": f"{brand} smartphone review India",
        "type": "video",
        "maxResults": 10,
        "regionCode": "IN",
        "relevanceLanguage": "en",
        "key": YOUTUBE_API_KEY
    }

    response = youtube_request("search", params)

    if response is None:
        print(f"Skipping {brand} because the request failed.")
        continue

    items = response.get("items", [])

    for item in items:

        video_id = item["id"]["videoId"]

        video_data.append({
            "brand": brand,
            "video_id": video_id,
            "title": item["snippet"]["title"],
            "channel": item["snippet"]["channelTitle"],
            "published_at": item["snippet"]["publishedAt"]
        })

    print(f"{brand}: {len(items)} videos collected")

    time.sleep(1)


# ==========================================
# 5. SAVE VIDEO DETAILS
# ==========================================

if not video_data:
    raise ValueError(
        "No videos collected. Check network, API quota and permissions."
    )

df = pd.DataFrame(video_data)

df.drop_duplicates(
    subset=["brand", "video_id"],
    inplace=True
)

print("\nTotal unique video records:", len(df))


# ==========================================
# 6. COLLECT VIDEO STATISTICS
# ==========================================

print("\nCollecting views, likes and comments...")

video_ids = df["video_id"].tolist()

statistics_data = {}

for i in range(0, len(video_ids), 50):

    batch_ids = video_ids[i:i + 50]

    params = {
        "part": "statistics",
        "id": ",".join(batch_ids),
        "key": YOUTUBE_API_KEY
    }

    response = youtube_request("videos", params)

    if response is None:
        print("Statistics request failed for this batch.")
        continue

    for item in response.get("items", []):

        statistics_data[item["id"]] = item["statistics"]


# ==========================================
# 7. ADD STATISTICS TO DATASET
# ==========================================

df["views"] = df["video_id"].map(
    lambda x: int(
        statistics_data.get(x, {}).get("viewCount", 0)
    )
)

df["likes"] = df["video_id"].map(
    lambda x: int(
        statistics_data.get(x, {}).get("likeCount", 0)
    )
)

df["comments"] = df["video_id"].map(
    lambda x: int(
        statistics_data.get(x, {}).get("commentCount", 0)
    )
)


# ==========================================
# 8. SAVE RAW DATASET
# ==========================================

output_path = "data/raw/youtube_smartphone_data.csv"

os.makedirs("data/raw", exist_ok=True)

df.to_csv(output_path, index=False)


# ==========================================
# 9. DISPLAY RESULTS
# ==========================================

print("\n================================")
print("DATA COLLECTION COMPLETED")
print("================================")

print("Total videos:", len(df))
print("Videos with retrieved statistics:", len(statistics_data))

print("\nDataset columns:")
print(df.columns.tolist())

print("\nDataset preview:")
print(df.head())

print("\nBrand-wise total views:")
print(df.groupby("brand")["views"].sum())

print("\nBrand-wise total likes:")
print(df.groupby("brand")["likes"].sum())

print("\nBrand-wise total comments:")
print(df.groupby("brand")["comments"].sum())

print("\nSaved dataset to:", output_path)
