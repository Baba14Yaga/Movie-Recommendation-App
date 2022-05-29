import streamlit as st
from pages import Home,Admin

from model.usertable import add_userdata,login_user
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

menu=["Login","SignUp"]
choice= st.sidebar.selectbox("Menu",menu)

if choice =="SignUp":

	st.sidebar.title("SignUp")
	new_user =st.sidebar.text_input("User Name")
	new_password =st.sidebar.text_input("Password",type='password')

	if st.sidebar.button("SignUp"):
		
		result=add_userdata(new_user,make_hashes(new_password))
		if result:
			st.sidebar.success("You have succesfully created valid Account")
			st.sidebar.info("Go to Login Menu to login")
		else:
			st.sidebar.warning("{} already exists try another username".format(new_user))	
		
if choice == 'Login':
	st.sidebar.title("Login")

	username=st.sidebar.text_input("User Name")
	password=st.sidebar.text_input("Password",type='password')	
			
	if st.sidebar.checkbox("Login"):

		if username=='admin' and password=='admin':
			Admin.app()
		else:
			user_id=login_user(username,make_hashes(password))
			if user_id:
				st.sidebar.success("logged in as {}".format(username)+" You can now access App")
				Home.app(user_id)

			else:
				st.sidebar.warning("Incorrect Username / Password")