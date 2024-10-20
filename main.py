import concurrent.futures
from util.config import parse_args
import src.database as db
import src.etl as etl
from logging_config.logging_config import setup_logger
import os
import sqlite3
from util.timing import log_execution_time
import time

logger = setup_logger()

@log_execution_time
def run_etl_process():
    try:
        start_time = time.time()
        # Parse command-line arguments
        args = parse_args()

        # Use the arguments
        db_path = args.db
        meta_file = args.meta
        csv_folder = args.csv_folder

        # Connect to database
        db_conn = db.connect_to_db(db_path)

        cursor = db_conn.cursor()
        db_conn.execute("BEGIN") # Start transaction

        # Create tables
        db.create_meta_devices_table(cursor)
        db.create_iot_device_table(cursor)

        # Load device metadata
        device_mapping = etl.load_device_meta(meta_file)
        # Run ETL process
        # Insert device metadata into device_meta table
        device_meta_data = [(device_id, device_name) for device_id, device_name in device_mapping.items()]
        db.insert_device_meta(cursor, device_meta_data)

        # Commit metadata before processing traffic data
        db_conn.commit()
        cursor.close()
        db_conn.close() # Close the initial connection

        # Parallel processing of CSV files 
        csv_files = [os.path.join(csv_folder, f) for f in os.listdir(csv_folder) if f.endswith('.csv')] # Just the file paths
        file_durations = [] # To store the time taken for each file
        '''
            SQLite, by default, doesn't support sharing cursors between threads.
            Need to create a new connection and cursor in each thread to avoid potential conflicts.
        '''
        def process_file(file_path):
            try:
                start_file_time = time.time()
                conn = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES) # New connection for each file
                cursor = conn.cursor()  # New cursor for each file
                etl.process_csv_files(cursor, device_mapping, file_path)
                conn.commit()
                cursor.close()
                conn.close()
                
                # Calculate and store the time taken to process the file
                file_duration = time.time() - start_file_time
                file_durations.append(file_duration)
                logger.info(f'Processed {file_path} in {file_duration:.4f} seconds.')
            except sqlite3.Error as e:
                logger.error(f"Error processing file {file_path}: {e}", exc_info=True)
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(process_file, csv_files)

        processed_files = [f for f in os.listdir(csv_folder) if f.endswith('.csv')]
        skipped_files = [f for f in processed_files if int(f.split('_')[1].split('.')[0]) not in device_mapping]         

        # Calculate average time per file
        average_file_time = sum(file_durations) / len(file_durations) if file_durations else 0
        logger.info(f'Average time per file: {average_file_time:.4f} seconds.')

        total_duration = time.time() - start_time   
        logger.info(f"ETL process completed in {total_duration:.4f} seconds.")   
        logger.info(f"Processed {len(processed_files)} CSV files, skipped {len(skipped_files)} due to missing device_ids.") 
    
    except sqlite3.IntegrityError as e:
        db_conn.rollback() # Rollback transaction on error
        logger.error(f"Transaction failed: {e}")
    finally:
        db_conn.close()


if __name__ == "__main__":
    run_etl_process()