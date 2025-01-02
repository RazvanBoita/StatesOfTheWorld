import requests
from bs4 import BeautifulSoup
import re


def clean_text(text):
    if text:
        text = re.sub(r'\[.*?\]', '', text).strip()
        text = re.sub(r'\(.*?\)', '', text).strip()
        text = re.sub(r'\s+', ' ', text)
        return text
    return None

def extract_capital(infobox):
    import re
    
    capital_terms = [r'Capital', r'Capital city', r'Capital and largest city']
    capital_rows = infobox.find_all('th', class_='infobox-label')  
    
    for capital_row in capital_rows:
        full_text = capital_row.get_text(strip=True).replace('\xa0', ' ')
        
        for term in capital_terms:
            if re.search(term, full_text, re.IGNORECASE):  
                capital_cell = capital_row.find_next('td', class_='infobox-data')
                if capital_cell:
                    capital_link = capital_cell.find('a')
                    if capital_link:
                        capital = clean_text(capital_link.get_text())
                        return capital
    
    return None


def extract_timezone(infobox):
    timezone_terms = [r'Time Zone']
    for term in timezone_terms:
        timezone_row = infobox.find('th', string=re.compile(term, re.IGNORECASE))
        if timezone_row:
            timezone_cell = timezone_row.find_next('td')
            timezone = clean_text(timezone_cell.get_text())
            return timezone
    return None


def extract_government(infobox):
    government_terms = [r'Government', r'Government type', r'Government Form']
    for term in government_terms:
        government_row = infobox.find('th', string=re.compile(term, re.IGNORECASE))
        if government_row:
            government_cell = government_row.find_next('td')
            government = clean_text(government_cell.get_text())
            return government
    return None


def extract_area(infobox):
    total_div = infobox.find('div', class_='ib-country-fake-li', string=re.compile(r'Total', re.IGNORECASE))
    
    if total_div:
        total_td = total_div.find_next('td')
        if total_td:
            raw_text = ''.join(total_td.stripped_strings)
            
            km_area = re.search(r'([\d,]+)\s*km²?', raw_text)
            mi_area = re.search(r'([\d,]+)\s*sq\s*mi', raw_text)
            
            if km_area:
                return km_area.group(1)
            elif mi_area:
                mi_value = mi_area.group(1).replace(',', '')
                km_value = float(mi_value) * 2.58999
                return f"{round(km_value):,}"  
            
            return raw_text

    return None


def extract_spoken_language(infobox):
    language_terms = [r'Official language', r'Official languages']
    for term in language_terms:
        language_rows = infobox.find_all('th', class_='infobox-label')
        
        for language_row in language_rows:
            full_text = language_row.get_text(strip=True).replace('\xa0', ' ')
            
            if re.search(term, full_text, re.IGNORECASE):
                language_cell = language_row.find_next('td', class_='infobox-data')
                if language_cell:
                    language = clean_text(language_cell.get_text())
                    return language
    
    return None
    

def extract_density(infobox):
    import re

    density_div = infobox.find('div', class_='ib-country-fake-li', string=re.compile(r'Density', re.IGNORECASE))
    
    if density_div:
        density_td = density_div.find_next('td')
        if density_td:
            raw_text = ''.join(density_td.stripped_strings)
            
            km_density = re.search(r'([\d,]+)\s*km²?', raw_text)
            
            if km_density:
                return km_density.group(1)
            
            mi_density = re.search(r'([\d,]+)\s*sq\s*mi', raw_text)
            if mi_density:
                mi_value = mi_density.group(1).replace(',', '') 
                km_value = float(mi_value) * 2.58999  
                return f"{round(km_value, 1)}"

            return raw_text  

    return None


def scrape_country_info(url):
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        country_info = {}
        
        infobox = soup.find('table', class_='infobox')
        if not infobox:
            return {"error": "Infobox not found"}
        
        
        country_info['Capital Name'] = extract_capital(infobox)
        country_info['Timezone'] = extract_timezone(infobox)       
        country_info['Government'] = extract_government(infobox)        
        country_info['Area'] = extract_area(infobox)
        country_info['Spoken Language'] = extract_spoken_language(infobox)
        country_info['Density'] = extract_density(infobox)

        country_info = {k: v for k, v in country_info.items() if v is not None}
        
        return country_info
    
    except requests.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

if __name__ == "__main__":
    urls = [
        "https://en.wikipedia.org/wiki/Romania",
        "https://en.wikipedia.org/wiki/Brazil",
        "https://en.wikipedia.org/wiki/Saint_Kitts_and_Nevis",
        "https://en.wikipedia.org/wiki/United_States",
        "https://en.wikipedia.org/wiki/Liberia",
        "https://en.wikipedia.org/wiki/Myanmar"
    ]
    
    for url in urls:
        print(f"Scraping {url}:")
        result = scrape_country_info(url)
        for key, value in result.items():
            print(f"{key}: {value}")
        print("\n")