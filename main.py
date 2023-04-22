import streamlit as st
from streamlit_card import card
from tools.tools import get_songs

# Define default value for 'selected_song'
if 'selected_song' not in st.session_state:
    st.session_state.selected_song = None
    
# Get the songs from airtable and store as a session state so we do not lose the data in each interaction
if 'songs' not in st.session_state:
	st.session_state.songs = get_songs()


# Define the main page:
if st.session_state.selected_song is None:
	# Note: You can write with MAGIC!
	# Write the header of our page
	st.write("""
	# Mood Melodies 🎶
	A streamlit web page for analize the sentiment of lyrics!
	""")

	# Create the columns to display the cards
	cols = st.columns(2)
	# Check when the user click the cards
	clicked_cards = [False] * len(st.session_state.songs)
	# Create the cards in each column from the session state songs
	for index, song in enumerate(st.session_state.songs):
		with cols[index % 2]:
			# Store the click state of each card
			clicked_cards[index] = card(
				title=song['song_name'],
				text=song['artist_name'],
				image=song['img'],
				key = index,
			)
	# Check the clicked cards (for some reason we need to do double click)
	for index, clicked in enumerate(clicked_cards):
		if clicked:
			st.session_state.selected_song = st.session_state.songs[index]
else: # Define the secondary page where it is suppose to be all the song information and sentiment analysis
	# Define the back button function
	def update_selected_song():
		st.session_state.selected_song = None
	st.button('👈 back', on_click=update_selected_song)
	
	# Here is all the structure
	st.session_state.selected_song
	
	