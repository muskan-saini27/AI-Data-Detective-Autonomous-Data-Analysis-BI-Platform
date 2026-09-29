# AI Data Detective v3.1

Local, dataset-adaptive data investigation platform built with Flask, Pandas, NumPy, Chart.js, ReportLab, and OpenPyXL.

## Supported files
CSV, XLS, XLSX.

## Dataset-adaptive behavior
The application does not require columns named Revenue, Category, or Region. It detects numeric metrics, categorical dimensions, date/time fields, identifiers and text columns, then adapts KPI cards, charts, suggestions, statistics, trend analysis, recommendations and report labels to the uploaded schema.

Examples:
- Sales: Revenue, Region, Category, Date
- HR: Salary, Department, Attrition, Joining Date
- Students: Math, Science, Attendance, Class

The bundled sample CSV is only a demonstration. Upload another dataset to see the schema-adaptive behavior.

## Run on Windows
```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe run.py
```
Open http://127.0.0.1:5000

## Important limitation
Q&A is deterministic local NLP, not a general-purpose LLM. It answers the implemented question patterns. Correlations and segment associations are statistical relationships, not proof of causation.
