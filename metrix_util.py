import pymysql
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv
import time
load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')


def get_query(k):
    q = f'''SELECT exp_condition,mapped_phosphosite,expression FROM  phospodb_nisar_differential_data WHERE mapped_genesymbol = '{k}' '''
    return q


def get_query_pr(k):
    q = f'''SELECT exp_condition,mapped_phosphosite,expression FROM  phospodb_nisar_differential_data WHERE mapped_genesymbol = '{k}'  '''
    return q

def get_d(query):
    connection = pymysql.connect(
        host=DB_HOST,
        port=3306,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
    )
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    df_result = pd.DataFrame(result, columns=[desc[0] for desc in cursor.description])
    cursor.close()
    connection.close()
    return df_result

def getcount_up(exp_c , exp_loc):
    count_up = 0
    count_down = 0
    
    filt_dict = {k:v for (k,v) in exp_c.items() if v == "Up-regulated"}
    filt_dict_loc = {k:v for (k,v) in exp_loc.items() if v == "Up-regulated"}

    count_up = len(set(filt_dict.keys()) & set(filt_dict_loc.keys()))


    filt_dict = {k:v for (k,v) in exp_c.items() if v == "down-regulated"}

    filt_dict_loc = {k:v for (k,v) in exp_loc.items() if v == "down-regulated"}

    count_down = len(set(filt_dict.keys()) & set(filt_dict_loc.keys()))


    return count_up , count_down

def getcount_up_oppo(exp_c , exp_loc):

    filt_dict = {k:v for (k,v) in exp_c.items() if v == "Up-regulated"}

    filt_dict_loc = {k:v for (k,v) in exp_loc.items() if v == "down-regulated" }

    count_up_dowm = len(set(filt_dict.keys()) & set(filt_dict_loc.keys()))


    filt_dict = {k:v for (k,v) in exp_c.items() if v == "Up-regulated"}

    filt_dict_loc = {k:v for (k,v) in exp_loc.items() if v == "down-regulated"}

    count_down_up = len(set(filt_dict.keys()) & set(filt_dict_loc.keys()))

    return count_up_dowm , count_down_up


def combine(cond, exp):
    return dict(zip(cond, exp))

def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))

def generate_red_gradient(value):
    if value > 0 and value <= 0.1:
        return "#EA7F7F"
    elif value >0.1 and value<=0.2:
        return "#D65D5D"
    elif value >0.2 and value<=0.3:
        return "#EE3F3F"
    elif value >0.3 and value<=0.4:
        return "#E01919 "
    elif value >0.4 and value<=0.5:
        return "#B51D1D"
    elif value > 0.5 and value <= 0.6:
        return "#A52222 "
    elif value >0.6 and value<=0.7:
        return "#8D1A1A"
    elif value >0.7 and value<=0.8:
        return "#751818"
    elif value >0.8 and value<=0.9:
        return "#651010 "
    elif value >0.9 and value<=1:
        return "#4D0808"
    else:
        return "#ffffff"

def normalize(value, min_val, max_val):
    return (value - min_val) / (max_val - min_val)

def get_colour_code_g( max_, min_ , v):
    n_v = normalize(v,min_,max_)
    return generate_green_gradient(n_v)


def get_colour_code_red(max_, min_ , v):
    print(v)
    n_v = normalize(v,min_,max_)
    print(n_v)
    return generate_red_gradient(n_v)


def generate_green_gradient(value):
    if value > 0 and value <= 0.1:
        return "#95F2BF"
    elif value >0.1 and value<=0.2:
        return "#6DEAA5"
    elif value >0.2 and value<=0.3:
        return "#3FF38F"
    elif value >0.3 and value<=0.4:
        return "#2BC770 "
    elif value >0.4 and value<=0.5:
        return "#1BAB5B"
    elif value > 0.5 and value <= 0.6:
        return "#1E9151"
    elif value >0.6 and value<=0.7:
        return "#1A7442"
    elif value >0.7 and value<=0.8:
        return "#136136"
    elif value >0.8 and value<=0.9:
        return "#0D4E2A "
    elif value >0.9 and value<=1:
        return "#053018"
    else:
        return "#ffffff"



def get_min_max(df):

    diagonal_values = np.diag(df.values)
    
    np.fill_diagonal(df.values,0)

    max_up = np.triu(df.values).max()
    min_up = np.triu(df.values).min()

    max_down = np.tril(df.values).max()
    min_down = np.tril(df.values).min()

    return max_up,min_up, max_down, min_down


