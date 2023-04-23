import time
import os.path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import toml
from spotify_tools import get_access_token, get_song, extract_relevant_info
import json
import requests

# Get the credentials, for optimal reasons we have it in a .streamlit > secrets.toml file
with open('../.streamlit/secrets.toml', 'r') as f:
    secrets = toml.load(f)
    
# Read every secret
airtable_token = secrets['airtable_token']
spotify_client_id = secrets['spotify_client_id']
spotify_client_secret = secrets['spotify_client_secret']

# Auth in Spotify
step1, spotify_access_token = get_access_token(spotify_client_id, spotify_client_secret)

# Set path to chromedriver as per your configuration
homedir = os.path.expanduser("~/chromedriver_things")
webdriver_service = Service(f"{homedir}/chromedriver/stable/chromedriver")

# Choose Chrome Browser
driver = webdriver.Chrome(service=webdriver_service)


def scrap_and_save(url, artist_name, sleeping_time = 2):
	# Navigate to the main page
	driver.get(url)
	driver.maximize_window()

	data = []
	# Click on each 'mini_card' element
	for index in range(10):
		# Search for the elements
		time.sleep(sleeping_time)
		cards = driver.find_elements(By.CLASS_NAME, 'mini_card')
		# Extract song name
		song_name = cards[index].text.split('\n')[0]
		# Click in the element
		cards[index].click()

		# Extract the lyrics
		time.sleep(sleeping_time)
		lyrics = "\n".join(driver.find_element(By.ID, 'lyrics-root').text.split('\n')[3:-2])

		# With the spotify API collect important data
		step2, song_info = get_song(f"{song_name} {artist_name}", spotify_access_token)
		if not step2:
			print(f'Sorry, did not work for: {song_name} by {artist_name}')
			continue

		relevant_info = extract_relevant_info(song_info)
		relevant_info['lyrics'] = lyrics
		relevant_info['artist_name'] = artist_name

		data.append(relevant_info)


		# Navigate back to the main page
		driver.back()



	# Save all the data in the database
	data_airtable = {'records': []}

	# Transform to data for airtable
	for record in data:
		data_airtable['records'].append({'fields': record})
		

	# Define the endpoint URL and headers
	endpoint_url = f"https://api.airtable.com/v0/appSU80hu0LcLPPg3/tbloxxkbjJ18A0Jjr"
	headers = {
		'Authorization': f'Bearer {airtable_token}',
		'Content-Type': 'application/json'
	}

	json_data = json.dumps(data_airtable)

	# Make a POST request to the endpoint URL with the JSON data and headers
	requests.post(endpoint_url, data=json_data, headers=headers)

url = "https://genius.com/artists/Justin-bieber"
artist_name = 'Justin Bieber'
# Try two times
try:
	scrap_and_save(url, artist_name, 5)
	print('Everything is right ✅')
except:
	print("The operations could not be completed 🔥")



driver.quit()