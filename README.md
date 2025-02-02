## Crypto Market Data Filter

This script fetches cryptocurrency data from the CoinCap API and filters coins based on market capitalization, 24-hour trading volume, and exchange listings. The results are saved as an Excel file for further analysis.

# Features

Fetches real-time cryptocurrency data using the CoinCap API.

Retrieves trading market data to determine where each coin is listed.

Filters coins based on:

Market Cap > $1M

24-hour Volume > $150K

Listed on at least one Tier-1 or Tier-2 exchange

Saves the filtered results in an Excel file (filtered_coins.xlsx).

Displays the top 10 and bottom 10 coins by market capitalization.

# Requirements

Ensure you have Python 3.x installed, along with the following dependencies:

pip install requests pandas openpyxl

# Installation & Usage

Clone the repository:

git clone https://github.com/yourusername/crypto-market-filter.git
cd crypto-market-filter

Install dependencies:

pip install -r requirements.txt

Run the script:

python main.py

Output

The script fetches data, applies filtering criteria, and saves the results in an Excel file (filtered_coins.xlsx).

It also prints insights about the number of coins filtered and their exchange listings.

Exchange Tiers

The filtering process checks if a coin is listed on Tier-1 or Tier-2 exchanges:

Tier-1 Exchanges:

Binance

Coinbase

Kraken

Bitfinex

OKEx

Bybit

Tier-2 Exchanges:

Gate.io

KuCoin

Huobi

Bitstamp

Crypto.com

Example Output

Fetching coin data from CoinCap API...
Successfully fetched data for 2500 coins.
Fetching exchange market data...
Successfully fetched 5000 markets.
Filtering coins based on criteria...
Total coins passing all criteria: 120

Bottom 10 coins by market cap:
1. XYZ - Market Cap: $1,000,500
...

Top 10 coins by market cap:
1. BTC - Market Cap: $800,000,000,000
...

Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

License

This project is licensed under the MIT License.

