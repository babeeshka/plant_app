from config import TREFLE_API_BASE_URL

import os
import requests

DESIRED_FIELDS = [
    'id', 'common_name', 'scientific_name', 'family_common_name', 'bibliography', 'author', 'year', 'family',
    'genus', 'duration', 'growth_habit', 'growth_rate', 'edible', 'vegetable', 'observations',
    'flower_color', 'images'
]


def get_plant_info(query):
    query = query.strip().lower()

    # Try searching by common name first
    endpoint = f"{TREFLE_API_BASE_URL}/plants&token={os.environ.get('TREFLE_TOKEN')}&filter[common_name]={query}"
    response = requests.get(endpoint)

    if response.status_code != 200:
        return None

    results = response.json().get('data', [])

    # If no results are found with common name search, try searching by scientific name
    if not results:
        endpoint = f"{TREFLE_API_BASE_URL}/plants&token={os.environ.get('TREFLE_TOKEN')}&filter[scientific_name]={query}"
        response = requests.get(endpoint)

        if response.status_code != 200:
            return None

        results = response.json().get('data', [])

    if not results:
        return None

    # Sort the results by the number of desired fields present in the result
    sorted_results = sorted(results, key=lambda x: -sum([1 for field in DESIRED_FIELDS if (field in x and x[field]) or (
            field == 'images' and x.get('images', {}).get('url'))]))

    best_matching_plant = sorted_results[0]
    plant_id = best_matching_plant['id']

    # Fetch the detailed information for the best matching plant
    detailed_endpoint = f"{TREFLE_API_BASE_URL}/plants/{plant_id}?token={os.environ.get('TREFLE_TOKEN')}"
    detailed_response = requests.get(detailed_endpoint)

    if detailed_response.status_code != 200:
        return None

    detailed_plant_info = detailed_response.json().get('data', {})

    # Extract only the desired fields from the detailed plant information
    extracted_info = {field: detailed_plant_info.get(field) for field in DESIRED_FIELDS}

    # Extract the image URL from the images object
    images = extracted_info.get('images')
    if images and 'url' in images:
        extracted_info['image_url'] = images['url']
    else:
        extracted_info['image_url'] = None
    del extracted_info['images']

    # Convert the durations list into a comma-separated string
    durations = extracted_info.get('durations')
    if durations:
        extracted_info['durations'] = ', '.join(durations)
    else:
        extracted_info['durations'] = None

    return extracted_info
