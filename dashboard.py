import streamlit as st
import sys
import os
import plotly.graph_objects as go
import numpy as np
import pandas as pd

from scipy.special import softmax
from time_series import *
from probability_toolkit import *
from utils import *

# Import the function
from streamlit_folium import st_folium
from bologna_simulation import plot_map_folium

st.set_page_config(layout="wide")

st.title("Bologna Simulation Dashboard")

# to be adjusted
import data # qua deve venire caricato il json con le impostazioni

def get_path(door):
    path = 'data/doors_flow_rates/'
    match door:
        case 'saragozza':
            path+='varco-n-59-saragozza-direzione-centro.csv'
        case 'san_isaia':
            path+='varco-n-1-s-isaia-direzione-centro.csv'
        case 'san_felice':
            path+='varco-n-1059-san-felice-direzione-centro.csv'
        case 'lame':
            path+='varco-n-55-lame-direzione-centro.csv'
        case 'galliera':
            path+='varco-n-38-indipendenza-direzione-centro.csv'
        case 'mascarella':
            path+='varco-n-53-mascarella-direzione-sud.csv'
        case 'san_donato':
            path+='varco-n-65.csv'
        case 'san_vitale':
            path+='varco-n-2-s-vitale-direzione-centro.csv'
        case 'santo_stefano':
            path+='varco-n-45-pta-santo-stefano-direzione-centro.csv'
        case 'castiglione':
            path+='varco-n-7-viale-xii-giugno-direzione-centro.csv'
    return path

def get_probs(t, probs):
    keys=probs.keys()
    scaled_probs_dict = {key: probs[key] * get_time_probs(key, t) for key in keys}

    # Estrai i valori nell'ordine corretto delle chiavi per la softmax
    scaled_values = [scaled_probs_dict[key] for key in keys]

    # Applica la softmax per far sommare le probabilità a 1
    softmaxed_probs = softmax(scaled_values)
    return scaled_probs_dict, {key:softmaxed_probs[_] for _,key in enumerate(keys)}


door = None

# --- Create Columns for Layout ---
col1, col2 = st.columns([3, 1]) # Main area takes 3/4, controls take 1/4

# --- Place Controls in the Right Column (col2) ---
with col2:
    st.title("Opzioni mappa") # Use st.title or st.header in the column
    show_scuole_opt = st.checkbox("🔵 Mostra Scuole", value=True)
    show_porte_opt = st.checkbox("🔴 Mostra Porte", value=True)
    show_aree_verdi_opt = st.checkbox("🟢 Mostra Aree Verdi", value=True)

# --- Place Map in the Left Column (col1) ---
with col1:
    try:
        # Call plot_map with options from the controls in col2
        map_object = plot_map_folium(
            show_scuole=show_scuole_opt,
            show_porte=show_porte_opt,
            show_aree_verdi=show_aree_verdi_opt
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

# --- Add a new row below the map with two columns ---
if door:

    # path = 'data/doors_flow_rates/varco-n-59-saragozza-direzione-centro.csv' # questo permette di trovare le ts per porta
    path = get_path(door)
    df = pd.read_csv(path, sep=';')
    ts_data=get_stats_ts(df)

    effort = {age_category : weight_function(age_category, data.weights, data.porte_data[door]) for age_category in data.weights.keys()}

    # P(attraversare)=1-costo attuale/massimo costo
    # max([effort[key] for key in effort.keys()])
    probs = {key:1-(effort[key]/MAX_VAL) for key in effort.keys()}

    keys = list(probs.keys())   # categories

    prob_history = {key: [] for key in keys}
    prob_history_non_softmax = {key: [] for key in keys}
    time_steps = np.linspace(0,24,num=100)

    for t in time_steps:
        scaled, softmaxed = get_probs(t, probs)
        for key in keys:
            prob_history[key].append(softmaxed[key])
            prob_history_non_softmax[key].append(scaled[key])


    volumes_scaled = {key: [] for key in keys}

    for index, row in ts_data.iterrows():
        t=(row['hour']*100+row['minute_interval']*1.6779661017)/100 # per convertire l'ora nel range 0..24

        softmax_dict = get_probs(t, probs)[1]
        
        prob_vals = np.array(list(softmax_dict.values()))
        for _,key in enumerate(keys):
            volumes_scaled[key].append(prob_vals[_]*row['mean'])
    

    col3, col4 = st.columns(2)

    with col3:
        st.title(f"Door settings: {door}")
        for key in data.porte_data[door]['vals']:
            data.porte_data[door]['vals'][key] = st.slider(key, min_value=-1.0, max_value=1.0, value=data.porte_data[door]['vals'][key])
            # data.porte_data[door]['vals']['costo ingresso'] = st.slider("costo ingresso", min_value=-1.0, max_value=1.0, value=data.porte_data[door]['vals']['costo ingresso'])
        

    with col4:
        st.title(f"Simulation prediction")
        # tabellina carina carina
        df_effort = pd.DataFrame(list(effort.items()), columns=["Category", "Effort"])
        st.dataframe(df_effort, use_container_width=True)

        # Grafico Matplotlib
        fig, ax = plt.subplots(figsize=(12, 7))  # Crea la figura

        for key in keys:
            ax.plot(volumes_scaled[key], label=key, linestyle='-')

        ax.plot(ts_data['mean'], label='flow rate of people', linestyle='dotted')

        ax.set_xticks(np.arange(0, len(ts_data), step=4))
        ax.set_xticklabels(
            [ts_data['timeStr'][i] for i in range(0, len(ts_data), 4)],
            rotation=45
        )

        ax.set_xlabel("hour")
        ax.set_ylabel("flow rate")
        ax.set_title("flow rate per hour of the day")
        ax.grid(True)
        ax.legend()
        plt.tight_layout()

        st.pyplot(fig)  # Visualizza il grafico in Streamlit