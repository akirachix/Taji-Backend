from .utils import fetch_table_data
from .models import PPBData
from django.utils.dateparse import parse_date
from django.db import transaction
def get_data_from_ppb():
    """
    Fetches and processes table data from multiple URLs and saves the data to the database.
    """
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
    for url in urls:
        print(f"Fetching data from {url}")
        data = fetch_table_data(url)
        if isinstance(data, list) and data:
            with transaction.atomic():  # Use transaction for batch operations
                for item in data:
                    if isinstance(item, dict):
                        recall_date = parse_date(item.get('Recall Date'))  # Parse date
                        drug_name = item.get('Drug Name')
                        scientific_name = item.get('Scientific Name')
                        batch_number = item.get('Batch Number(s)')
                        manufacturer_name = item.get('Name of Manufacturer')
                        recall_reason = item.get('Reasons for recall')
                        # Add a check to avoid duplicates (optional)
                        if not PPBData.objects.filter(recall_date=recall_date, drug_name=drug_name).exists():
                            print(f"Saving to database: {recall_date}, {drug_name}, {scientific_name}, {batch_number}, {manufacturer_name}, {recall_reason}")
                            PPBData.objects.create(
                                recall_date=recall_date,
                                drug_name=drug_name,
                                scientific_name=scientific_name,
                                batch_number=batch_number,
                                manufacturer_name=manufacturer_name,
                                recall_reason=recall_reason,
                            )
                        else:
                            print(f"Duplicate entry found for {drug_name} on {recall_date}. Skipping.")
                    else:
                        print(f"Unexpected data format: {item}")
        else:
            print(f"Error or no data found for {url}: {data}")