import streamlit as st
st.set_page_config(page_title="FootballMent",layout='wide')
import requests
from PIL import Image
from io import BytesIO
import importlib
from shared import dict_camp

st.title("Top 5 campionati ai raggi X(G)")

st.subheader("Statistiche avanzate sul calcio moderno europeo")

home_img=Image.open(BytesIO(requests.get(f"https://github.com/tommyblasco/SerieA_Advanced/blob/master/images/varie/home.png?raw=true").content))
st.image(home_img, use_container_width=True)

st.sidebar.title("Sezione analisi")
pagina = st.sidebar.radio("Vai a:", ["Squadre", "Giocatori", "Partite"])

stagione_corso='2024-2025'

list_stag2pass=[str(int(stagione_corso[:4])-1)+'-'+stagione_corso[:4], str(int(stagione_corso[:4])-2)+'-'+str(int(stagione_corso[:4])-1)]


if 'camp' not in st.session_state:
    st.session_state['camp'] = "Serie A"
if 'stag' not in st.session_state:
    st.session_state['stag'] = stagione_corso

st.sidebar.title("Filtra per:")
st.session_state['camp']=st.sidebar.selectbox('Scegli un campionato:',dict_camp.keys())
st.session_state['stag']=st.sidebar.selectbox('Scegli una stagione:',[stagione_corso]+list_stag2pass)

pagine = {
    "Squadre": "01_Squadre",
    "Giocatori": "02_Giocatori",
    "Partite": "03_Partite"
}

# Importazione dinamica della pagina
modulo = importlib.import_module(f"pages/{pagine[pagina]}")
modulo.show()


