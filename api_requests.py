import config
import requests
import json
from pprint import pprint





sample_image_="https://www.gardeningknowhow.com/wp-content/uploads/2012/03/houseplant-sansevieria.jpg" #snake plant

api_endpoint = api_endpoint = f"https://my-api.plantnet.org/v2/identify/all?api-key={config.API_KEY}"



#opening the sample image in binary
image_data_1 = open(sample_image_, 'rb')

image_path_2 = "../data/image_2.jpeg"

data = {
		'organs': ['leaf']
}

files = [
		('images', (image_path_1, image_data_1))
]

req = requests.Request('POST', url=api_endpoint, files=files, data=data)
prepared = req.prepare()

s = requests.Session()
response = s.send(prepared)
json_result = json.loads(response.text)

pprint(response.status_code)
pprint(json_result)
						