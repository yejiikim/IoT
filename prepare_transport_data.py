import pandas as pd
import os

def prepare_transport_data(folder):
    """
    Ensure Transport data files contain a valid 'datetime' column.
    """
    # Get all transport files in the folder
    files = sorted(
        [os.path.join(folder, file) for file in os.listdir(folder) if file.endswith('.csv')]
    )

    for file in files:
        # Load the transport data
        data = pd.read_csv(file)
        print(f"Processing file: {file}")
        print("Columns:", data.columns)

        # Check if 'best_departure_estimate' column exists
        if 'best_departure_estimate' in data.columns:
            # Convert 'best_departure_estimate' to 'datetime', handling errors
            data['datetime'] = pd.to_datetime(data['best_departure_estimate'], errors='coerce')

            # Count invalid datetime values
            invalid_count = data['datetime'].isna().sum()
            if invalid_count > 0:
                print(f"Warning: {invalid_count} invalid datetime values in {file}")
                print("Removing invalid rows...")
                data = data.dropna(subset=['datetime'])

            # Log valid rows count
            print(f"Valid rows remaining: {len(data)}")
        else:
            print(f"Column 'best_departure_estimate' not found in {file}. Skipping...")

        # Save the cleaned data
        data.to_csv(file, index=False)
        print(f"Updated file saved: {file}")

if __name__ == "__main__":
    # Set folder path for transport data
    transport_folder = "/Users/gim-yeji/PycharmProjects/pythonProject/IoT/transport_data_collection/"

    # Process transport data
    prepare_transport_data(transport_folder)