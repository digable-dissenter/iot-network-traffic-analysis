# IoT Network Traffic Analysis

This was a coding assessment presented to me by Prescient back in February 2022. I did dismally. Here I am, attempting it again, 2-and-a-half years later. 

This project analyses network traffic data from IoT devices. The project includes ETL (Extract, Transform, Load) processing to clean and organise raw CSV data, then visualises traffic trends over time using Matplotlib and Plotly. It supports multi-device comparisons, traffic distribution analysis, and interactive time-series plots.

## Features
 - ETL processing of IoT device traffic data from CSV files into a SQLite database.
 - Visualisation of traffic trends for individual devices and multiple devices over time.
 - Histograms to analyse the distribution of traffic values.
 - Interactive time-series analysis using Plotly.
 - Data aggregation for daily, weekly, or monthly traffic trends.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/digable-dissenter/iot-network-traffic-analysis.git
```

2. Navigate into the project directory:
```bash
cd iot-network-traffic-analysis
```

3. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate # On Windows use `venv\Scripts\activate`
```

4. Install the dependencies
```bash
pip install -r requirements.txt
```

5. Run ETL process
```bash
python main.py --db iot_data.db --csv_folder data --meta data/device_meta.txt
```

6. (Optional): Run interactive Plotly visualisations in a Jupyter notebook or another Python environment.

## **Usage:**
Run the ETL process to load and process IoT traffic data from CSV files into the SQLite database:

```bash
python main.py --db iot_data.db --csv_folder data --meta data/device_meta.txt
```

## **Project Structure**

```bash
iot-network-traffic-analysis/
│
├── data/                       # Folder containing CSV files and device metadata
│   ├── iot_5.csv               # Example CSV file
│   ├── device_meta.txt         # Metadata file for devices
│
├── scripts/                    # Python scripts for ETL and visualization
│   ├── main.py                 # Entry point for running the ETL process
│   ├── etl.py                  # ETL logic for processing device traffic data
│   ├── database.py             # Functions for interacting with the SQLite database
│   ├── visualizations.py       # Visualization functions (Matplotlib, Plotly)
│
├── notebooks/                  # Jupyter notebooks for interactive data exploration
│   ├── analysis.ipynb          # Example notebook for exploring the data
│
├── tests/                      # Unit and integration tests
│   ├── test_etl.py             # Tests for the ETL process
│
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
└── iot_data.db                 # SQLite database (if stored locally)




## Future Enhancements
 - Implementing more visualisations
 - Implement unit testing
 - Web-based dashboard for visualising IoT traffic trends.