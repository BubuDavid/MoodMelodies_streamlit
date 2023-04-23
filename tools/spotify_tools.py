import requests

def get_access_token(client_id, client_secret, verbose = False):
	# Get an access token from the Spotify API
	auth_url = 'https://accounts.spotify.com/api/token'
	auth_response = requests.post(auth_url, {
		'grant_type': 'client_credentials',
		'client_id': client_id,
		'client_secret': client_secret,
	})
	if auth_response.status_code in range(200, 300):
		access_token = auth_response.json()['access_token']
		if verbose:
			print('Autenticated 👍')
		return True, access_token

	if verbose:
		print("Something's wrong with the authentication 👎")
		print(auth_response.status_code)
	return False, ''


def get_song(song_name, access_token, verbose = False):
    # Use the access token to make a request to the Spotify API
    search_url = 'https://api.spotify.com/v1/search'
    headers = {'Authorization': 'Bearer ' + access_token}
    params = {'q': song_name, 'type': 'track'}
    response = requests.get(search_url, headers=headers, params=params)
    if response.status_code in range(200, 300):
        song_info = response.json()['tracks']['items'][0]
        if verbose:
            print('Everything is okay in the song retrieve ✅')
        return True, song_info
    else:
        if verbose:
            print('Everything is in flames with the song retrieve! Watch OUT!!! 🔥')
        return False, ''


def extract_relevant_info(song_info):
    # Extract relevant information about the song
    relevant_info = {}
    relevant_info['song_name'] = song_info['name']
    relevant_info['artist_name'] = song_info['artists'][0]['name']
    relevant_info['album_name'] = song_info['album']['name']
    relevant_info['release_date'] = song_info['album']['release_date']
    relevant_info['img'] = song_info['album']['images'][0]['url']

    return relevant_info

