from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import pandas as pd
from datetime import datetime, timedelta
import random


from idf_batch_processor import update_idf_and_save, fetch_buildings_data
from config import get_idf_config, get_conn_params
from runner_generator import simulate_all

app = Flask(__name__)
CORS(app)

@app.route('/run_analysis', methods=['GET'])
def run_analysis():
    pc6_input = request.args.get('pc6')
    print(f"Received pc6 input: {pc6_input}")  # Debug: Check input

    conn_params = get_conn_params()  
    print(f"Database connection parameters: {conn_params}")
    output_dir = get_idf_config()['output_dir']
    print(f"Output directory: {output_dir}")  # Debug: Check output directory config

    
    table_name = "test_pc6"


    try:

        buildings_df = fetch_buildings_data(table_name, conn_params)
        print(f"Fetched Data: {buildings_df.head()}")

        update_idf_and_save(buildings_df, output_dir) # df, 
        print(f"Updated IDF and saved.")
        simulate_all()  # This could also generate additional data if necessary
        print(f"Simulation completed.")
 

    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)
