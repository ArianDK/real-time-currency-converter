def get_exchange_rate(target_currency, rates): # Get exchange rate for the target currency
        if target_currency in rates["rates"]:
            return rates["rates"][target_currency]
        else:
            raise ValueError(f"Target currency {target_currency} not found in rates.")

def convert_currency(amount, exchange_rate): # Convert the amount of base currency with the exchange rate
    return amount * exchange_rate
