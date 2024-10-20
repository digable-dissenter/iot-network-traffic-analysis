import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Run ETL process.")
    parser.add_argument('--db', default='iot_data.db', help="Path to SQLite database.")
    parser.add_argument('--meta', default='data/device_meta.txt', help='Path to device metadata file.')
    parser.add_argument('--csv_folder', default='data/', help='Folder containing CSV files.')
    return parser.parse_args()