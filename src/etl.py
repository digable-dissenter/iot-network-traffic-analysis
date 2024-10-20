
from database import insert_iot_data
import json
from logging_config.logging_config import setup_logger
import pandas as pd
from pathlib import Path
from util.timing import log_execution_time
import time

logger = setup_logger()

# Function to load metadata frim the device_meta.txt file
@log_execution_time
def load_device_meta(file_path):
    # Load device metadata from JSON file
    file_path = Path(file_path)
    logger.info(f"Loading device metadata from {file_path}")
    # Ensure file path is correctly joined with the current directory
    # if file_path.exists():
    try:
        with open(file_path, 'r') as f:
            device_meta = json.load(f)
            device_mapping = {device['id']: device['name'] for device in device_meta}
            logger.info("Device metatdata file opened successfully")
            return device_mapping
    except FileNotFoundError as e:
        logger.error(f"Device metadata file not found: {e}", exc_info=True)
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON in device metadata file: {e}", exc_info=True)


# ETL process to extract, transform, and load CSV data into SQLite table
@log_execution_time
def process_csv_files(cursor, device_mapping, csv_file):
    start_time = time.time()

    device_id = int(csv_file.split('_')[1].split('.')[0]) # Extract device ID from CSV file name
    logger.info(f"Processing CSV file: {csv_file} for device_id: {device_id}")

    # Check if the device_id exists in device_meta
    if device_id not in device_mapping:
        logger.warning(f"Warning: device_id {device_id} not found in device_meta, skipping...")        
        return
        
    # Load CSV into a dataframe
    df = pd.read_csv(csv_file)
    df['traffic_date'] = pd.to_datetime(df['date']).dt.date
    df['traffic_value'] = df['traffic'].astype(float)

    # Prepare data for insertion
    data_to_insert = [(device_id, row['traffic_date'], row['traffic_value'])
                                    for _, row in df.iterrows()]
        
    # Log the number of rows processed
    logger.info(f"CSV file: {csv_file} contains {len(df)} rows for device_id {device_id} from file: {csv_file}.")
        
    # Insert data into the database
    insert_iot_data(cursor, data_to_insert, device_id)  