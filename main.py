import streamlit as st
from tools.tools import initialize_page
from tools.pages import  create_main_page, 	create_artist_page

initialize_page()

# Define the main page:
if st.session_state.selected_artist is None:
	create_main_page()
else: # Define the song page where it is suppose to be all the song information and sentiment analysis
	create_artist_page()