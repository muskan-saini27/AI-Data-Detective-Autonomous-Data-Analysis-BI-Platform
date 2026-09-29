class RecommendationEngine:
    def __init__(self,df,analysis): self.df=df; self.analysis=analysis
    def generate(self):
        out=[]; o=self.analysis['overview']
        if o['missing']: out.append({'type':'Data Quality','title':'Review missing values','message':f"The dataset contains {o['missing']} missing cell(s). Review affected columns before downstream decisions."})
        if o['duplicates']: out.append({'type':'Data Quality','title':'Review duplicate rows','message':f"{o['duplicates']} duplicate row(s) were detected. Confirm whether they are legitimate repeated records."})
        if self.analysis['anomalies']:
            a=max(self.analysis['anomalies'],key=lambda x:x['count']); out.append({'type':'Anomaly','title':f"Investigate unusual {a['column']} values",'message':f"{a['count']} unusual value(s) were detected using IQR + Z-score checks. Validate them before treating them as errors or events."})
        if self.analysis['trends']:
            t=max(self.analysis['trends'],key=lambda x:abs(x['change_percent']));
            if t['direction'] not in ('Flat','Weak / no clear trend'): out.append({'type':'Trend','title':f"Review {t['column']} trend",'message':f"{t['column']} is {t['direction'].lower()} with a {t['change_percent']:.2f}% change. Investigate the periods or records behind the movement."})
        if self.analysis['root_causes']:
            r=self.analysis['root_causes'][0]; d='higher' if r['difference_percent']>0 else 'lower'; out.append({'type':'Potential Driver','title':f"Investigate {r['dimension']} = {r['segment']}",'message':f"Average {r['metric']} is {abs(r['difference_percent']):.2f}% {d} than the overall mean. This is an association, not proof of causation."})
        if self.analysis['correlation']['strongest']:
            c=self.analysis['correlation']['strongest']; out.append({'type':'Association','title':'Review strongest numeric relationship','message':f"{c['col1']} and {c['col2']} have the strongest observed linear correlation (r = {float(c['value']):.2f}). Correlation does not establish causation."})
        if not out: out.append({'type':'General','title':'No high-priority issues detected','message':'The configured checks did not identify a high-priority quality, anomaly, trend, or segment issue.'})
        return out[:10]
