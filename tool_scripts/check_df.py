import pandas as pd

df = pd.read_pickle(r"C:\Users\me424\Documents\nanopore\stExp23_06_07\01111_ecds\ints.pkl")

print(df.head(50))