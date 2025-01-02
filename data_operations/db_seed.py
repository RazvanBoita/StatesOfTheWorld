import json
import sqlite3
from typing import List, Dict

def create_tables(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS countries (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,
    population INTEGER,  
    capital TEXT,
    timezone TEXT,
    government TEXT,
    area REAL,           
    spoken_language TEXT,
    density REAL          
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS neighbors (
        country_id INTEGER,
        neighbor TEXT,
        FOREIGN KEY (country_id) REFERENCES countries (id)
    )''')

def get_safe_value(dict_obj, *keys):
    """Safely get value from dictionary with multiple possible keys"""
    for key in keys:
        if key in dict_obj:
            return dict_obj[key]
    return None

def import_data(data: List[Dict], db_path: str = 'countries.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    create_tables(cursor)
    
    for country in data:
        additional = country.get('additional_info', {})
        cursor.execute('''
        INSERT INTO countries (name, population, capital, timezone, government, 
                            area, spoken_language, density)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            country.get('name'),
            int(country.get('population', 0)),
            get_safe_value(additional, 'Capital Name', 'Capital'),
            get_safe_value(additional, 'Timezone', 'Time Zone'),
            get_safe_value(additional, 'Government'),
            float(get_safe_value(additional, 'Area', 0)), 
            get_safe_value(additional, 'Spoken Language', 'Spoken Languages', 'Language', 'Languages'),
            float(get_safe_value(additional, 'Density', 0))
        ))
        
        country_id = cursor.lastrowid
        
        for neighbor in country.get('neighbors', []):
            cursor.execute('''
            INSERT INTO neighbors (country_id, neighbor)
            VALUES (?, ?)
            ''', (country_id, neighbor))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    with open('data/final_data.json', 'r') as f:
        data = json.load(f)
    import_data(data)