import yfinance as yf
import yahoo_fin.stock_info as si

# Mapping from company names to stock tickers.
COMPANY_TICKERS = {
    'apple': 'AAPL',
    'google': 'GOOGL',
    'microsoft': 'MSFT',
}

def get_stock_price(company):
    try:
        input_ticker = COMPANY_TICKERS.get(company.lower())
        ticker = yf.Ticker(input_ticker)
        stock_info = ticker.info

        latest_price = stock_info.get('regularMarketPrice')
        if latest_price is None:
            return {"error": "Could not fetch latest stock price"}
        
        return {
            "company": company,
            "ticker": input_ticker,
            "stock_price": latest_price
        }
    return "hi"