from pathlib import Path
from flask import Blueprint,request,jsonify,render_template,send_file
import pandas as pd
from .analysis import analyze_dataset
from .dashboard import build_dashboard
from .qa_engine import QAEngine
from .recommendation_engine import RecommendationEngine
from .report_pdf import PDFReport
from .report_excel import ExcelReport
bp=Blueprint('main',__name__); ROOT=Path(__file__).resolve().parent.parent; EXPORT=ROOT/'exports'; EXPORT.mkdir(parents=True,exist_ok=True); CURRENT_DATASET=None; CURRENT_ANALYSIS=None
@bp.route('/')
def home(): return render_template('index.html')
def read_file(f):
    n=(f.filename or '').lower()
    if n.endswith('.csv'):
        try:return pd.read_csv(f)
        except UnicodeDecodeError: f.stream.seek(0); return pd.read_csv(f,encoding='latin-1')
    if n.endswith(('.xlsx','.xls')): return pd.read_excel(f)
    raise ValueError('Unsupported file type. Use CSV, XLS or XLSX.')
@bp.route('/api/analyze',methods=['POST'])
def analyze():
    global CURRENT_DATASET,CURRENT_ANALYSIS
    if 'file' not in request.files:return jsonify(error='No file uploaded.'),400
    f=request.files['file']
    try:
        df=read_file(f)
        if df.empty:return jsonify(error='The uploaded dataset is empty.'),400
        cols=[]; seen={}
        for c in df.columns:
            base=str(c).strip() or 'Unnamed'; seen[base]=seen.get(base,0)+1; cols.append(base if seen[base]==1 else f'{base}_{seen[base]}')
        df.columns=cols; a=analyze_dataset(df); a['dashboard']=build_dashboard(df,a); a['recommendations']=RecommendationEngine(df,a).generate(); a['filename']=f.filename; CURRENT_DATASET=df.copy(); CURRENT_ANALYSIS=a; return jsonify(a)
    except Exception as e:return jsonify(error=f'Analysis failed: {e}'),500
@bp.route('/api/ask',methods=['POST'])
def ask():
    if CURRENT_DATASET is None:return jsonify(error='Analyze a dataset first.',answer='Upload and analyze a dataset first.'),400
    q=str((request.get_json(silent=True) or {}).get('question','')).strip()
    if not q:return jsonify(error='Please enter a question.',answer='Please enter a question.'),400
    try:return jsonify(answer=QAEngine(CURRENT_DATASET,CURRENT_ANALYSIS).ask(q),type='text')
    except Exception as e:return jsonify(error=str(e),answer=f'Unable to answer the question: {e}'),500
@bp.route('/api/export/pdf')
def export_pdf():
    if CURRENT_DATASET is None:return jsonify(error='Analyze a dataset first.'),400
    p=EXPORT/'AI_Data_Report.pdf'; PDFReport(CURRENT_ANALYSIS['dashboard'],CURRENT_ANALYSIS['recommendations'],CURRENT_ANALYSIS).generate(str(p)); return send_file(str(p),as_attachment=True,download_name=p.name,mimetype='application/pdf')
@bp.route('/api/export/excel')
def export_excel():
    if CURRENT_DATASET is None:return jsonify(error='Analyze a dataset first.'),400
    p=EXPORT/'AI_Data_Report.xlsx'; ExcelReport(CURRENT_DATASET,CURRENT_ANALYSIS['dashboard'],CURRENT_ANALYSIS,CURRENT_ANALYSIS['recommendations']).generate(str(p)); return send_file(str(p),as_attachment=True,download_name=p.name,mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
