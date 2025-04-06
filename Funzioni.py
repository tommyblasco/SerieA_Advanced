import streamlit as st
import pandas as pd
import time

dict_camp = {'Premier League':'9','La Liga':'12','Serie A':'11','Bundesliga':'20','Ligue 1':'13'}
stagione_corso='2024-2025'
list_stag2pass=[str(int(stagione_corso[:4])-1)+'-'+stagione_corso[:4], str(int(stagione_corso[:4])-2)+'-'+str(int(stagione_corso[:4])-1)]

ppda_det=pd.read_csv("https://raw.githubusercontent.com/tommyblasco/SerieA_Advanced/refs/heads/master/ppda_det.csv",sep=',')
ppda_riep=pd.read_csv("https://raw.githubusercontent.com/tommyblasco/SerieA_Advanced/refs/heads/master/ppda_fin.csv",sep=',')
shots=pd.read_csv("https://raw.githubusercontent.com/tommyblasco/SerieA_Advanced/refs/heads/master/shot.csv",sep=',')

conversione_nomi = {'Verona': 'Hellas Verona', 'Parma Calcio 1913': 'Parma', 'AC Milan': 'Milan'}
ppda_det['Squadra']=ppda_det['Squadra'].replace(conversione_nomi)

def update_colnames(col_list):
    n=len(col_list)
    new_col=[]
    for i in list(range(n)):
        if col_list[i][0][:5]=='Unnam':
            new_col.append(col_list[i][1])
        else:
            new_col.append(col_list[i][0]+"_"+col_list[i][1])
    return new_col

@st.cache_data
def get_stats_fbref(table,stag,league):
    if stag!=stagione_corso:
        s = f'https://fbref.com/it/comp/{dict_camp[league]}/{stag}/Statistiche-di-{league.replace(' ', '-')}-{stag}'
    else:
        s = f'https://fbref.com/it/comps/{dict_camp[league]}/{league.replace(' ', '-')}-Stats'
    df=pd.read_html(s,attrs={'id':table})[0]
    if table!=f'results{stag}{dict_camp[league]}1_overall':
        df.columns=update_colnames(df.columns)
    rad_sito=f"https://raw.githubusercontent.com/tommyblasco/SerieA_Advanced/master/images/stemmi/{league}/"
    df['link_img']=[rad_sito+x+'.png' for x in df['Squadra']]
    return df

def create_subdf(stag,league,db_ppda=ppda_det):
    df_overall=get_stats_fbref(table=f'results{stag}{dict_camp[league]}1_overall', stag=stag, league=league)
    time.sleep(1)
    df_std=get_stats_fbref(table='stats_squads_standard_for', stag=stag, league=league)
    time.sleep(1)
    df_std_ag=get_stats_fbref(table='stats_squads_standard_against', stag=stag, league=league)
    time.sleep(1)
    df_sh = get_stats_fbref(table='stats_squads_shooting_for', stag=stag, league=league)
    time.sleep(1)
    df_sh_ag = get_stats_fbref(table='stats_squads_shooting_against', stag=stag, league=league)
    time.sleep(1)
    df_pass = get_stats_fbref(table='stats_squads_passing_for', stag=stag, league=league)
    time.sleep(1)
    df_pass_types = get_stats_fbref(table='stats_squads_passing_types_for', stag=stag, league=league)
    time.sleep(1)
    df_misc = get_stats_fbref(table='stats_squads_misc_for', stag=stag, league=league)
    time.sleep(1)

    df1 = df_overall[['Squadra','Pt','Rf','Rs','xG','xGA']].merge(df_std[['Squadra','Poss.']],on='Squadra',how='left')
    df2 = df1.merge(df_sh[['Squadra', 'Standard_Tiri.1']], on='Squadra', how='left')
    df3 = df2.merge(df_pass[['Squadra', 'Prestazione prevista_xA','PF','PPA','Cross in area','PrgP']], on='Squadra', how='left')
    df4 = df3.merge(df_pass_types[['Squadra', 'Tipologie di passaggi_PassFil']], on='Squadra', how='left')
    df5 = df4.merge(df_misc[['Squadra', 'Rendimento_Falli','Rendimento_Cross','Rendimento_Int']], on='Squadra', how='left')
    df5.columns=['Squadra','Punti','GolF','GolS','xG_for','xGA','Possesso','TiP','xA','PF','PPA','Cross in area','PrgP','Filtranti','Falli','Cross','Intercetti']
    df6 = df5.merge(df_std_ag[['Squadra', 'Prestazione prevista_xG']], on='Squadra', how='left')
    df_fin = df6.merge(df_sh_ag[['Squadra', 'Standard_Tiri.1']], on='Squadra', how='left')
    df_fin.columns=list(df5.columns)+['xG_conc','TiP_conc']
    if league=='Serie A':
        ppda_det=db_ppda[db_ppda['Anno']==stag]
        df_fin = df_fin.merge(ppda_det[['Squadra', 'Media PPDA']], on='Squadra', how='left')
    return df_fin