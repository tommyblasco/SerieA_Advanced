from Funzioni import *

st.header('Analisi Squadre')

att_sk, cen_sk, def_sk = st.tabs(['Attacking skills','Passing skills','Defending skills'])

with att_sk:
    string_quest='standard'
    fa='for'
    df_std=get_stats_fbref(table=f'stats_squads_{string_quest}_{fa}')
    df_std['G-xG']=[x-y for x,y in zip(df_std['Rendimento_Reti'],df_std['Prestazione prevista_xG'])]
    df_std['npG-npxG'] = [x - y for x, y in zip(df_std['Rendimento_R - Rig'], df_std['Prestazione prevista_npxG'])]
    st.subheader('Gol vs XG')
    opt_ex_pen=st.toggle('Escludi rigori')
    if opt_ex_pen:
        x_sel='Rendimento_R - Rig'
        y_sel='Prestazione prevista_npxG'
        diff_sel='npG-npxG'
    else:
        x_sel = 'Rendimento_Reti'
        y_sel = 'Prestazione prevista_xG'
        diff_sel = 'G-xG'
    xg_gl = go.Figure()
    for x, y, png in zip(df_std[x_sel], df_std[y_sel], df_std['link_img']):
        xg_gl.add_layout_image( x=x, y=y, source=png,
            xref="x", yref="y", sizex=4, sizey=4, xanchor="center", yanchor="middle")
    x_min, x_max = df_std[x_sel].min() - 1, df_std[x_sel].max() + 1
    y_min, y_max = df_std[y_sel].min() - 1, df_std[y_sel].max() + 1
    #bisettrice
    xg_gl.add_trace(go.Scatter(x=[x_min, x_max],y=[x_min, x_max],
        mode='lines', line=dict(color='red', dash='dash')))
    #tooltip
    xg_gl.add_trace(go.Scatter(x=df_std[x_sel], y=df_std[y_sel],
    mode='markers', marker_opacity=0, customdata=df_std[['Squadra',x_sel, y_sel, diff_sel]],
    hovertemplate=
        "%{customdata[0]}<br>" +
        "Gol Fatti: %{customdata[1]}<br>" +
        "xG: %{customdata[2]:.2f}<br>" +
        "Gol-xG: %{customdata[3]:.2f}<extra></extra>"))
    xg_gl.update_xaxes(dict(range=[min(x_min,y_min), max(x_max,y_max)],title='Gol Fatti'))
    xg_gl.update_yaxes(dict(range=[min(x_min,y_min), max(x_max,y_max)],title='xG'))
    xg_gl.update_layout(showlegend=False, annotations=[dict(text="Underperform", x=0.05, y=0.95, xref='paper', yref='paper',font_size=13, showarrow=False, xanchor='left'),
                                     dict(text="Overperform",x=0.95, y=0.05, xref='paper', yref='paper', font_size=13,showarrow=False,xanchor='right')])
    st.plotly_chart(go.FigureWidget(data=xg_gl), use_container_width=True)