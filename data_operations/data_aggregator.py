import json
from typing import Any, Dict, List

from scrapers.border_scraper import get_neighbors_for_country
from scrapers.country_info_scraper import CountryScraper



def process_countries(file_path: str) -> List[Dict[str, Any]]:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            countries_data = json.load(file)
    except Exception as e:
        print(f"Failed to load JSON file: {e}")
        return []

    scraper = CountryScraper()
    processed_data = []

    for country in countries_data:
        try:
            name = country.get("name")
            link = country.get("country_link")
            if not name or not link:
                print(f"Invalid entry in JSON: {country}")
                continue

            neighbors = get_neighbors_for_country(name)

            country_info = scraper.scrape_country_info(link)

            processed_data.append({
                "name": name,
                "population": country.get("population", "Unknown"),
                "neighbors": neighbors,
                "additional_info": country_info
            })

            print(f"Processed data for {name}")
        except Exception as e:
            print(f"Failed to process {country}: {e}")

    return processed_data

def save_processed_data(data: List[Dict[str, Any]], output_path: str):
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        print(f"Processed data saved to {output_path}")
    except Exception as e:
        print(f"Failed to save data: {e}")

def main():
    input_file = 'data/countries_data_with_links.json'
    output_file = 'data/processed_country_data_new.json' #fara new inainte
    
    processed_data = process_countries(input_file)
    if processed_data:
        save_processed_data(processed_data, output_file)

if __name__ == "__main__":
    main()
