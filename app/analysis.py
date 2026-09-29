from __future__ import annotations
import math
import numpy as np
import pandas as pd
from .schema import infer_schema

def safe(v):
    if v is None or pd.isna(v): return None
    if isinstance(v,(np.integer,np.floating)): return float(v)
    return v

def numeric_summary(df, cols):
    out=[]
    for c in cols:
        s=pd.to_numeric(df[c],errors='coerce').dropna()
        if s.empty: continue
        q1,q3=s.quantile(.25),s.quantile(.75); iqr=q3-q1
        mask=((s<q1-1.5*iqr)|(s>q3+1.5*iqr)) if iqr!=0 else pd.Series(False,index=s.index)
        out.append({'column':c,'count':int(s.size),'mean':safe(s.mean()),'median':safe(s.median()),'min':safe(s.min()),'max':safe(s.max()),'sum':safe(s.sum()),'std':safe(s.std()),'missing':int(df[c].isna().sum()),'outliers':int(mask.sum())})
    return out

def categorical_summary(df, cols):
    out=[]
    for c in cols:
        vc=df[c].fillna('Missing').value_counts(dropna=False)
        out.append({'column':c,'unique':int(df[c].nunique(dropna=True)),'missing':int(df[c].isna().sum()),'top_values':[{'value':str(k),'count':int(v)} for k,v in vc.head(8).items()]})
    return out

def datetime_summary(df, cols):
    out=[]
    for c in cols:
        s=pd.to_datetime(df[c],errors='coerce').dropna()
        if s.empty: continue
        out.append({'column':c,'min':s.min().date().isoformat(),'max':s.max().date().isoformat(),'unique_dates':int(s.dt.normalize().nunique()),'missing':int(df[c].isna().sum())})
    return out

def correlation(df, cols):
    if len(cols)<2: return {'matrix':{},'strongest':None}
    c=df[cols].apply(pd.to_numeric,errors='coerce').corr(); a=c.abs(); np.fill_diagonal(a.values,np.nan)
    if a.isna().all().all(): return {'matrix':c.fillna(0).round(3).to_dict(),'strongest':None}
    i=int(np.nanargmax(a.to_numpy())); r,cc=np.unravel_index(i,a.shape)
    return {'matrix':c.fillna(0).round(3).to_dict(),'strongest':{'col1':c.index[r],'col2':c.columns[cc],'value':safe(c.iloc[r,cc]),'abs_value':safe(a.iloc[r,cc])}}

def anomalies(df, cols):
    out=[]
    for c in cols:
        s=pd.to_numeric(df[c],errors='coerce'); v=s.dropna()
        if len(v)<5: continue
        q1,q3=v.quantile(.25),v.quantile(.75); iqr=q3-q1
        m=(s<q1-1.5*iqr)|(s>q3+1.5*iqr) if iqr!=0 else pd.Series(False,index=df.index)
        mean,std=v.mean(),v.std()
        if std and np.isfinite(std): m=m.fillna(False)|((s-mean).abs()>3*std).fillna(False)
        idx=list(df.index[m.fillna(False)])[:8]
        if idx: out.append({'column':c,'count':int(m.sum()),'method':'IQR + Z-score','sample_values':[float(s.loc[i]) for i in idx]})
    return out

