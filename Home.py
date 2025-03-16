import streamlit as st
st.set_page_config(page_title="FootballMent",layout='wide')
import requests
from PIL import Image
from io import BytesIO

st.title("Top 5 campionati ai raggi X(G)")

st.subheader("Statistiche avanzate sul calcio moderno europeo")

home_img=Image.open(BytesIO(requests.get(f"https://github.com/tommyblasco/SerieA_Advanced/blob/master/images/varie/home.png?raw=true").content))
st.image(home_img, use_container_width=True)


stagione_corso='2024-2025'

list_stag2pass=[str(int(stagione_corso[:4])-1)+'-'+stagione_corso[:4], str(int(stagione_corso[:4])-2)+'-'+str(int(stagione_corso[:4])-1)]
dict_camp = {'Premier League':'9','La Liga':'12','Serie A':'11','Bundesliga':'20','Ligue 1':'13'}
sel_camp=st.sidebar.selectbox('Scegli un campionato:',dict_camp.keys())
sel_stag=st.sidebar.selectbox('Scegli una stagione:',[stagione_corso]+list_stag2pass)

sito_fbref=f'https://fbref.com/it/comps/{dict_camp[sel_camp]}/{sel_camp.replace(' ','-')}-Stats'
