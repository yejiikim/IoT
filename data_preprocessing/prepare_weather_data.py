import pandas as pd
import os

def prepare_weather_data(folder):
    """
    Ensure Weather data files contain a valid 'datetime' column.
    """
    # Get all weather files in the folder
    files = sorted(
        [os.path.join(folder, file) for file in os.listdir(folder) if file.endswith('.csv')]
    )

    for file in files:
        # Load the weather data
        data = pd.read_csv(file)
        print(f"Processing file: {file}")
        print("Columns:", data.columns)

        # Check if 'datetime' column exists or create it from another column
        if 'datetime' not in data.columns:
            if 'time' in data.columns:  # Replace 'time' with the actual column name in your dataset
                data['datetime'] = pd.to_datetime(data['time'], errors='coerce')
                print(f"'datetime' column created for {file}")
            else:
                print(f"Column 'time' not found in {file}. Skipping...")
                continue

        # Count invalid datetime values
        invalid_count = data['datetime'].isna().sum()
        if invalid_count > 0:
            print(f"Warning: {invalid_count} invalid datetime values in {file}")
            print("Removing invalid rows...")
            data = data.dropna(subset=['datetime'])

        # Save the cleaned data
        data.to_csv(file, index=False)
        print(f"Updated file saved: {file}")

if __name__ == "__main__":
    # Set folder path for weather data
    weather_folder = "/Users/gim-yeji/PycharmProjects/pythonProject/IoT/weather_data_collection/"

    # Process weather data
    prepare_weather_data(weather_folder)