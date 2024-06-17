
import os
import pandas as pd
from eppy.modeleditor import IDF

def modify_idf_for_detailed_output(idf):
    energy_variables = [
        "Facility Total Electric Demand Power",
        "Facility Total Gas Demand Power",
        "Electricity:Building"
    ]
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
    except FileNotFoundError:
        print(f"Output file {output_file} not found. Please check the simulation ran successfully.")
        return
    columns_of_interest = ['Date/Time', 'Electricity:Facility [W]', 'Gas:Facility [W]']
    filtered_df = df[columns_of_interest]
    print(filtered_df.head())

def run_energyplus_simulation(idf_path, epwfile):
    IDF.setiddname(iddfile)
    idf = IDF(idf_path, epwfile)
    modify_idf_for_detailed_output(idf)
    options = make_eplaunch_options(idf, idf_path)
    idf.run(**options)
    process_output_files(options['output_directory'], options['output_prefix'])

def main():
    global iddfile
    iddfile = "D:/EnergyPlus/Energy+.idd"
    idf_directory = "D:/EnergyPlus_Output"
    epwfile = "C:/Users/aminj/OneDrive/Desktop/EnergyPlus/Weather/NLD_Amsterdam.062400_IWEC.epw"
    for filename in os.listdir(idf_directory):
        if filename.endswith(".idf"):
            idf_path = os.path.join(idf_directory, filename)
            run_energyplus_simulation(idf_path, epwfile)

if __name__ == '__main__':
    main()
