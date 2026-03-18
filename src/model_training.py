import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report

DATA_FILE = "data/training_dataset.csv"


def load_dataset():

    df = pd.read_csv(DATA_FILE)

    df["date"] = pd.to_datetime(df["date"])

    return df


def prepare_features(df):

    features = [
        "ma20",
        "ma50",
        "rsi",
        "macd",
        "macd_signal",
        "volatility",
        "momentum",
        "returns"
    ]

    X = df[features]
    y = df["target"]

    return X, y


def train_models(X_train, y_train):

    rf = RandomForestClassifier(n_estimators=100, n_jobs=-1)
    rf.fit(X_train, y_train)

    gb = GradientBoostingClassifier()
    gb.fit(X_train, y_train)

    return rf, gb


def evaluate(model, X_test, y_test):

    preds = model.predict(X_test)

    print("Accuracy:", accuracy_score(y_test, preds))
    print(classification_report(y_test, preds))


def main():

    df = load_dataset()

    # time-based split
    split_date = "2023-01-01"

    train_df = df[df["date"] < split_date]
    test_df = df[df["date"] >= split_date]

    X_train, y_train = prepare_features(train_df)
    X_test, y_test = prepare_features(test_df)

    print("Training models...")

    rf, gb = train_models(X_train, y_train)

    print("\nRandom Forest Results")
    evaluate(rf, X_test, y_test)

    print("\nGradient Boosting Results")
    evaluate(gb, X_test, y_test)


if __name__ == "__main__":
    main()