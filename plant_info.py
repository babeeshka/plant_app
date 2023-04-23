import requests
from models import Plant
from config import TREFLE_API_BASE_URL
import os


def get_plant_info(plant_name):
    """Fetches plant information from the Trefle API"""
    url = f"{TREFLE_API_BASE_URL}/plants/search?q={plant_name}&token={os.environ.get('TREFLE_TOKEN')}"
    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()["data"][0]
    plant = {
        "common_name": data.get("common_name"),
        "scientific_name": data.get("scientific_name"),
        "sunlight_care": data.get("growth.light"),
        "water_care": data.get("growth.water"),
        "temperature_care": data.get("growth.temperature"),
        "humidity_care": data.get("growth.humidity"),
        "growing_tips": data.get("growth.growing_days"),
        "propagation_tips": data.get("propagation"),
        "common_pests": data.get("pests"),
        "image_url": data.get("image_url"),
        "family": data["family"].get("name") if isinstance(data.get("family"), dict) else None,
        "genus": data["genus"]["name"] if isinstance(data.get("genus"), dict) else None,
        "year": data.get("year"),
        "edible": data.get("edible") == True,
        "edible_part": data.get("edible_part"),
        "edible_notes": data.get("edible_notes"),
        "medicinal": data.get("medicinal") == True,
        "medicinal_notes": data.get("medicinal_notes"),
        "toxicity": data.get("toxicity"),
        "synonyms": data.get("synonyms"),
        "native_status": data.get("distribution", {}).get("native", "Unknown"),
        "conservation_status": data["conservation_status"] if isinstance(data.get("conservation_status"), dict) else None,
    }
    return plant
