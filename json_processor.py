import os
import pandas as pd
import json
import re
from datetime import datetime

def process_output_files(output_dir, pc6):
    # Ensure the output directory exists, if not, create it
    #if not os.path.exists(output_dir):
    #    os.makedirs(output_dir)
    
    # Today's date in YYYY-MM-DD format
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"Ensured output directory exists: {output_dir}")

    # Create dictionaries to hold all the data for each energy type
    natural_gas_data = {'timeIntervals': [], 'buildings': []}
    electricity_data = {'timeIntervals': [], 'buildings': []}
    total_energy_data = {'timeIntervals': [], 'buildings': []}

    # Define a regex to extract the BAG ID from filenames
    bag_id_pattern = re.compile(r"modified_building_NL.IMBAG.Pand.(\d+)Meter.csv")

    # Iterate through all files in the directory
    for filename in os.listdir(output_dir):
        if filename.startswith('modified_building') and filename.endswith('Meter.csv'):
            print(f"Processing file: {filename}")
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


    file_paths = []
    for energy_type, content in [('natural_gas', natural_gas_data), ('electricity', electricity_data), ('total_energy', total_energy_data)]:
        file_path = os.path.join(output_dir, f"{pc6}_{energy_type}_{today}.json")
        print(f"Writing to file: {file_path}")
        with open(file_path, 'w') as f:
            json.dump(content, f, indent=4)
        file_paths.append(file_path)

    return file_paths


    # Save the data to JSON files with the pc6 and date in the filename
  #  with open(os.path.join(output_dir, f'{pc6}_natural_gas_{today}.json'), 'w') as f:
  #      json.dump(natural_gas_data, f, indent=4)
  #  with open(os.path.join(output_dir, f'{pc6}_electricity_{today}.json'), 'w') as f:
  #      json.dump(electricity_data, f, indent=4)
  #  with open(os.path.join(output_dir, f'{pc6}_total_energy_{today}.json'), 'w') as f:
  #      json.dump(total_energy_data, f, indent=4)


#output_dir="D:\Try21"
#pc6 = "2628zl"
#process_output_files(output_dir, pc6)