import requests as req
import streamlit as st
import random

def get_songs(airtable_token):
    # Define the haeaders for the search
	# Remember to change to secrets that bearer (and re-generate it)
	headers = {
		'Authorization': f'Bearer {airtable_token}'
	}
	# Get the url
	url = 'https://api.airtable.com/v0/appSU80hu0LcLPPg3/Lyrics%20Sentimental%20Analysis?'
	# Get the data from requests
	res = req.get(url, headers=headers)
	records = res.json()['records'] # Get records

	# Map out all the fields instead of all the object
	songs = list(map(lambda record: record['fields'], records))

	return songs

def get_artists():

	artists_name = []
	artists_image = {}
	for song in st.session_state.songs:
		artists_name.append(song['artist_name'])
		if song['artist_name'] not in artists_image:
			artists_image[song['artist_name']] = []
		artists_image[song['artist_name']].append(song['img'])

	artists_name = list(set(artists_name))
	for name, imgs in artists_image.items():
		artists_image[name] = random.choice(imgs)

	return artists_name, artists_image


def initialize_page():
	# Define default value for 'selected_artist'
	if 'selected_artist' not in st.session_state:
		st.session_state.selected_artist = None
		
	# Get the songs from airtable and store as a session state so we do not lose the data in each interaction
	if 'songs' not in st.session_state:
		# Eror handling
		try:
			st.session_state.songs = get_songs(st.secrets['airtable_token'])
			st.session_state.artists, st.session_state.imgs = get_artists()
		except:
			# In case something is wrong with the request
			st.session_state.songs = []

