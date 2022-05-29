import streamlit as st
import pandas as pd
import sqlite3
# Create your connection.

def app():
    st.title("Admin Page")
    if st.button("show user table"):
        cnx = sqlite3.connect('model/data.db')
        try:
            df = pd.read_sql_query("SELECT * FROM userstable", cnx)
            st.dataframe(df )
        except:
            st.write("No Users registered yet")
        
    if st.button("show ratings table"):
        cnx = sqlite3.connect('model/data.db')
        try:
            df = pd.read_sql_query("SELECT * FROM ratings", cnx)
            st.dataframe(df )
        except:
            st.write("No movies rated  yet")
        
