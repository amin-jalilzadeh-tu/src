import os

idf_file_path = os.getenv('IDDFILE')
if idf_file_path is None:
    raise ValueError("IDDFILE environment variable is not set")
else:
    print(f"IDDFILE is set to: {idf_file_path}")
