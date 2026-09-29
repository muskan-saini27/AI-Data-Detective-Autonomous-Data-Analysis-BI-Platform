from __future__ import annotations
import re
import numpy as np
import pandas as pd
from .schema import normalize_name

class QAEngine:
    def __init__(self,df,analysis): self.df=df.copy(); self.analysis=analysis; self.schema=analysis['schema']
    def find_col(self,text,candidates=None):
        q=normalize_name(text); candidates=candidates or list(self.df.columns); qtok=set(q.split()); scored=[]
        for c in candidates:
            n=normalize_name(c); nt=set(n.split())
            if n==q:return c
            if q and (q in n or n in q):return c
            ov=len(qtok&nt)
            if ov: scored.append((ov/max(len(qtok|nt),1),ov,c))
        scored.sort(reverse=True)
        return scored[0][2] if scored and (scored[0][0]>=.34 or scored[0][1]>=2) else None
    def metric(self,q): return self.find_col(q,self.schema['metric_columns']) or self.schema.get('primary_metric')
    def dim(self,q): return self.find_col(q,self.schema['dimension_columns']) or self.schema.get('primary_dimension')
    def fmt(self,v):
        try:return f'{float(v):,.2f}'
        except:return str(v)
    def ask(self,question):
        q=re.sub(r'\s+',' ',question.lower().strip())
        if not q:return 'Please enter a question.'
        if re.search(r'\b(rows?|records?)\b',q): return f'There are {len(self.df)} rows.'
        if re.search(r'\b(columns?|fields?)\b',q): return f'There are {len(self.df.columns)} columns.'
        if 'missing' in q:
            c=self.find_col(q)
            return f"{c} has {int(self.df[c].isna().sum())} missing value(s)." if c else f"There are {int(self.df.isna().sum().sum())} missing values across the dataset."
        if 'duplicate' in q:return f"There are {int(self.df.duplicated().sum())} duplicate row(s)."
        if 'correlation' in q or 'correlated' in q:
            c=self.analysis['correlation']['strongest']; return f"The strongest numeric correlation is between {c['col1']} and {c['col2']} (r = {float(c['value']):.2f})." if c else 'At least two suitable numeric columns are required for correlation analysis.'
        if 'trend' in q:
            m=self.metric(q); t=next((x for x in self.analysis['trends'] if x['column']==m),None); return f"{m} is {t['direction'].lower()} with {t['change_percent']:.2f}% early-to-late change (R² = {t['r2']:.2f}; {t['basis']})." if t else 'No clear trend was detected for that metric.'
        if any(p in q for p in ['most common','most frequent','appears most','most popular']):
            c=self.dim(q)
            if not c:return 'I could not identify a dimension column for that question.'
            vc=self.df[c].fillna('Missing').value_counts(); return f"The most common {c} is '{vc.index[0]}' ({int(vc.iloc[0])} rows)." if not vc.empty else f'{c} has no usable values.'
        if 'unique' in q:
            c=self.find_col(q); return f'{c} has {int(self.df[c].nunique(dropna=True))} unique non-missing values.' if c else 'I could not identify the requested column.'
        if any(w in q for w in ['highest','maximum','max']) and any(w in q for w in ['which','region','category','department','group','segment','dimension']):
            dim=self.dim(q); m=self.metric(q)
            if dim and m:
                t=pd.DataFrame({'d':self.df[dim].fillna('Missing'),'m':pd.to_numeric(self.df[m],errors='coerce')}).dropna(); g=t.groupby('d').m.sum().sort_values(ascending=False)
                if not g.empty:return f"{g.index[0]} has the highest total {m} at {self.fmt(g.iloc[0])}."
        ops=[('average','mean'),('mean','mean'),('median','median'),('highest','max'),('maximum','max'),('lowest','min'),('minimum','min'),('total','sum'),('sum','sum'),('standard deviation','std')]
        for word,op in ops:
            if word in q:
                m=self.metric(q)
                if not m:return 'I could not identify a suitable numeric metric in this dataset.'
                s=pd.to_numeric(self.df[m],errors='coerce').dropna()
                if s.empty:return f'{m} has no usable numeric values.'
                v={'mean':s.mean(),'median':s.median(),'max':s.max(),'min':s.min(),'sum':s.sum(),'std':s.std()}[op]; return f'The {"average" if op=="mean" else op} {m} is {self.fmt(v)}.'
        return 'I can answer counts, missing/duplicate values, statistics, most-common values, segment comparisons, trends, and correlations. Try asking about a specific metric or dimension.'
