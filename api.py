import requests

def fetch_exchange_rates(base_currency): # Get a dictionary if exchange rates
    url = f"https://open.er-api.com/v6/latest/{base_currency}"
    rates = requests.get(url)
    if rates.status_code == 200:
        return rates.json() # Return dictionary
    else:
        raise Exception("Failed to fetch exchange rates.")