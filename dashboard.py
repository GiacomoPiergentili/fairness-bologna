import streamlit as st
import sys
import os
import plotly.graph_objects as go

# Import the function
from bologna_simulation import plot_map

st.set_page_config(layout="wide")

st.title("Bologna Simulation Dashboard")

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

    except Exception as e:
        # Display more detailed error in Streamlit
        st.error(f"An error occurred while generating the map:")
        st.exception(e) # Shows the full traceback

# Note: The "Dashboard execution finished" message will appear below col1