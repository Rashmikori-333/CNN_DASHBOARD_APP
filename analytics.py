import pandas as pd

def prepare_dataframe(data):
    return pd.DataFrame(
        data,
        columns=["ID", "Image", "Prediction", "Confidence", "Time"]
    )

def class_count(df):
    return df["Prediction"].value_counts()

def average_confidence(df):
    return df.groupby("Prediction")["Confidence"].mean()
