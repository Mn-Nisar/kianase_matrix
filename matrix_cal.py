import pandas as pd

from metrix_util import get_d , get_query , calculate_mat , get_query_pr , calculate_mat_op
from get_plot import get_matrix_plot

kianase = 'PAK1'

q = get_query(kianase)
df = get_d(q)

CUT_OFF = 0

mdf , cdf = calculate_mat(df , CUT_OFF )

get_matrix_plot(mdf , cdf)


