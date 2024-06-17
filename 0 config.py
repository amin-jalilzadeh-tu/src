# config.py

import json
import os

### For SQLALchemy
from urllib.parse import quote

def get_db_config():
    return {
        "dbname": os.getenv('DB_NAME', "DATALES_20240512"),
        "user": os.getenv('DB_USER', "postgres"),
        "password": os.getenv('DB_PASSWORD', "865990289"),
        "host": os.getenv('DB_HOST', "localhost") #leda.geodan.nl 5432
        
    }

#def get_conn_params():
#    config = get_db_config()
#    return f"dbname='{config['dbname']}' user='{config['user']}' password='{config['password']}' host='{config['host']}'"

#  for SQLALchemy
def get_conn_params():
    config = get_db_config()
    username = quote(config['user'])
    password = quote(config['password'])
    conn_string = f"postgresql://{username}:{password}@{config['host']}/{'config['dbname']}"
    print("Generated connection string:", conn_string)
    return conn_string

def get_idf_config():
    return {
        "iddfile": os.getenv('IDDFILE', "D:/EnergyPlus/Energy+.idd"),
        "idf_file_path": os.getenv('IDFFILE', "C:/Users/aminj/OneDrive/Desktop/EnergyPlus/Minimal.idf"),
        "epwfile": os.getenv('EPWFILE'),  # Load EPW file path from environment variables
        "output_dir": os.getenv('OUTPUT_DIR', "D:/Try21")
    }

# Export the table

# pg_dump -h leda.geodan.nl -U postgres -d Dataless -t all_databases_columns > table.sql

# pg_dump -h leda.geodan.nl -U postgres -d research -t nldata.gebouw > gebouw.sql

# pg_dump -h leda.geodan.nl -U postgres -d maquette_nl -t bag_latest.adres_plus > adres_plus.sql

# pg_dump -h leda.geodan.nl -U postgres -d research -t tomahawk.energypoint > energypoint.sql

# pg_dump -h leda.geodan.nl -U postgres -d research -t tomahawk.adres > adres.sql

# pg_dump -h leda.geodan.nl -U postgres -d maquette_nl -t dt_heerlen.cesium_buildings > cesium_buildings.sql


# maquette_nl cesium.bag3d_v20231008



# Import the table
# psql -h hostname -U username -d targetdatabase -f table.sql