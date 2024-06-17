import os
import pandas as pd
from eppy.modeleditor import IDF
from concurrent.futures import ProcessPoolExecutor

def modify_idf_for_detailed_output(idf):
    energy_variables = [
        "Facility Total Electric Demand Power",
        "Facility Total Gas Demand Power",
        "Electricity:Building"
    ]
    #print("Adding output variables...")
    for variable in energy_variables:
        idf.newidfobject(
            'OUTPUT:VARIABLE',
            Key_Value='*',
            Variable_Name=variable,
            Reporting_Frequency='timestep'
        )

def make_eplaunch_options(idf, fname):
    options = {
        'output_prefix': os.path.basename(fname).split('.')[0],
        'output_suffix': 'C',
        'output_directory': os.path.dirname(fname),
        'readvars': True,
        'expandobjects': True,
    }
    return options

def process_output_files(output_directory, output_prefix):
    output_file = os.path.join(output_directory, f"{output_prefix}eplusout.csv")
    try:
        df = pd.read_csv(output_file)
        columns_of_interest = ['Date/Time', 'Electricity:Facility [W]', 'Gas:Facility [W]']
        filtered_df = df[columns_of_interest]
        #print(filtered_df.head())
    except FileNotFoundError:
        print(f"Output file {output_file} not found. Please check the simulation ran successfully.")
    except Exception as e:
        print(f"Error processing output file: {e}")

def run_energyplus_simulation(args, iddfile):
    idf_path, epwfile = args
    try:
        #print(f"Running simulation for: {idf_path}")
        IDF.setiddname(iddfile)
        idf = IDF(idf_path, epwfile)
        modify_idf_for_detailed_output(idf)
        options = make_eplaunch_options(idf, idf_path)
        idf.run(**options)
        process_output_files(options['output_directory'], options['output_prefix'])
    except Exception as e:
        print(f"Error during simulation for {idf_path}: {e}")

def main():
    iddfile = "D:/EnergyPlus/Energy+.idd"  # Correct path to your Energy+.idd
    idf_directory = "D:/EnergyPlus_Output"
    epwfile = "C:/Users/aminj/OneDrive/Desktop/EnergyPlus/Weather/NLD_Amsterdam.062400_IWEC.epw"

    idf_paths = [os.path.join(idf_directory, filename) for filename in os.listdir(idf_directory) if filename.endswith(".idf")]
    
    if not idf_paths:
        print("No IDF files found. Check your directory.")
        return

    # Use ProcessPoolExecutor to manage parallel processing
    with ProcessPoolExecutor() as executor:
        executor.map(run_energyplus_simulation, [(path, epwfile) for path in idf_paths], [iddfile]*len(idf_paths))

if __name__ == '__main__':
    main()
