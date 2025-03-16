import streamlit as st
import pandas as pd
import requests
from PIL import Image
from io import BytesIO
import plotly.graph_objects as go
from shared import dict_camp

sito_fbref=f'https://fbref.com/it/comps/{dict_camp[st.session_state['camp']]}/{st.session_state['camp'].replace(' ','-')}-Stats'

def update_colnames(col_list):
    n=len(col_list)
    new_col=[]
    for i in list(range(n)):
        if col_list[i][0][:5]=='Unnam':
            new_col.append(col_list[i][1])
        else:
            new_col.append(col_list[i][0]+"_"+col_list[i][1])
    return new_col
def get_stats_fbref(table,s=sito_fbref,stag=st.session_state['stag']):
    df=pd.read_html(s,attrs={'id':table})[0]
    if table!=f'results{stag}{dict_camp[st.session_state['camp']]}1_overall':
        df.columns=update_colnames(df.columns)
    rad_sito=f"https://raw.githubusercontent.com/tommyblasco/SerieA_Advanced/master/images/stemmi/{st.session_state['camp'].replace(' ','-')}/"
    df['link_img']=[rad_sito+x+'.png' for x in df['Squadra']]
    return df