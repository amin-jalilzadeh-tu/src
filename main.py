# main.py

# Import all necessary functions from the modules
from database_utils import validate_pc6, fetch_raw_data_for_pc6, create_or_replace_table
from f1_final_energy_label import assign_final_energy_labels
from f2_building_function import classify_building_functions
from f3_housing_type import map_housing_types
from f4_population_estimation import estimate_population
from idf_batch_processor import update_idf_and_save
from config import get_idf_config, get_db_config
from Runner_generator import simulate_all

def main():
    try:
        pc6_input = input("Enter the pc6 value to analyze: ")
        if validate_pc6(pc6_input):
            df = fetch_raw_data_for_pc6(pc6_input)
            table_name = "PC6_" + pc6_input.replace(" ", "_")
            create_or_replace_table(df, table_name)
            print(f"Data successfully added to {table_name}")
            assign_final_energy_labels(table_name)
            classify_building_functions(table_name)
            map_housing_types(table_name)
            estimate_population(table_name)
            update_idf_and_save(df, get_idf_config()['output_dir'])
            simulate_all()  # Call to run simulations

        else:
            print("Invalid or non-existing pc6 value.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

# import subprocess
# subprocess.run(["python", "C:\\Users\\aminj\\OneDrive\\Desktop\\EnergyPlus\\generator.py"], check=True)
