
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Smartphone Market Analysis",
    page_icon="📱",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent


# ==========================================
# 2. DASHBOARD DESIGN
# ==========================================

st.markdown("""
<style>
.stApp {
    background-color: #080d1a;
    color: #f1f5f9;
}

section[data-testid="stSidebar"] {
    background-color: #111827;
}

.main-title {
    font-size: 38px;
    font-weight: 800;
    color: #f8fafc;
}

.subtitle {
    color: #94a3b8;
    font-size: 17px;
    margin-bottom: 25px;
}

.metric-card {
    background: linear-gradient(145deg, #17243b, #101827);
    padding: 20px;
    border: 1px solid #334155;
    border-radius: 16px;
    text-align: center;
    min-height: 135px;
}

.metric-label {
    color: #cbd5e1;
    font-size: 14px;
    font-weight: 600;
}

.metric-value {
    font-size: clamp(17px, 1.6vw, 24px) !important;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    font-variant-numeric: tabular-nums;
}
}

.section-title {
    color: #f8fafc;
    font-size: 23px;
    font-weight: 700;
    margin-top: 20px;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. LOAD CLEANED DATASET
# ==========================================

dataset_path = (
    BASE_DIR / "data" / "processed"
    / "cleaned_youtube_data.csv"
)

if not dataset_path.exists():
    st.error("Cleaned dataset not found!")
    st.info(
        "Please run notebooks/02_clean_youtube_data.py first."
    )
    st.stop()

try:
    df = pd.read_csv(dataset_path)
except Exception as error:
    st.error(f"Unable to load dataset: {error}")
    st.stop()

if df.empty:
    st.error("The dataset is empty.")
    st.stop()


# ==========================================
# 4. CHECK REQUIRED COLUMNS
# ==========================================

required_columns = [
    "brand",
    "video_id",
    "title",
    "published_at",
    "views",
    "likes",
    "comments",
    "engagement_rate"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    st.error(
        f"Missing columns in dataset: {missing_columns}"
    )
    st.stop()


# ==========================================
# 5. DATA PREPARATION
# ==========================================

df["brand"] = (
    df["brand"]
    .fillna("")
    .astype(str)
    .str.strip()
)

df = df[df["brand"] != ""].copy()

df["published_at"] = pd.to_datetime(
    df["published_at"],
    errors="coerce",
    utc=True
)

df["year"] = df["published_at"].dt.year

numeric_columns = [
    "views",
    "likes",
    "comments",
    "engagement_rate"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    ).fillna(0)

if df.empty:
    st.error("No valid records available.")
    st.stop()


# ==========================================
# 6. DASHBOARD HEADER
# ==========================================

st.markdown(
    '<div class="main-title">'
    '📱 Smartphone Market Analysis Dashboard'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'YouTube Trends, Brand Performance and Audience Engagement'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# ==========================================
# 7. SIDEBAR FILTERS
# ==========================================

st.sidebar.title("🔍 Dashboard Filters")

st.sidebar.markdown("### Select Smartphone Brands")

all_brands = sorted(df["brand"].unique().tolist())

selected_brands = st.sidebar.multiselect(
    "Choose brands",
    options=all_brands,
    default=all_brands
)

filtered_df = df[
    df["brand"].isin(selected_brands)
].copy()

available_years = sorted(
    filtered_df["year"].dropna().astype(int).unique().tolist()
)

if available_years:

    selected_years = st.sidebar.multiselect(
        "Select Years",
        options=available_years,
        default=available_years
    )

    filtered_df = filtered_df[
        filtered_df["year"].isin(selected_years)
    ].copy()

st.sidebar.divider()

st.sidebar.caption(
    f"Dataset: {dataset_path.name}"
)

st.sidebar.caption(
    f"Available brands: {len(all_brands)}"
)

st.sidebar.caption(
    f"Total source records: {len(df)}"
)


# ==========================================
# 8. HANDLE EMPTY FILTER RESULTS
# ==========================================

if filtered_df.empty:
    st.warning(
        "No records found. Please select at least one brand and year."
    )
    st.stop()


# ==========================================
# 9. KPI CALCULATIONS
# ==========================================

total_videos = len(filtered_df)

total_brands = filtered_df["brand"].nunique()

total_views = filtered_df["views"].sum()

total_likes = filtered_df["likes"].sum()

total_comments = filtered_df["comments"].sum()

avg_views = (
    total_views / total_videos
    if total_videos > 0 else 0
)

avg_engagement = filtered_df[
    "engagement_rate"
].mean()


# ==========================================
# 10. MARKET OVERVIEW KPI CARDS
# ==========================================

st.markdown(
    '<div class="section-title">'
    '📊 Market Overview'
    '</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

metrics = [
    (col1, "🎬 TOTAL VIDEOS", f"{total_videos:,}"),
    (col2, "📱 SMARTPHONE BRANDS", f"{total_brands:,}"),
    (col3, "👀 TOTAL VIEWS", f"{total_views:,.0f}"),
    (col4, "❤️ TOTAL LIKES", f"{total_likes:,.0f}")
]

for column, label, value in metrics:
    with column:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

st.write("")

col5, col6, col7, col8 = st.columns(4)

extra_metrics = [
    (col5, "💬 TOTAL COMMENTS", f"{total_comments:,.0f}"),
    (col6, "📊 AVG VIEWS / VIDEO", f"{avg_views:,.0f}"),
    (col7, "📈 AVG ENGAGEMENT", f"{avg_engagement:.2f}%"),
    (col8, "📅 YEARS COVERED", f"{filtered_df['year'].nunique()}")
]

for column, label, value in extra_metrics:
    with column:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

st.divider()


# ==========================================
# 11. VIDEOS BY SMARTPHONE BRAND
# ==========================================

st.markdown(
    '<div class="section-title">'
    '📊 Videos Published by Smartphone Brand'
    '</div>',
    unsafe_allow_html=True
)

brand_count = (
    filtered_df["brand"]
    .value_counts()
    .sort_values(ascending=False)
)

fig, ax = plt.subplots(figsize=(10, 5))

brand_count.plot(
    kind="bar",
    ax=ax,
    color="#3498db"
)

ax.set_xlabel("Smartphone Brand")
ax.set_ylabel("Number of Videos")
ax.set_title("Videos by Smartphone Brand")
ax.tick_params(axis="x", rotation=45)
ax.grid(axis="y", alpha=0.25)

fig.tight_layout()
st.pyplot(fig, use_container_width=True)
plt.close(fig)

st.divider()


# ==========================================

# 12. YEARLY PUBLISHING TREND
# ==========================================

st.markdown(
    '<div class="section-title">'
    '📈 Yearly YouTube Publishing Trend'
    '</div>',
    unsafe_allow_html=True
)

yearly_count = (
    filtered_df.dropna(subset=["year"])
    .groupby("year")
    .size()
    .sort_index()
)

if not yearly_count.empty:

    latest_year = int(yearly_count.index.max())

    if latest_year == pd.Timestamp.now().year:
        st.info(
            f"Note: {latest_year} is an ongoing year. "
            "The video count may be lower than previous full years."
        )

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(
        yearly_count.index,
        yearly_count.values,
        marker="o",
        linewidth=3,
        markersize=9,
        color="#16b9d5"
    )

    ax.set_xlabel("Year")
    ax.set_xticks(yearly_count.index)
    ax.set_ylabel("Number of Videos")
    ax.set_title("Yearly YouTube Publishing Trend")
    ax.grid(True, alpha=0.25)

    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

else:
    st.info("Yearly publishing information unavailable.")

st.divider()



# ==========================================
# 13. BRAND PERFORMANCE COMPARISON
# ==========================================

st.markdown(
    '<div class="section-title">'
    '🏆 Brand Performance Comparison'
    '</div>',
    unsafe_allow_html=True
)

brand_performance = (
    filtered_df.groupby("brand")
    .agg(
        total_views=("views", "sum"),
        total_likes=("likes", "sum"),
        total_comments=("comments", "sum"),
        average_views=("views", "mean"),
        average_engagement=("engagement_rate", "mean"),
        video_count=("video_id", "count")
    )
    .sort_values("total_views", ascending=False)
)

st.markdown("### 👀 Total Views by Brand")

fig, ax = plt.subplots(figsize=(10, 5))

brand_performance["total_views"].plot(
    kind="bar",
    ax=ax,
    color="#8b5cf6"
)

ax.set_xlabel("Smartphone Brand")
ax.set_ylabel("Total Views")
ax.set_title("Total YouTube Views by Brand")
ax.tick_params(axis="x", rotation=45)
ax.grid(axis="y", alpha=0.25)

fig.tight_layout()
st.pyplot(fig, use_container_width=True)
plt.close(fig)


# ==========================================

# ==========================================
# 14. LIKES AND COMMENTS COMPARISON
# ==========================================

st.markdown("### ❤️ Total Likes by Smartphone Brand")

# Likes chart
likes_data = brand_performance["total_likes"].sort_values(
    ascending=False
)

fig1, ax1 = plt.subplots(figsize=(10, 5))

likes_data.plot(
    kind="bar",
    ax=ax1,
    color="royalblue"
)

ax1.set_xlabel("Smartphone Brand")
ax1.set_ylabel("Total Likes")
ax1.set_title("Total YouTube Likes by Smartphone Brand")
ax1.tick_params(axis="x", rotation=45)
ax1.grid(axis="y", alpha=0.25)

fig1.tight_layout()
st.pyplot(fig1, use_container_width=True)
plt.close(fig1)


st.markdown("### 💬 Total Comments by Smartphone Brand")

# Comments chart
comments_data = brand_performance["total_comments"].sort_values(
    ascending=False
)

fig2, ax2 = plt.subplots(figsize=(10, 5))

comments_data.plot(
    kind="bar",
    ax=ax2,
    color="darkorange"
)

ax2.set_xlabel("Smartphone Brand")
ax2.set_ylabel("Total Comments")
ax2.set_title("Total YouTube Comments by Smartphone Brand")
ax2.tick_params(axis="x", rotation=45)
ax2.grid(axis="y", alpha=0.25)

fig2.tight_layout()
st.pyplot(fig2, use_container_width=True)
plt.close(fig2)

# ==========================================
# 15. ENGAGEMENT RATE COMPARISON
# ==========================================

st.markdown("### 📈 Average Engagement Rate by Brand")

engagement_rate = (
    brand_performance["average_engagement"]
    .sort_values(ascending=False)
)

fig, ax = plt.subplots(figsize=(10, 5))

engagement_rate.plot(
    kind="bar",
    ax=ax,
    color="#14b8a6"
)

ax.set_xlabel("Smartphone Brand")
ax.set_ylabel("Average Engagement Rate (%)")
ax.set_title("Average Engagement Rate by Brand")
ax.tick_params(axis="x", rotation=45)
ax.grid(axis="y", alpha=0.25)

fig.tight_layout()
st.pyplot(fig, use_container_width=True)
plt.close(fig)

st.divider()


# ==========================================
# 16. TOP 10 MOST VIEWED VIDEOS
# ==========================================

st.markdown(
    '<div class="section-title">'
    '🔥 Top 10 Most Viewed Smartphone Videos'
    '</div>',
    unsafe_allow_html=True
)

top_videos = (
    filtered_df.sort_values(
        "views",
        ascending=False
    )
    .head(10)
)

top_display = top_videos[
    [
        "brand",
        "title",
        "channel",
        "views",
        "likes",
        "comments"
    ]
].copy()

st.dataframe(
    top_display,
    use_container_width=True,
    hide_index=True
)

st.divider()


# ==========================================
# 17. BRAND PERFORMANCE TABLE
# ==========================================

st.markdown(
    '<div class="section-title">'
    '📋 Brand Performance Summary'
    '</div>',
    unsafe_allow_html=True
)

display_performance = brand_performance.copy()

display_performance.columns = [
    "Total Views",
    "Total Likes",
    "Total Comments",
    "Average Views",
    "Average Engagement Rate (%)",
    "Video Count"
]

st.dataframe(
    display_performance.style.format({
        "Total Views": "{:,.0f}",
        "Total Likes": "{:,.0f}",
        "Total Comments": "{:,.0f}",
        "Average Views": "{:,.0f}",
        "Average Engagement Rate (%)": "{:.2f}%",
        "Video Count": "{:,.0f}"
    }),
    use_container_width=True
)

st.divider()


# ==========================================
# 18. DATASET PREVIEW
# ==========================================

st.markdown(
    '<div class="section-title">'
    '📁 Dataset Preview'
    '</div>',
    unsafe_allow_html=True
)

st.write(f"Showing {len(filtered_df)} records")

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)


# ==========================================
# 19. DOWNLOAD FILTERED DATASET
# ==========================================

st.markdown(
    '<div class="section-title">'
    '⬇️ Download Your Data'
    '</div>',
    unsafe_allow_html=True
)

csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Download Filtered Dataset",
    data=csv_data,
    file_name="smartphone_market_analysis.csv",
    mime="text/csv"
)

st.divider()


# ==========================================
# 20. BUSINESS INSIGHTS
# ==========================================

st.markdown(
    '<div class="section-title">'
    '💡 Business Insights and Recommendations'
    '</div>',
    unsafe_allow_html=True
)

if not brand_performance.empty:

    views_leader = brand_performance[
        "total_views"
    ].idxmax()

    likes_leader = brand_performance[
        "total_likes"
    ].idxmax()

    comments_leader = brand_performance[
        "total_comments"
    ].idxmax()

    engagement_leader = brand_performance[
        "average_engagement"
    ].idxmax()

    st.markdown("### 🏆 Performance Leaders")

    col1, col2 = st.columns(2)

    with col1:
        st.success(
            f"Views Leader: {views_leader} "
            f"({brand_performance.loc[views_leader, 'total_views']:,.0f} views)"
        )

        st.info(
            f"Likes Leader: {likes_leader} "
            f"({brand_performance.loc[likes_leader, 'total_likes']:,.0f} likes)"
        )

    with col2:
        st.info(
            f"Comments Leader: {comments_leader} "
            f"({brand_performance.loc[comments_leader, 'total_comments']:,.0f} comments)"
        )

        st.success(
            f"Engagement Leader: {engagement_leader} "
            f"({brand_performance.loc[engagement_leader, 'average_engagement']:.2f}%)"
        )

    st.markdown("### 🎯 Business Recommendations")

    recommendations = [
        f"Study the YouTube content strategy of {views_leader}, "
        "which leads this dataset in total views.",

        f"Analyse the audience interaction strategy of {engagement_leader}, "
        "which has the highest average engagement rate.",

        "Compare average views per video to understand performance "
        "without relying only on total views.",

        "Monitor competitor publishing activity and audience response "
        "to identify content opportunities."
    ]

    for recommendation in recommendations:
        st.markdown(f"- {recommendation}")

st.caption(
    "Insights describe the selected YouTube video sample, "
    "not total smartphone market share."
)


# ==========================================
# 21. FOOTER
# ==========================================

st.divider()

st.markdown(
    """
    <div style="text-align:center; color:#94a3b8;">
        Smartphone Market Analysis Dashboard<br>
        Data Analytics Project | Built with Python, Pandas,
        Matplotlib and Streamlit
    </div>
    """,
    unsafe_allow_html=True
)

