import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import sqlite3

def fetch_network_traffic_data(db_path, device_id):
    db_conn = sqlite3.connect(db_path)
    query = f"""
    SELECT traffic_date, traffic_value
    FROM network_traffic
    WHERE device_id = {device_id}
    ORDER BY traffic_date;
    """
    df = pd.read_sql_query(query, db_conn)
    db_conn.close()
    df['traffic_date'] = pd.to_datetime(df['traffic_date'])
    return df

def plot_network_traffic(df, device_id):
    plt.figure(figsize=(10, 6))
    plt.plot(df['traffic_date'], df['traffic_value'], marker='o', linestyle='-', color='b')
    plt.title(f"Network Traffic for Device {device_id} Over Time")
    plt.xlabel("Date")
    plt.ylabel("Traffic Value")

    # Format the date labels on the x-axis
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=1))
  # Explicitly set the interval 
    plt.xticks(rotation=45)  # You might want to keep this for better readability
    
    plt.tight_layout()
    plt.show()