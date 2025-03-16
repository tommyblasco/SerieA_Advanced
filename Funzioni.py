import streamlit as st
import pandas as pd

dict_camp = {'Premier League':'9','La Liga':'12','Serie A':'11','Bundesliga':'20','Ligue 1':'13'}
stagione_corso='2024-2025'
list_stag2pass=[str(int(stagione_corso[:4])-1)+'-'+stagione_corso[:4], str(int(stagione_corso[:4])-2)+'-'+str(int(stagione_corso[:4])-1)]

def update_colnames(col_list):
    n=len(col_list)
    new_col=[]
    for i in list(range(n)):
        if col_list[i][0][:5]=='Unnam':
            new_col.append(col_list[i][1])
        else:
            new_col.append(col_list[i][0]+"_"+col_list[i][1])
    return new_col

def get_stats_fbref(table,stag,league):
    s = f'https://fbref.com/it/comps/{stag}/{dict_camp[league]}/{league.replace(' ', '-')}-Stats'
    df=pd.read_html(s,attrs={'id':table})[0]
    if table!=f'results{stag}{dict_camp[league]}1_overall':
        df.columns=update_colnames(df.columns)
    rad_sito=f"https://raw.githubusercontent.com/tommyblasco/SerieA_Advanced/master/images/stemmi/{league}/"
    df['link_img']=[rad_sito+x+'.png' for x in df['Squadra']]
    return df