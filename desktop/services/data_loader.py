import os
import pandas as pd

def load_transactions(excel_path=None):
    if excel_path is None:
        excel_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'excel', 'Preferred_Package_6788_051925.xlsx')
    if not os.path.exists(excel_path):
        return pd.DataFrame(columns=["Date", "Amount"])
    df = pd.read_excel(excel_path, usecols=["Date", "Amount"])
    df = df.dropna(subset=["Date", "Amount"])
    df["Date"] = pd.to_datetime(df["Date"])
    return df 