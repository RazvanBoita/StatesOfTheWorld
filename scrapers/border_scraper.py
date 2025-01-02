import requests
from bs4 import BeautifulSoup
from typing import List, Dict

def get_countries_and_neighbors() -> Dict[str, List[str]]:
    url = "https://en.wikipedia.org/wiki/List_of_countries_and_territories_by_number_of_land_borders"
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        table = soup.find('table', class_='wikitable sortable')
        if not table:
            print("Table not found")
            return {}

        tbody = table.find('tbody')
        if not tbody:
            print("Tbody not found")
            return {}

        rows = tbody.find_all('tr')
        country_neighbors = {}

        for row in rows[1:]:
            tds = row.find_all('td')
            if len(tds) >= 6:
                first_td = tds[0]
                country_a_tag = first_td.find('a')

                last_td = tds[5]
                neighbor_a_tags = last_td.find_all('a')

                if country_a_tag:
                    country = country_a_tag.get_text().strip()
                    neighbors = [a.get_text().strip() for a in neighbor_a_tags]

                    neighbors = [neighbor for neighbor in neighbors if neighbor and "[" not in neighbor and "]" not in neighbor]

                    country_neighbors[country] = neighbors

        return country_neighbors

    except Exception as e:
        print(f"An error occurred while fetching country data: {e}")
        return {}

def get_neighbors_for_country(country_name: str) -> List[str]:
    try:
        country_neighbors = get_countries_and_neighbors()
        if country_name not in country_neighbors:
            print(f"Country '{country_name}' not found on the land borders wiki page, defaulting to no neighbors.")
            return []
        return country_neighbors.get(country_name, [])
    except Exception as e:
        print(f"An error occurred while fetching neighbors for {country_name}: {e}")
        return []

# if __name__ == "__main__":
#     country_name = "Tuvalu"
#     neighbors = get_neighbors_for_country(country_name)
#     print(f"Neighbors of {country_name}: {neighbors}")
