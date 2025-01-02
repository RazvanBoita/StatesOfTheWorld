import json

def clean_number(number_str):
    if not number_str:
        return None
    cleaned = str(number_str).replace(',', '')
    try:
        float(cleaned)
        return cleaned
    except ValueError:
        return None

def process_json_file():
    with open('data/processed_country_data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    cleaned_data = []
    
    for country in data:
        population = clean_number(country.get('population'))
        
        add_info = country.get('additional_info', {})
        area = clean_number(add_info.get('Area'))
        density = clean_number(add_info.get('Density'))
        
        if not all([population, area, density]):
            print(f"Skipping {country['name']} due to missing or invalid numerical data")
            continue
        
        country['population'] = population
        add_info['Area'] = area
        add_info['Density'] = density
        
        capital_name = add_info.get('Capital Name')
        if capital_name and 'city-state' in capital_name.lower():
            add_info['Capital Name'] = country['name']
        
        cleaned_data.append(country)
    
    with open('data/final_data.json', 'w', encoding='utf-8') as file:
        json.dump(cleaned_data, file, indent=4, ensure_ascii=False)
    
    print(f"Processed {len(data)} countries, kept {len(cleaned_data)} countries")
    return cleaned_data

if __name__ == "__main__":
    cleaned_data = process_json_file()