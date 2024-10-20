import datetime
from logging_config.logging_config import setup_logger
import sqlite3
import sys
from util.timing import log_execution_time
import time

logger = setup_logger()

# Adapter to convert Python date to a string
def adapt_date(date):
    return date.isoformat()

# Converter to convert a string back to Python date
def convert_date(date_str):
    return datetime.datetime.strptime(date_str.decode("utf-8"), "%Y-%m-%d").date()

# Register the adapters and converters with sqlite3
sqlite3.register_adapter(datetime.date, adapt_date)
sqlite3.register_converter("DATE", convert_date)

@log_execution_time
def connect_to_db(db_path='iot_data.db'):
    # Connect to SQLite database
    try:
        db_conn = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        db_conn.execute("PRAGMA foreign_keys = ON;") # Enable FOREIGN KEYS
        logger.info("Connection to database established.")
    except sqlite3.Error as e:
        logger.error(f"Error connecting to database: {e}", exc_info=True)
        sys.exit(1)
    return db_conn

# Functions to create SQLite table
def create_meta_devices_table(cursor):
    drop_query = """
    DROP TABLE IF EXISTS device_meta;
    """
    create_query = """
    CREATE TABLE device_meta (
        device_id INTEGER,
        device_name TEXT,
        PRIMARY KEY (device_id)
    );
    """
    try:
        cursor.execute(drop_query)
        logger.info("device_meta table dropped.")
    except sqlite3.Error as e:
        logger.error(f"Error dropping device_meta table: {e}", exc_info=True)

    try:
        cursor.execute(create_query)
        logger.info("device_meta table created.")
    except sqlite3.Error as e:
        logger.error(f"Error creating device_meta table: {e}", exc_info=True)   


def create_iot_device_table(cursor):
    drop_query = """
    DROP TABLE IF EXISTS network_traffic;
    """
    create_query = """    
    CREATE TABLE network_traffic (
        device_id INTEGER,
        traffic_date DATE,
        traffic_value FLOAT,
        PRIMARY KEY (device_id, traffic_date),
        FOREIGN KEY (device_id) REFERENCES device_meta (device_id) 
    );
    """

    try:
        cursor.execute(drop_query)
        logger.info("network_traffic table dropped.")
    except sqlite3.Error as e:
        logger.error(f"Error dropping network_traffic table: {e}", exc_info=True)

    try:
        cursor.execute(create_query)
        logger.info("network_traffic table created.")
    except sqlite3.Error as e:
        logger.error(f"Error creating network_traffic table: {e}", exc_info=True)

@log_execution_time
def create_tables(cursor):
    create_meta_devices_table(cursor)
    create_iot_device_table(cursor)

# Functions to insert data into SQLite table
@log_execution_time
def insert_device_meta(cursor, data):
    insert_query = """
    INSERT INTO device_meta (device_id, device_name)
    VALUES (?, ?);
    """   
    try:
        logger.info(f"Inserting {len(data)} rows into device_meta.")
        cursor.executemany(insert_query, data)
        logger.info(f"Inserted {len(data)} rows into device_meta table.")
    except sqlite3.Error as e:
        logger.error(f"Error inserting data into device_meta table: {e}", exc_info=True)
    
@log_execution_time
def insert_iot_data(cursor, data, device_id):    
    insert_query = """
    INSERT INTO network_traffic (device_id, traffic_date, traffic_value)
    VALUES(?, ?, ?)
    """
    try:   
        logger.info(f"Inserting {len(data)} rows for device_id {device_id} into network_traffic table.")
        cursor.executemany(insert_query, data)
        logger.info(f"Inserted {len(data)} rows for device_id {device_id} into network_traffic table.")
    except sqlite3.Error as e:
        logger.error(f"Error inserting data into network_traffic table: {e}", exc_info=True)