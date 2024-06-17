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








def update_idf_and_save(buildings_df, output_dir=config['output_dir']):
    base_idf_path = config['idf_file_path']
    idd_path = config['iddfile']
    # Iterate over each row in the DataFrame
    for index, row in buildings_df.iterrows():
        # Load the IDF object for this building
        idf = IDF(base_idf_path)
        
        # Apply modifications using the refactored functions
        remove_building_object(idf)
        create_building_block(idf, row)
        update_construction_materials(idf, row)
        update_idf_for_fenestration(idf, row)
        assign_constructions_to_surfaces(idf)
        add_ground_temperatures(idf)
        add_internal_mass_to_all_zones_with_first_construction(idf, row)
        add_people_and_activity_schedules(idf, row)
        add_people_to_all_zones(idf, row)
        add_lights_to_all_zones(idf, row)
        generate_detailed_electric_equipment(idf, row)
        add_year_long_run_period(idf)
        add_hvac_schedules(idf, row)
        add_outdoor_air_and_zone_sizing_to_all_zones(idf)
        add_detailed_Hvac_system_to_zones(idf)
        check_and_add_idfobject(idf)
        
     
        
        # Save the modified IDF file with a new name to indicate it's modified
        modified_idf_path = os.path.join(output_dir, f"modified_building_{row['ogc_fid']}.idf")
        print(f"Saving IDF to: {modified_idf_path}")  # This will show the full path being used

        idf.save(modified_idf_path)
        
        print(f"Saved modified IDF for building {row['ogc_fid']}.")