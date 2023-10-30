import pymysql
import pandas as pd
import os
from dotenv import load_dotenv

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
    for k,v in exp_loc.items():
        if v == "Up-regulated":
            for ke, ve in exp_c.items():
                if (k == ke ) and (ve == v):
                    count_up += 1 
        else:
            for ke, ve in exp_c.items():
                if (k == ke ) and (ve == v):
                    count_down += 1 

    return count_up , count_down

    # return sum(x in exp_c for k,v in exp_loc if )

def combine(cond, exp):
    return dict(zip(cond, exp))

def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))

def generate_red_gradient(value):
    color = (1, 1-value, 1-value)
    hex_code = rgb_to_hex(color)
    return hex_code

def normalize(value, min_val, max_val):
    return (value - min_val) / (max_val - min_val)

def get_colour_code_g( max_, min_ , v):
    if v != 0:
        max_ = max_+ 10
        v = v + 10

    n_v = normalize(v,min_,max_)
    return generate_green_gradient(n_v)


def get_colour_code_red(max_, min_ , v):
    if v != 0:
        max_ = max_+ 10
        v = v + 10

    n_v = normalize(v,min_,max_)
    return generate_red_gradient(n_v)


def generate_green_gradient(value):
    color = (1-value, 1, 1-value)  
    hex_code = rgb_to_hex(color)
    return hex_code



def calculate_mat(df):

    df = df.groupby('mapped_phosphosite').agg(pd.Series.tolist).reset_index()
    df['count'] = df["exp_condition"].apply(lambda x:len(x))

    df['up_count'] = df["expression"].apply(lambda x:x.count("Up-regulated"))
    df['down_count'] = df["expression"].apply(lambda x:x.count("down-regulated")) 

    df = df.sort_values(by=['count'], ascending=False)

    max_up = max((df['up_count']))
    min_up = min((df['up_count']))

    max_down = max((df['down_count']))
    min_down = min((df['down_count']))

    print(max_up,min_up, max_down, min_down)

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
    
    df.to_excel('testtt.xlsx')


    _dict = {}
    main_dic = {}
    
    c_dict = {}
    c_main_dic = {}

    for i , row in df.iterrows():
        came = False
        for k,v in row.items():
            if i == k:
                _dict[k] = sum(v)
                c_dict[k] = "#7393B3"
                came = True
            else:
                if came:
                    _dict[k] = v[1]
                    c_dict[k] = get_colour_code_g( max_down, min_down , v[1])


                else:
                    _dict[k] = v[0]
                    c_dict[k] = get_colour_code_red( max_up, min_up , v[0])

        main_dic[i] = _dict
        c_main_dic[i] = c_dict
        _dict = {}
        c_dict = {}

    result  = pd.DataFrame(main_dic)
    colour_df  = pd.DataFrame(c_main_dic)

    return result , colour_df

def sum_up_down(mdf_up,mdf_down):
    pass