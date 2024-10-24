import os
import sys
from datetime import datetime
import logging
import requests
from bs4 import BeautifulSoup
from django.utils import timezone

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bheta_solution.settings")

import django
django.setup()

from recall_drugs.models import PPBData

log_file_path = os.path.join(project_root, 'recall_drugs', 'scraper.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO)

urls = [
    'https://web.pharmacyboardkenya.org/Product%20recalled%202024/',
    'https://web.pharmacyboardkenya.org/product-recall-2023/',
    'https://web.pharmacyboardkenya.org/products-recalled-in-2022/',
    'https://web.pharmacyboardkenya.org/products-recalled-in-2021/',
    'https://web.pharmacyboardkenya.org/products-recalled-in-2020/',
    'https://web.pharmacyboardkenya.org/products-recalled-in-2019/',
    'https://web.pharmacyboardkenya.org/products-recalled-in-2018/',
    'https://web.pharmacyboardkenya.org/products-recalled-in-2017/',
    'https://web.pharmacyboardkenya.org/products-recalled-in-2016/'
]

def parse_date(date_str):
    try:
        cleaned_date = date_str.split('.')[-1].strip() if '.' in date_str else date_str.strip()
        return datetime.strptime(cleaned_date, '%d/%m/%Y').date()
    except ValueError as e:
        logging.error(f"Date parsing error for {date_str}: {str(e)}")
        return None

def clean_text(text):
    return text.strip() if text else ""

def scrape_and_save():
    for url in urls:
        try:
            logging.info(f"Processing URL: {url}")
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            table = soup.find('table')
            
            if table:
                rows = table.find_all('tr')[1:]  
                for row in rows:
                    cols = row.find_all('td')
                    
                    logging.info("Raw row data: " + " | ".join([col.text.strip() for col in cols]))
                    
                    if len(cols) >= 8:
                        try:
                          
                            date_str = clean_text(cols[1].text)
                            recall_date = parse_date(date_str)
                            
                            if not recall_date:
                                logging.error(f"Invalid date format: {date_str}")
                                continue

                            data = {
                                'recall_date': recall_date,
                                'recall_reference_number': clean_text(cols[2].text), 
                                'product_name': clean_text(cols[3].text),             
                                'inn_name': clean_text(cols[4].text),                 
                                'batch_number': clean_text(cols[5].text),            
                                'manufacturer_name': clean_text(cols[6].text),       
                                'recall_reason': clean_text(cols[7].text),           
                                'status': 'recalled'
                            }

                           
                            logging.info("Mapped data:")
                            for key, value in data.items():
                                logging.info(f"{key}: {value}")

                        
                            existing = PPBData.objects.filter(
                                batch_number=data['batch_number'],
                                recall_reference_number=data['recall_reference_number']
                            ).first()

                            if not existing:
                                new_record = PPBData.objects.create(**data)
                                logging.info(f"Created new record: {new_record}")
                            else:
                                logging.info(f"Record exists: {data['product_name']} - {data['batch_number']}")

                        except Exception as e:
                            logging.error(f"Error processing row: {str(e)}")
                            continue

        except Exception as e:
            logging.error(f"Error processing URL {url}: {str(e)}")
            continue

def run_scraper():
    start_time = timezone.now()
    logging.info(f"Scraper started at {start_time}")
    
    try:
              
        scrape_and_save()
        logging.info(f"Scraper completed successfully at {timezone.now()}")
    except Exception as e:
        logging.error(f"Error occurred while scraping: {str(e)}")
        
    end_time = timezone.now()
    duration = end_time - start_time
    logging.info(f"Scraper run duration: {duration}")

if __name__ == "__main__":
    run_scraper()