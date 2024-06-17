# f2_building_function.py

import pandas as pd
import psycopg2
from config import get_conn_params

conn_params = get_conn_params()

function_groups = {
    'Woon- en Verblijfsfuncties': ['bag_gebr_woonfunctie', 'bag_gebr_logiesfunctie', 'tno_n_f1woon', 'tno_n_f7logies'],
    'Commerciële en Institutionele Functies': ['bag_gebr_bijeenkomstfunctie', 'bag_gebr_kantoorfunctie', 'bag_gebr_onderwijsfunctie', 'bag_gebr_gezondheidszorg', 'bag_gebr_winkelfunctie', 'tno_n_f2kantoor', 'tno_n_f3bijeenkomst', 'tno_n_f4onderwijs', 'tno_n_f5winkel', 'tno_n_f8gezondheidszorg', 'tno_n_f12bedrpand_zvbo_industri', 'tno_n_f13bedrpand_zvbo_groen'],
    'Industriële en Speciale Functies': ['bag_gebr_celfunctie', 'bag_gebr_industriefunctie', 'bag_gebr_sportfunctie', 'tno_n_f6sport', 'tno_n_f9industrie', 'tno_n_f10cel'],
    'Overige': ['bag_gebr_overige', 'tno_n_f11overig']
}

def fetch_data(table_name):
    with psycopg2.connect(conn_params) as conn:
        query = f'SELECT id, ' + ', '.join([col for group in function_groups.values() for col in group]) + f' FROM "{table_name}"'
        df = pd.read_sql(query, conn)
    return df

def update_database_with_classifications(df, table_name):
    with psycopg2.connect(conn_params) as conn, conn.cursor() as cursor:
        for index, row in df.iterrows():
            update_query = f"""
            UPDATE "{table_name}"
            SET assigned_function = %s
            WHERE id = %s
            """
            cursor.execute(update_query, (row['AssignedClass'], row['id']))
        conn.commit()

def classify_building_functions(table_name):
    df = fetch_data(table_name)

    # Calculate the total sum of all function-related columns for normalization
    total_functions_columns = [col for group in function_groups.values() for col in group]
    df['TotalFunctions'] = df[total_functions_columns].apply(lambda row: row.dropna().sum(), axis=1)

    # Calculate and add percentage columns for each function group
    for group_name, columns in function_groups.items():
        df[f'{group_name} Percentage'] = df.apply(lambda row: 100 * sum(row[col] for col in columns if not pd.isna(row[col])) / row['TotalFunctions'] if row['TotalFunctions'] > 0 else 0, axis=1)

    # Drop the temporary 'TotalFunctions' column
    df.drop('TotalFunctions', axis=1, inplace=True)

    # Assign a class based on the highest percentage value
    percentage_columns = [f'{group_name} Percentage' for group_name in function_groups]
    df['AssignedClass'] = df[percentage_columns].idxmax(axis=1).apply(lambda x: x.replace(' Percentage', ''))

    # Assign "Niet Geclassificeerd" when all percentages are 0
    df['AssignedClass'] = df.apply(lambda row: "Niet Geclassificeerd" if row[percentage_columns].max() == 0 else row['AssignedClass'], axis=1)

    update_database_with_classifications(df, table_name)
    print("Building functions have been classified and the database updated.")

