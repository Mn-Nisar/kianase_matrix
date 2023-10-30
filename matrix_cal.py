import pandas as pd

from metrix_util import get_d , get_query , calculate_mat , get_query_pr , sum_up_down
from get_plot import get_matrix_plot

kianase = 'PAK1'

q = get_query(kianase)
df = get_d(q)
mdf , cdf = calculate_mat(df)

get_matrix_plot(mdf , cdf)

# mdf.to_excel(f"{kianase}_site_matrix.xlsx")
# print("differentil down-regulated done")

# profile
# q = get_query_pr(kianase)
# df = get_d(q)
# mdf = calculate_mat(df)
# mdf.to_excel(f"{kianase}_Profile_site_matrix.xlsx")
# print("Profile done")
