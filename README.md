# Eplus_202405

## Overview

This project is designed to run energy simulations using EnergyPlus and PostgreSQL, fully containerized via Docker. The necessary data is included in the `data` folder, and configurations can be adjusted via the `.env` file if needed.

## Setup Instructions

1. **Clone the repository**:
   ```sh
   git clone https://github.com/yourusername/Eplus_202405.git
   cd Eplus_202405/src

Build and Run the Docker Containers:
```sh
Copy code
docker-compose down
docker-compose build
docker-compose up

## Data
The project connects to a PostgreSQL database set up in pgAdmin (database name: Dataless).
The necessary data files are located in the data folder.
Configuration details (currently no need for changes) are stored in the .env file.

## Running the Simulation
The API is set to run with the hardcoded test data :


## Start the simulation:
The API is designed to receive the name of a district. However, for now, it runs with predefined test data.
Upon execution, the simulation will start and results will be saved in the output folder.
At the end of the simulation, all necessary data will be integrated into JSON format.


## Debugging
For testing purposes, numerous print statements are included in the code to help track errors.
