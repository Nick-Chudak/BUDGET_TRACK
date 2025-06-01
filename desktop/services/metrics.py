def total_earned(df):
    return df[df['amount'] > 0]['amount'].sum()

def total_spent(df):
    return abs(df[df['amount'] < 0]['amount'].sum())

def savings(df):
    return total_earned(df) - total_spent(df) 