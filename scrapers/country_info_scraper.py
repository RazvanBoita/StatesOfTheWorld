import requests
from bs4 import BeautifulSoup
import re
from typing import Optional, Dict, List


class TextCleaner:
    @staticmethod
    def clean_text(text: Optional[str]) -> Optional[str]:
        if text:
            text = re.sub(r'\[.*?\]', '', text).strip()
            text = re.sub(r'\(.*?\)', '', text).strip()
            text = re.sub(r'\s+', ' ', text)
            return text
        return None


class WikiInfoboxParser:
    def __init__(self, infobox: BeautifulSoup):
        self.infobox = infobox

    def _find_row_by_terms(
        self,
        terms: List[str],
        tag: str = 'th',
        class_name: Optional[str] = None
    ) -> Optional[BeautifulSoup]:
        rows = self.infobox.find_all(tag, class_=class_name)
        for row in rows:
            full_text = row.get_text(strip=True).replace('\xa0', ' ')
            for term in terms:
                if re.search(term, full_text, re.IGNORECASE):
                    return row
        return None

    def extract_capital(self) -> Optional[str]:
        capital_terms = ['Capital', 'Capital city', 'Capital and largest city']
        capital_row = self._find_row_by_terms(
            capital_terms,
            'th',
            'infobox-label'
        )

        if capital_row:
            capital_cell = capital_row.find_next('td', class_='infobox-data')
            if capital_cell and (capital_link := capital_cell.find('a')):
                return TextCleaner.clean_text(capital_link.get_text())
        return None

    def extract_timezone(self) -> Optional[str]:
        timezone_terms = [r'Time Zone']
        for term in timezone_terms:
            timezone_row = self.infobox.find(
                'th', string=re.compile(term, re.IGNORECASE))
            if timezone_row:
                timezone_cell = timezone_row.find_next('td')
                timezone = TextCleaner.clean_text(timezone_cell.get_text())
                return timezone
        return None

    def extract_government(self) -> Optional[str]:
        government_terms = [r'Government',
                            r'Government type', r'Government Form']
        for term in government_terms:
            government_row = self.infobox.find(
                'th', string=re.compile(term, re.IGNORECASE))
            if government_row:
                government_cell = government_row.find_next('td')
                government = TextCleaner.clean_text(government_cell.get_text())
                return government
        return None

    def extract_area(self) -> Optional[str]:
        total_div = self.infobox.find(
            'div',
            class_='ib-country-fake-li',
            string=re.compile(r'Total', re.IGNORECASE)
        )

        if not total_div:
            return None

        total_td = total_div.find_next('td')
        if not total_td:
            return None

        raw_text = ''.join(total_td.stripped_strings)

        if km_area := re.search(r'([\d,]+(?:\.\d+)?)\s*km²?', raw_text):
            return km_area.group(1).replace(',', '')

        if mi_area := re.search(r'([\d,]+(?:\.\d+)?)\s*sq\s*mi', raw_text):
            mi_value = float(mi_area.group(1).replace(',', ''))
            km_value = mi_value * 2.58999
            return f"{km_value:,.2f}".rstrip('0').rstrip('.')

        return raw_text

    def extract_density(self) -> Optional[str]:
        density_div = self.infobox.find(
            'div',
            class_='ib-country-fake-li',
            string=re.compile(r'Density', re.IGNORECASE)
        )

        if not density_div:
            return None

        density_td = density_div.find_next('td')
        if not density_td:
            return None

        raw_text = ''.join(density_td.stripped_strings)

        km_pattern = (
            r'([\d,.]+)(?:\[[\d\w]+\])?(?:\s*\/\s*km2|\s*\/\s*km²)'
        )
        if km_match := re.search(km_pattern, raw_text, re.IGNORECASE):
            value = float(km_match.group(1).replace(',', '.'))
            return f"{value:.1f}"

        mi_pattern = r'([\d,.]+)(?:\[[\d\w]+\])?(?:\s*\/\s*sq\s*mi)'
        if mi_match := re.search(mi_pattern, raw_text, re.IGNORECASE):
            mi_value = float(mi_match.group(1).replace(',', '.'))
            km_value = mi_value * 0.386102
            return f"{km_value:.1f}"

        return None

    def extract_spoken_language(self) -> Optional[str]:
        language_row = self._find_row_by_terms(
            ['Official language', 'Official languages'],
            'th',
            'infobox-label'
        )
        if language_row:
            language_cell = language_row.find_next('td', class_='infobox-data')
            if language_cell:
                languages = TextCleaner.clean_text(language_cell.get_text())
                text = re.sub(r'(?<=[a-zA-Z])(?=[A-Z])', ', ', languages)
                return text.strip()
        return None


class CountryScraper:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0'}

    def scrape_country_info(self, url: str) -> Dict[str, str]:
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            infobox = soup.find('table', class_='infobox')

            if not infobox:
                return {"error": "Infobox not found"}

            parser = WikiInfoboxParser(infobox)
            country_info = {
                'Capital Name': parser.extract_capital(),
                'Timezone': parser.extract_timezone(),
                'Government': parser.extract_government(),
                'Area': parser.extract_area(),
                'Spoken Language': parser.extract_spoken_language(),
                'Density': parser.extract_density()
            }

            return {k: v for k, v in country_info.items() if v is not None}

        except requests.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}
        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}


def main():
    urls = [
        "https://en.wikipedia.org/wiki/Singapore",
        "https://en.wikipedia.org/wiki/Vietnam",
        "https://en.wikipedia.org/wiki/Bulgaria",
        "https://en.wikipedia.org/wiki/United_States",
        "https://en.wikipedia.org/wiki/Liberia",
        "https://en.wikipedia.org/wiki/Myanmar"
    ]

    scraper = CountryScraper()
    for url in urls:
        print(f"Scraping {url}:")
        result = scraper.scrape_country_info(url)
        for key, value in result.items():
            print(f"{key}: {value}")
        print("\n")


# if __name__ == "__main__":
#     main()
