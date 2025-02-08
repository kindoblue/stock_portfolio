import yfinance as yf

def get_current_price(symbol):
    """Get the current price for a stock symbol."""
    try:
        # Validate symbol format
        symbol = symbol.strip().upper()
        if not symbol:
            raise ValueError("Empty stock symbol")
        
        stock = yf.Ticker(symbol)
        info = stock.info
        
        # Try different possible price keys
        price = None
        for price_key in ['currentPrice', 'regularMarketPrice', 'price', 'previousClose']:
            if price_key in info and info[price_key] is not None:
                price = info[price_key]
                break
        
        if price is None:
            raise ValueError(f"No price data available for symbol '{symbol}'. Please verify the symbol is correct.")
        
        return price
    except Exception as e:
        error_msg = str(e)
        print(f"Error fetching price for {symbol}: {error_msg}")
        return None 