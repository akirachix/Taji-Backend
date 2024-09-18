import requests
from bs4 import BeautifulSoup
def fetch_table_data(url):
    """
    Fetches table data from a given URL and parses it into a list of dictionaries.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        content_type = response.headers.get('Content-Type')
        print(f"Content-Type from {url}: {content_type}")
        if 'html' not in content_type:
            return f"Unexpected content type: {content_type}"
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')
        if table is None:
            return "No table found in HTML"
        headers = [th.get_text(strip=True) for th in table.find_all('th')]
        rows = table.find_all('tr')
        table_data = []
        for row in rows:
            cells = [td.get_text(strip=True) for td in row.find_all('td')]
            if cells:
                if headers:
                    table_data.append(dict(zip(headers, cells)))
                else:
                    table_data.append(cells)
        print(f"Table data fetched from {url}: {table_data}")
        return table_data
    except requests.RequestException as e:
        return f"An error occurred: {e}"