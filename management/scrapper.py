import requests
import json

address_ids = [
    "R4583217",
    "R4583216",
    "R4583212",
    "R4583211",
    "R4583221",
    "R4583213",
    "R4583223",
]

def scrapper():
    all_cities = []
    for each in address_ids:
        url = f'https://member.daraz.com.np/locationtree/api/getSubAddressList?countryCode=NP&addressId={each}&page=addressEdit'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for item in data['module']:
                all_cities.append({
                    "name": item['name'],
                    "id": item['id']
                })
        else:
            print(f"Failed to fetch {each}, status code: {response.status_code}")
    return all_cities


def fetch_areas():
    all_areas = []
    all_cities = scrapper()
    for each in all_cities:
        city_id = each['id']
        city = each['name']
        url = f'https://member.daraz.com.np/locationtree/api/getSubAddressList?countryCode=NP&addressId={city_id}&page=addressEdit'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for area in data['module']:
                all_areas.append({'city': city, 'area': area['name']})

    return all_areas

output = fetch_areas()
with open('all_areas.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=4, ensure_ascii=False)
