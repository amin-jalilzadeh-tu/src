from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os

from datetime import datetime, timedelta

from database_utils import validate_pc6, fetch_raw_data_for_pc6, create_or_replace_table
from f1_final_energy_label import assign_final_energy_labels
from f2_building_function import classify_building_functions
from f3_housing_type import map_housing_types
from f4_population_estimation import estimate_population
from idf_batch_processor import update_idf_and_save, fetch_buildings_data
from config import get_idf_config, get_conn_params
from runner_generator import simulate_all
from json_processor import process_output_files


####-------------------------------------------------------------
# this function is just to check the availability of the idd and minimal files in the dockerised energy plus
energyplus_dir = "/usr/local/EnergyPlus-22.2.0-c249759bad-Linux-Ubuntu20.04-x86_64"
examples_dir = os.path.join(energyplus_dir, "ExampleFiles")
files_to_check = {
    "minimal.idf in ExampleFiles": os.path.join(examples_dir, "minimal.idf"),
    "Energy+.idd in EnergyPlus directory": os.path.join(energyplus_dir, "Energy+.idd")
}
def check_file_exists(file_description, path):
    """ Check if a file exists at the given path """
    if os.path.isfile(path):
        print(f"Success: {file_description} - {path} exists.")
    else:
        print(f"Error: {file_description} - {path} does not exist.")
# Check each file
for description, path in files_to_check.items():
    check_file_exists(description, path)
####-------------------------------------------------------------


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
        
        json_files = process_output_files (output_dir, pc6_input)
        if not json_files:
            return jsonify({"error": "No JSON files generated"}), 500
        print(f"Processed output files: {json_files}")

        return send_file(json_files[0], as_attachment=True, attachment_filename=os.path.basename(json_files[0]))

        #filename = generate_excel(pc6_input)
        #print(f"Sending file: {filename}")
        #return send_file(filename, as_attachment=True, download_name=f'{pc6_input}_results.xlsx')

    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)



### This is for checking the availability of the idd and minimal files in dockerised energy plus

# Correct the path according to the actual installation directory
energyplus_dir = "/usr/local/EnergyPlus-22.2.0-c249759bad-Linux-Ubuntu20.04-x86_64"

# Path to the ExampleFiles directory
examples_dir = os.path.join(energyplus_dir, "ExampleFiles")

# File to check for
file_to_check = "minimal.idf"

# Full path to the file
full_file_path = os.path.join(examples_dir, file_to_check)

def check_file_exists(path):
    """ Check if a file exists at the given path """
    if os.path.isfile(path):
        print(f"Success: {path} exists.")
    else:
        print(f"Error: {path} does not exist.")

# Check if the minimal.idf file exists
check_file_exists(full_file_path)


















# curl "http://127.0.0.1:5000/run_analysis?pc6=2628zl"


