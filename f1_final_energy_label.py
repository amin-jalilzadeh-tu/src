# f1_final_energy_label.py

from collections import Counter
import pandas as pd
import psycopg2
from config import get_conn_params

conn_params = get_conn_params()

def normalize_label(label):
    replacements = {'A+++': 'A3+', 'A++': 'A2+', 'A+': 'A1+'}
    return replacements.get(label, label)

def determine_final_label(row):
    labels = [row['label_gem'], row['label_ind'], row['label_keus'], # TNO
              row['el_meest_voorkomende_label'], row['el_minst_zuinige_label'], 
              row['el_meest_zuinige_label']]
    labels = [normalize_label(label) for label in labels if pd.notnull(label)]
    label_counts = pd.Series(labels).value_counts()
    max_count = label_counts.max()
    common_labels = label_counts[label_counts == max_count].index.tolist()
    for priority_label in ['A3+', 'A2+', 'A1+', 'A', 'B', 'C', 'D', 'E', 'F', 'G']:
        if priority_label in common_labels:
            return priority_label
    return 'Unknown'

def fetch_data(table_name):
    with psycopg2.connect(conn_params) as conn:
        query = f'SELECT * FROM "{table_name}"'
        df = pd.read_sql(query, conn)
    return df

def update_database_with_labels(df, table_name):
    with psycopg2.connect(conn_params) as conn, conn.cursor() as cursor:
        for index, row in df.iterrows():
            update_query = f"""
            UPDATE "{table_name}"
            SET final_energy_label = %s
            WHERE id = %s  -- Assuming there's an 'id' column to uniquely identify rows
            """
            cursor.execute(update_query, (row['final_energy_label'], row['id']))
        conn.commit()

def assign_final_energy_labels(table_name):
    df = fetch_data(table_name)
    df['final_energy_label'] = df.apply(determine_final_label, axis=1)
    update_database_with_labels(df, table_name)
    print("The final energy labels have been assigned and the database table is updated.")
    print(df['final_energy_label'].value_counts())
