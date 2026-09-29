# 🔎 AI Data Detective — Autonomous Data Analysis & BI Platform

A Flask-based automated data analysis and business intelligence platform that transforms raw CSV and Excel datasets into data quality reports, exploratory analysis, visualizations, trends, anomalies, potential root causes, business insights, and natural-language answers.

---

## 🚀 Overview

AI Data Detective is an end-to-end data analytics platform built with Python, Flask, Pandas, NumPy, HTML, CSS, and JavaScript.

Users can upload a CSV or Excel dataset and automatically receive:

- Dataset profiling
- Data quality analysis
- Statistical analysis
- Exploratory data analysis
- Data visualizations
- Trend detection
- Anomaly detection
- Correlation analysis
- Segment-level analysis
- Potential root-cause insights
- Natural-language data questions
- Business recommendations
- Downloadable PNG visualizations
- Excel reports
- PDF reports

The platform is designed to reduce repetitive manual analysis and provide a structured workflow from raw data to actionable insights.

---

## ✨ Features

### 📂 Dataset Upload

- Upload CSV datasets
- Upload Excel datasets
- Automatic dataset profiling
- Dataset preview
- Row and column analysis

### 🧹 Data Quality Analysis

- Missing-value detection
- Duplicate-row detection
- Data quality scoring
- Numeric data validation
- Outlier detection using statistical methods

### 📊 Exploratory Data Analysis

- Numeric statistics
- Mean, median, minimum, maximum, and standard deviation
- Categorical value analysis
- Frequency analysis
- Correlation analysis
- Automatic analytical findings

### 📈 Trend Intelligence

- Automatic trend detection
- Increasing/decreasing/flat trend identification
- Percentage change analysis
- Trend strength analysis
- Time-series-oriented insights where suitable

### 🚨 Anomaly Detection

- Statistical anomaly detection
- IQR-based outlier detection
- Z-score based detection
- Anomaly counts by numeric column
- Sample anomalous records

### 🔍 Root-Cause Intelligence

- Segment-level analysis
- Comparison of categorical groups against overall metrics
- Identification of potential business drivers
- Percentage difference analysis
- Association-strength analysis

> Note: The root-cause module identifies statistical associations and potential drivers. It does not claim causal relationships.

### 💬 Ask Your Data

Users can ask questions about their uploaded dataset using natural language.

Example questions:

- How many rows are there?
- How many columns are there?
- What is the average Revenue?
- What is the highest Revenue?
- What is the lowest Revenue?
- What is the total Revenue?
- What is the median Revenue?
- What is the most common Category?
- What is the most common Region?
- What is the strongest correlation?

The Q&A engine uses deterministic local data-analysis logic rather than requiring an external LLM or API key.

### 📊 Visual Analytics

The platform automatically generates visual representations of analyzed data.

Visualizations can be downloaded as:

- PNG images
- Analytical reports

### 📥 Report Export

Users can export analysis results into:

- Excel reports
- PDF reports
- PNG visualizations

This makes the analysis easier to share and use for reporting.

---

## 📌 Data Analysis Workflow

```text
Upload Dataset
      ↓
Dataset Profiling
      ↓
Data Quality Analysis
      ↓
Data Cleaning & Validation
      ↓
Exploratory Data Analysis
      ↓
Visualizations
      ↓
Trend Detection
      ↓
Anomaly Detection
      ↓
Correlation Analysis
      ↓
Root-Cause / Segment Analysis
      ↓
Business Insights
      ↓
Ask Your Data
      ↓
Export Reports
📊 Key Analytics

The platform analyzes datasets using metrics such as:

Total Rows
Total Columns
Missing Values
Duplicate Records
Data Quality Score
Numeric Statistics
Categorical Frequencies
Correlations
Outliers
Anomalies
Trends
Segment-Level Differences
Potential Drivers
Automated Insights
🧠 Intelligence Modules
Data Quality Engine

Evaluates the overall quality of an uploaded dataset by analyzing missing values, duplicates, and statistical irregularities.

EDA Engine

Automatically analyzes numeric and categorical variables and generates descriptive statistics and visualizations.

Anomaly Engine

Uses statistical methods such as IQR and Z-score techniques to identify unusual observations.

Trend Engine

Analyzes numeric trends and identifies increasing, decreasing, or relatively flat patterns where appropriate.

Root-Cause Engine

Compares segments within categorical dimensions against overall numeric metrics to identify potential drivers and significant differences.

Q&A Engine

Processes natural-language questions and maps them to dataset-level, numeric, categorical, and correlation analysis operations.

🛠️ Technologies Used
Python
Flask
Pandas
NumPy
JavaScript
HTML5
CSS3
Matplotlib
Plotly
OpenPyXL
🎯 Project Objective

The primary objective of AI Data Detective is to automate repetitive data-analysis tasks and help users move from raw datasets to meaningful analytical insights.

The platform focuses on:

Improving data quality understanding
Automating exploratory analysis
Detecting unusual patterns
Identifying trends
Finding potential data-driven business drivers
Answering common analytical questions
Presenting results through visualizations
Generating downloadable analytical reports
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
python -m venv venv
4. Install dependencies
Windows
venv\Scripts\python.exe -m pip install -r requirements.txt
Linux / macOS
python3 -m pip install -r requirements.txt
5. Start the Flask application
venv\Scripts\python.exe run.py

Or on Linux/macOS:

python run.py
6. Open the application

Visit:

http://127.0.0.1:5000
🧪 Testing

The project includes a core test suite covering major functionality.

Run:

python tests/test_core.py

The test suite validates:

Dataset analysis
Multiple dataset schemas
Report generation
PDF export
Excel export
📄 Sample Dataset

A sample sales dataset is included in:

data/sample/sample_sales.csv

You can use it to test the application immediately after starting the Flask server.

🔐 Data & Privacy

The application is designed for local dataset analysis.

Uploaded datasets are processed by the local Flask application and are not sent to an external AI API as part of the deterministic analysis and Q&A workflow.

Users should still avoid uploading confidential or sensitive business information when using the application in an unsecured environment.

🚧 Future Enhancements

Possible future improvements include:

Advanced machine learning-based insights
More sophisticated natural-language querying
Additional statistical tests
Interactive dashboard filters
More advanced business recommendation models
Database connectivity
Scheduled report generation
Cloud deployment
User authentication
Dataset history and project management
Additional BI export formats
👨‍💻 Author

Muskan Saini

B.Tech Computer Science Student | Data Analytics | Python | SQL | Power BI | Machine Learning

⭐ If you found this project useful, consider giving the repository a star!

.





