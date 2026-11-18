
import pandas as pd
import os

# ==========================================
# 1. LOAD RAW YOUTUBE DATA
# ==========================================

input_path = "data/raw/youtube_smartphone_data.csv"

df = pd.read_csv(input_path)

print("Original dataset shape:", df.shape)


# ==========================================
# 2. CHECK REQUIRED COLUMNS
# ==========================================

required_columns = [
    "brand",
    "video_id",
    "title",
    "channel",
    "published_at",
    "views",
    "likes",
    "comments"
]

missing_columns = [
    col for col in required_columns if col not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )

print("\nAll required columns are available!")


# ==========================================
# 3. CHECK MISSING VALUES
# ==========================================

print("\nMissing values before cleaning:")
print(df.isnull().sum())


# ==========================================
# 4. REMOVE DUPLICATE RECORDS
# ==========================================

df = df.drop_duplicates(
    subset=["brand", "video_id"]
)


# ==========================================
# 5. REMOVE ROWS WITH MISSING INFORMATION
# ==========================================

df = df.dropna(
    subset=[
        "brand",
        "video_id",
        "title",
        "channel"
    ]
)


# ==========================================
# 6. CONVERT DATA TYPES
# ==========================================

# Convert publishing date

df["published_at"] = pd.to_datetime(
    df["published_at"],
    errors="coerce",
    utc=True
)

# Convert numerical statistics

numeric_columns = [
    "views",
    "likes",
    "comments"
]

for column in numeric_columns:

    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )

    df[column] = df[column].fillna(0).astype("int64")


# ==========================================
# 7. REMOVE INVALID DATES
# ==========================================

df = df.dropna(
    subset=["published_at"]
)


# ==========================================
# 8. CREATE ADDITIONAL DATE COLUMNS
# ==========================================

df["year"] = df["published_at"].dt.year

df["month"] = df["published_at"].dt.month

df["month_name"] = df["published_at"].dt.month_name()


# ==========================================
# 9. CREATE ENGAGEMENT METRICS
# ==========================================

df["engagement"] = (
    df["likes"] + df["comments"]
)

df["engagement_rate"] = (
    df["engagement"] / df["views"].replace(0, pd.NA)
) * 100

df["engagement_rate"] = (
    df["engagement_rate"].fillna(0)
)


# ==========================================
# 10. RESET INDEX
# ==========================================

df = df.reset_index(drop=True)


# ==========================================
# 11. SAVE CLEANED DATASET
# ==========================================

output_path = "data/processed/cleaned_youtube_data.csv"

os.makedirs(
    "data/processed",
    exist_ok=True
)

df.to_csv(
    output_path,
    index=False
)


# ==========================================
# 12. DISPLAY CLEANING RESULTS
# ==========================================

print("\n================================")
print("DATA CLEANING COMPLETED!")
print("================================")

print("\nCleaned dataset shape:", df.shape)

print("\nSaved to:", output_path)

print("\nFinal dataset columns:")
print(df.columns.tolist())

print("\nCleaned dataset preview:")
print(df.head())

print("\nBrand-wise total views:")
print(df.groupby("brand")["views"].sum())

print("\nBrand-wise total likes:")
print(df.groupby("brand")["likes"].sum())

print("\nBrand-wise total comments:")
print(df.groupby("brand")["comments"].sum())

print("\nRemaining missing values:")
print(df.isnull().sum())

print("\nAll cleaning tasks completed successfully!")
