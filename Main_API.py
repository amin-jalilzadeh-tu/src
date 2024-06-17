from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import pandas as pd
from datetime import datetime, timedelta
import random

from database_utils import validate_pc6, fetch_raw_data_for_pc6, create_or_replace_table
from f1_final_energy_label import assign_final_energy_labels
from f2_building_function import classify_building_functions
from f3_housing_type import map_housing_types
from f4_population_estimation import estimate_population
from idf_batch_processor import update_idf_and_save, fetch_buildings_data
from config import get_idf_config, get_conn_params
from runner_generator import simulate_all
from json_processor import process_output_files


app = Flask(__name__)
CORS(app)

@app.route('/run_analysis', methods=['GET'])
def run_analysis():
    pc6_input = request.args.get('pc6')
    print(f"Received pc6 input: {pc6_input}")  
    conn_params = get_conn_params()  
    print(f"Database connection parameters: {conn_params}")
    output_dir = get_idf_config()['output_dir']
    print(f"Output directory: {output_dir}")  # Debug: Check output directory config

    
    table_name = "test_pc6"

    #if not pc6_input or not validate_pc6(pc6_input):
    #    return jsonify({"error": "Invalid or non-existing pc6 value."}), 400

    try:
        #df = fetch_raw_data_for_pc6(pc6_input)
        #table_name = "PC6_" + pc6_input.replace(" ", "_")
        #create_or_replace_table(df, table_name)
        
        #assign_final_energy_labels(table_name)
        #classify_building_functions(table_name)
        #map_housing_types(table_name)
        #estimate_population(table_name)

        ### Temporal fix
        buildings_df = fetch_buildings_data(table_name, conn_params)
        print(f"Fetched Data: {buildings_df.head()}")

        ###

        update_idf_and_save(buildings_df, output_dir) # df, 
        print(f"Updated IDF and saved.")
        simulate_all()  # This could also generate additional data if necessary
        print(f"Simulation completed.")
        process_output_files (output_dir, pc6_input)
        #filename = generate_excel(pc6_input)
        #print(f"Sending file: {filename}")
        #return send_file(filename, as_attachment=True, download_name=f'{pc6_input}_results.xlsx')

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def generate_excel(district):
    data = {'District': [district], 'Date': [datetime.now().strftime("%Y-%m-%d")], 'Note': ['Processed data']}
    df = pd.DataFrame(data)
    filename = f'tmp/{district}_results.xlsx'
    if not os.path.exists('tmp'):
        os.makedirs('tmp')

    df.to_excel(filename, index=False, engine='openpyxl')
    return filename

if __name__ == '__main__':
    app.run(debug=True)



# For test
#if __name__ == "__main__":
    # Assuming get_conn_params and get_idf_config are correctly defined in config.py
 #   from config import get_conn_params, get_idf_config
 #   conn_params = get_conn_params()
 #   output_dir = get_idf_config()['output_dir']
 #   table_name = "test_pc6"

    # Fetch building data
 #   buildings_df = fetch_buildings_data(table_name, conn_params)
 #   if not buildings_df.empty:
 #       print("Successfully fetched building data:")
 #       print(buildings_df.head())  # Display the first few rows of the DataFrame

    # Run update_idf_and_save
 #   update_idf_and_save(buildings_df, output_dir)
 #   print(f"Check the output directory for modified IDF files: {output_dir}")




