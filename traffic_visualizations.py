import pandas as pd
import matplotlib.pyplot as plt
import os

# Define paths
DATA_PATH = "/Users/gim-yeji/PycharmProjects/pythonProject/IoT/merged_data_collection/"
VISUALIZATION_PATH = "/Users/gim-yeji/PycharmProjects/pythonProject/IoT/static/visualizations/"

# Ensure the visualization folder exists
os.makedirs(VISUALIZATION_PATH, exist_ok=True)

# Load merged data
file_paths = [os.path.join(DATA_PATH, f) for f in os.listdir(DATA_PATH) if f.endswith('.csv')]
merged_data = pd.concat([pd.read_csv(file) for file in file_paths], ignore_index=True)

# Convert 'datetime' column to datetime type
merged_data['datetime'] = pd.to_datetime(merged_data['datetime'])

# Extract hour for traffic by hour visualization
merged_data['hour'] = merged_data['datetime'].dt.hour


# 1. Traffic by Hour Visualization
def plot_traffic_by_hour(data, output_path):
    traffic_by_hour = data.groupby('hour').size()

    plt.figure(figsize=(10, 6))
    traffic_by_hour.plot(kind='bar', color='skyblue')
    plt.title("Traffic Volume by Hour of the Day")
    plt.xlabel("Hour of the Day")
    plt.ylabel("Number of Traffic Events")
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

    print(f"Traffic by Hour visualization saved at {output_path}")


# 2. Top Routes Visualization
def plot_top_routes(data, output_path):
    top_routes = data['line'].value_counts().head(5)  # Top 5 routes

    plt.figure(figsize=(10, 6))
    top_routes.plot(kind='bar', color='orange')
    plt.title("Top 5 Routes by Traffic Volume")
    plt.xlabel("Route")
    plt.ylabel("Number of Traffic Events")
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

    print(f"Top Routes visualization saved at {output_path}")


# Generate visualizations
plot_traffic_by_hour(merged_data, os.path.join(VISUALIZATION_PATH, "traffic_by_hour.png"))
plot_top_routes(merged_data, os.path.join(VISUALIZATION_PATH, "top_routes.png"))