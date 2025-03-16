import streamlit as st
import pandas as pd
from shared import *

def update_colnames(col_list):
    n=len(col_list)
    new_col=[]
    for i in list(range(n)):
        if col_list[i][0][:5]=='Unnam':
            new_col.append(col_list[i][1])
        else:
            new_col.append(col_list[i][0]+"_"+col_list[i][1])
    return new_col

stagion = st.session_state.get('stag', 'Serie A')
league = st.session_state.get('camp', stagione_corso)
def get_stats_fbref(table,stag=stagion):
    s = f'https://fbref.com/it/comps/{dict_camp[league]}/{league.replace(' ', '-')}-Stats'
    df=pd.read_html(s,attrs={'id':table})[0]
    if table!=f'results{stag}{dict_camp[league]}1_overall':
        df.columns=update_colnames(df.columns)
    rad_sito=f"https://raw.githubusercontent.com/tommyblasco/SerieA_Advanced/master/images/stemmi/{league.replace(' ','-')}/"
    df['link_img']=[rad_sito+x+'.png' for x in df['Squadra']]
    return df