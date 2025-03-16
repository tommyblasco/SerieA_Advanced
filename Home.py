import streamlit as st
st.set_page_config(page_title="FootballMent",layout='wide')
import requests
from PIL import Image
import pages.Squadre
import pages.Partite
import pages.Giocatori
from io import BytesIO
import pandas as pd

st.title("Top 5 campionati ai raggi X(G)")

st.subheader("Statistiche avanzate sul calcio moderno europeo")

home_img=Image.open(BytesIO(requests.get(f"https://github.com/tommyblasco/SerieA_Advanced/blob/master/images/varie/home.png?raw=true").content))
st.image(home_img, use_container_width=True)

stagione_corso='2024-2025'
list_stag2pass=[str(int(stagione_corso[:4])-1)+'-'+stagione_corso[:4], str(int(stagione_corso[:4])-2)+'-'+str(int(stagione_corso[:4])-1)]
dict_camp = {'Premier League':'9','La Liga':'12','Serie A':'11','Bundesliga':'20','Ligue 1':'13'}

if 'camp' not in st.session_state:
    st.session_state['camp'] = "Serie A"
if 'stag' not in st.session_state:
    st.session_state['stag'] = stagione_corso

st.sidebar.title("Sezione analisi")
pagina = st.sidebar.radio("Vai a:", ["Squadre", "Giocatori", "Partite"])
st.sidebar.title("Filtra per:")
st.session_state['camp']=st.sidebar.selectbox('Scegli un campionato:',dict_camp.keys())
st.session_state['stag']=st.sidebar.selectbox('Scegli una stagione:',[stagione_corso]+list_stag2pass)


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

if pagina == "Squadre":
    pages.Squadre.show()
elif pagina == "Giocatori":
    pages.Giocatori.show()
elif pagina == "Partite":
    pages.Partite.show()