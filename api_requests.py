
import requests
import json
from pprint import pprint
import config

api_endpoint = f"https://my-api.plantnet.org/v2/identify/all?api-key={config.API_KEY}"

image_path_1 = "static/user_uploads/snake_plant.jpg"
#image_data_1 = open(image_path_1, 'rb')


#data = {
	#	'organs': ['leaf']
#}

#files = [
	#	('images', (image_path_1, image_data_1))
#]

#req = requests.Request('POST', url=api_endpoint, files=files, data=data)
#prepared = req.prepare()

#s = requests.Session()
#response = s.send(prepared)
#json_result = json.loads(response.text)

#pprint(response.status_code)
#pprint(json_result)





plant_name = test_json["bestMatch"]
pictures_uploaded = test_json["query"]["organs"]
common_name = test_json["results"][2]["species"]["commonNames"]
family_name = test_json["results"][2]["species"]["family"]["scientificName"]
genus = test_json["results"][2]["species"]["genus"]["scientificName"]

print(plant_name, pictures_uploaded, common_name, family_name, genus)