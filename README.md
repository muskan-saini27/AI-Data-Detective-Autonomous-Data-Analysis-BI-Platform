# 🔎 AI Data Detective — Autonomous Data Analysis & BI Platform

A Flask-based, dataset-adaptive data analysis and business intelligence platform that transforms CSV and Excel datasets into automated profiling, data-quality reports, exploratory analysis, visualizations, anomaly detection, trend analysis, potential drivers, business recommendations, natural-language data questions, and downloadable reports.

---

## 🚀 Overview

**AI Data Detective** is an end-to-end analytics platform built with Python, Flask, Pandas, NumPy, JavaScript, HTML, CSS, and Chart.js.

The system is designed to work with different types of structured datasets rather than being limited to a single business domain.

Users can upload a CSV or Excel dataset, after which the platform automatically detects the dataset schema and generates relevant analysis based on the available columns.

The application has been tested with different dataset types, including:

- Student datasets
- IPL / sports datasets
- McDonald's datasets
- Sales datasets
- AI usage datasets

The goal is to reduce repetitive manual analysis and provide a structured workflow from raw data to actionable insights.

---

## ✨ Features

### 📂 Dataset Upload

- Upload CSV datasets
- Upload XLS datasets
- Upload XLSX datasets
- Drag-and-drop dataset upload
- Automatic dataset profiling
- Dataset preview
- Row and column analysis

### 🧠 Automatic Schema Detection

The platform automatically identifies different column roles, including:

- Numeric metrics
- Categorical dimensions
- Date/time columns
- Identifier columns
- Text columns
- Boolean columns
- Low-information / constant columns

The detected schema is then used to determine which analyses, charts, questions, and recommendations are appropriate for the uploaded dataset.

### 🧹 Data Quality Analysis

- Missing-value detection
- Duplicate-row detection
- Data quality scoring
- Numeric validation
- Statistical irregularity detection
- Data-quality findings

### 📊 Exploratory Data Analysis

- Numeric statistics
- Mean
- Median
- Minimum
- Maximum
- Standard deviation
- Missing values
- Categorical frequency analysis
- Unique-value analysis
- Correlation analysis
- Automated analytical findings

### 📈 Trend Intelligence

Where suitable columns are available, the platform can perform:

- Automatic trend detection
- Increasing / decreasing / weak trend identification
- Percentage-change analysis
- Trend-strength analysis
- Date/time-oriented analysis
- Early-to-late observation comparison

Identifier-like columns are excluded from business trend analysis when detected.

### 🚨 Anomaly Detection

The platform identifies unusual numeric observations using statistical techniques such as:

- IQR-based detection
- Z-score-based detection
- Outlier counting
- Anomaly hotspots
- Sample anomalous records

### 🔍 Potential Driver Analysis

The platform compares categorical segments against overall numeric metrics to identify potentially important statistical associations.

Examples include:

- Category-level differences
- Region-level differences
- Department-level differences
- City-level differences
- Team-level differences
- Segment-level metric comparisons

> **Important:** These are statistical associations and potential drivers. They do not prove causation.

### 💬 Ask Your Data

Users can ask questions about the uploaded dataset using natural-language-style questions.

Examples:

