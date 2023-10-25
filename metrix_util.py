import pymysql
import pandas as pd


def get_query(k):
    q = f'''SELECT exp_condition,mapped_phosphosite,expression FROM  phospodb_nisar_differential_data WHERE mapped_genesymbol = '{k}' '''
    return q


def get_query_pr(k):
    q = f'''SELECT exp_condition,mapped_phosphosite,expression FROM  phospodb_nisar_differential_data WHERE mapped_genesymbol = '{k}'  '''
    return q

def get_d(query):
    connection = pymysql.connect(
        host='ciodsdb.cubtgfved0u5.us-west-1.rds.amazonaws.com',
        port=3306,
        user='admin',
        password='ciods123',
        database='ciodsdb'
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



def calculate_mat(df):

    df = df.groupby('mapped_phosphosite').agg(pd.Series.tolist).reset_index()
    df['count'] = df["exp_condition"].apply(lambda x:len(x))

    df['up_count'] = df["expression"].apply(lambda x:x.count("Up-regulated"))
    df['down_count'] = df["expression"].apply(lambda x:x.count("down-regulated")) 

    df = df.sort_values(by=['count'], ascending=False)


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

    result.to_excel("PRPF4B_matrix.xlsx")


    return df

def sum_up_down(mdf_up,mdf_down):
    pass








