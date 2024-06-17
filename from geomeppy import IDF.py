from geomeppy import IDF
import os
import pandas as pd
import psycopg2
import numpy as np
import shutil
import subprocess
from config import get_conn_params, get_idf_config
from sqlalchemy import create_engine

# Use centralized configurations
config = get_idf_config()
conn_params = get_conn_params()

# Database connection and building data fetching
def fetch_buildings_data(table_name, conn_params):
    print("Using connection string:", conn_params)  # This will display the connection string
    engine = create_engine(conn_params)
    query = f"SELECT * FROM {table_name};"
    buildings_df = pd.read_sql_query(query, engine)
    engine.dispose()
    return buildings_df

IDF.setiddname(config['iddfile'])
idf = IDF(config['idf_file_path'])

# Directory setup
if not os.path.exists(config['output_dir']):
    os.makedirs(config['output_dir'])













def get_conn_params():
    config = get_db_config()
    # URL encode username and password to handle special characters
    username = quote(config['user'])
    password = quote(config['password'])
    # Include the port if it's not the default, or just remove the port segment if using default (5432)
    return f"postgresql://{username}:{password}@{config['host']}:5432/{config['dbname']}"










def get_idf_config():
    return {
        "iddfile": os.getenv('IDDFILE', "D:/EnergyPlus/Energy+.idd"),
        "idf_file_path": os.getenv('IDFFILE', "C:/Users/aminj/OneDrive/Desktop/EnergyPlus/Minimal.idf"),
        "epwfile": os.getenv('EPWFILE'),  # Load EPW file path from environment variables
        "output_dir": os.getenv('OUTPUT_DIR', "D:/Try21")
    }







        modified_idf_path = os.path.join(output_dir, f"modified_building_{row['ogc_fid']}.idf")
        idf.save(modified_idf_path)
        
        print(f"Saved modified IDF for building {row['ogc_fid']}.")
    



































    import os
import pandas as pd
from eppy.modeleditor import IDF
from multiprocessing import Pool
from config import get_idf_config  # Import configuration function

def modify_idf_for_detailed_output(idf):
    """ Adds detailed output variables to the IDF file. """
    variables = [
        "Facility Total Electric Demand Power",
        "Facility Total Gas Demand Power",
        "Electricity:Building"
    ]
    for variable in variables:
        idf.newidfobject(
            'OUTPUT:VARIABLE',
            Key_Value='*',
            Variable_Name=variable,
            Reporting_Frequency='timestep'
        )

def make_eplaunch_options(idf, fname):
    """ Sets options similar to those used in EPLaunch. """
    return {
        'output_prefix': os.path.basename(fname).split('.')[0],
        'output_suffix': 'C',
        'output_directory': os.path.dirname(fname),
        'readvars': True,
        'expandobjects': True,
    }

def run_simulation(args):
    idf_path, epwfile, iddfile = args
    try:
        IDF.setiddname(iddfile)
        idf = IDF(idf_path, epwfile)
        modify_idf_for_detailed_output(idf)
        options = make_eplaunch_options(idf, idf_path)
        idf.run(**options)
        print(f"Simulation completed for {idf_path}")
    except Exception as e:
        print(f"Error during simulation for {idf_path}: {e}")

def generate_simulations(idf_directory, epwfile, iddfile):
    """ Yields a tuple of arguments needed for each simulation. """
    for filename in os.listdir(idf_directory):
        if filename.endswith(".idf"):
            idf_path = os.path.join(idf_directory, filename)
            yield (idf_path, epwfile, iddfile)

def simulate_all():
    config = get_idf_config()  # Use configuration settings
    idf_directory = config['output_dir']
    epwfile = config['epwfile']
    iddfile = config['iddfile']
    num_workers = 4  # Adjust based on your CPU cores

    with Pool(num_workers) as pool:
        pool.map(run_simulation, generate_simulations(idf_directory, epwfile, iddfile))

if __name__ == '__main__':
    simulate_all()
