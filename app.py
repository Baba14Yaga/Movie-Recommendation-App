from tkinter import Menu
import streamlit as st
import pandas as pd
from pages import Home
st.set_page_config(page_title='MOVIE RECOMMENDATION APP',
					page_icon="https://external-preview.redd.it/8cUAmZu7R2ncp2D_P3k8ZVuo8mp5y6qRedaY1Eas_04.jpg?auto=webp&s=effb685dc047beb005046aedad44aa0234b2fcec",
					layout="wide", initial_sidebar_state="auto", menu_items=None)

# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False
# DB Management
import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data


def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data


menu=["Login","SignUp"]
choice= st.sidebar.selectbox("Menu",menu)

if choice =="SignUp":

	st.title("SignUp")
	new_user =st.text_input("User Name")
	new_password =st.text_input("Password",type='password')

	if st.button("SignUp"):
		create_usertable()
		add_userdata(new_user,make_hashes(new_password))
		st.success("You have succesfully created valid Account")
		st.info("Go to Login Menu to login")
		
if choice == 'Login':
	st.title("Login")

	username=st.text_input("User Name")
	password=st.text_input("Password",type='password')	
			
	if st.checkbox("Login"):
		create_usertable()
		result=login_user(username,make_hashes(password))
		if result:
			user_result=view_all_users()
			clean_db=pd.DataFrame(user_result,columns=['username','password'])
			#st.dataframe(clean_db)

			st.success("logged in as {}".format(username)+" You can now access App")
			Home.app()

		else:
			st.warning("Incorrect Username / Password")