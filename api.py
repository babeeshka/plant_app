import requests
import os

TREFLE_TOKEN = os.environ.get('TREFLE_TOKEN')

def api_call(plant_name):
    token = os.environ.get('TREFLE_TOKEN')
    url = f"https://trefle.io/api/v1/plants/search?q={plant_name}&token={token}"
    response = requests.get(url)
    return response.json()
