from Funzioni import *

st.header('Analisi Squadre')

att_sk, cen_sk, def_sk = st.tabs(['Attacking skills','Passing skills','Defending skills'])

with att_sk:
    string_quest='standard'
    fa='for'
    df_std=get_stats_fbref(table=f'stats_squads_{string_quest}_{fa}')
    st.write('Gol vs XG')
    xg_gl = go.Figure()
    for x, y, png in zip(df_std['Rendimento_Reti'], df_std['Prestazione prevista_xG'], df_std['link_img']):
        xg_gl.add_layout_image( x=x, y=y, source=png,
            xref="x", yref="y", sizex=2, sizey=2, xanchor="center", yanchor="middle")
    xg_gl.update_xaxes(range=[min(min(df_std['Rendimento_Reti']),min(df_std['Prestazione prevista_xG']))-1, max(max(df_std['Rendimento_Reti']),max(df_std['Prestazione prevista_xG']))+1])
    xg_gl.update_yaxes(range=[min(min(df_std['Rendimento_Reti']),min(df_std['Prestazione prevista_xG']))-1, max(max(df_std['Rendimento_Reti']),max(df_std['Prestazione prevista_xG']))+1])
    st.plotly_chart(go.FigureWidget(data=xg_gl), use_container_width=True)