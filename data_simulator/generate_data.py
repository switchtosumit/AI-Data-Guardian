import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def generate_transactions(n=1000, drift = False, schema_change = False):
    np.random.seed(50)

    df = pd.DataFrame({
        "transaction_id": np.arange(n),
        "user_id": np.random.randint(1000, 2000, n),
        "amount": np.random.normal(100,20, n),
        "timestamp": pd.date_range(end=datetime.now(), periods=n, freq='h')
    })

    if drift:
        df["amount"] = np.random.normal(300, 50, n)

    if schema_change == True:
        df["transaction_id"] = df["transaction_id"].astype(str) + "_txn"

   
    

    return df

if __name__ == "__main__":
    os.makedirs("./data", exist_ok=True)
