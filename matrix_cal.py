import pandas as pd

from metrix_util import get_d , get_query , calculate_mat , get_query_pr , calculate_mat_op
from get_plot import get_matrix_plot

kianase = 'PAK1'

q = get_query(kianase)
df = get_d(q)

CUT_OFF = 3

mdf , cdf = calculate_mat(df , CUT_OFF )
get_matrix_plot(mdf , cdf,kianase,type_="UU_DD" )

mdf_op , cdf_op = calculate_mat_op(df , CUT_OFF)
get_matrix_plot(mdf_op , cdf_op, kianase,type_="UD_DU" )

