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
        print(url)
        return None

    results = response.json()

    if not results or not results['data']:
        print("No results found")
        return None

    extracted_info = []
    for result in results['data']:
        info = {
            'id': result['id'],
            'common_name': result['common_name'],
            'scientific_name': ', '.join(result.get('scientific_name', [])),
            'other_name': ', '.join(result.get('other_name', [])),
            'cycle': result['cycle'],
            'watering': result['watering'],
            'sunlight': ', '.join(result.get('sunlight', [])),
            'default_image': result['default_image']['regular_url'],
        }

        if get_detailed_info:
            detail_url = f'https://perenual.com/api/species/details/{result["id"]}/?key={PERENUAL_API_KEY}'
            detail_response = requests.get(detail_url)

            if detail_response.status_code == 200:
                detail_result = detail_response.json()
                info.update({
                    'family': detail_result['family'],
                    'origin': ', '.join(detail_result.get('origin', [])),
                    'soil': ', '.join(detail_result.get('soil', [])),
                    'pest_susceptibility': ', '.join(detail_result.get('pest_susceptibility', [])),
                    'type': detail_result['type'],
                    'dimension': detail_result['dimension'],
                    'propagation': detail_result['propagation'],
                    'hardiness': detail_result['hardiness'],
                    'leaf_color': ', '.join(detail_result.get('leaf_color', [])),
                    'maintenance': detail_result['maintenance'],
                    'growth_rate': detail_result['growth_rate'],
                    'drought_tolerant': detail_result['drought_tolerant'],
                    'salt_tolerant': detail_result['salt_tolerant'],
                    'flowering_season': detail_result['flowering_season'],
                    'flower_color': detail_result['flower_color'],
                })

        extracted_info.append(info)

    return extracted_info
