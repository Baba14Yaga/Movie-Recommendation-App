import streamlit as st
import pandas as pd
from pages import TfIdf,UserBased,BagOfWords
def app(user_id):
    st.title("Home")
    menu=["Content Based (Bag of Words)","Content Based (Tf-Idf)","User Based (K-Neighbour)"]
    choice= st.selectbox("Menu",menu)
    if choice =="Content Based (Bag of Words)":
        BagOfWords.app(user_id)
    if choice =="Content Based (Tf-Idf)":
        TfIdf.app(user_id)
    if choice =="User Based (K-Neighbour)":
        UserBased.app(user_id)        