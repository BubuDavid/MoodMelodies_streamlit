import requests as req

def get_songs():
    # Define the haeaders for the search
	# Remember to change to secrets that bearer (and re-generate it)
	headers = {
		'Authorization': 'Bearer patz6X6tWMIc2WX9W.b9ff32c0815ae279a224ca8454e69065b92252b7576c470f30c680fae05b54ab'
	}
	# Get the url
	url = 'https://api.airtable.com/v0/appSU80hu0LcLPPg3/Lyrics%20Sentimental%20Analysis?'
	# Get the data from requests
	res = req.get(url, headers=headers)
	records = res.json()['records'] # Get records

	# Map out all the fields instead of all the object
	songs = list(map(lambda record: record['fields'], records))

	return songs