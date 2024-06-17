# f3_housing_type.py

import pandas as pd
import psycopg2
from config import get_conn_params

conn_params = get_conn_params()

# Building type to housing type mapping
building_type_mapping = {
    'appartement': 'Apartment',
    'hoekwoning': 'Terraced housing',
    'tussenwoning/geschakeld': 'Terraced housing',
    'twee-onder-een-kap': 'Semi Detached',
    'vrijstaande woning': 'Detached'
}

def fetch_data(table_name):
    with psycopg2.connect(conn_params) as conn:
        pc6_data = pd.read_sql(f'SELECT * FROM "{table_name}"', conn)
        housing_standards = pd.read_sql('SELECT * FROM "housing_Standards_2011"', conn)
    return pc6_data, housing_standards

def map_and_update_database(pc6_data, housing_standards, table_name):
    with psycopg2.connect(conn_params) as conn, conn.cursor() as cursor:
        for index, row in pc6_data.iterrows():
            mapped_type = building_type_mapping.get(row['building_type'], None)
            if mapped_type:
                year_range = '<1945' if row['construction_year'] < 1945 else '>1995' if row['construction_year'] > 1995 else '1945 - 1975' if row['construction_year'] <= 1975 else '1975 - 1995'
                query = f"""
                SELECT * FROM "housing_Standards_2011" 
                WHERE housing_type = '{mapped_type}' AND construction_year_range = '{year_range}'
                """
                housing_data = pd.read_sql(query, conn)
                if not housing_data.empty:
                    # Assuming housing_data has columns like 'average_space', 'population_density', etc.
                    for col in housing_data.columns.difference(['id', 'housing_type', 'construction_year_range']):
                        pc6_data.at[index, col] = housing_data.iloc[0][col]
        
        # Update the database with new columns
        for col in housing_standards.columns.difference(['id', 'housing_type', 'construction_year_range']):
            if col not in pc6_data:
                pc6_data[col] = None  # Add new columns if they don't exist
            cursor.execute(f"""
            ALTER TABLE "{table_name}" ADD COLUMN IF NOT EXISTS {col} TEXT;
            """)
        conn.commit()
        
        # Now update the actual data
        for index, row in pc6_data.iterrows():
            update_query = f"""
            UPDATE "{table_name}" SET {', '.join([f'{col} = %s' for col in housing_standards.columns.difference(['id', 'housing_type', 'construction_year_range'])])}
            WHERE id = {row['id']}
            """
            cursor.execute(update_query, tuple(row[col] for col in housing_standards.columns.difference(['id', 'housing_type', 'construction_year_range'])))
        conn.commit()

def map_housing_types(table_name):
    pc6_data, housing_standards = fetch_data(table_name)
    map_and_update_database(pc6_data, housing_standards, table_name)
    print("The database has been updated with housing types and additional standards.")
