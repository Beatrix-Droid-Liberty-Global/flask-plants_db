
## a file that contians teh functions for handling the api requests from the client


import requests
import json
from pprint import pprint
from config import API_KEY





def get_json_response(image, organ: str) -> dict:

	"""A function that accepts an image and an  text input from the user and returns
	submits the user input to the plant.net machine learning api for plant recognition"""
	
	api_endpoint = f"https://my-api.plantnet.org/v2/identify/all?api-key={API_KEY}"

	data = {
		'organs': organ
	}

	image_path_1 = f"static/user_uploads/{image}"
	image_data_1 = open(image_path_1, 'rb')

	files = [
		('images', (image_path_1, image_data_1))
	]
	
	#submit a post request to the api
	#Whenever you receive a Response object from an API call or a Session call, 
	# the request attribute is actually the PreparedRequest that was used. 
	# In some cases you may wish to do some extra work to the body or headers
	#  (or anything else really) before sending a request.
	req = requests.Request('POST', url=api_endpoint, files=files, data=data)
	
	prepared = req.prepare()
	
	#The Session object allows you toparameters across requests.
	s = requests.Session()
	response = s.send(prepared)
	json_result = json.loads(response.text)

	return json_result



def process_response(json_result):

	""""A function that takes the json from the api response and extracts the information we 
	need to display on the frontend"""

	plant_name = json_result["bestMatch"]
	pictures_uploaded = json_result["query"]["organs"]
	common_name = json_result["results"][2]["species"]["commonNames"]
	family_name = json_result["results"][2]["species"]["family"]["scientificName"]
	genus = json_result["results"][2]["species"]["genus"]["scientificName"]

	return plant_name, pictures_uploaded, common_name, family_name, genus


#print(get_json_response("snake_plant.jpg", "leaf"))