import pandas as pd
import os

def merge_datasets(transport_folder, weather_folder, output_folder):
    """
    Merge Transport and Weather datasets based on the 'datetime' column.
    """
    transport_files = sorted(
        [os.path.join(transport_folder, file) for file in os.listdir(transport_folder) if file.endswith('.csv')]
    )
    weather_files = sorted(
        [os.path.join(weather_folder, file) for file in os.listdir(weather_folder) if file.endswith('.csv')]
    )

    if len(transport_files) != len(weather_files):
        print("Error: Mismatch in number of Transport and Weather files.")
        return

    os.makedirs(output_folder, exist_ok=True)

    for transport_file, weather_file in zip(transport_files, weather_files):
        transport_data = pd.read_csv(transport_file)
        weather_data = pd.read_csv(weather_file)

        # Ensure datetime columns are correctly formatted
        transport_data['datetime'] = pd.to_datetime(transport_data['datetime'])
        weather_data['datetime'] = pd.to_datetime(weather_data['datetime'])

        # Merge datasets on 'datetime'
        merged_data = pd.merge_asof(
            transport_data.sort_values('datetime'),
            weather_data.sort_values('datetime'),
            on='datetime',
            direction='nearest'
        )

        # Save merged data
        date = transport_file.split('_')[-1].replace('.csv', '')
        output_file = os.path.join(output_folder, f"merged_data_{date}.csv")
        merged_data.to_csv(output_file, index=False)
        print(f"Merged data saved to: {output_file}")

if __name__ == "__main__":
    transport_folder = "/Users/gim-yeji/PycharmProjects/pythonProject/IoT/transport_data_collection/"
    weather_folder = "/Users/gim-yeji/PycharmProjects/pythonProject/IoT/weather_data_collection/"
    output_folder = "/Users/gim-yeji/PycharmProjects/pythonProject/IoT/merged_data_collection/"

    merge_datasets(transport_folder, weather_folder, output_folder)