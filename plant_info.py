from config import TREFLE_API_BASE_URL

import os
import requests

# DESIRED_FIELDS = [
#     'light',
#     'atmospheric_humidity',
#     'ph_minimum',
#     'ph_maximum',
#     'precipitation_minimum',
#     'precipitation_maximum',
#     'temperature_minimum',
#     'temperature_maximum',
#     'soil_humidity_minimum',
#     'soil_humidity_maximum',
#     'soil_nutriments'
# ]

# TREFLE_API_KEY = os.environ.get('TREFLE_TOKEN')
PERENUAL_API_KEY = os.getenv('PERENUAL_API_KEY')


# def get_plant_info(query):
#     query = query.strip().lower()
#
#     # Try fuzzy search first
#     endpoint = f"{TREFLE_API_BASE_URL}/plants?token={TREFLE_API_KEY}&filter[common_name]=*{query}*"
#     response = requests.get(endpoint)
#
#     if response.status_code != 200:
#         print(f"Error searching by fuzzy search: {response.status_code}")
#         return None
#
#     results = response.json().get('data', [])
#     print(f"Response from Trefle API: {response.json()}")
#
#     # If no results are found with fuzzy search, try searching by genus name
#     if not results:
#         endpoint = f"{TREFLE_API_BASE_URL}/plants?token={TREFLE_API_KEY}&filter[genus]={query}"
#         response = requests.get(endpoint)
#
#         if response.status_code != 200:
#             print(f"Error searching by genus name: {response.status_code}")
#             return None
#
#         results = response.json().get('data', [])
#
#     if not results:
#         print("No results found")
#         return None
#
# # Sort the results by the number of desired fields present in the result sorted_results = sorted(results,
# key=lambda x: -sum([1 for field in DESIRED_FIELDS if (field in x and x[field]) or ( field == 'images' and x.get(
# 'images', {}).get('url')) or ('care' in str( x.get('main_species', {})).lower())]))
#
#     best_matching_plant = sorted_results[0]
#     plant_id = best_matching_plant['id']
#
#     # Fetch the detailed information for the best matching plant
#     detailed_endpoint = f"{TREFLE_API_BASE_URL}/plants/{plant_id}?token={TREFLE_API_KEY}"
#     detailed_response = requests.get(detailed_endpoint)
#
#     if detailed_response.status_code != 200:
#         print(f"Error fetching plant details: {detailed_response.status_code}")
#         return None
#
#     detailed_plant_info = detailed_response.json().get('data', {})
#
#     # Extract only the desired fields from the detailed plant information
#     extracted_info = {field: detailed_plant_info.get(field) for field in DESIRED_FIELDS}
#
#     # Convert the min/max values for certain fields to a tuple
#     extracted_info['ph'] = (extracted_info.pop('ph_minimum'), extracted_info.pop('ph_maximum'))
#     extracted_info['precipitations'] = (
#         extracted_info.pop('precipitation_minimum'), extracted_info.pop('precipitation_maximum'))
#     extracted_info['temperature'] = (
#         extracted_info.pop('temperature_minimum'), extracted_info.pop('temperature_maximum'))
#     extracted_info['soil_humidity'] = (
#         extracted_info.pop('soil_humidity_minimum'), extracted_info.pop('soil_humidity_maximum'))
#
#     return extracted_info
def get_plant_info(query):
    query = query.strip().lower()

    # Search by common name
    url = f'https://api.perenual.com/plants/search?api_key={PERENUAL_API_KEY}&q={query}'
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error searching by common name: {response.status_code}")
        return None

    results = response.json()

    if not results:
        print("No results found")
        return None

    # Choose the first result
    first_result = results[0]

    # Map the Perenual API fields to the desired schema
    extracted_info = {
        'common_name': first_result['common_name'],
        'scientific_name': first_result['scientific_name'],
        'other_names': first_result['other_names'] or None,
        'cycle': first_result['cycle'],
        'image_url': first_result['default_image.original_url'],
        'sunlight_care': first_result['sunlight'],
        'water_care': first_result['watering']
    }

    if detailed:
        plant_id = first_result['id']
        detail_url = f'https://perenual.com/api/species/details/{plant_id}/?key={PERENUAL_API_KEY}'
        detail_response = requests.get(detail_url)

        if detail_response.status_code != 200:
            print(f"Error fetching detailed information: {detail_response.status_code}")
            return extracted_info

        detail_result = detail_response.json()

        # add detailed information to the extracted_info dictionary
        extracted_info.update({
            'family': detail_result['family'],
            'origin': detail_result['origin'],
            'type': detail_result['type'],
            'dimension': detail_result['dimension'],
            'propagation': detail_result['propagation'],
            'hardiness': detail_result['hardiness'],
            'maintenance': detail_result['maintenance'],
            'soil': detail_result['soil'],
            'growth_rate': detail_result['growth_rate'],
            'drought_tolerant': detail_result['drought_tolerant'],
            'salt_tolerant': detail_result['salt_tolerant'],
            'pest_susceptibility': detail_result['pest_susceptibility'],
            'flowering_season': detail_result['flowering_season'],
            'flower_color': detail_result['flower_color'],
            'leaf_color': detail_result['leaf_color'],
            # add more fields as needed - some are "coming soon" in the API broker
        })

    return extracted_info
