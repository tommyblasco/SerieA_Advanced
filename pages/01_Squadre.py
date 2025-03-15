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
        x_sel, y_sel, diff_sel='Rendimento_R - Rig', 'Prestazione prevista_npxG', 'npG-npxG'
    else:
        x_sel, y_sel, diff_sel = 'Rendimento_Reti', 'Prestazione prevista_xG', 'G-xG'
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
    xg_gl.update_yaxes(dict(range=[min(x_min,y_min), max(x_max,y_max)],title=diff_sel.split('-')[1]))
    xg_gl.update_layout(showlegend=False, annotations=[dict(text="Underperform", x=0.05, y=0.95, xref='paper', yref='paper',font_size=13, showarrow=False, xanchor='left'),
                                     dict(text="Overperform",x=0.95, y=0.05, xref='paper', yref='paper', font_size=13,showarrow=False,xanchor='right')])
    st.plotly_chart(go.FigureWidget(data=xg_gl), use_container_width=True)

    st.divider()

    string_quest = 'shooting'
    fa = 'for'
    df_sh = get_stats_fbref(table=f'stats_squads_{string_quest}_{fa}')
    st.subheader('Tiri vs Tiri in porta vs Gol')
    fun, sh_gol=st.columns([1,2])
    with fun:
        team_fun=st.selectbox('Seleziona una squadra',list(df_sh['Squadra']))
        fun_gr=go.Figure(go.Funnel(
            y=['Tiri','Tiri in porta','Gol'], x=[df_sh.loc[df_sh['Squadra']==team_fun,'Standard_Tiri'].item(),
                                                 df_sh.loc[df_sh['Squadra']==team_fun,'Standard_Tiri.1'].item(),
                                                 df_sh.loc[df_sh['Squadra']==team_fun,'Standard_Reti'].item()],
            textposition='inside',textinfo='value+percent initial', marker={'color':['red','orange','yellow']}
        ))
        st.plotly_chart(go.FigureWidget(data=fun_gr), use_container_width=True)

    with sh_gol:
        opt_tt = st.toggle('Rapporta ai tiri totali')
        if opt_tt:
            x_sel1, perc_sel, title_gr='Standard_Tiri', 'Standard_G/Tiri', 'Tiri totali'
        else:
            x_sel1,  perc_sel, title_gr= 'Standard_Tiri.1', 'Standard_G/TiP', 'Tiri in porta'
        sh_gr = go.Figure()
        for x, y, png in zip(df_sh[x_sel1], df_sh['Standard_Reti'], df_sh['link_img']):
            sh_gr.add_layout_image(x=x, y=y, source=png,
                                   xref="x", yref="y", sizex=3, sizey=3, xanchor="center", yanchor="middle")
        sh_gr.add_trace(go.Scatter(x=df_sh[x_sel1], y=df_sh['Standard_Reti'],
                                       mode='markers', marker_opacity=0,
                                       customdata=df_sh[['Squadra', x_sel1, 'Standard_Reti', perc_sel]],
                                       hovertemplate=
                                       "%{customdata[0]}<br>" +
                                       "Tiri: %{customdata[1]}<br>" +
                                       "Gol: %{customdata[2]}<br>" +
                                       "% conversione: %{customdata[3]:.2f}<extra></extra>"))
        sh_gr.update_xaxes(dict(range=[min(df_sh[x_sel1])-1, max(df_sh[x_sel1])+1], title=title_gr))
        sh_gr.update_yaxes(dict(range=[min(df_sh['Standard_Reti'])-1, max(df_sh['Standard_Reti'])+1], title='Gol'))
        sh_gr.update_layout(showlegend=False, annotations=[
            dict(text="> efficienza", x=0.05, y=0.95, xref='paper', yref='paper', font_size=13, showarrow=False,xanchor='left'),
            dict(text="< efficienza", x=0.95, y=0.05, xref='paper', yref='paper', font_size=13, showarrow=False,xanchor='right')])
        st.plotly_chart(go.FigureWidget(data=sh_gr), use_container_width=True)


