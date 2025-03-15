import streamlit as st
import pandas as pd
import requests
from PIL import Image
from io import BytesIO
import plotly.graph_objects as go

sito_fbref='https://fbref.com/it/comps/11/Serie-A-Stats'
stagione_corso='2024-2025'

def update_colnames(col_list):
    n=len(col_list)
    new_col=[]
    for i in list(range(n)):
        if col_list[i][0][:5]=='Unnam':
            new_col.append(col_list[i][1])
        else:
            new_col.append(col_list[i][0]+"_"+col_list[i][1])
    return new_col
def get_stats_fbref(table,s=sito_fbref,stag=stagione_corso):
    df=pd.read_html(s,attrs={'id':table})[0]
    if table!=f'results{stag}111_overall':
        df.columns=update_colnames(df.columns)
    rad_sito="https://raw.githubusercontent.com/tommyblasco/SerieA_Advanced/master/images/stemmi/"
    df['link_img']=[rad_sito+x.upper()+'.png' if x!='Hellas Verona' else rad_sito+'VERONA.png' for x in df['Squadra']]
    return df