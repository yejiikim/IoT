import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Define file paths for merged datasets
file_paths = [
    '/Users/gim-yeji/PycharmProjects/pythonProject/IoT/merged_data_collection/merged_data_2024-12-02.csv',
    '/Users/gim-yeji/PycharmProjects/pythonProject/IoT/merged_data_collection/merged_data_2024-12-03.csv',
    '/Users/gim-yeji/PycharmProjects/pythonProject/IoT/merged_data_collection/merged_data_2024-12-04.csv',
    '/Users/gim-yeji/PycharmProjects/pythonProject/IoT/merged_data_collection/merged_data_2024-12-06.csv',
    '/Users/gim-yeji/PycharmProjects/pythonProject/IoT/merged_data_collection/merged_data_2024-12-07.csv',
    '/Users/gim-yeji/PycharmProjects/pythonProject/IoT/merged_data_collection/merged_data_2024-12-08.csv',
    '/Users/gim-yeji/PycharmProjects/pythonProject/IoT/merged_data_collection/merged_data_2024-12-09.csv',
    '/Users/gim-yeji/PycharmProjects/pythonProject/IoT/merged_data_collection/merged_data_2024-12-11.csv'
]

# Ensure the analysis folder exists
output_folder = "/Users/gim-yeji/PycharmProjects/pythonProject/IoT/analysis"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    print(f"Created missing folder: {output_folder}")

# Combine all merged files into a single DataFrame
def load_data(files):
    """
    Load and combine all merged CSV files into a single DataFrame.
    """
    data = pd.concat([pd.read_csv(file) for file in files], ignore_index=True)
    print(f"Loaded {len(data)} rows from {len(files)} files.")
    return data


# Ensure datetime column is correctly formatted and extract analysis fields
def preprocess_data(data):
    """
    Preprocess data by formatting 'datetime' and extracting useful columns.
    """
    # Convert 'datetime' column to pandas datetime format
    data['datetime'] = pd.to_datetime(data['datetime'], errors='coerce')

    # Drop rows with invalid datetime values
    data = data.dropna(subset=['datetime'])

    # Extract hour for hourly traffic analysis
    data['hour'] = data['datetime'].dt.hour

    # Log preprocessing results
    print(f"Preprocessed data contains {len(data)} valid rows after cleaning.")
    return data


# Analyze and visualize traffic volume by hour
def analyze_traffic_by_hour(data):
    """
    Analyze traffic volume by hour and create a bar chart.
    """
    traffic_by_hour = data.groupby('hour')['line'].count()
    print("Traffic volume by hour:")
    print(traffic_by_hour)

    # Visualization: Traffic volume by hour
    plt.figure(figsize=(10, 6))
    sns.barplot(x=traffic_by_hour.index, y=traffic_by_hour.values, palette="Blues_d")
    plt.title("Traffic Volume by Hour")
    plt.xlabel("Hour of Day")
    plt.ylabel("Number of Departures")
    plt.grid()
    plt.savefig("/Users/gim-yeji/PycharmProjects/pythonProject/IoT/analysis/traffic_by_hour.png")
    plt.show()


# Analyze and visualize correlation between temperature and traffic volume
def analyze_weather_impact(data):
    """
    Analyze correlation between temperature and traffic volume.
    """
    correlation_data = data.groupby('temperature')['line'].count().reset_index()
    print("Correlation between temperature and traffic volume:")
    print(correlation_data.head())

    # Visualization: Correlation between temperature and traffic volume
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=correlation_data, x="temperature", y="line", color="green")
    plt.title("Correlation: Temperature vs. Traffic Volume")
    plt.xlabel("Temperature (°C)")
    plt.ylabel("Number of Departures")
    plt.grid()
    plt.savefig("/Users/gim-yeji/PycharmProjects/pythonProject/IoT/analysis/temp_vs_traffic.png")
    plt.show()


# Analyze and visualize route utilization
def analyze_route_utilization(data):
    """
    Analyze route utilization and create a bar chart for the top routes.
    """
    route_usage = data['line'].value_counts()
    print("Top 10 most utilized routes:")
    print(route_usage.head(10))

    # Visualization: Top 10 most utilized routes
    plt.figure(figsize=(12, 6))
    route_usage.head(10).plot(kind='bar', color='purple')
    plt.title("Top 10 Routes by Usage")
    plt.xlabel("Route")
    plt.ylabel("Number of Departures")
    plt.grid()
    plt.savefig("/Users/gim-yeji/PycharmProjects/pythonProject/IoT/analysis/route_usage.png")
    plt.show()


# Main execution flow
if __name__ == "__main__":
    # Load the data
    raw_data = load_data(file_paths)

    # Preprocess the data
    clean_data = preprocess_data(raw_data)

    # Perform analysis and visualizations
    analyze_traffic_by_hour(clean_data)
    analyze_weather_impact(clean_data)
    analyze_route_utilization(clean_data)