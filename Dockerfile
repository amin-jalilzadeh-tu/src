# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    wget \
    unzip \
    tk \
    tcl \
    && rm -rf /var/lib/apt/lists/*

# Copy just the requirements.txt first to leverage Docker cache
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Define EnergyPlus version
ARG ENERGYPLUS_VERSION="22.2.0"
ARG ENERGYPLUS_SHA="c249759bad"
ARG ENERGYPLUS_INSTALL_VERSION="22-2-0"

# Install EnergyPlus
RUN wget "https://github.com/NREL/EnergyPlus/releases/download/v${ENERGYPLUS_VERSION}/EnergyPlus-${ENERGYPLUS_VERSION}-${ENERGYPLUS_SHA}-Linux-Ubuntu20.04-x86_64.tar.gz" && \
    tar -xzvf "EnergyPlus-${ENERGYPLUS_VERSION}-${ENERGYPLUS_SHA}-Linux-Ubuntu20.04-x86_64.tar.gz" -C /usr/local/ && \
    rm "EnergyPlus-${ENERGYPLUS_VERSION}-${ENERGYPLUS_SHA}-Linux-Ubuntu20.04-x86_64.tar.gz"

# Set environment variables from the .env file
ENV PATH="/usr/local/EnergyPlus-${ENERGYPLUS_INSTALL_VERSION}/:$PATH" \
    IDDFILE="${IDDFILE}" \
    IDFFILE="${IDFFILE}" \
    EPWFILE="${EPWFILE}" \
    OUTPUT_DIR="${OUTPUT_DIR}" \
    DB_NAME="${DB_NAME}" \
    DB_USER="${DB_USER}" \
    DB_PASSWORD="${DB_PASSWORD}" \
    DB_HOST="${DB_HOST}"

# Copy the rest of the application
COPY . .

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Command to run the application
CMD ["python", "main.py"]
