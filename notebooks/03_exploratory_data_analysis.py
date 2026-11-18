
# ==========================================
# SMARTPHONE MARKET ANALYSIS - EDA
# ==========================================

import pandas as pd
import matplotlib.pyplot as plt
import os

# ==========================================
# 1. LOAD CLEANED DATASET
# ==========================================

df = pd.read_csv(
    "data/processed/cleaned_youtube_data.csv"
)

print("=" * 60)
print("SMARTPHONE MARKET ANALYSIS - EDA")
print("=" * 60)


# ==========================================
# 2. DATASET OVERVIEW
# ==========================================

print("\nDATASET INFORMATION")
print("-" * 40)

print("Total videos:", len(df))
print("Total brands:", df["brand"].nunique())

print("\nDataset columns:")
print(df.columns.tolist())

print("\nDataset information:")
df.info()

print("\nFirst five records:")
print(df.head())


# ==========================================
# 3. DATA PREPARATION
# ==========================================

df["published_at"] = pd.to_datetime(
    df["published_at"],
    errors="coerce",
    utc=True
)

numeric_columns = [
    "views",
    "likes",
    "comments",
    "engagement_rate"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    ).fillna(0)

# Create output folder

os.makedirs("reports/figures", exist_ok=True)


# ==========================================
# GRAPH 1: VIDEOS BY SMARTPHONE BRAND
# ==========================================

brand_videos = (
    df.groupby("brand")
    .size()
    .sort_values(ascending=False)
)

print("\nVIDEOS COLLECTED BY BRAND")
print("-" * 40)
print(brand_videos)

plt.figure(figsize=(10, 6))

brand_videos.plot(
    kind="bar",
    title="Number of YouTube Videos by Smartphone Brand"
)

plt.xlabel("Smartphone Brand")
plt.ylabel("Number of Videos")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    "reports/figures/brand_video_count.png",
    dpi=300
)

plt.show()
plt.close()


# ==========================================
# GRAPH 2: YEARLY VIDEO PUBLISHING TREND
# ==========================================

df["year"] = df["published_at"].dt.year

yearly_videos = (
    df["year"]
    .dropna()
    .astype(int)
    .value_counts()
    .sort_index()
)

print("\nVIDEOS PUBLISHED BY YEAR")
print("-" * 40)
print(yearly_videos)

plt.figure(figsize=(10, 6))

yearly_videos.plot(
    kind="bar",
    title="YouTube Videos Published by Year"
)

plt.xlabel("Year")
plt.ylabel("Number of Videos")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig(
    "reports/figures/yearly_video_trend.png",
    dpi=300
)

plt.show()
plt.close()


# ==========================================
# GRAPH 3: TOTAL VIEWS BY BRAND
# ==========================================

brand_views = (
    df.groupby("brand")["views"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTOTAL VIEWS BY BRAND")
print("-" * 40)
print(brand_views)

plt.figure(figsize=(10, 6))

brand_views.plot(
    kind="bar",
    title="Total YouTube Views by Smartphone Brand"
)

plt.xlabel("Smartphone Brand")
plt.ylabel("Total Views")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    "reports/figures/brand_total_views.png",
    dpi=300
)

plt.show()
plt.close()


# ==========================================
# GRAPH 4: TOTAL LIKES BY BRAND
# ==========================================

brand_likes = (
    df.groupby("brand")["likes"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTOTAL LIKES BY BRAND")
print("-" * 40)
print(brand_likes)

plt.figure(figsize=(10, 6))

brand_likes.plot(
    kind="bar",
    title="Total YouTube Likes by Smartphone Brand"
)

plt.xlabel("Smartphone Brand")
plt.ylabel("Total Likes")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    "reports/figures/brand_total_likes.png",
    dpi=300
)

plt.show()
plt.close()


# ==========================================
# GRAPH 5: TOTAL COMMENTS BY BRAND
# ==========================================

brand_comments = (
    df.groupby("brand")["comments"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTOTAL COMMENTS BY BRAND")
print("-" * 40)
print(brand_comments)

plt.figure(figsize=(10, 6))

brand_comments.plot(
    kind="bar",
    title="Total YouTube Comments by Smartphone Brand"
)

plt.xlabel("Smartphone Brand")
plt.ylabel("Total Comments")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    "reports/figures/brand_total_comments.png",
    dpi=300
)

plt.show()
plt.close()


# ==========================================
# GRAPH 6: AVERAGE ENGAGEMENT RATE
# ==========================================

brand_engagement = (
    df.groupby("brand")["engagement_rate"]
    .mean()
    .sort_values(ascending=False)
)

print("\nAVERAGE ENGAGEMENT RATE BY BRAND")
print("-" * 40)
print(brand_engagement.round(2))

plt.figure(figsize=(10, 6))

brand_engagement.plot(
    kind="bar",
    title="Average YouTube Engagement Rate by Brand"
)

plt.xlabel("Smartphone Brand")
plt.ylabel("Average Engagement Rate (%)")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    "reports/figures/brand_engagement_rate.png",
    dpi=300
)

plt.show()
plt.close()


# ==========================================
# GRAPH 7: TOP 10 MOST VIEWED VIDEOS
# ==========================================

top_videos = (
    df.sort_values(
        by="views",
        ascending=False
    )
    .head(10)
)

print("\nTOP 10 MOST VIEWED VIDEOS")
print("-" * 40)

print(
    top_videos[
        ["brand", "title", "views", "likes", "comments"]
    ].to_string(index=False)
)

plt.figure(figsize=(12, 7))

plt.barh(
    top_videos["title"].str.slice(0, 40),
    top_videos["views"]
)

plt.title("Top 10 Most Viewed Smartphone Videos")
plt.xlabel("Total Views")
plt.ylabel("Video Title")
plt.gca().invert_yaxis()

plt.tight_layout()

plt.savefig(
    "reports/figures/top_10_videos.png",
    dpi=300
)

plt.show()
plt.close()


# ==========================================
# 8. BUSINESS INSIGHTS
# ==========================================

print("\n" + "=" * 60)
print("BUSINESS INSIGHTS")
print("=" * 60)

highest_views_brand = brand_views.idxmax()
highest_likes_brand = brand_likes.idxmax()
highest_comments_brand = brand_comments.idxmax()
highest_engagement_brand = brand_engagement.idxmax()

print(
    "\nBrand with highest total views:",
    highest_views_brand
)

print(
    "Brand with highest total likes:",
    highest_likes_brand
)

print(
    "Brand with highest total comments:",
    highest_comments_brand
)

print(
    "Brand with highest average engagement rate:",
    highest_engagement_brand
)

print(
    "\nHighest total views:",
    f"{brand_views.max():,}"
)

print(
    "Highest average engagement rate:",
    f"{brand_engagement.max():.2f}%"
)


# ==========================================
# 9. FINAL SUMMARY
# ==========================================

print("\n" + "=" * 60)
print("EXPLORATORY DATA ANALYSIS COMPLETED!")
print("=" * 60)

print("Total videos analysed:", len(df))
print("Total smartphone brands:", df["brand"].nunique())

print("\nGraphs saved in reports/figures/:")

figures = [
    "brand_video_count.png",
    "yearly_video_trend.png",
    "brand_total_views.png",
    "brand_total_likes.png",
    "brand_total_comments.png",
    "brand_engagement_rate.png",
    "top_10_videos.png"
]

for figure in figures:
    print("-", figure)

print("\nEDA PROCESS FINISHED SUCCESSFULLY!")
