import streamlit as st
from streamlit_card import card
from tools.tools import get_songs

# Define default value for 'selected_song'
if 'selected_song' not in st.session_state:
    st.session_state.selected_song = None
    
# Get the songs from airtable
if 'songs' not in st.session_state:
	st.session_state.songs = get_songs()


# Define the main page:
if st.session_state.selected_song is None:
	# Note: You can write with MAGIC!
	st.write("""
	# Mood Melodies 🎶
	A streamlit web page for analize the sentiment of lyrics!
	""")

	cols = st.columns(2)
	clicked_cards = [False] * len(st.session_state.songs)
	for index, song in enumerate(st.session_state.songs):
		with cols[index % 2]:
			clicked_cards[index] = card(
				title=song['song_name'],
				text=song['artist_name'],
				image=song['img'],
				key = index,
			)

	for index, clicked in enumerate(clicked_cards):
		if clicked:
			st.session_state.selected_song = st.session_state.songs[index]
else:
	def update_selected_song():
		st.session_state.selected_song = None
	st.session_state.selected_song
	st.button('👈 back', on_click=update_selected_song)