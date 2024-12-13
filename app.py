from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
import os

app = Flask(__name__)

# Define model paths
MODEL_PATHS = {
    "Linear Regression": "/Users/gim-yeji/PycharmProjects/pythonProject/IoT/models/linear_regression_model.pkl",
    "Random Forest": "/Users/gim-yeji/PycharmProjects/pythonProject/IoT/models/random_forest_model.pkl",
    "Gradient Boosting": "/Users/gim-yeji/PycharmProjects/pythonProject/IoT/models/gradient_boosting_model.pkl"
}

# Path to visualization images
VISUALIZATION_PATHS = {
    "Traffic by Hour": "/static/visualizations/traffic_by_hour.png",
    "Top Routes": "/static/visualizations/top_routes.png"
}

# Load merged data for the dashboard table
DATA_PATH = "/Users/gim-yeji/PycharmProjects/pythonProject/IoT/merged_data_collection/"
file_paths = [os.path.join(DATA_PATH, f) for f in os.listdir(DATA_PATH) if f.endswith('.csv')]
merged_data = pd.concat([pd.read_csv(file) for file in file_paths], ignore_index=True)

@app.route("/")
def index():
    """
    Render the main dashboard with the table and prediction form.
    """
    data_preview = merged_data.head(10).to_dict(orient="records")
    return render_template("index.html", data_preview=data_preview, visualizations=VISUALIZATION_PATHS)

@app.route("/api/predict", methods=["POST"])
def predict():
    """
    Predict traffic volume based on temperature and humidity using multiple models.
    """
    input_data = request.json
    temperature = float(input_data["temperature"])
    humidity = float(input_data["humidity"])

    predictions = {}

    for model_name, model_path in MODEL_PATHS.items():
        with open(model_path, "rb") as f:
            model = pickle.load(f)
        prediction = model.predict([[temperature, humidity]])[0]
        predictions[model_name] = round(prediction, 2)

    return jsonify(predictions)

@app.route("/api/correlation", methods=["GET"])
def correlation():
    """
    Provide static correlation analysis results (precomputed).
    """
    correlation_results = {
        "Temperature vs Traffic Volume": 0.82,
        "Humidity vs Traffic Volume": -0.45
    }
    return jsonify(correlation_results)

if __name__ == "__main__":
    app.run(debug=True)