import os
from eppy.modeleditor import IDF
from dask.distributed import Client

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

def run_simulation(file_details):
    """ Runs the simulation for a given IDF file, ensuring the IDD file is set. """
    idf_path, epwfile, iddfile = file_details
    
    # Check if the EPW and IDD files exist before proceeding
    if not epwfile or not os.path.exists(epwfile):
        return f"EPW file not found or not specified: {epwfile}"
    if not iddfile or not os.path.exists(iddfile):
        return f"IDD file not found or not specified: {iddfile}"

    try:
        IDF.setiddname(iddfile)
        idf = IDF(idf_path, epwfile)
        modify_idf_for_detailed_output(idf)
        options = make_eplaunch_options(idf, idf_path)
        idf.run(**options)
        return f"Simulation completed for {idf_path}"
    except Exception as e:
        return f"Error during simulation for {idf_path}: {e}"

def get_file_paths():
    """ Retrieves file paths using local environment variables on each worker. """
    idf_directory = os.getenv('IDF_DIRECTORY')
    epwfile = os.getenv('EPWFILE')
    iddfile = os.getenv('IDDFILE', "C:/EnergyPlusV23-2-0/Energy+.idd")
    
    if not all([idf_directory, epwfile, iddfile]):
        raise EnvironmentError(f"Environment variables not all set: IDF_DIRECTORY={idf_directory}, EPWFILE={epwfile}, IDDFILE={iddfile}")
    
    files = [os.path.join(idf_directory, f) for f in os.listdir(idf_directory) if f.endswith('.idf')]
    return [(f, epwfile, iddfile) for f in files]

def main():
    client = Client("tcp://192.168.0.105:8786")
    print("Connected to client:", client)

    workers = list(client.scheduler_info()["workers"])
    print("Workers available:", workers)

    try:
        file_paths = client.submit(get_file_paths).result()
    except Exception as e:
        print(f"Failed to get file paths: {e}")
        return
    
    # Distribute tasks manually across workers
    futures = []
    for i, file_detail in enumerate(file_paths):
        worker_url = workers[i % len(workers)]  # Round-robin distribution
        futures.append(client.submit(run_simulation, file_detail, workers=[worker_url]))

    results = client.gather(futures)
    for result in results:
        print(result)

if __name__ == '__main__':
    main()
