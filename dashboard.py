"""
This script creates an interactive Streamlit dashboard to visualize Bologna
geographical data (schools, parks, city gates) using Folium. It allows users
to toggle map layers, adjust parameters like search radius, and view
simulation results or details specific to a selected city gate ('Porta')
clicked on the map.
"""

import streamlit as st
import sys
import os
import plotly.graph_objects as go
import numpy as np
import pandas as pd

from time_series import *
from probability_toolkit import *
from utils import *

# Import the function
from streamlit_folium import st_folium
from bologna_simulation import plot_map_folium, find_points_in_range

st.set_page_config(layout="wide")

st.title("Bologna Simulation Dashboard")

# to be adjusted
import data

door = None

if 'old_door' not in st.session_state:
    st.session_state.old_door = None
if 'effort_t0' not in st.session_state:
    st.session_state.effort_t0 = {}

# --- Create Columns for Layout ---
col1, col2 = st.columns([3, 1]) # Main area takes 3/4, controls take 1/4

# --- Place Controls in the Right Column (col2) ---
with col2:
    st.title("Opzioni mappa") # Use st.title or st.header in the column
    show_scuole_opt = st.checkbox("🔵 Mostra Scuole", value=True)
    show_porte_opt = st.checkbox("🔴 Mostra Porte", value=True)
    show_aree_verdi_opt = st.checkbox("🟢 Mostra Aree Verdi", value=True)
    show_radius_opt = st.checkbox("⭕ Mostra Raggio di Azione", value=False)
    choose_radius = st.slider("Raggio di azione", min_value=0, max_value=1000, value=650, step=25)


# --- Place Map in the Left Column (col1) ---
with col1:
    try:
        # Call plot_map with options from the controls in col2
        map_object = plot_map_folium(
            show_scuole=show_scuole_opt,
            show_porte=show_porte_opt,
            show_aree_verdi=show_aree_verdi_opt,
            show_porte_range=show_radius_opt,
            porte_range_radius=choose_radius
        )

        map_data = st_folium(map_object, width=700, height=400)

        # non è elegante ma è il modo più facile
        door = None
        if map_data and map_data["last_object_clicked"]:
            lat_click = map_data["last_object_clicked"]["lat"]
            lon_click = map_data["last_object_clicked"]["lng"]
            for nome, porta in data.porte_data.items():
                lat, lon = porta["coords"]
                if abs(lat_click - lat) < 0.0005 and abs(lon_click - lon) < 0.0005:
                    door = nome
                    # st.text("{door}")
                    break

    except Exception as e:
        # Display more detailed error in Streamlit
        st.error(f"An error occurred while generating the map:")
        st.exception(e) # Shows the full traceback

# Note: The "Dashboard execution finished" message will appear below col1
col3, col4 = st.columns(2)
# --- Add a new row below the map with two columns ---
# --- Add a new row below the map with two columns ---

