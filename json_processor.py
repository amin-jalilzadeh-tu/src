import os
import pandas as pd
import json
import re

def process_output_files(output_dir, ):
    # Make sure the output output_dir exists, if not, create it
    #if not os.path.exists(output_dir):
    #    os.makedirs(output_dir)
    
    # Create dictionaries to hold all the data for each energy type
    natural_gas_data = {'timeIntervals': [], 'buildings': []}
    electricity_data = {'timeIntervals': [], 'buildings': []}
    total_energy_data = {'timeIntervals': [], 'buildings': []}

    # Define a regex to extract the BAG ID from filenames
    bag_id_pattern = re.compile(r"modified_building_NL.IMBAG.Pand.(\d+)Meter.csv")

    # Iterate through all files in the output_dir
    for filename in os.listdir(output_dir):
        if filename.startswith('modified_building') and filename.endswith('Meter.csv'):
            bag_id_match = bag_id_pattern.search(filename)
            if not bag_id_match:
                continue
            bag_id = bag_id_match.group(1)

            # Read the CSV file
            file_path = os.path.join(output_dir, filename)
            df = pd.read_csv(file_path, usecols=['Date/Time', 'Electricity:Facility [J](TimeStep)'])
            
            # Assume natural gas consumption as zero for now
            df['NaturalGas:Facility [J](TimeStep)'] = 0
            df['TotalEnergy [J](TimeStep)'] = df['Electricity:Facility [J](TimeStep)'] + df['NaturalGas:Facility [J](TimeStep)']

            # Rename columns
            df.rename(columns={
                'Date/Time': 'Time',
                'NaturalGas:Facility [J](TimeStep)': 'Natural Gas Consumption (J)',
                'Electricity:Facility [J](TimeStep)': 'Electricity Consumption (J)',
                'TotalEnergy [J](TimeStep)': 'Total Energy (J)'
            }, inplace=True)

            # If time intervals are empty, fill them
            if not natural_gas_data['timeIntervals']:
                natural_gas_data['timeIntervals'] = df['Time'].tolist()
                electricity_data['timeIntervals'] = df['Time'].tolist()
                total_energy_data['timeIntervals'] = df['Time'].tolist()

            # Append the data
            natural_gas_data['buildings'].append({'bagId': bag_id, 'data': df['Natural Gas Consumption (J)'].tolist()})
            electricity_data['buildings'].append({'bagId': bag_id, 'data': df['Electricity Consumption (J)'].tolist()})
            total_energy_data['buildings'].append({'bagId': bag_id, 'data': df['Total Energy (J)'].tolist()})

    # Save the data to JSON files
    with open(os.path.join(output_dir, 'natural_gas_consumption.json'), 'w') as f:
        json.dump(natural_gas_data, f, indent=4)
    with open(os.path.join(output_dir, 'electricity_consumption.json'), 'w') as f:
        json.dump(electricity_data, f, indent=4)
    with open(os.path.join(output_dir, 'total_energy.json'), 'w') as f:
        json.dump(total_energy_data, f, indent=4)

# Define the output_dir to read files from and where to save the JSON files
#   output_dir = 'D:/Try21'
#   output_dir = 'D:/Output'  # Change this to your desired output output_dir

#    process_output_files(output_dir, output_dir)
