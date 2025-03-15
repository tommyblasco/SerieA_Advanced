from Funzioni import *

st.header('Analisi Squadre')

att_sk, cen_sk, def_sk = st.tabs(3)

with att_sk:
    string_quest='standard'
    fa='for'
    df_std=get_stats_fbref(table=f'stats_squads_{string_quest}_{fa}')
    st.write('Gol vs XG')
    xg_gl = go.Figure()
    for _, row in df_std.iterrows():
        xg_gl.add_layout_image(
            dict( source=row['link_img'],
                x=row['Rendimento_Reti'], y=row['Prestazione prevista_xG'],
                xref="x", yref="y", sizex=0.4,  sizey=0.4,
                xanchor="center", yanchor="middle", layer="above"
            ) )
    st.plotly_chart(xg_gl)