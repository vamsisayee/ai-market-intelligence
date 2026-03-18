# Import required libraries
import pandas as pd
import requests
import yfinance as yf
import os

# Folder where stock data will be stored
DATA_FOLDER = "data"

# Create the data folder if it does not exist
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)


# Function to get S&P500 ticker symbols
def get_sp500_tickers():

    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    tables = pd.read_html(response.text)

    df = tables[0]

    tickers = df["Symbol"].tolist()

    return tickers


# Function to download stock data
def download_stock_data(ticker):

    try:

        df = yf.download(
            ticker,
            start="2018-01-01",
            progress=False,
            auto_adjust=False
        )

        if len(df) == 0:
            return

        # Convert index (Date) to column
        df.reset_index(inplace=True)

        # Flatten multi-index columns if present
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [col[0] for col in df.columns]

        # Standardize column names
        df.columns = [c.lower().replace(" ", "_") for c in df.columns]

        file_path = f"{DATA_FOLDER}/{ticker}.csv"

        df.to_csv(file_path, index=False)

        print(f"{ticker} saved")

    except Exception as e:
        print(f"Error downloading {ticker}: {e}")

# Main function that runs the pipeline
def main():

    tickers = get_sp500_tickers()

    print(f"Total stocks found: {len(tickers)}")

    print("Starting download process...")

    for ticker in tickers:

        download_stock_data(ticker)


# Run the script
if __name__ == "__main__":
    main()