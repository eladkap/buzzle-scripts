import sys
import os
from bs4 import BeautifulSoup
import requests
from utils import *

"""
This script collects data from resources (HTML pages, download links)
and creates json and csv files in raw data folder with the following structure:
- raw_data [folder]
    - csv_files
        - raw_countries.csv
        - raw_cities.csv
        - raw_capital_cities.csv
        - raw_landmarks.csv
        - raw_movies.csv
        - raw_actors.csv
    - json_files
        - raw_countries.json
        - raw_cities.json
        - raw_capital_cities.json
        - raw_landmarks.json
        - raw_movies.json
        - raw_actors.json
    
Usage:   python collect_data.py <base_dir>
Example: python collect_data.py C:/buzzle_app/buzzle-db/raw_data
"""


def collect_countries():
    url = 'https://www.worldometers.info/world-population/population-by-country/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html5lib')
    countries = []

    table = soup.find('div', attrs={'class': 'table-responsive'})
    trs = table.findAll('tr')
    first_tr = trs[0]
    column_names = [th.text for th in first_tr.findAll('th')]

    for tr in trs[1:]:
        country = {}
        tds = tr.findAll('td')

        for i, column_name in enumerate(column_names):
            country[column_name] = tds[i].text

        countries.append(country)

    return countries


def create_directories(base_dir: str):
    os.makedirs(os.path.join(base_dir, 'csv_files'), exist_ok=True)
    os.makedirs(os.path.join(base_dir, 'json_files'), exist_ok=True)


if __name__ == '__main__':
    base_dir = sys.argv[1]

    if not os.path.exists(base_dir):
        print(f'Error: no such folder {base_dir}')
        exit(1)

    print('Creating directories')
    create_directories(base_dir)

    # Collect countries
    try:
        print('Collecting countries')
        countries = collect_countries()
        write_to_json('countries', countries, os.path.join(base_dir, 'json_files', 'raw_countries.json'))
        write_to_csv(countries, os.path.join(base_dir, 'csv_files', 'raw_countries.csv'))
    except Exception as ex:
        print(f'Exception was occurred: {ex}')
        exit(1)

    print('Countries file created.')
