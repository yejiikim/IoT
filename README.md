# 🚍 IoT Traffic Prediction and Visualization Platform

An interactive platform for analyzing and predicting traffic patterns in urban areas, leveraging real-time traffic and weather data.

---

## 📖 Table of Contents
1. [About the Project](#about-the-project)
2. [Features](#features)
3. [Project Structure](#project-structure)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Deployment](#deployment)
7. [Screenshots](#screenshots)

---

## 📌 About the Project

Urban traffic management requires sophisticated tools to ensure efficiency and scalability. This project integrates real-time traffic data from the **Transport API** with weather data from the **OpenWeather API** to:
- Identify traffic trends
- Analyze correlations between weather and traffic
- Enable predictive modeling to forecast traffic volumes

The platform provides an interactive dashboard for visualization and predictions, making it an essential tool for transportation planning and optimization.

---

## ✨ Features

### 📊 Dynamic Visualizations
- **Traffic by Hour Heatmap**
- **Top Routes Bar Chart**

### 🤖 Predictive Analytics
- Traffic prediction based on **temperature** and **humidity**

### 🌐 Interactive Dashboard
- User-friendly interface for data exploration

### 🔗 Real-Time Data Integration
- Fetches traffic and weather data seamlessly

---

## 📂 Project Structure

```plaintext
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

```
---
## 💻 Installation

Follow these steps to set up the project locally:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yejiikim/IoT_Final-Project.git
   cd IoT_Final-Project

2. **Install Dependencies**
   Ensure Python 3.8+ is installed on your system. Install the required dependencies by running:
   ```bash
   pip install -r requirements.txt

3. ** Set API Keys**
   Add your API keys in a config.py file located in the project root directory:
   ```bash
   TRANSPORT_API_KEY = "your_transport_api_key"
   OPENWEATHER_API_KEY = "your_openweather_api_key"

## 🚀 Usage
1. **Run the Application**
    Start the Flask app with the following command:
    ```bash
    python app.py
    ```
    Once started, open your browser and navigate to http://127.0.0.1:5000 to access the 	
    dashboard.

2. **Interact with the Dashboard**
   - View traffic trends and correlations through interactive visualizations.
   - Input weather parameters (temperature and humidity) to predict traffic volume using the trained models.
  
## 🌐 Deployment

**Deploy Locally**
Follow the steps in the Usage section to run the project locally on your machine

**Deploy on Render**

To deploy the project using Render:
1. Link your GitHub repository to Render.
2. Set up the build command:
```bash
pip install -r requirements.txt
```

3. Use the start command:
```bash
python app.py
```

4. Deploy the application and access the live URL provided by Render.

## 🛠️ Built With

- **Python**  
  - Flask: Web framework for building the dashboard and APIs.  
  - Matplotlib & Seaborn: Libraries for data visualization.  
  - Scikit-learn: Machine learning for traffic prediction.  

- **HTML/CSS**  
  - Templates for the frontend user interface.  

- **Google Cloud Storage**  
  - For secure and scalable data backup.  

- **Transport API & OpenWeather API**  
  - Data sources for traffic and weather information.  

---

## 📊 Results and Insights

### 1. Traffic Patterns:
- Evening rush hour (5–6 PM) shows peak traffic activity.  
- Route A1 consistently has the highest usage.  

### 2. Weather Correlation:
- Minimal direct impact of weather variables on traffic.  
- Weak correlation between temperature, humidity, and traffic volume.  

### 3. Model Performance:
- Gradient Boosting achieved the best R² score (0.04).  
- Models are limited by dataset features and the short observation period.  

---

## 🌟 Future Enhancements

- **Real-Time Integration**: Include live traffic feeds, event data, and additional contextual features.  
- **Extended Data Collection**: Capture seasonal and long-term patterns to improve prediction accuracy.  
- **Advanced Modeling**: Explore neural networks or hybrid techniques for better prediction performance.  
- **Cloud Deployment**: Deploy the platform to a scalable cloud service for real-time operations.  

---

## 👩‍💻 Contributor

- **Yeji Kim**  
  - Contact: [yk1924@ic.ac.uk](mailto:yk1924@ic.ac.uk) / [yejikim001120@gmail.com](mailto:yejikim001120@gmail.com)  