def calculate_mat(df, CUT_OFF):

    df = df.groupby('mapped_phosphosite').agg(pd.Series.tolist).reset_index()
    df['count'] = df["exp_condition"].apply(lambda x:len(x))

    df['up_count'] = df["expression"].apply(lambda x:x.count("Up-regulated"))
    df['down_count'] = df["expression"].apply(lambda x:x.count("down-regulated")) 

    df = df.sort_values(by=['count'], ascending=False)

    df = df.loc[df['count'] >= CUT_OFF]

    all_sites = df['mapped_phosphosite']

    df['condition_exp'] = df.apply(lambda x:combine(x["exp_condition"],x["expression"]) , axis = 1) 


    df = df[['mapped_phosphosite','condition_exp']]

    df.set_index('mapped_phosphosite', inplace=True)

    li_up = []

    for i, val in df.iterrows():
        for site in all_sites:
            c_up = getcount_up(val['condition_exp'], df.loc[site, 'condition_exp'])
            li_up.append(c_up)
        df[i] = li_up
        li_up = []
    
    df.drop('condition_exp',axis=1, inplace = True)
    

    _dict = {}
    main_dic = {}
    
    for i , row in df.iterrows():
        came = False
        for k,v in row.items():
            if i == k:
                _dict[k] = sum(v)
                came = True
            else:
                if came:
                    _dict[k] = v[1]
                else:
                    _dict[k] = v[0]
        main_dic[i] = _dict
        _dict = {}

    result  = pd.DataFrame(main_dic)

# ===========================================================================

    max_up,min_up, max_down, min_down = get_min_max(result)

    c_dict = {}
    c_main_dic = {}

    for i , row in df.iterrows():
        came = False
        for k,v in row.items():
            if i == k:
                c_dict[k] = "#5D6163"
                came = True
            else:
                if came:
                    c_dict[k] = get_colour_code_g( max_down, min_down , v[1])
                else:
                    c_dict[k] = get_colour_code_red( max_up, min_up , v[0])

        c_main_dic[i] = c_dict
        c_dict = {}

# =============================================================================

    colour_df  = pd.DataFrame(c_main_dic)

    return result , colour_df




def calculate_mat_op(df , CUT_OFF):

    df = df.groupby('mapped_phosphosite').agg(pd.Series.tolist).reset_index()
    df['count'] = df["exp_condition"].apply(lambda x:len(x))

    df['up_count'] = df["expression"].apply(lambda x:x.count("Up-regulated"))
    df['down_count'] = df["expression"].apply(lambda x:x.count("down-regulated")) 

    df = df.sort_values(by=['count'], ascending=False)

    df = df.loc[df['count'] >= CUT_OFF]
    max_up = max((df['up_count']))
    min_up = min((df['up_count']))

    max_down = max((df['down_count']))
    min_down = min((df['down_count']))


    all_sites = df['mapped_phosphosite']

    df['condition_exp'] = df.apply(lambda x:combine(x["exp_condition"],x["expression"]) , axis = 1) 


    df = df[['mapped_phosphosite','condition_exp']]

    df.set_index('mapped_phosphosite', inplace=True)

    li_up = []

    for i, val in df.iterrows():
        for site in all_sites:
            c_up = getcount_up_oppo(val['condition_exp'], df.loc[site, 'condition_exp'])
            li_up.append(c_up)
        df[i] = li_up
        li_up = []

    df.drop('condition_exp',axis=1, inplace = True)
    
    _dict = {}
    main_dic = {}
    
    for i , row in df.iterrows():
        came = False
        for k,v in row.items():
            if i == k:
                _dict[k] = sum(v)
                came = True
            else:
                if came:
                    _dict[k] = v[1]
                else:
                    _dict[k] = v[0]
        main_dic[i] = _dict
        _dict = {}

    result  = pd.DataFrame(main_dic)

# ===========================================================================

    max_up,min_up, max_down, min_down = get_min_max(result)

    c_dict = {}
    c_main_dic = {}

    for i , row in df.iterrows():
        came = False
        for k,v in row.items():
            if i == k:
                c_dict[k] = "#5D6163"
                came = True
            else:
                if came:
                    c_dict[k] = get_colour_code_g( max_down, min_down , v[1])
                else:
                    c_dict[k] = get_colour_code_red( max_up, min_up , v[0])

        c_main_dic[i] = c_dict
        c_dict = {}

# =============================================================================

    colour_df  = pd.DataFrame(c_main_dic)

    return result , colour_df


def divide_arrays(numerator, denominator):
    result = np.where(denominator != 0, numerator / denominator, numerator)
    return result

def calculate_ratio(df,odf):
    df[:] = divide_arrays(df.values, odf.values)
    max_up,min_up, max_down, min_down = get_min_max(df)

    print(max_up,min_up, max_down, min_down)

    c_dict = {}
    c_main_dic = {}

    for i , row in df.iterrows():
        came = False
        for k,v in row.items():
            if i == k:
                c_dict[k] = "#5D6163"
                came = True
            else:
                if came:
                    c_dict[k] = get_colour_code_g( max_down, min_down , v)
                else:
                
                    c_dict[k] = get_colour_code_red( max_up, min_up , v)

        c_main_dic[i] = c_dict
        c_dict = {}
    
    colour_df  = pd.DataFrame(c_main_dic)
    colour_df.to_csv('colour_df.csv')
    colour_df.fillna('#ffffff', inplace=True)

    return df , colour_df

