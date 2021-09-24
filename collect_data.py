import sys
import os
from bs4 import BeautifulSoup
from datetime import datetime
import requests
from constants import *
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
        - raw_united_states.csv
        - raw_movies.csv
        - raw_actors.csv
    - json_files
        - raw_countries.json
        - raw_cities.json
        - raw_capital_cities.json
        - raw_landmarks.json
        - raw_united_states.json
        - raw_movies.json
        - raw_actors.json
    
Usage:   python collect_data.py <base_dir>
Example: python collect_data.py C:/buzzle_app/buzzle-db/raw_data
"""


def collect_countries():
    url = COUNTRIES_URL
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


def collect_united_states():
    url = UNITED_STATES_URL
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html5lib')
    united_state = []

    return united_states


def DownloadFlags(base_dir: str):
    url = COUNTRY_FLAGS_URL
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html5lib')
    target_folder = os.path.join(base_dir, 'images', 'flags')

    country_flags = []
    main_div = soup.find('div', attrs={'class': 'content-inner'})
    country_divs = main_div.findAll('div', attrs={'class': 'col-md-4'})

    for country_div in country_divs:
        country_name = country_div.text
        flag_url = country_div.find('a').attrs['href']
        full_flag_url = '/'.join([MAIN_URL, flag_url])
        country_flags.append([country_name, full_flag_url])

        print(f'Downloading file {full_flag_url}')
        r = requests.get(full_flag_url)
        with open(os.path.join(target_folder, country_name) + '.gif', 'wb') as writer:
            writer.write(r.content)


def create_directories(base_dir: str):
    os.makedirs(os.path.join(base_dir, 'csv_files'), exist_ok=True)
    os.makedirs(os.path.join(base_dir, 'json_files'), exist_ok=True)
    os.makedirs(os.path.join(base_dir, 'images/flags'), exist_ok=True)
    os.makedirs(os.path.join(base_dir, 'images/landmarks'), exist_ok=True)


if __name__ == '__main__':
    base_dir = sys.argv[1]

    if not os.path.exists(base_dir):
        print(f'Error: no such folder {base_dir}')
        exit(1)

    print('Creating directories')
    create_directories(base_dir)

    now_date = datetime.now()

    # DownloadFlags(base_dir)

    # Collect countries
    try:
        print('Collecting countries')
        countries = collect_countries()
        write_to_json('countries', countries, os.path.join(base_dir, 'json_files', 'raw_countries.json'))
        write_to_csv(countries, os.path.join(base_dir, 'csv_files', 'raw_countries.csv'))
    except Exception as ex:
        print(f'Exception was occurred: {ex}')
        exit(1)

    # Collect united states
    try:
        print('Collecting united states')
        united_states = collect_united_states()
        write_to_json('united_states', united_states, os.path.join(base_dir, 'json_files', 'raw_united_states.json'))
        write_to_csv(united_states, os.path.join(base_dir, 'csv_files', 'raw_united_states.csv'))
    except Exception as ex:
        print(f'Exception was occurred: {ex}')
        exit(1)

    print('Countries file created.')
