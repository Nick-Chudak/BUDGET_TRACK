def total_earned(df):
    return df[df['Amount'] > 0]['Amount'].sum()

def total_spent(df):
    return abs(df[df['Amount'] < 0]['Amount'].sum())

def savings(df):
    return total_earned(df) - total_spent(df) 