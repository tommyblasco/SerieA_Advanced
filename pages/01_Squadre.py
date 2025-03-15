from Funzioni import *

st.header('Analisi Squadre')

att_sk, cen_sk, def_sk = st.tabs(['Attacking skills','Passing skills','Defending skills'])

with att_sk:
    string_quest='standard'
    fa='for'
    df_std=get_stats_fbref(table=f'stats_squads_{string_quest}_{fa}')
    df_std['G-xG']=[x-y for x,y in zip(df_std['Rendimento_Reti'],df_std['Prestazione prevista_xG'])]
    st.write('Gol vs XG')
    xg_gl = go.Figure()
    for x, y, png in zip(df_std['Rendimento_Reti'], df_std['Prestazione prevista_xG'], df_std['link_img']):
        xg_gl.add_layout_image( x=x, y=y, source=png,
            xref="x", yref="y", sizex=4, sizey=4, xanchor="center", yanchor="middle")
    x_min, x_max = df_std['Rendimento_Reti'].min() - 1, df_std['Rendimento_Reti'].max() + 1
    y_min, y_max = df_std['Prestazione prevista_xG'].min() - 1, df_std['Prestazione prevista_xG'].max() + 1
    xg_gl.add_trace(go.Scatter(x=[x_min, x_max],y=[x_min, x_max],
        mode='lines', line=dict(color='red', dash='dash')))
    xg_gl.add_trace(go.Scatter(x=df_std['Rendimento_Reti'], y=df_std['Prestazione prevista_xG'],
    mode='markers', marker_opacity=0, customdata=df_std[['Squadra','Rendimento_Reti', 'Prestazione prevista_xG', 'G-xG']],
    hovertemplate=
        "%{customdata[0]}<br>" +
        "Gol Fatti: %{customdata[1]}<br>" +
        "xG: %{customdata[2]:.2f}<br>" +
        "Gol-xG: %{customdata[3]:.2f}<extra></extra>"
))
    xg_gl.update_xaxes(dict(range=[min(x_min,y_min), max(x_max,y_max)],title='Gol Fatti'))
    xg_gl.update_yaxes(dict(range=[min(x_min,y_min), max(x_max,y_max)],title='xG'))
    xg_gl.update_layout(showlegend=False, annotations=[dict(text="Underperform", x=0.05, y=0.95, xref='paper', yref='paper',font_size=13, showarrow=False, xanchor='left'),
                                     dict(text="Overperform",x=0.95, y=0.05, xref='paper', yref='paper', font_size=13,showarrow=False,xanchor='right')])
    st.plotly_chart(go.FigureWidget(data=xg_gl), use_container_width=True)