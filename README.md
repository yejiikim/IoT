🚍 IoT Traffic Prediction and Visualization Platform

An interactive platform for analyzing and predicting traffic patterns in urban areas, leveraging real-time traffic and weather data.

📖 Table of Contents
	1.	About the Project
	2.	Features
	3.	Project Structure
	4.	Installation
	5.	Usage
	6.	Deployment
	7.	Screenshots

📌 About the Project

Urban traffic management requires sophisticated tools to ensure efficiency and scalability. This project integrates real-time traffic data from the Transport API with weather data from OpenWeather API to:
 •	Identify traffic trends.
 •	Analyze correlations between weather and traffic.
 •	Enable predictive modeling to forecast traffic volumes.

The platform provides an interactive dashboard for visualization and predictions, making it an essential tool for transportation planning and optimization.

✨ Features

📊 Dynamic Visualizations:
 •	Traffic by Hour Heatmap.
 •  Top Routes Bar Chart.

🤖 Predictive Analytics:
 •	Traffic prediction based on temperature and humidity.
 
🌐 Interactive Dashboard:
 •	User-friendly interface for data exploration.
 
🔗 Real-Time Data Integration:
 •	Fetches traffic and weather data seamlessly.

📂 Project Structure
IoT
├── analysis/                # Visualizations and data analysis scripts
├── data_preprocessing/      # Data merging and preprocessing scripts
├── log/                     # Logging files for data collection
├── merged_data_collection/  # Merged weather and traffic datasets
├── models/                  # Trained machine learning models (Pickle files)
├── static/                  # Static assets (e.g., visualization images)
├── templates/               # HTML templates for Flask
├── transport_data_collection/ # Raw transport data
├── weather_data_collection/ # Raw weather data
├── app.py                   # Main Flask application
├── part1.py                 # Data collection scripts (Part 1)
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation

💻 Installation

Follow these steps to set up the project locally:
1.	Clone the Repository
git clone https://github.com/your-username/IoT_Final-Project.git
cd IoT_Final-Project

2. Install Dependencies
Ensure Python 3.8+ is installed, then run:
pip install -r requirements.txt

3. Set API Keys
Add your API keys in config.py:
	•	Transport API
	•	OpenWeather API

🚀 Usage
1.	Run the Application
Start the Flask app with the following command:
python app.py
Visit http://127.0.0.1:5000 in your browser to access the dashboard.

2. 	Interact with the Dashboard	
•	View traffic trends and correlations.	
•	Input weather parameters to predict traffic.

🌐 Deployment

Deploy Locally

Follow the usage instructions to run the project locally.

Deploy on Render
	1.	Link the repository to Render.
	2.	Set up the build command:
        pip install -r requirements.txt
    3. Use the start command:
        python app.py
    4. Deploy and access the live URL.

🛠️ Built With
•	Python
	• Flask: Web framework
	• Matplotlib & Seaborn: Visualization
	• Scikit-learn: Machine learning
•	HTML/CSS: Frontend templates
•	Google Cloud Storage: Data backup
•	Transport API & OpenWeather API: Data sources

📊 Results and Insights
	1.	Traffic Patterns:
	•	Evening rush hour (5–6 PM) shows peak traffic activity.
	•	Route A1 consistently has the highest usage.
	2.	Weather Correlation:
	•	Minimal direct impact of weather variables on traffic.
	•	Weak correlation between temperature, humidity, and traffic volume.
	3.	Model Performance:
	•	Gradient Boosting achieved the best R² score (0.04).
	•	Models are limited by dataset features and short observation period.

🌟 Future Enhancements
	•	Include real-time traffic feeds, event data, and additional contextual features.
	•	Extend data collection to capture seasonal and long-term patterns.
	•	Explore neural networks for better prediction accuracy.
	•	Deploy the platform on a cloud service for real-time scalability.

👩‍💻 Contributor
• Yeji Kim
Contact: yk1924@ic.ac.uk / yejikim001120@gmail.com