import sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# Avoid executing Flask package initialization when running this lightweight test.
import types
pkg = types.ModuleType("app")
pkg.__path__ = [str(ROOT / "app")]
sys.modules["app"] = pkg

from app.analysis import analyze_dataset
from app.dashboard import build_dashboard
from app.qa_engine import QAEngine
from app.recommendation_engine import RecommendationEngine
from app.report_pdf import PDFReport
from app.report_excel import ExcelReport


def check_dataset(name, df):
    a = analyze_dataset(df)
    assert a["overview"]["rows"] == len(df)
    assert len(a["columns"]) == len(df.columns)
    d = build_dashboard(df, a)
    q = QAEngine(df, a)
    assert "There are" in q.ask("How many rows are there?")
    RecommendationEngine(df, a).generate()
    print(f"PASS: {name} -> metric={a['schema']['primary_metric']}, dimension={a['schema']['primary_dimension']}, date={a['schema']['date_column']}")
    return a, d

sales = pd.read_csv(ROOT / "data/sample/sample_sales.csv")
hr = pd.DataFrame({
    "employee_id": range(1, 11),
    "department": ["IT","HR","IT","Sales","Sales","HR","IT","Finance","Finance","Sales"],
    "salary": [50000,45000,70000,60000,65000,48000,80000,55000,58000,72000],
    "score": [70,75,90,65,80,78,95,72,81,88],
    "join_date": pd.date_range("2025-01-01", periods=10),
})
students = pd.DataFrame({
    "student_id": [1,2,3,4,5],
    "class": ["A","A","B","B","C"],
    "math": [80,90,70,85,95],
    "science": [78,88,75,82,91],
    "attendance": [90,95,75,88,98],
})

for name, df in [("sales", sales), ("hr", hr), ("students", students)]:
    check_dataset(name, df)

an, dash = check_dataset("export-sales", sales)
recs = RecommendationEngine(sales, an).generate()
out = ROOT / "exports"
PDFReport(dash, recs, an).generate(str(out / "self_test.pdf"))
ExcelReport(sales, dash, an, recs).generate(str(out / "self_test.xlsx"))
assert (out / "self_test.pdf").exists() and (out / "self_test.pdf").stat().st_size > 1000
assert (out / "self_test.xlsx").exists() and (out / "self_test.xlsx").stat().st_size > 1000
print("PASS: PDF and Excel export")
