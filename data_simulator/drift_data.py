from data_simulator.generate_data import generate_transactions
import pandas as pd

df = generate_transactions(n= 10, drift=False,schema_change=False)
df.to_csv("./data/gold.csv", index=False) 

df = pd.read_csv("./data/gold.csv")
print(df.count())
print(df.dtypes)





