import pandas as pd
import numpy as np

# Create two sample dataframes
data1 = {'A': [1, 2, 3],
         'B': [4, 5, 6],
         'C': [7, 8, 9]}

data2 = {'A': [10, 11, 12],
         'B': [13, 14, 15],
         'C': [16, 17, 18]}

df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)

# Extract upper triangle from df1 and lower triangle from df2
upper_triangle = np.triu(df1.values, k=-1import pandas as pd
import numpy as np

# Create two sample dataframes
data1 = {'A': [1, 2, 3],
         'B': [4, 5, 6],
         'C': [7, 8, 9]}

data2 = {'A': [10, 11, 12],
         'B': [13, 14, 15],
         'C': [16, 17, 18]}

df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)

# Extract upper triangle from df1 and lower triangle from df2
upper_triangle = np.triu(df1.values, k=0)  # k=0 keeps the diagonal
lower_triangle = np.tril(df2.values, k=-1)  # k=-1 excludes the diagonal

# Create a new dataframe from the triangles
result_df = pd.DataFrame(upper_triangle + lower_triangle, columns=df1.columns, index=df1.index)

print(result_df)
)  # k=0 keeps the diagonal
lower_triangle = np.tril(df2.values, k=-1)  # k=-1 excludes the diagonal

# Create a new dataframe from the triangles
result_df = pd.DataFrame(upper_triangle + lower_triangle, columns=df1.columns, index=df1.index)

print(result_df)
