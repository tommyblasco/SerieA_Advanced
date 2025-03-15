import streamlit as st
st.set_page_config(page_title="Serie A",layout='wide')
import requests
from PIL import Image
from io import BytesIO

st.title("Serie A ai raggi X(G)")

st.subheader("Statistiche avanzate sulla moderna Serie A")

home_img=Image.open(BytesIO(requests.get(f"https://github.com/tommyblasco/SerieA_Advanced/blob/master/images/varie/home.png?raw=true").content))
st.image(home_img, use_container_width=True)