if door:
    # --- Define Sliders First (in col3) ---
    with col3:
        st.title(f"Door settings: {door}")

        min_schools, max_schools = 30, 0
        min_parks, max_parks = 30, 0

        for key in data.porte_data.keys():
            schools, parks = find_points_in_range(data.porte_data[key]["coords"][0], data.porte_data[key]["coords"][1], choose_radius)
            min_schools = min(min_schools, len(schools))
            max_schools = max(max_schools, len(schools))
            min_parks = min(min_parks, len(parks))
            max_parks = max(max_parks, len(parks))
            print(f"Min schools: {min_schools}, Max schools: {max_schools}")
            print(f"Min parks: {min_parks}, Max parks: {max_parks}")

        # Use a temporary dictionary to store slider values for this run
        current_door_vals = {}
        for key in data.porte_data[door]['vals']:
            # Read the current value from the data structure for the default
            schools, parks = find_points_in_range(data.porte_data[door]["coords"][0], data.porte_data[door]["coords"][1], choose_radius)
            if (key == 'aree verdi gratuite' or 
                    key == 'aree verdi pagamento'):
                default_value = ramp_val(2.0,
                                         min_parks,
                                         max_parks,
                                         len(parks)
                                    )-1.0
            elif(key == 'scuole pubbliche' or 
                    key == 'scuole private'):
                default_value = ramp_val(2.0,
                                         min_schools,
                                         max_schools,
                                         len(schools)
                                    )-1.0
            else:
                default_value = data.porte_data[door]['vals'][key]
            # Create the slider and store its *current* return value
            current_door_vals[key] = st.slider(
                key,
                min_value=-1.0,
                max_value=1.0,
                value=default_value, # Set initial value from data
                key=f"{door}_{key}" # Add unique key for persistence
            )
        # --- Important: Update the main data structure *after* all sliders are drawn ---
        # This ensures the data reflects the latest slider positions for the *next* part of the script
        data.porte_data[door]['vals'] = current_door_vals

    # --- Perform Calculations Using Updated Values ---
    path = get_path(door)
    df = pd.read_csv(path, sep=';')
    ts_data = get_stats_ts(df)
    # Calculations now use the values just set by the sliders in this run
    effort = {age_category: weight_function(age_category, data.weights, data.porte_data[door]) for age_category in data.weights.keys()}
    
    if st.session_state.old_door!=door:
        st.session_state.effort_t0 = effort.copy()
        st.session_state.old_door=door

    probs = {key: 1 - (effort[key] / MAX_VAL) for key in effort.keys()}

    keys = list(probs.keys())   # categories

    prob_history = {key: [] for key in keys}
    prob_history_non_softmax = {key: [] for key in keys}
    time_steps = np.linspace(0, 24, num=100)

    for t in time_steps:
        scaled, softmaxed = get_probs(t, probs)
        for key in keys:
            prob_history[key].append(softmaxed[key])
            prob_history_non_softmax[key].append(scaled[key])

    volumes_scaled = {key: [] for key in keys}

    for index, row in ts_data.iterrows():
        t = (row['hour'] * 100 + row['minute_interval'] * 1.6779661017) / 100 # per convertire l'ora nel range 0..24
        softmax_dict = get_probs(t, probs)[1]
        prob_vals = np.array(list(softmax_dict.values()))
        for _, key in enumerate(keys):
            volumes_scaled[key].append(prob_vals[_] * row['mean'])

    # --- Display Results (in col4) ---
    with col4:
        st.title(f"Simulation prediction")
        # tabellina carina carina
        df_effort = pd.DataFrame(list(st.session_state.effort_t0.items()), columns=["Category", "Effort"])
        df_effort.columns = ["Category", "Baseline effort"]
        df_new = pd.DataFrame(list(effort.items()), columns=["Category", "Effort"])
        df_effort['Current Effort'] = df_new['Effort']

        # Round the numerical columns to three decimal places
        df_effort['Baseline effort'] = df_effort['Baseline effort']
        df_effort['Current Effort'] = df_effort['Current Effort']

        def style_effort(df):
            def color_effort(row):
                if row['Current Effort'] < row['Baseline effort']:
                    color = '#8FBC8F'
                elif row['Current Effort'] > row['Baseline effort']:
                    color = '#F08080'
                else:
                    return [None, None, None] # No color change
                return [None, None, f'background-color: {color}'] # Apply to 'Current Effort' column only
            return df.style.apply(color_effort, axis=1)
        
        st.dataframe(
            style_effort(df_effort).format("{:.3f}", subset=['Baseline effort', 'Current Effort']), 
            use_container_width=True
        )

        # Grafico Matplotlib
        # IMPORTANT: Need to import matplotlib.pyplot as plt earlier in the file
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(12, 7))  # Crea la figura

        for key in keys:
            ax.plot(volumes_scaled[key], label=key, linestyle='-')

        ax.plot(ts_data['mean'], label='flow rate of people', linestyle='dotted')

        # Adjust x-ticks for better readability if needed
        tick_step = max(1, len(ts_data) // 10) # Show around 10 labels
        ax.set_xticks(np.arange(0, len(ts_data), step=tick_step))
        ax.set_xticklabels(
            [ts_data['timeStr'][i] for i in np.arange(0, len(ts_data), step=tick_step)],
            rotation=45,
            ha="right" # Align rotated labels better
        )

        ax.set_xlabel("Hour of Day")
        ax.set_ylabel("Flow Rate / Scaled Volume")
        ax.set_title("Flow Rate Simulation per Category")
        ax.grid(True)
        ax.legend()
        plt.tight_layout()

        st.pyplot(fig)  # Visualizza il grafico in Streamlit
else:
    # Display a simple message below the map when no door is selected
    st.info("Click a 'Porta' marker on the map to view details and simulation.")

