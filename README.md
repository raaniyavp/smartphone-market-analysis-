
# 📱 Smartphone Market Analysis

An end-to-end Data Analytics project that analyzes YouTube video performance and audience engagement across eight smartphone brands in India.

## 📌 Project Overview

This project explores how different smartphone brands perform on YouTube by analyzing video views, likes, comments, publishing trends, and audience engagement.

The project uses the YouTube Data API to collect data and Python to clean, analyze, and visualize the information. An interactive Streamlit dashboard presents the findings and business insights.

## 🎯 Objectives

- Analyze YouTube content performance across smartphone brands.
- Compare views, likes, and comments.
- Identify brands with higher audience engagement.
- Examine yearly video publishing trends.
- Identify the most-viewed smartphone videos.
- Present findings through an interactive dashboard.

## 🏷️ Brands Analyzed

1. Apple
2. Samsung
3. Xiaomi
4. OnePlus
5. Vivo
6. Oppo
7. Realme
8. Motorola

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Data processing and analysis |
| Pandas | Data cleaning and manipulation |
| NumPy | Numerical operations |
| Matplotlib | Data visualization |
| YouTube Data API | Data collection |
| Streamlit | Interactive dashboard |
| VS Code | Development environment |

## 📂 Project Structure

```text
smartphone-market-analysis/
│
├── app.py
├── README.md
├── requirements.txt
│
├── src/
│   └── collect_smartphone_data.py
│
├── notebooks/
│   ├── 02_clean_youtube_data.py
│   └── 03_exploratory_data_analysis.py
│
├── data/
│   ├── raw/
│   │   └── youtube_smartphone_data.csv
│   │
│   └── processed/
│       └── cleaned_youtube_data.csv
│
└── reports/
    └── figures/
```

## ⚙️ Project Workflow

### 1. Data Collection

- Integrated the YouTube Data API.
- Collected video information for eight smartphone brands.
- Retrieved video titles, channels, publishing dates, and video IDs.
- Collected views, likes, and comments.

### 2. Data Cleaning

- Removed duplicate records.
- Handled missing values.
- Converted publishing dates into datetime format.
- Converted engagement statistics into numerical values.
- Created additional date and engagement columns.

### 3. Exploratory Data Analysis

Performed analysis on:

- Number of videos by brand.
- Yearly publishing trends.
- Total views by brand.
- Total likes by brand.
- Total comments by brand.
- Average engagement rate.
- Top 10 most-viewed videos.

### 4. Dashboard Development

Developed an interactive Streamlit dashboard featuring:

- KPI cards.
- Brand and year filters.
- Video publishing trends.
- Brand performance comparisons.
- Audience engagement analysis.
- Top 10 videos.
- Business insights.
- CSV download functionality.

## 📊 Key Findings

Based on the collected sample of 80 YouTube videos:

- Samsung recorded the highest total views.
- Realme recorded the highest total likes.
- Realme recorded the highest total comments.
- Oppo recorded the highest average engagement rate.

These findings describe the collected YouTube video sample, not the overall Indian smartphone market share.

## 🚀 How to Run the Project

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Navigate to the project folder

```bash
cd smartphone-market-analysis
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the environment

Mac/Linux:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure the YouTube API key

Create a `.env` file in the project root:

```text
YOUTUBE_API_KEY=your_api_key_here
```

Do not upload your actual API key to GitHub.

### 7. Run the dashboard

```bash
streamlit run app.py
```

## 📈 Dashboard

The dashboard provides an interactive overview of YouTube content performance across the selected smartphone brands.

## ⚠️ Limitations

- The analysis uses a sample of 80 collected videos.
- The sample contains 10 videos per brand at collection time.
- YouTube engagement does not represent actual product sales or market share.
- Results depend on the search terms and videos returned by the YouTube API.
- Video statistics can change over time.

## 👩‍💻 Author

Developed as a Data Analytics portfolio project using Python, YouTube Data API, and Streamlit.