```text
How many rows are there?
How many columns are there?
How many missing values are there?
What is the average Revenue?
What is the highest Revenue?
What is the total Revenue?
What is the median Revenue?
What is the most common Category?
What is the strongest correlation?
The question suggestions are generated from the currently detected dataset schema.

When a new dataset is analyzed, the previous Q&A context is cleared and new dataset-specific questions are generated.

The Q&A engine operates locally using deterministic analysis logic and does not require an external LLM API key.

📊 Visual Investigation

The dashboard automatically creates visualizations based on the detected dataset structure.

Depending on the available columns, the system can generate:

Metric trends over time
Metric trends by row sequence
Top categorical-value charts
Average metric by category/dimension
Dataset-specific visualizations

Charts are responsive and can be downloaded as PNG files.

Wide datasets and long column names are handled through responsive chart and table layouts.

💡 Business Recommendations

The platform generates evidence-based recommendations using detected analytical signals such as:

Data-quality issues
Anomalies
Trends
Potential drivers
Strong numeric relationships
Important segment differences

Recommendations are adapted to the current dataset rather than being hard-coded to a single business domain.

📥 Report Export

The platform supports:

PDF executive reports
Excel analytical reports
PNG chart downloads

PDF reports can include:

Dataset overview
Key metrics
Data-quality information
Business recommendations
Anomalies
Trend insights
Potential drivers

Excel reports can include multiple analytical sheets such as:

Executive Summary
Cleaned Data
Numeric Summary
Categorical Summary
Anomalies
📌 Data Analysis Workflow
Upload Dataset
      ↓
Automatic Schema Detection
      ↓
Data Profiling
      ↓
Data Quality Analysis
      ↓
Exploratory Data Analysis
      ↓
Automatic Visualizations
      ↓
Trend Detection
      ↓
Anomaly Detection
      ↓
Correlation Analysis
      ↓
Potential Driver / Segment Analysis
      ↓
Business Recommendations
      ↓
Ask Your Data
      ↓
Export PDF / Excel / PNG
📊 Key Analytics

The platform can automatically analyze available dataset characteristics such as:

Total Rows
Total Columns
Missing Values
Duplicate Records
Data Quality Score
Numeric Statistics
Categorical Frequencies
Unique Values
Correlations
Outliers
Anomalies
Trends
Segment-Level Differences
Potential Drivers
Automated Findings
Business Recommendations

The exact dashboard metrics depend on the schema detected in the uploaded dataset.

🧠 Intelligence Modules
Data Quality Engine

Evaluates the quality of an uploaded dataset using indicators such as missing values, duplicates, and statistical irregularities.

EDA Engine

Automatically analyzes numeric and categorical variables and produces descriptive statistics and analytical findings.

Schema Detection Engine

Classifies dataset columns into useful analytical roles such as metrics, dimensions, dates, identifiers, text, and booleans.

Anomaly Engine

Uses statistical techniques such as IQR and Z-score analysis to identify unusual observations.

Trend Engine

Analyzes appropriate numeric columns over time or observation sequence and identifies increasing, decreasing, or weak trends.

Potential Driver Engine

Compares categorical segments against overall numeric metrics to identify potentially significant statistical differences.

Potential drivers represent association-based evidence and should not be interpreted as proof of causation.

Q&A Engine

Maps supported natural-language-style questions to dataset calculations such as:

Counts
Totals
Averages
Medians
Minimums
Maximums
Most common categories
Correlations

The Q&A engine runs locally and does not require an external AI API.

Recommendation Engine

Combines analytical findings into evidence-based recommendations tailored to the uploaded dataset.

Reporting Engine

Generates downloadable PDF and Excel reports from the current analysis.

🛠️ Technologies Used
Backend
Python
Flask
Pandas
NumPy
Frontend
HTML5
CSS3
JavaScript
Chart.js
Reporting
ReportLab
OpenPyXL
Development
Git
GitHub
🎯 Project Objective

The primary objective of AI Data Detective is to automate repetitive data-analysis tasks and help users move from raw datasets to structured analytical insights.

The platform focuses on:

Understanding dataset quality
Automatically identifying dataset structure
Automating exploratory analysis
Detecting unusual patterns
Identifying trends
Finding potential data-driven drivers
Answering common analytical questions
Generating dataset-specific visualizations
Providing evidence-based recommendations
Producing downloadable analytical reports
🌐 Dataset-Adaptive Design

One of the core goals of the project is to avoid relying on fixed business columns such as Revenue, Category, or Region.

For example:

Sales Dataset
Revenue       → Metric
Category      → Dimension
Region        → Dimension
Order_ID      → Identifier
Date          → Date/Time
Student Dataset
Math          → Metric
Science       → Metric
Attendance    → Metric
Class         → Dimension
Student_ID    → Identifier
IPL Dataset
team1_runs    → Metric
team2_runs    → Metric
match_type    → Dimension
season        → Date/Time / temporal field
match_number  → Identifier-like field

The same analytical system adapts its dashboard, charts, Q&A suggestions, anomalies, trends, and recommendations according to the detected schema.

📁 Project Structure
AI-Data-Detective/
│
├── app/
│   ├── __init__.py
│   ├── analysis.py
│   ├── dashboard.py
│   ├── qa_engine.py
│   ├── recommendation_engine.py
│   ├── report_excel.py
│   ├── report_pdf.py
│   ├── routes.py
│   ├── schema.py
│   │
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   │
│   │   └── js/
│   │       ├── app.js
│   │       └── chart_export.js
│   │
│   └── templates/
│       └── index.html
│
├── data/
│   └── sample/
│       └── sample_sales.csv
│
├── docs/
│   └── ARCHITECTURE.md
│
├── tests/
│   └── test_core.py
│
├── .gitignore
├── CHANGELOG.md
├── README.md
├── requirements.txt
├── run.py
└── run_windows.bat
▶️ How to Run
1. Clone the repository
git clone https://github.com/muskan-saini27/AI-Data-Detective-Autonomous-Data-Analysis-BI-Platform.git
2. Open the project directory
cd AI-Data-Detective-Autonomous-Data-Analysis-BI-Platform
3. Create a virtual environment
Windows
python -m venv venv
Linux / macOS
python3 -m venv venv
4. Install dependencies
Windows
venv\Scripts\python.exe -m pip install -r requirements.txt
Linux / macOS
python3 -m pip install -r requirements.txt
5. Start the Flask application
Windows
venv\Scripts\python.exe run.py
Linux / macOS
python run.py
6. Open the application

Visit:

http://127.0.0.1:5000
🧪 Testing

The project includes a core test suite covering major functionality.

Run:

python tests/test_core.py

The test suite is designed to validate areas such as:

Dataset analysis
Multiple dataset schemas
Dataset-adaptive calculations
Q&A functionality
Recommendation generation
PDF report generation
Excel report generation
📄 Sample Dataset

A sample sales dataset is included at:

data/sample/sample_sales.csv

Use it for a quick first test after starting the application.

The platform can also be tested with other structured CSV/XLS/XLSX datasets.

🔐 Data & Privacy

The application is designed primarily for local dataset analysis.

Uploaded datasets are processed by the local Flask application and the deterministic Q&A workflow does not require sending the dataset to an external AI API.

Users should still avoid uploading confidential or sensitive information when running the application in an unsecured environment.

🚧 Future Enhancements

Possible future improvements include:

Advanced machine-learning-based insights
More sophisticated natural-language querying
Additional statistical tests
Interactive dashboard filters
Advanced business recommendation models
Database connectivity
Scheduled report generation
Cloud deployment
User authentication
Dataset history
Project management
Additional BI export formats
👨‍💻 Author

Muskan Saini

B.Tech Computer Science Student
Data Analytics | Python | SQL | Power BI | Machine Learning

⭐ Support

If you find this project useful, consider giving the repository a star.

Built with Python • Flask • Pandas • NumPy • Chart.js




