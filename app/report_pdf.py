from datetime import datetime
import os
from html import escape
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle
class PDFReport:
    def __init__(self,dashboard,recommendations,analysis): self.dashboard=dashboard; self.recommendations=recommendations; self.analysis=analysis
    def generate(self,path):
        os.makedirs(os.path.dirname(path),exist_ok=True); doc=SimpleDocTemplate(path,pagesize=A4,rightMargin=.45*inch,leftMargin=.45*inch,topMargin=.45*inch,bottomMargin=.45*inch); st=getSampleStyleSheet(); st.add(ParagraphStyle(name='Small',parent=st['BodyText'],fontSize=8.5,leading=11)); title=st['Title']; title.alignment=TA_CENTER; title.textColor=colors.HexColor('#0f172a'); head=st['Heading2']; head.textColor=colors.HexColor('#1d4ed8'); story=[Paragraph('AI Data Detective',title),Paragraph('Executive Business Intelligence Report',st['BodyText']),Paragraph(datetime.now().strftime('%d %B %Y, %I:%M %p'),st['Small']),Spacer(1,.15*inch),Paragraph('Executive Summary',head)]
        m=self.dashboard.get('primary_metric') or 'Primary Metric'; d=self.dashboard.get('primary_dimension') or 'Primary Dimension'; rows=[['Rows',self.dashboard['rows']],['Columns',self.dashboard['columns']],['Quality',f"{self.dashboard['quality']}%"],[f'Total {m}',self._fmt(self.dashboard['primary_metric_total'])],[f'Average {m}',self._fmt(self.dashboard['primary_metric_average'])],[f'Highest {m}',self._fmt(self.dashboard['primary_metric_max'])],[f'Most Common {d}',self.dashboard.get('top_dimension_value') or '-'],[f'Highest Total {m} by {d}',self.dashboard.get('top_dimension_metric_value') or '-']]; t=Table(rows,colWidths=[2.8*inch,2.2*inch]); t.setStyle(TableStyle([('BACKGROUND',(0,0),(0,-1),colors.HexColor('#1d4ed8')),('TEXTCOLOR',(0,0),(0,-1),colors.white),('FONTNAME',(0,0),(0,-1),'Helvetica-Bold'),('BACKGROUND',(1,0),(1,-1),colors.HexColor('#0f172a')),('TEXTCOLOR',(1,0),(1,-1),colors.white),('GRID',(0,0),(-1,-1),.5,colors.white),('PADDING',(0,0),(-1,-1),6)])); story += [t,Spacer(1,.16*inch),Paragraph('Key Findings',head)]
        for x in self.analysis.get('findings',[]): story += [Paragraph('• '+escape(x),st['Small']),Spacer(1,.03*inch)]
        story += [Spacer(1,.08*inch),Paragraph('Business Recommendations',head)]
        for r in self.recommendations: story += [Paragraph(f"<b>{escape(r['title'])}</b>",st['Small']),Paragraph(escape(r['message']),st['Small']),Spacer(1,.07*inch)]
        story += [Paragraph('Anomaly Detection',head)]
        if self.analysis['anomalies']:
            for a in self.analysis['anomalies']: story.append(Paragraph(f"• {escape(a['column'])}: {a['count']} unusual value(s)",st['Small']))
        else: story.append(Paragraph('No unusual numeric values were detected.',st['Small']))
        story += [Spacer(1,.08*inch),Paragraph('Trend Insights',head)]
        if self.analysis['trends']:
            for z in self.analysis['trends']: story.append(Paragraph(f"• {escape(z['column'])}: {escape(z['direction'])} ({z['change_percent']:.2f}%, R² {z['r2']:.2f}; {escape(z['basis'])})",st['Small']))
        else: story.append(Paragraph('No usable trend signal was detected.',st['Small']))
        story += [Spacer(1,.15*inch),Paragraph('Generated automatically by AI Data Detective v3.1',st['Small'])]; doc.build(story); return path
    @staticmethod
    def _fmt(v):
        if v is None:return '-'
        try:return f'{float(v):,.2f}'
        except:return str(v)
