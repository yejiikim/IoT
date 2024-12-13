import pandas as pd
import matplotlib.pyplot as plt

# Define file paths
file_paths = [
    '/Users/gim-yeji/PycharmProjects/pythonProject/IoT/transport_data_collection/transport_data_2024-12-02.csv',
    '/Users/gim-yeji/PycharmProjects/pythonProject/IoT/transport_data_collection/transport_data_2024-12-03.csv',
    '/Users/gim-yeji/PycharmProjects/pythonProject/IoT/transport_data_collection/transport_data_2024-12-04.csv',
    '/Users/gim-yeji/PycharmProjects/pythonProject/IoT/transport_data_collection/transport_data_2024-12-06.csv',
    '/Users/gim-yeji/PycharmProjects/pythonProject/IoT/transport_data_collection/transport_data_2024-12-07.csv',
    '/Users/gim-yeji/PycharmProjects/pythonProject/IoT/transport_data_collection/transport_data_2024-12-08.csv',
    '/Users/gim-yeji/PycharmProjects/pythonProject/IoT/transport_data_collection/transport_data_2024-12-09.csv',
    '/Users/gim-yeji/PycharmProjects/pythonProject/IoT/transport_data_collection/transport_data_2024-12-11.csv'
]

# Combine all files into a single DataFrame
data_frames = [pd.read_csv(file) for file in file_paths]
transport_data = pd.concat(data_frames, ignore_index=True)

print(transport_data.head())
# Convert the 'best_departure_estimate' column to datetime format
# Ensure errors are coerced to avoid issues with invalid formats
transport_data['best_departure_estimate'] = pd.to_datetime(
    transport_data['best_departure_estimate'], format='%H:%M', errors='coerce'
)

# Extract the hour of the day from the 'best_departure_estimate'
transport_data['hour'] = transport_data['best_departure_estimate'].dt.hour

# Group data by 'line' and 'hour' to count the number of departures
line_hour_data = transport_data.groupby(['line', 'hour']).size().reset_index(name='num_departures')

# Pivot the table for better visualization
line_hour_pivot = line_hour_data.pivot(index='line', columns='hour', values='num_departures').fillna(0)

# Preview the pivot table
print(line_hour_pivot.head())

# Create a heatmap to visualize departures by line and hour
plt.figure(figsize=(12, 8))
plt.imshow(line_hour_pivot, aspect='auto', cmap='coolwarm', interpolation='nearest')
plt.colorbar(label='Number of Departures')
plt.xticks(ticks=range(len(line_hour_pivot.columns)), labels=line_hour_pivot.columns, fontsize=10)
plt.yticks(ticks=range(len(line_hour_pivot.index)), labels=line_hour_pivot.index, fontsize=10)
plt.title('Heatmap of Departures by Line and Hour', fontsize=16)
plt.xlabel('Hour of the Day', fontsize=14)
plt.ylabel('Line', fontsize=14)
plt.show()

# Analyze top 3 routes by total departures
top_routes = transport_data.groupby('line')['hour'].count().nlargest(3).reset_index()
top_routes.columns = ['line', 'total_departures']

# Analyze busiest time period (hours) for the top 3 routes
top_routes_hours = transport_data[transport_data['line'].isin(top_routes['line'])]
busiest_hours = top_routes_hours.groupby(['line', 'hour']).size().reset_index(name='num_departures')
busiest_hours = busiest_hours.sort_values(by=['line', 'num_departures'], ascending=[True, False]).groupby('line').head(1)

# Merge results for a summarized table
top_routes_summary = pd.merge(top_routes, busiest_hours, on='line')
top_routes_summary.columns = ['line', 'total_departures', 'busiest_hour', 'departures_in_busiest_hour']

# Display the top 3 routes summary
print("Top 3 Routes Summary:")
print(top_routes_summary)

# Visualize the total departures for top 3 routes
plt.figure(figsize=(8, 6))
plt.bar(top_routes_summary['line'], top_routes_summary['total_departures'], color='skyblue')
plt.title('Top 3 Routes by Total Departures', fontsize=16)
plt.xlabel('Route', fontsize=14)
plt.ylabel('Total Departures', fontsize=14)
plt.grid(axis='y')
plt.show()

# Visualize busiest hours for the top 3 routes
plt.figure(figsize=(8, 6))
plt.bar(top_routes_summary['line'], top_routes_summary['departures_in_busiest_hour'], color='orange')
plt.title('Busiest Hour Departures for Top 3 Routes', fontsize=16)
plt.xlabel('Route', fontsize=14)
plt.ylabel('Departures in Busiest Hour', fontsize=14)
plt.grid(axis='y')
plt.show()