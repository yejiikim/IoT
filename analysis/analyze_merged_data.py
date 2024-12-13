import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

# File paths for merged datasets
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

# Output folder for analysis results
output_folder = "/Users/gim-yeji/PycharmProjects/pythonProject/IoT/models/analysis"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Function to load and combine all data files
def load_data(files):
    """
    Load and combine all merged CSV files into a single DataFrame.
    """
    data = pd.concat([pd.read_csv(file) for file in files], ignore_index=True)
    return data

# Function to preprocess the data
def preprocess_data(data):
    """
    Preprocess data by formatting 'datetime' and creating useful fields.
    """
    # Convert 'datetime' to pandas datetime format
    data['datetime'] = pd.to_datetime(data['datetime'], errors='coerce')
    # Drop rows with invalid datetime
    data = data.dropna(subset=['datetime'])
    # Extract hour for hourly traffic analysis
    data['hour'] = data['datetime'].dt.hour
    # Convert categorical 'line' to numeric values
    data['line_numeric'] = pd.factorize(data['line'])[0]
    return data

# Function to analyze correlation
def analyze_correlation(data):
    """
    Analyze correlations between temperature, humidity, and traffic volume.
    """
    corr_matrix = data[['temperature', 'humidity', 'line_numeric']].corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm")
    plt.title("Correlation Matrix")
    plt.savefig(f"{output_folder}/correlation_matrix.png")
    plt.close()

# Function to create an hourly heatmap
def analyze_hourly_heatmap(data):
    """
    Analyze and visualize traffic volume by hour for each route.
    """
    pivot = data.pivot_table(index='line', columns='hour', values='line_numeric', aggfunc='count', fill_value=0)
    plt.figure(figsize=(12, 8))
    sns.heatmap(pivot, cmap="YlGnBu", annot=False)
    plt.title("Hourly Traffic Heatmap")
    plt.xlabel("Hour")
    plt.ylabel("Line")
    plt.savefig(f"{output_folder}/hourly_heatmap.png")
    plt.close()

# Function to compare models and visualize their performance
def model_analysis(data):
    """
    Compare multiple machine learning models and evaluate their performance.
    """
    X = data[['temperature', 'humidity']]
    y = data['line_numeric']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Define models
    models = {
        "Linear Regression": LinearRegression(),
        "Random Forest": RandomForestRegressor(random_state=42),
        "Gradient Boosting": GradientBoostingRegressor(random_state=42)
    }

    # Train models and evaluate R² scores
    results = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        r2 = r2_score(y_test, y_pred)
        results[name] = r2

    # Visualize R² scores
    plt.figure(figsize=(10, 6))
    plt.bar(results.keys(), results.values(), color=["blue", "orange", "green"])
    plt.title("Model Comparison: R² Scores")
    plt.ylabel("R² Score")
    plt.savefig(f"{output_folder}/model_comparison.png")
    plt.close()

    # Visualize Actual vs Predicted values for the best model
    y_pred = models["Gradient Boosting"].predict(X_test)
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, y_pred, label="Predicted vs Actual", alpha=0.6)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', label="Ideal Fit")
    plt.title("Model Performance: Actual vs Predicted")
    plt.xlabel("Actual Traffic Volume")
    plt.ylabel("Predicted Traffic Volume")
    plt.legend()
    plt.savefig(f"{output_folder}/actual_vs_predicted.png")
    plt.close()

# Main execution flow
if __name__ == "__main__":
    # Load and preprocess data
    raw_data = load_data(file_paths)
    clean_data = preprocess_data(raw_data)

    # Perform correlation analysis
    analyze_correlation(clean_data)

    # Create hourly traffic heatmap
    analyze_hourly_heatmap(clean_data)

    # Perform model comparison and evaluation
    model_analysis(clean_data)