# load_transactions.py

import os
import pandas as pd
from data.db.service import bulk_insert_transactions

# Path to your Excel file
excel_path = os.path.join("data", "excel", "")

# Load and clean the Excel file
df = pd.read_excel(excel_path, skiprows=1)  # skip 'Current statement period' row
df.columns = ['date', 'description', 'sub_description', 'transaction_type', 'amount', 'balance']
df = df.dropna(subset=['date', 'amount'])
df['date'] = pd.to_datetime(df['date'])

# Insert into the database
bulk_insert_transactions(df, source_file=os.path.basename(excel_path))
