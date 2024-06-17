import psycopg2

def analyze_table_data():
    base_table_name = input("Enter the base table name (e.g., 2628ze): ")
    table_name = f"pc6_{base_table_name}"
    summary_table_name = f"DEA_{table_name}"
    conn_params = "dbname='DATALES_20240512' user='postgres' password='865990289' host='localhost'"

    with psycopg2.connect(conn_params) as conn, conn.cursor() as cur:
        cur.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'")
        columns = cur.fetchall()

        cur.execute(f"""
        DROP TABLE IF EXISTS {summary_table_name};
        CREATE TABLE {summary_table_name} (
            Column_Name TEXT,
            Missing_Values_Count INT,
            Unique_Values_Count INT,
            Most_Frequent_Value_1 TEXT,
            Most_Frequent_Value_2 TEXT,
            Most_Frequent_Value_3 TEXT,
            Most_Frequent_Value_4 TEXT,
            Most_Frequent_Value_5 TEXT
        );
        """)

        for col in columns:
            col_name = col[0]
            cur.execute(f"SELECT COUNT(*) FROM {table_name} WHERE {col_name} IS NULL")
            missing_values_count = cur.fetchone()[0]
            cur.execute(f"SELECT COUNT(DISTINCT {col_name}) FROM {table_name}")
            unique_values_count = cur.fetchone()[0]
            cur.execute(f"SELECT {col_name}, COUNT({col_name}) FROM {table_name} GROUP BY {col_name} ORDER BY COUNT({col_name}) DESC LIMIT 5")
            top_values = cur.fetchall()
            top_values_list = [item[0] if item[0] is not None else 'X' for item in top_values] + ['X'] * (5 - len(top_values))
            insert_query = f"""
            INSERT INTO {summary_table_name} (Column_Name, Missing_Values_Count, Unique_Values_Count, Most_Frequent_Value_1, Most_Frequent_Value_2, Most_Frequent_Value_3, Most_Frequent_Value_4, Most_Frequent_Value_5)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """
            cur.execute(insert_query, (col_name, missing_values_count, unique_values_count) + tuple(top_values_list))
        conn.commit()
        print(f"Summary table {summary_table_name} created successfully.")

if __name__ == "__main__":
    analyze_table_data()
