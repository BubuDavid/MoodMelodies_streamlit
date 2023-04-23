import streamlit as st
from streamlit_card import card
import re
import nltk
nltk.download('stopwords')
nltk.download('vader_lexicon')
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
import time


def create_main_page():
	# Note: You can write with MAGIC!
	# Write the header of our page
	st.write("""
	# Mood Melodies 🎶
	A streamlit web page for analize the sentiment of lyrics!
	""")

	# Error display
	if not st.session_state.songs:
		st.write("""
			# Sorry, something went wrong with the data base token 😢
		""")
		st.stop()

	# Create the columns to display the cards
	cols = st.columns(2)
	# Check when the user click the cards
	clicked_cards = [False] * len(st.session_state.songs)
	# Create the cards in each column from the session state songs
	counter = 0
	progress_bar = st.progress(counter, text = 'Loading')
	for index, artist in enumerate(st.session_state.artists):
		counter += 100 // len(st.session_state.artists)
		progress_bar.progress(counter, text='Loading')
		with cols[index % 2]:
			# Store the click state of each card
			clicked_cards[index] = card(
				title = artist,
				text = '',
				image = st.session_state.imgs[artist],
				key = index,
			)

	progress_bar.progress(100, text='Completed!')
	# Check the clicked cards (for some reason we need to do double click)
	for index, clicked in enumerate(clicked_cards):
		if clicked:
			st.session_state.selected_artist = st.session_state.artists[index]
	time.sleep(1)
	progress_bar.empty()

def update_selected_artist():
	st.session_state.selected_artist = None

def create_artist_page():
	# Define the back button function
	st.button('👈 back', on_click=update_selected_artist)
	# Here is all the structure
	# Access the data
	artist_name = st.session_state.selected_artist
	artist_image = st.session_state.imgs[artist_name]
	# Create structure

	st.image(artist_image)

	st.markdown(f"""
	# {artist_name}
	""")
	
	songs = list(filter(lambda song: song['artist_name'] == artist_name, st.session_state.songs))
	
	create_song_analysis_section(songs)
	

def create_song_analysis_section(songs):
	pass