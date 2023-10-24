import pymysql
import pandas as pd


def get_query(k, expression):
    q = f'''SELECT exp_condition,mapped_phosphosite,expression FROM  phospodb_nisar_differential_data WHERE mapped_genesymbol = '{k}' AND expression='{expression}' '''
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

def getcount(exp_c , exp_loc):
    return sum(x in exp_c for x in exp_loc)

def calculate_mat(df):
    df = df.groupby('mapped_phosphosite').agg(pd.Series.tolist).reset_index()
    df['count'] = df["exp_condition"].apply(lambda x:len(x))
    df = df.sort_values(by=['count'], ascending=False)
    all_sites = df['mapped_phosphosite']

    df = df[['mapped_phosphosite','exp_condition','count']]
    df.set_index('mapped_phosphosite', inplace=True)

    li = []

    for i, val in df.iterrows():
        for site in all_sites:
            c = getcount(val['exp_condition'], df.loc[site, 'exp_condition'])
            li.append(c)
        df[i] = li
        li = []
    
    df.drop(['exp_condition'], axis=1, inplace=True)
    return df
