from config import TREFLE_API_BASE_URL

import os
import requests

DESIRED_FIELDS = [
    'light',
    'atmospheric_humidity',
    'ph_minimum',
    'ph_maximum',
    'precipitation_minimum',
    'precipitation_maximum',
    'temperature_minimum',
    'temperature_maximum',
    'soil_humidity_minimum',
    'soil_humidity_maximum',
    'soil_nutriments'
]

TREFLE_API_KEY = os.environ.get('TREFLE_TOKEN')


def get_plant_info(query):
    query = query.strip().lower()

    # Try fuzzy search first
    endpoint = f"{TREFLE_API_BASE_URL}/plants?token={TREFLE_API_KEY}&filter[common_name]=*{query}*"
    response = requests.get(endpoint)

    if response.status_code != 200:
        print(f"Error searching by fuzzy search: {response.status_code}")
        return None

    results = response.json().get('data', [])
    print(f"Response from Trefle API: {response.json()}")

    # If no results are found with fuzzy search, try searching by genus name
    if not results:
        endpoint = f"{TREFLE_API_BASE_URL}/plants?token={TREFLE_API_KEY}&filter[genus]={query}"
        response = requests.get(endpoint)

        if response.status_code != 200:
            print(f"Error searching by genus name: {response.status_code}")
            return None

        results = response.json().get('data', [])

    if not results:
        print("No results found")
        return None

    # Sort the results by the number of desired fields present in the result
    sorted_results = sorted(results, key=lambda x: -sum([1 for field in DESIRED_FIELDS if (field in x and x[field]) or (
            field == 'images' and x.get('images', {}).get('url')) or ('care' in str(
        x.get('main_species', {})).lower())]))

    best_matching_plant = sorted_results[0]
    plant_id = best_matching_plant['id']

    # Fetch the detailed information for the best matching plant
    detailed_endpoint = f"{TREFLE_API_BASE_URL}/plants/{plant_id}?token={TREFLE_API_KEY}"
    detailed_response = requests.get(detailed_endpoint)

    if detailed_response.status_code != 200:
        print(f"Error fetching plant details: {detailed_response.status_code}")
        return None

    detailed_plant_info = detailed_response.json().get('data', {})

    # Extract only the desired fields from the detailed plant information
    extracted_info = {field: detailed_plant_info.get(field) for field in DESIRED_FIELDS}

    # Convert the min/max values for certain fields to a tuple
    extracted_info['ph'] = (extracted_info.pop('ph_minimum'), extracted_info.pop('ph_maximum'))
    extracted_info['precipitations'] = (
    extracted_info.pop('precipitation_minimum'), extracted_info.pop('precipitation_maximum'))
    extracted_info['temperature'] = (
    extracted_info.pop('temperature_minimum'), extracted_info.pop('temperature_maximum'))
    extracted_info['soil_humidity'] = (
    extracted_info.pop('soil_humidity_minimum'), extracted_info.pop('soil_humidity_maximum'))

    return extracted_info

