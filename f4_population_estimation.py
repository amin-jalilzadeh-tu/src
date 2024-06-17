# f4_population_estimation.py

import pandas as pd
import psycopg2
from config import get_conn_params

conn_params = get_conn_params()

def fetch_data(table_name):
    with psycopg2.connect(conn_params) as conn:
        query = f'SELECT id, AssignedClass, Area FROM "{table_name}"'
        df = pd.read_sql(query, conn)
    return df

def estimate_people(row):
    if row['AssignedClass'] == 'Residential':
        if row['Area'] < 40:
            return 2
        elif 40 <= row['Area'] <= 90:
            return 4
        else:
            return 6
    elif row['AssignedClass'] == 'Commercial':
        if row['Area'] < 100:
            return 5
        elif 100 <= row['Area'] <= 200:
            return 10
        else:
            return 15
    elif row['AssignedClass'] == 'Industrial':
        if row['Area'] < 500:
            return 8
        elif 500 <= row['Area'] <= 1000:
            return 12
        else:
            return 16
    else:
        return 0

def update_database_with_estimates(df, table_name):
    with psycopg2.connect(conn_params) as conn, conn.cursor() as cursor:
        for index, row in df.iterrows():
            update_query = f"""
            UPDATE "{table_name}"
            SET Estimated_People = %s
            WHERE id = %s
            """
            cursor.execute(update_query, (row['Estimated_People'], row['id']))
        conn.commit()

def estimate_population(table_name):
    df = fetch_data(table_name)
    df['Estimated_People'] = df.apply(estimate_people, axis=1)
    update_database_with_estimates(df, table_name)
    print("The estimated population has been updated in the database.")
