import pandas as pd

from metrix_util import get_d , get_query , calculate_mat , get_query_pr

kianase = 'PAK1'

# upregulated 
expression = 'Up-regulated'
q = get_query(kianase,expression)
df = get_d(q)
mdf = calculate_mat(df)
mdf.to_excel(f"{kianase}_site_matrix{expression}.xlsx")
print("differentil upregulated done")
# down-regulated

expression = 'down-regulated'
q = get_query(kianase,expression)
df = get_d(q)
mdf = calculate_mat(df)
mdf.to_excel(f"{kianase}_site_matrix{expression}.xlsx")
print("differentil down-regulated done")



# profile
q = get_query_pr(kianase)
df = get_d(q)
mdf = calculate_mat(df)
mdf.to_excel(f"{kianase}_Profile_site_matrix.xlsx")
print("Profile done")
