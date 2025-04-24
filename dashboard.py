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
from bologna_simulation import plot_map

from streamlit_plotly_events import plotly_events


st.set_page_config(layout="wide")

st.title("Bologna Simulation Dashboard")


# to be adjusted
import data # qua deve venire caricato il json con le impostazioni
path = 'data/varco-n-59-saragozza-direzione-centro.csv' # questo permette di trovare le ts per porta

df = pd.read_csv(path, sep=';')
ts_saragozza=get_stats_ts(df)
ts_saragozza.head(5)

door = 'saragozza'
effort = {age_category : weight_function(age_category, data.weights, data.porte_data[door]) for age_category in data.weights.keys()}

# P(attraversare)=1-costo attuale/massimo costo
# max([effort[key] for key in effort.keys()])
probs = {key:1-(effort[key]/MAX_VAL) for key in effort.keys()}

def get_probs(t, probs):
    keys=probs.keys()
    scaled_probs_dict = {key: probs[key] * get_time_probs(key, t) for key in keys}

    # Estrai i valori nell'ordine corretto delle chiavi per la softmax
    scaled_values = [scaled_probs_dict[key] for key in keys]

    # Applica la softmax per far sommare le probabilità a 1
    softmaxed_probs = softmax(scaled_values)
    return scaled_probs_dict, {key:softmaxed_probs[_] for _,key in enumerate(keys)}


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

for index, row in ts_saragozza.iterrows():
    t=(row['hour']*100+row['minute_interval']*1.6779661017)/100 # per convertire l'ora nel range 0..24

    softmax_dict = get_probs(t, probs)[1]
    
    prob_vals = np.array(list(softmax_dict.values()))
    for _,key in enumerate(keys):
        volumes_scaled[key].append(prob_vals[_]*row['mean'])


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
        fig = plot_map(
            show_scuole=show_scuole_opt,
            show_porte=show_porte_opt,
            show_aree_verdi=show_aree_verdi_opt
        )

        # Check if the figure has data before displaying
        if fig and fig.data:
            # Display the figure using Streamlit's Plotly chart component
            # use_container_width=True will make it fill col1's width
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No data to display based on selected options or data loading error.")

        # if fig and fig.data:
        #     click_data = plotly_events(fig, click_event=True, select_event=True)
        #     st.plotly_chart(fig, use_container_width=True)

        #     if click_data:
        #         selected_porta = click_data[0]['customdata']  # <-- nome cliccato
        #         st.success(f"Hai selezionato la porta: {selected_porta}")
        # if click_data:
        #     clicked_label = click_data[0]['customdata']  # o altro campo utile
        #     st.text(clicked_label)

    except Exception as e:
        # Display more detailed error in Streamlit
        st.error(f"An error occurred while generating the map:")
        st.exception(e) # Shows the full traceback

# Note: The "Dashboard execution finished" message will appear below col1

# --- Add a new row below the map with two columns ---
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

    ax.plot(ts_saragozza['mean'], label='flow rate of people', linestyle='dotted')

    ax.set_xticks(np.arange(0, len(ts_saragozza), step=4))
    ax.set_xticklabels(
        [ts_saragozza['timeStr'][i] for i in range(0, len(ts_saragozza), 4)],
        rotation=45
    )

    ax.set_xlabel("hour")
    ax.set_ylabel("flow rate")
    ax.set_title("flow rate per hour of the day")
    ax.grid(True)
    ax.legend()
    plt.tight_layout()

    st.pyplot(fig)  # Visualizza il grafico in Streamlit