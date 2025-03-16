import streamlit as st
st.set_page_config(page_title="FootballMent",layout='wide')
import requests
from PIL import Image
from io import BytesIO


st.title("Top 5 campionati ai raggi X(G)")

st.subheader("Statistiche avanzate sul calcio moderno europeo")
home_img=Image.open(BytesIO(requests.get(f"https://github.com/tommyblasco/SerieA_Advanced/blob/master/images/varie/home.png?raw=true").content))
st.image(home_img, use_container_width=True)

st.subheader('I campionati')
l1, l2, l3, l4, l5 = st.columns(5)
l1.image(Image.open(BytesIO(requests.get(f"https://github.com/tommyblasco/SerieA_Advanced/blob/master/images/varie/premier_league.png?raw=true").content)), use_container_width=True, caption='🇬🇧 Premier League')
l2.image(Image.open(BytesIO(requests.get(f"https://github.com/tommyblasco/SerieA_Advanced/blob/master/images/varie/serie_a.png?raw=true").content)), use_container_width=True, caption='🇮🇹 Serie A')
l3.image(Image.open(BytesIO(requests.get(f"https://github.com/tommyblasco/SerieA_Advanced/blob/master/images/varie/la_liga.png?raw=true").content)), use_container_width=True, caption='🇪🇸 LaLiga')
l4.image(Image.open(BytesIO(requests.get(f"https://github.com/tommyblasco/SerieA_Advanced/blob/master/images/varie/bundesliga.png?raw=true").content)), use_container_width=True, caption='🇩🇪 Bundesliga')
l5.image(Image.open(BytesIO(requests.get(f"https://github.com/tommyblasco/SerieA_Advanced/blob/master/images/varie/ligue1.png?raw=true").content)), use_container_width=True, caption='🇫🇷 Ligue 1')
