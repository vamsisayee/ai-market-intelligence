import pandas as pd
import os

DATA_FOLDER = "data"
OUTPUT_FILE = "data/training_dataset.csv"


def create_dataset():

    all_data = []

    files = os.listdir(DATA_FOLDER)

    for file in files:

        if file.endswith("_features.csv"):

            file_path = os.path.join(DATA_FOLDER, file)

            ticker = file.split("_")[0]

            df = pd.read_csv(file_path)

            # add ticker column
            df["ticker"] = ticker

            # create future price column
            df["future_price"] = df["adj_close"].shift(-5)

            # create target variable
            df["target"] = (df["future_price"] > df["adj_close"]).astype(int)

            # remove rows where future price is missing
            df = df.dropna(subset=["future_price"])

            all_data.append(df)

            print(f"Processed {ticker}")

    dataset = pd.concat(all_data)

    dataset.to_csv(OUTPUT_FILE, index=False)

    print("Training dataset created")


if __name__ == "__main__":
    create_dataset()