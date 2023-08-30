import requests
import datetime
from environs import Env
from decimal import Decimal

from django.utils import timezone

from stocks.models import Stock


env = Env()
env.read_env()

api_url = "https://twelve-data1.p.rapidapi.com/price"
timediff_const = datetime.timedelta(minutes=10)

def get_realtime_prices(symbols):
    querystring = {"symbol": f"{symbols}", "format": "json", "outputsize": "30"}
    headers = {
        "X-RapidAPI-Key": env.str("X-RapidAPI-Key", default=""),
        "X-RapidAPI-Host": "twelve-data1.p.rapidapi.com",
    }
    
    try:
        response = requests.get(api_url, headers=headers, params=querystring)
        data = response.json()
    except:
        return {}
        
    return data


def update_realtime_prices(symbols):
    now = timezone.now()
    symbol_price_will_updated = []
    
    # Calculate the symbol realtime prices to be updated(more than 10 min)
    for symbol in symbols:
        try:
            stock = Stock.objects.get(symbol=symbol)
            time_diff = now - stock.last_price_date
            if time_diff > timediff_const:
                symbol_price_will_updated.append(stock.symbol)
        except Stock.DoesNotExist:
            print(f"No stock found with symbol {symbol}")
        except Stock.MultipleObjectsReturned:
            print(f"Multiple stocks found with symbol {symbol}, expected only one")
            
    # Do nothing if no stock price to update
    if not symbol_price_will_updated:
        return
    
    # Calculate to stock symbols as string for the REST API
    symbols_string = ""
    for symbol in symbol_price_will_updated:
        symbols_string += symbol + ", "
    
    # Update the model with the realtime stock prices
    try:    
        realtime_prices = get_realtime_prices(symbols_string)
        for symbol in realtime_prices:
            try:
                price = realtime_prices[symbol]['price']
                stock = Stock.objects.get(symbol=symbol)
                stock.last_price = Decimal(price)
                stock.save()
            except:
                # If there is an error, update the price with existing one so we 
                # don't request the price from API everytime
                try:
                    stock = Stock.objects.get(symbol=symbol)
                    stock.last_price = stock.last_price
                    stock.save()
                except:
                    pass
    except:
        print("Error while fetching the realtime prices from the API")