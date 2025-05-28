# Fairness Consideration in Digital Twin

## Description
This project provides an interactive dashboard to visualize and analyze geographical data of Bologna, Italy. The dashboard displays schools, city gates, and green areas on an interactive map, allowing users to:

- Toggle visibility of different map elements (schools, gates, green areas)
- Set and visualize a customizable radius of action
- View points of interest within the specified range
- Analyze simulation results for selected city gates

The application combines geographical visualization with data analysis to provide insights into urban accessibility and resource distribution in Bologna.

## Visuals
The dashboard features an interactive map of Bologna with color-coded markers:
- 🔵 Blue markers for schools
- 🔴 Red markers for city gates
- 🟢 Green areas represented with polygons
- ⭕ Optional radius circles to show areas of influence

## Installation

### Requirements
- Python 3.6+
- Git (for cloning the repository)

### Steps
1. Clone the repository:
```
git clone https://dvcs.apice.unibo.it/pika-lab/courses/ai-ethics/projects/piergentilicavaleri2425.git
cd piergentilicavaleri2425
```

2. Install the required dependencies:
```
pip install -r requirements.txt
```

Dependencies include:
- streamlit
- plotly
- geopandas
- shapely
- scipy
- matplotlib
- streamlit-plotly-events
- folium
- streamlit-folium
- PyQt5

## Usage
To launch the dashboard, run:
```
streamlit run dashboard.py
```

This will start the Streamlit server and automatically open the dashboard in your default web browser. If it doesn't open automatically, you can access it at http://localhost:8501.

### Dashboard Controls
- Use checkboxes in the right panel to toggle visibility of schools, gates, and green areas
- Enable the "Show Action Radius" option to visualize coverage radius
- Adjust the radius size using the slider
- Click on map elements to get detailed information

## Authors and Acknowledgment
Created by Piergentili and Cavaleri as part of the AI Ethics course project.