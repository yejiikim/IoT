import pandas as pd
import os


def merge_datasets(transport_folder, weather_folder, output_folder):
    """
    Merge Transport and Weather datasets based on the datetime column.
    """
    # List all transport and weather files
    transport_files = sorted(
        [os.path.join(transport_folder, file) for file in os.listdir(transport_folder) if file.endswith('.csv')]
    )
    weather_files = sorted(
        [os.path.join(weather_folder, file) for file in os.listdir(weather_folder) if file.endswith('.csv')]
    )

    # Ensure the number of files match for daily merging
    if len(transport_files) != len(weather_files):
        print("Error: Mismatch in number of Transport and Weather files.")
        return

    for transport_file, weather_file in zip(transport_files, weather_files):
        # Load Transport and Weather datasets
        transport_data = pd.read_csv(transport_file)
        weather_data = pd.read_csv(weather_file)

        # Ensure datetime columns are formatted correctly
        transport_data["datetime"] = pd.to_datetime(transport_data["datetime"])
        weather_data["datetime"] = pd.to_datetime(weather_data["datetime"])

        # Merge datasets based on nearest datetime
        merged_data = pd.merge_asof(
            transport_data.sort_values("datetime"),
            weather_data.sort_values("datetime"),
            on="datetime",
            direction="nearest"
        )

        # Generate output filename
        date = transport_file.split('_')[-1].replace('.csv', '')
        output_file = os.path.join(output_folder, f"merged_data_{date}.csv")

        # Save merged dataset
        merged_data.to_csv(output_file, index=False)
        print(f"Merged data saved to: {output_file}")


if __name__ == "__main__":
    transport_folder = "/Users/gim-yeji/PycharmProjects/pythonProject/IoT/transport_data_collection/"
    weather_folder = "/Users/gim-yeji/PycharmProjects/pythonProject/IoT/weather_data_collection/"
    output_folder = "/Users/gim-yeji/PycharmProjects/pythonProject/IoT/merged_data_collection/"

    os.makedirs(output_folder, exist_ok=True)
    merge_datasets(transport_folder, weather_folder, output_folder)


def analyze_data(merged_folder, output_folder):
    """
    Perform data analysis on merged datasets.
    """
    merged_files = sorted(
        [os.path.join(merged_folder, file) for file in os.listdir(merged_folder) if file.endswith('.csv')]
    )

    # Initialize a DataFrame for summary results
    summary_results = []

    for file in merged_files:
        data = pd.read_csv(file)

        # Calculate statistics
        busiest_hour = data.groupby(data["datetime"].str[11:13]).size().idxmax()  # Extract hour from datetime
        total_departures = data["line"].count()
        avg_temperature = data["temperature"].mean()
        avg_wind_speed = data["wind_speed"].mean()

        summary_results.append({
            "file": file,
            "busiest_hour": busiest_hour,
            "total_departures": total_departures,
            "avg_temperature": avg_temperature,
            "avg_wind_speed": avg_wind_speed
        })

    # Save summary results
    summary_df = pd.DataFrame(summary_results)
    output_file = os.path.join(output_folder, "summary_analysis.csv")
    summary_df.to_csv(output_file, index=False)
    print(f"Summary analysis saved to: {output_file}")

if __name__ == "__main__":
    merged_folder = "/Users/gim-yeji/PycharmProjects/pythonProject/IoT/merged_data_collection/"
    output_folder = "/Users/gim-yeji/PycharmProjects/pythonProject/IoT/analysis_results/"

    os.makedirs(output_folder, exist_ok=True)
    analyze_data(merged_folder, output_folder)