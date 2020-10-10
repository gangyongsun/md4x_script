import pandas as pd
import numpy as np

df = pd.DataFrame(np.arange(20).reshape(5, 4), index=[1, 3, 4, 6, 8])
print(df)

# df = df.reset_index().drop('index', axis=1)
# print(df)

df = df.reset_index(drop=True)

print(df)
