import requests

from config import TREFLE_API_BASE_URL
import os


def get_plant_info(plant_name):
    """Fetches plant information from the Trefle API"""
    url = f"{TREFLE_API_BASE_URL}/plants/search?q={plant_name}&token={os.environ.get('TREFLE_TOKEN')}"
    response = requests.get(url)
    print(response)

    if response.status_code != 200:
        print(f"no plant found, status code: {response.status_code}, response: {response.content}")
        return None

    # List of desired fields
    desired_fields = ["common_name", "scientific_name", "growth.light", "growth.water", "growth.temperature",
                      "growth.humidity", "growth.growing_days", "propagation", "pests", "image_url"]

    # Find record with highest score
    max_score = 0
    max_score_data = None
    for data in response.json()["data"]:
        score = 0
        for field in desired_fields:
            if data.get(field):
                score += 1
        if score > max_score:
            max_score = score
            max_score_data = data

    if not max_score_data:
        print(f"no matching plant found")
        return None

    # Extract fields from highest score data
    plant = {
        "common_name": max_score_data.get("common_name"),
        "scientific_name": max_score_data.get("scientific_name"),
        "sunlight_care": max_score_data.get("growth.light"),
        "water_care": max_score_data.get("growth.water"),
        "temperature_care": max_score_data.get("growth.temperature"),
        "humidity_care": max_score_data.get("growth.humidity"),
        "growing_tips": max_score_data.get("growth.growing_days"),
        "propagation_tips": max_score_data.get("propagation", {}).get("vegetative", {}).get("cutting", "Unknown"),
        "common_pests": max_score_data.get("observations"),
        "image_url": max_score_data.get("image_url"),
        "family": max_score_data["family"].get("name") if isinstance(max_score_data.get("family"), dict) else None,
        "genus": max_score_data["genus"]["name"] if isinstance(max_score_data.get("genus"), dict) else None,
        "year": max_score_data.get("year"),
        "edible": bool(max_score_data.get("edible")),
        "edible_part": max_score_data.get("edible_part"),
        "edible_notes": max_score_data.get("edible_notes"),
        "medicinal": bool(max_score_data.get("medicinal")),
        "medicinal_notes": max_score_data.get("medicinal_notes"),
        "toxicity": max_score_data.get("toxicity"),
        "synonyms": max_score_data.get("synonyms"),
        "native_status": max_score_data.get("distribution", {}).get("native", "Unknown"),
        "conservation_status": max_score_data["conservation_status"] if isinstance(
            max_score_data.get("conservation_status"), dict) else None,
    }
    return plant