def trend(values):
    y=pd.to_numeric(values,errors='coerce').dropna().to_numpy(float)
    if len(y)<5:return None
    x=np.arange(len(y),dtype=float); slope=float(np.polyfit(x,y,1)[0]); pred=slope*x+(y.mean()-slope*x.mean())
    ssr=float(((y-pred)**2).sum()); sst=float(((y-y.mean())**2).sum()); r2=1-ssr/sst if sst else 0.0
    h=max(1,len(y)//2); first,last=float(y[:h].mean()),float(y[-h:].mean()); change=((last-first)/abs(first)*100) if first else None
    if change is None or r2<.2: direction='Weak / no clear trend'
    elif change>5: direction='Increasing'
    elif change<-5: direction='Decreasing'
    else: direction='Flat'
    return {'direction':direction,'slope':safe(slope),'r2':round(r2,3),'change_percent':round(change,2) if change is not None else 0}

def trends(df, metric_cols, date_col):
    out=[]
    for c in metric_cols:
        if date_col:
            t=pd.DataFrame({'date':pd.to_datetime(df[date_col],errors='coerce'),'value':pd.to_numeric(df[c],errors='coerce')}).dropna(); g=t.groupby(t.date.dt.normalize()).value.mean().sort_index()
            z=trend(g); basis=f'time: {date_col}'
        else:
            z=trend(df[c]); basis='row sequence (no date column detected)'
        if z: z.update({'column':c,'basis':basis}); out.append(z)
    return out

def root_causes(df, metrics, dims):
    out=[]
    for metric in metrics[:6]:
        v=pd.to_numeric(df[metric],errors='coerce'); valid=v.dropna();
        if valid.empty: continue
        overall=float(valid.mean()); total_ss=float(((valid-overall)**2).sum())
        for dim in dims[:10]:
            t=pd.DataFrame({'d':df[dim].fillna('Missing'),'v':v}).dropna();
            if t.d.nunique()<2: continue
            g=t.groupby('d').v.mean(); n=t.groupby('d').v.count(); eta=float((n*(g-overall)**2).sum()/total_ss) if total_ss else 0.0
            for seg,m in g.items():
                diff=(float(m)-overall)/abs(overall)*100 if overall else 0
                if abs(diff)>=20: out.append({'metric':metric,'dimension':dim,'segment':str(seg),'segment_mean':safe(m),'overall_mean':safe(overall),'difference_percent':round(diff,2),'association_strength':round(max(0,min(1,eta)),3),'note':'Potential statistical association; this does not prove causation.'})
    out.sort(key=lambda x:(abs(x['difference_percent']),x['association_strength']),reverse=True)
    return out[:20]

def chart_data(df, schema):
    m,d,dt=schema.get('primary_metric'),schema.get('primary_dimension'),schema.get('date_column'); out={'metric':m,'dimension':d,'date':dt}
    if m and dt:
        t=pd.DataFrame({'date':pd.to_datetime(df[dt],errors='coerce'),'v':pd.to_numeric(df[m],errors='coerce')}).dropna(); g=t.groupby(t.date.dt.normalize()).v.mean().sort_index().tail(30); out['series']={'labels':[x.strftime('%Y-%m-%d') for x in g.index],'values':[float(x) for x in g.values]}
    elif m:
        s=pd.to_numeric(df[m],errors='coerce').dropna().head(30); out['series']={'labels':[str(i+1) for i in range(len(s))],'values':[float(x) for x in s.values]}
    else: out['series']={'labels':[],'values':[]}
    if d:
        vc=df[d].fillna('Missing').value_counts().head(10); out['dimension_count']={'labels':[str(x) for x in vc.index],'values':[int(x) for x in vc.values]}
        if m:
            g=df.assign(__m=pd.to_numeric(df[m],errors='coerce'),__d=df[d].fillna('Missing')).groupby('__d').__m.mean().dropna().sort_values(ascending=False).head(10); out['dimension_metric']={'labels':[str(x) for x in g.index],'values':[float(x) for x in g.values]}
    else: out['dimension_count']={'labels':[],'values':[]}; out['dimension_metric']={'labels':[],'values':[]}
    return out

def findings(df,schema,corr,anoms,tr,roots):
    x=[]; miss=int(df.isna().sum().sum()); dup=int(df.duplicated().sum())
    x.append(f"{miss} missing cell(s) detected." if miss else 'No missing cells detected.')
    x.append(f"{dup} duplicate row(s) detected." if dup else 'No duplicate rows detected.')
    if anoms:
        a=max(anoms,key=lambda z:z['count']); x.append(f"Anomaly hotspot: {a['column']} contains {a['count']} unusual value(s).")
    if corr.get('strongest'):
        c=corr['strongest']; x.append(f"Strongest numeric correlation: {c['col1']} ↔ {c['col2']} (r = {float(c['value']):.2f}).")
    if tr:
        t=max(tr,key=lambda z:abs(z['change_percent'])); x.append(f"Trend signal: {t['column']} is {t['direction'].lower()} with {t['change_percent']:.2f}% early-to-late change.")
    if roots:
        r=roots[0]; d='higher' if r['difference_percent']>0 else 'lower'; x.append(f"Potential driver: {r['dimension']} = {r['segment']} has a {abs(r['difference_percent']):.2f}% {d} average {r['metric']} than overall; this is not causation.")
    return x[:8]

def analyze_dataset(df):
    schema=infer_schema(df); nums=numeric_summary(df,schema['metric_columns']); cats=categorical_summary(df,schema['dimension_columns']); dts=datetime_summary(df,schema['datetime_columns']); corr=correlation(df,schema['metric_columns']); anoms=anomalies(df,schema['metric_columns']); tr=trends(df,schema['metric_columns'],schema.get('date_column')); roots=root_causes(df,schema['metric_columns'],schema['dimension_columns']); total=max(len(df)*max(len(df.columns),1),1); quality=max(0,int(round(100-(df.isna().sum().sum()/total)*100-(df.duplicated().sum()/max(len(df),1))*20)))
    return {'overview':{'rows':int(len(df)),'columns':int(len(df.columns)),'missing':int(df.isna().sum().sum()),'duplicates':int(df.duplicated().sum()),'quality_score':quality},'columns':[str(c) for c in df.columns],'schema':schema,'preview':df.head(12).where(pd.notna(df.head(12)), '').to_dict('records'),'numeric_summary':nums,'categorical_summary':cats,'datetime_summary':dts,'correlation':corr,'anomalies':anoms,'trends':tr,'root_causes':roots,'chart_data':chart_data(df,schema),'findings':findings(df,schema,corr,anoms,tr,roots)}
