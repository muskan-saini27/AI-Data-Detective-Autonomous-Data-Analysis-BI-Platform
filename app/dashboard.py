def build_dashboard(df, analysis):
    s=analysis['schema']; nums=analysis['numeric_summary']; d=analysis['categorical_summary']; m=s.get('primary_metric'); dim=s.get('primary_dimension')
    dash={'rows':analysis['overview']['rows'],'columns':analysis['overview']['columns'],'missing':analysis['overview']['missing'],'duplicates':analysis['overview']['duplicates'],'quality':analysis['overview']['quality_score'],'primary_metric':m,'primary_dimension':dim,'primary_metric_total':None,'primary_metric_average':None,'primary_metric_max':None,'top_dimension_value':None,'top_dimension_metric_value':None,'outlier_count':sum(x['count'] for x in analysis['anomalies'])}
    if m:
        z=next((x for x in nums if x['column']==m),None)
        if z: dash.update(primary_metric_total=z['sum'],primary_metric_average=z['mean'],primary_metric_max=z['max'])
    if dim:
        vc=df[dim].fillna('Missing').value_counts(); dash['top_dimension_value']=str(vc.index[0]) if not vc.empty else None
        if m:
            g=df.assign(__m=df[m].astype(float),__d=df[dim].fillna('Missing')).groupby('__d').__m.sum().sort_values(ascending=False); dash['top_dimension_metric_value']=str(g.index[0]) if not g.empty else None
    return dash
