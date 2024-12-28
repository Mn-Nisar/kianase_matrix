import pandas as pd

from metrix_util import get_d , get_query , calculate_mat , get_query_pr , calculate_mat_op , calculate_ratio
from get_plot import get_matrix_plot
from zipping import zip_and_delete_output
kianase = 'ANTXR1'
diff_tabel = "Updated_final_Differential"
q = get_query(kianase,diff_tabel)
df = get_d(q)

CUT_OFF = 0

mdf , cdf = calculate_mat(df , CUT_OFF )

mdf.to_excel(f"output/{kianase}_UUDD.xlsx")

get_matrix_plot(mdf , cdf,kianase,type_="UU_DD" )

mdf_op , cdf_op = calculate_mat_op(df , CUT_OFF)

mdf_op.to_excel(f"output/{kianase}_UDDU.xlsx")

get_matrix_plot(mdf_op , cdf_op, kianase,type_="UD_DU" )

ratio_df , colour_df = calculate_ratio(mdf , mdf_op)

get_matrix_plot(ratio_df , colour_df, kianase,type_="_RATIO_" )


ratio_df.to_excel(f"output/{kianase}_ratio.xlsx")

zip_and_delete_output(kianase)