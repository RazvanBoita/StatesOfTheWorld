import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin

BASE_URL = "https://en.wikipedia.org"

URL = "https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population"

response = requests.get(URL)
soup = BeautifulSoup(response.content, 'html.parser')

table = soup.find('table', {'class': 'wikitable'})
rows = table.find_all('tr')

countries_data = []

for row in rows[1:]:
    cols = row.find_all('td')
    if cols:
        name_tag = cols[1].find('a')
        if name_tag:
            name = name_tag.text.strip()
            country_link = urljoin(BASE_URL, name_tag['href'])
        else:
            name = cols[1].text.strip()
            country_link = None

        population = cols[2].text.strip()  

        countries_data.append({
            'name': name,
            'population': population,
            'country_link': country_link,
        })

output_file = 'data/countries_data_with_links_new.json' #fara new la inceput
with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(countries_data, file, indent=4, ensure_ascii=False)

print(f"Data has been saved to {output_file}")