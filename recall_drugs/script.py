import os
import sys
import django
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging
from django.utils import timezone


sys.path.append('/home/studen/Documents/Taji-Backend/bheta_solution/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bheta_solution.settings")
django.setup()

from recall_drugs.models import PPBData


logging.basicConfig(filename='/home/studen/Documents/Taji-Backend/bheta_solution/recall_drugs/cron.log', level=logging.INFO)

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

def scrape_and_save():
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        year = int(url.rstrip('/').split('/')[-1][-4:])
        
        table = soup.find('table')
        if table:
            rows = table.find_all('tr')[1:]
            
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 5:
                    product_name = cols[0].text.strip()
                    batch_number = cols[1].text.strip()
                    inn_name = cols[2].text.strip()
                    manufacturer_name = cols[3].text.strip() 
                    recall_reason = cols[4].text.strip() 
                    recall_date = datetime.now().date()
                    recall_reference_number = ''
                    
                    if not PPBData.objects.filter(batch_number=batch_number).exists():
                        PPBData.objects.create(
                            recall_date=recall_date,
                            recall_reference_number=recall_reference_number,
                            product_name=product_name,
                            inn_name=inn_name,
                            batch_number=batch_number,
                            manufacturer_name=manufacturer_name,
                            recall_reason=recall_reason,
                            status='recalled'
                        )
                        logging.info(f"Saved: {product_name} - {batch_number}")
                    else:
                        logging.info(f"Already exists: {product_name} - {batch_number}")

    logging.info(f"Scraping completed at {datetime.now()}")

    saved_data = PPBData.objects.all()
    for data in saved_data:
        logging.info(str(data))

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