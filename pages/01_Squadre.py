import plotly.graph_objects as go
from Funzioni import *


st.header('Analisi Squadre')

s1, s2 = st.columns(2)
camp_sel=s1.selectbox('Scegli una campionato',dict_camp.keys())
stag_sel=s2.selectbox('Scegli una stagione',[stagione_corso]+list_stag2pass)

df_std=get_stats_fbref(table='stats_squads_standard_for', stag=stag_sel, league=camp_sel)
df_sh = get_stats_fbref(table='stats_squads_shooting_for', stag=stag_sel, league=camp_sel)
df_pass = get_stats_fbref(table='stats_squads_passing_for', stag=stag_sel, league=camp_sel)

att_sk, cen_sk, def_sk = st.tabs(['Attacking skills','Passing skills','Defending skills'])

with att_sk:
    df_std['G-xG']=[x-y for x,y in zip(df_std['Rendimento_Reti'],df_std['Prestazione prevista_xG'])]
    df_std['npG-npxG'] = [x - y for x, y in zip(df_std['Rendimento_R - Rig'], df_std['Prestazione prevista_npxG'])]
    rapp_x = (df_std['Rendimento_Reti'].max()-df_std['Rendimento_Reti'].min())/(df_std['Rendimento_R - Rig'].max()-df_std['Rendimento_R - Rig'].min())
    rapp_y = (df_std['Prestazione prevista_xG'].max()-df_std['Prestazione prevista_xG'].min())/(df_std['Prestazione prevista_npxG'].max()-df_std['Prestazione prevista_npxG'].min())
    st.subheader('Gol vs XG')
    opt_ex_pen=st.toggle('Escludi rigori')
    if opt_ex_pen:
        x_sel, y_sel, diff_sel, coeff_x, coeff_y='Rendimento_R - Rig', 'Prestazione prevista_npxG', 'npG-npxG', 1, 1
    else:
        x_sel, y_sel, diff_sel, coeff_x, coeff_y = 'Rendimento_Reti', 'Prestazione prevista_xG', 'G-xG', rapp_x, rapp_y
    xg_gl = go.Figure()
    for x, y, png in zip(df_std[x_sel], df_std[y_sel], df_std['link_img']):
        xg_gl.add_layout_image( x=x, y=y, source=png,
                    xref="x", yref="y", sizex=5*coeff_x, sizey=5*coeff_y, xanchor="center", yanchor="middle")
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
        rapp_x1 = (df_sh['Standard_Tiri'].max() - df_sh['Standard_Tiri'].min()) / ( df_sh['Standard_Tiri.1'].max() - df_sh['Standard_Tiri.1'].min())
        opt_tt = st.toggle('Rapporta ai tiri totali')
        if opt_tt:
            x_sel1, perc_sel, title_gr, coeff_x1='Standard_Tiri', 'Standard_G/Tiri', 'Tiri totali', rapp_x1
        else:
            x_sel1,  perc_sel, title_gr, coeff_x1= 'Standard_Tiri.1', 'Standard_G/TiP', 'Tiri in porta', 1
        sh_gr = go.Figure()
        for x, y, png in zip(df_sh[x_sel1], df_sh['Standard_Reti'], df_sh['link_img']):
            sh_gr.add_layout_image(x=x, y=y, source=png,
                                           xref="x", yref="y", sizex=5*coeff_x1, sizey=5, xanchor="center", yanchor="middle")
        sh_gr.add_trace(go.Scatter(x=df_sh[x_sel1], y=df_sh['Standard_Reti'],
                                               mode='markers', marker_opacity=0,
                                               customdata=df_sh[['Squadra', x_sel1, 'Standard_Reti', perc_sel]],
                                               hovertemplate=
                                               "%{customdata[0]}<br>" +
                                               "Tiri: %{customdata[1]}<br>" +
                                               "Gol: %{customdata[2]}<br>" +
                                               "%Conv Gol/Tiri: %{customdata[3]}<extra></extra>"))
        sh_gr.update_xaxes(dict(range=[min(df_sh[x_sel1])-4, max(df_sh[x_sel1])+4], title=title_gr))
        sh_gr.update_yaxes(dict(range=[min(df_sh['Standard_Reti'])-4, max(df_sh['Standard_Reti'])+4], title='Gol'))
        sh_gr.update_layout(showlegend=False, annotations=[
                    dict(text="> efficienza", x=0.05, y=0.95, xref='paper', yref='paper', font_size=13, showarrow=False,xanchor='left'),
                    dict(text="< efficienza", x=0.95, y=0.05, xref='paper', yref='paper', font_size=13, showarrow=False,xanchor='right')])
        st.plotly_chart(go.FigureWidget(data=sh_gr), use_container_width=True)

    st.divider()

    st.subheader('Distanza media e xg medio tiri')
    dm, xgm = st.columns([2,1])
    with dm:
        df_sh1 = df_sh.sort_values('Standard_Dist.',ascending=False)
        dm_gr = go.Figure(data=[go.Bar(
                            x=[x/10 for x in df_sh1['Standard_Dist.']], y=df_sh1['Squadra'], orientation='h',
                            width=0.1,  marker=dict(color='orange', line=dict(color='orange', width=1)), showlegend=False )
                    ])
        dm_gr.add_trace(go.Scatter(
                        x=[x/10 for x in df_sh1['Standard_Dist.']], y=df_sh1['Squadra'], mode='markers+text',
                        marker=dict(size=12, symbol='arrow-right', color='orange'),  text=[x/10 for x in df_sh1['Standard_Dist.']], textposition='middle right',
                        showlegend=False ))
        dm_gr.update_layout( xaxis=dict(side='top',range=[0,max([x/10 for x in df_sh1['Standard_Dist.']])+2]), height=500)
        st.plotly_chart(go.FigureWidget(data=dm_gr), use_container_width=True)
    with xgm:
        df_sh['npxG/Sh']=[x/100 for x in df_sh['Prestazione prevista_npxG/Sh']]
        df_sh2=df_sh[['Squadra','npxG/Sh']]
        df_sh2=df_sh2.sort_values('npxG/Sh',ascending=False)
        st.dataframe(df_sh2,hide_index=True)

    st.divider()

    st.subheader('Possesso palla vs Gol')
    pp_gr = go.Figure()
    for x, y, png in zip(df_std['Poss.'], df_std['Rendimento_Reti'], df_std['link_img']):
        pp_gr.add_layout_image(x=x, y=y, source=png, xref="x", yref="y", sizex=5, sizey=5, xanchor="center", yanchor="middle")
    pp_gr.add_vline(x=50,line_dash="dash", line_color="red")
    pp_gr.add_trace(go.Scatter(x=df_std['Poss.'], y=df_std['Rendimento_Reti'],
                               mode='markers', marker_opacity=0,
                               customdata=df_std[['Squadra', 'Poss.', 'Rendimento_Reti']],
                               hovertemplate=
                               "%{customdata[0]}<br>" +
                               "Possesso: %{customdata[1]}<br>" +
                               "Gol: %{customdata[2]}<br>" ))
    pp_gr.update_xaxes(dict(range=[min(df_std['Poss.']) - 4, max(df_std['Poss.']) + 4],title='Possesso palla'))
    pp_gr.update_yaxes(dict(range=[min(df_std['Rendimento_Reti']) - 4, max(df_std['Rendimento_Reti']) + 4], title='Gol'))
    st.plotly_chart(go.FigureWidget(data=pp_gr), use_container_width=True)
