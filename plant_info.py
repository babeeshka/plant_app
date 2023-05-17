import os
import requests

PERENUAL_API_KEY = os.getenv('PERENUAL_API_KEY')


def get_plant_info(query, get_detailed_info=False):
    query = query.strip().lower()

    # Search by common name
    url = f'https://perenual.com/api/species-list?key={PERENUAL_API_KEY}&q={query}'
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error searching by common name: {response.status_code}")
        return None

    results = response.json()
    print(results)

    if not results:
        print("No results found")
        return None

    # Choose the first result
    first_result = results['data'][0]

    # Map the Perenual API fields to the desired schema
    extracted_info = {
        'id': first_result['id'],  # Add the plant ID to the extracted_info dictionary
        'common_name': first_result['common_name'],
        'scientific_name': first_result['scientific_name'],
        'other_names': first_result.get('other_names', None),
        'cycle': first_result['cycle'],
        'image_url': first_result['default_image']['original_url'],
        'sunlight_care': first_result['sunlight'],
        'water_care': first_result['watering']
    }

    if get_detailed_info:
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
            'leaf_color': detail_result['leaf_color']
            # add more fields as needed - some are "coming soon" in the API broker
        })

    return extracted_info
