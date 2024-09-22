import requests

def geocode_address(address, api_key):
    endpoint = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
    response = requests.get(endpoint)
    if response.status_code == 200:
        results = response.json().get('results')
        if results:
            location = results[0]['geometry']['location']
            return location['lat'], location['lng']
        else:
            return None, None  
    else:
        raise Exception(f"Error with Google Maps API: {response.status_code}")
