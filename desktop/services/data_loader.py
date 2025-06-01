import os
import pandas as pd
from data.db.engine import engine

def load_transactions():
    df = pd.read_sql("SELECT * FROM transactions", engine)
    df = df.dropna(subset=["date", "amount"])
    df["date"] = pd.to_datetime(df["date"])
    return df 