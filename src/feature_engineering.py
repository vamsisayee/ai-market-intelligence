import pandas as pd
import os
import ta

DATA_FOLDER = "data"


def compute_features(file_path):

    df = pd.read_csv(file_path)

    # standardize column names
    df.columns = [c.lower() for c in df.columns]

    # convert date column
    df["date"] = pd.to_datetime(df["date"])

    # sort data chronologically
    df = df.sort_values("date")

    # convert numeric columns
    numeric_cols = ["open", "high", "low", "close", "adj_close", "volume"]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # use adjusted close for indicators
    price = df["adj_close"]

    # moving averages
    df["ma20"] = price.rolling(window=20).mean()
    df["ma50"] = price.rolling(window=50).mean()

    # RSI
    rsi_indicator = ta.momentum.RSIIndicator(close=price, window=14)
    df["rsi"] = rsi_indicator.rsi()

    # MACD
    macd_indicator = ta.trend.MACD(close=price)
    df["macd"] = macd_indicator.macd()
    df["macd_signal"] = macd_indicator.macd_signal()

    # volatility
    df["volatility"] = price.pct_change().rolling(window=20).std()

    # momentum
    df["momentum"] = price - price.shift(10)

    # daily returns
    df["returns"] = price.pct_change()

    # remove rows where indicators cannot exist yet
    df = df.dropna(subset=["ma50", "rsi", "macd"])

    return df


def process_all_stocks():

    files = os.listdir(DATA_FOLDER)

    for file in files:

        if file.endswith(".csv") and "_features" not in file:

            file_path = os.path.join(DATA_FOLDER, file)

            print(f"Processing {file}")

            df = compute_features(file_path)

            output_file = file.replace(".csv", "_features.csv")

            df.to_csv(os.path.join(DATA_FOLDER, output_file), index=False)

            print(f"Saved features → {output_file}")


if __name__ == "__main__":

    process_all_stocks()