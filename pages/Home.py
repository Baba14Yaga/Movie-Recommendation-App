import streamlit as st
from MultiApp import MultiApp
import pandas as pd
from pages import TfIdf,UserBased,BagOfWords
def app():
    st.title("Home")
    menu=MultiApp()
    menu.add_app('Content Based(TF-IDF)',TfIdf.app)
    menu.add_app('User Based(K_neighbor)',UserBased.app)
    menu.add_app('Content Based(Bag of Words)',BagOfWords.app)
    menu.run()