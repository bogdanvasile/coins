import requests
import pandas as pd

def fetch_data_from_coincap():
    """Fetch all available coin data from CoinCap API using pagination."""
    url = "https://api.coincap.io/v2/assets"
    print("Fetching coin data from CoinCap API...")
    
    try:
        coins = []
        offset = 0
        limit = 2000
        
        while True:
            response = requests.get(f"{url}?offset={offset}&limit={limit}")
            response.raise_for_status()
            data = response.json()["data"]
            
            if not data:
                break
                
            coins.extend(data)
            offset += limit
            
            if len(data) < limit:
                break
        
        print(f"Successfully fetched data for {len(coins)} coins (using pagination)")
        return coins
    except requests.RequestException as e:
        print(f"Failed to fetch coin data: {str(e)}")
        return []

def fetch_exchange_markets():
    """Fetch all markets (trading pairs) from major exchanges."""
    base_url = "https://api.coincap.io/v2/markets"
    print("Fetching exchange market data...")
    
    try:
        markets = []
        offset = 0
        limit = 2000
        
        while True:
            response = requests.get(f"{base_url}?offset={offset}&limit={limit}")
            response.raise_for_status()
            data = response.json()["data"]
            
            if not data:
                break
                
            markets.extend(data)
            offset += limit
            
            if len(data) < limit:
                break
        
        print(f"Successfully fetched {len(markets)} markets")
        return markets
    except requests.RequestException as e:
        print(f"Failed to fetch market data: {str(e)}")
        return []

def get_exchange_listings(markets):
    """Create a mapping of coins to their exchange listings."""
    coin_listings = {}
    
    for market in markets:
        base_symbol = market.get("baseSymbol", "").upper()
        exchange_id = market.get("exchangeId", "").lower()
        
        if base_symbol and exchange_id:
            if base_symbol not in coin_listings:
                coin_listings[base_symbol] = set()
            coin_listings[base_symbol].add(exchange_id)
    
    return coin_listings

def filter_coins(coins, coin_listings):
    """Filter coins based on the following criteria:
    1. Market Cap > 1M USD 
    2. Daily Volume > 150K USD
    3. Must be listed on at least one Tier-1 OR Tier-2 exchange
    """
    tier_1_exchanges = {"binance", "coinbase", "kraken", "bitfinex", "okex", "bybit"}
    tier_2_exchanges = {"gate.io", "kucoin", "huobi", "bitstamp", "crypto.com"}
    
    filtered_coins = []
    skipped_reasons = {
        "market_cap": 0,
        "volume": 0,
        "exchanges": 0,
        "invalid_data": 0
    }
    
    for coin in coins:
        try:
            # Check for None or empty values first
            market_cap_str = coin.get("marketCapUsd")
            volume_str = coin.get("volumeUsd24Hr")
            symbol = coin.get("symbol", "UNKNOWN").upper()
            
            if market_cap_str is None or market_cap_str == "":
                skipped_reasons["invalid_data"] += 1
                print(f"Skipping {symbol}: Missing market cap data")
                continue
                
            if volume_str is None or volume_str == "":
                skipped_reasons["invalid_data"] += 1
                print(f"Skipping {symbol}: Missing volume data")
                continue
                
            # Convert to float after validating
            market_cap = float(market_cap_str)
            volume = float(volume_str)
            
            # Check market cap
            if market_cap <= 1_000_000:
                skipped_reasons["market_cap"] += 1
                print(f"Skipping {symbol}: Market cap ${market_cap:.2f} below 1M USD threshold")
                continue
                
            # Check volume
            if volume <= 150_000:
                skipped_reasons["volume"] += 1
                print(f"Skipping {symbol}: 24h volume ${volume:.2f} below 150K USD threshold")
                continue
            
            # Check exchange listings
            coin_exchanges = coin_listings.get(symbol, set())
            tier1_count = len(coin_exchanges.intersection(tier_1_exchanges))
            tier2_count = len(coin_exchanges.intersection(tier_2_exchanges))

            # Must be listed on at least one Tier-1 OR Tier-2 exchange
            if tier1_count + tier2_count == 0:
                skipped_reasons["exchanges"] += 1
                print(f"Skipping {symbol}: Not listed on any Tier-1 or Tier-2 exchange")
                continue
            
            filtered_coins.append({
                "Name": coin["name"],
                "Symbol": symbol,
                "Market Cap (USD)": market_cap,
                "24h Volume (USD)": volume,
                "Price (USD)": float(coin["priceUsd"]),
                "Tier 1 Exchanges": tier1_count,
                "Tier 2 Exchanges": tier2_count
            })
        except (KeyError, ValueError) as e:
            print(f"Error processing {coin.get('symbol', 'UNKNOWN')}: {str(e)}")
            continue
    
    print("\nFiltering Results:")
    print(f"Skipped due to invalid/missing data: {skipped_reasons['invalid_data']}")
    print(f"Skipped due to market cap (<1M USD): {skipped_reasons['market_cap']}")
    print(f"Skipped due to volume (<150K USD): {skipped_reasons['volume']}")
    print(f"Skipped due to no Tier-1/Tier-2 listings: {skipped_reasons['exchanges']}")
    print(f"Total coins passing all criteria: {len(filtered_coins)}")
    
    return filtered_coins

def save_to_excel(filtered_coins, filename="filtered_coins.xlsx"):
    """Save the filtered coins to an Excel file."""
    df = pd.DataFrame(filtered_coins)
    df.to_excel(filename, index=False)
    print(f"Data saved to {filename}")

def main():
    coins = fetch_data_from_coincap()
    if not coins:
        print("No coin data available. Exiting.")
        return
        
    markets = fetch_exchange_markets()
    if not markets:
        print("No market data available. Exiting.")
        return
        
    print("\nProcessing exchange listings...")
    coin_listings = get_exchange_listings(markets)
    print(f"Found listings for {len(coin_listings)} unique coins")
    
    print("\nFiltering coins based on criteria...")
    filtered_coins = filter_coins(coins, coin_listings)
    
    print(f"\nFound {len(filtered_coins)} coins matching all criteria.")
    save_to_excel(filtered_coins)

    # Sort coins by market cap (ascending order)
    sorted_coins = sorted(filtered_coins, key=lambda x: float(x["Market Cap (USD)"]))

    # Display bottom 10 coins by market cap
    print("\nBottom 10 coins by market cap (ascending):")
    for i, coin in enumerate(sorted_coins[:10], 1):
        print(f"{i}. {coin['Symbol']} - Market Cap: ${coin['Market Cap (USD)']:,.2f}")
        
    # Display top 10 coins by market cap
    print("\nTop 10 coins by market cap (descending):")
    for i, coin in enumerate(reversed(sorted_coins[-10:]), 1):
        print(f"{i}. {coin['Symbol']} - Market Cap: ${coin['Market Cap (USD)']:,.2f}")
    else:
        print("\nNo coins found matching all criteria.")

if __name__ == "__main__":
    main()
