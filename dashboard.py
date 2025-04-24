import streamlit as st
import plotly.graph_objects as go

from bologna_simulation import plot_map, scuole_gdf, porte_gdf, aree_verdi_gdf

st.set_page_config(layout="wide")

st.title("Bologna Simulation Dashboard")

col1, col2 = st.columns([3, 1])

with col2:
    st.title("Opzioni mappa")
    show_scuole_opt = st.checkbox("🔵 Mostra Scuole", value=True)
    show_porte_opt = st.checkbox("🔴 Mostra Porte", value=True)
    show_aree_verdi_opt = st.checkbox("🟢 Mostra Aree Verdi", value=True)

    st.markdown("---")

    porte_radius_val = 0
    show_porte_radius_opt = False

    if show_porte_opt:
        show_porte_radius_opt = st.checkbox("⭕ Mostra Raggio Porte", value=True)

        if show_porte_radius_opt:
            porte_radius_val = st.slider(
                "Raggio Porte (metri)",
                min_value=0,
                max_value=1000, 
                value=650,      
                step=50,
                help="Imposta un raggio (in metri) per visualizzare un cerchio attorno a ciascuna porta."
            )
        else:
            porte_radius_val = 0


with col1:
    try:
        radius_to_pass = porte_radius_val if show_porte_opt and show_porte_radius_opt else 0

        fig = plot_map(
            scuole_gdf=scuole_gdf,         
            porte_gdf=porte_gdf,           
            aree_verdi_gdf=aree_verdi_gdf, 
            show_scuole=show_scuole_opt,
            show_porte=show_porte_opt,
            show_aree_verdi=show_aree_verdi_opt,
            porte_radius_meters=radius_to_pass 
        )

        # Check if the figure has data before displaying
        # Check fig.data for scatter points, fig.layout.mapbox.layers for circles/polygons
        if fig and (fig.data or (fig.layout.mapbox and fig.layout.mapbox.layers)):
            st.plotly_chart(fig, use_container_width=True)
        else:
            # If the figure itself is valid but has no data/layers, show it (it might have title/layout)
            if fig:
                 st.plotly_chart(fig, use_container_width=True)
                 st.info("Nessun dato da visualizzare con le opzioni selezionate.")
            else:
                 st.warning("Errore durante la generazione della mappa o nessun dato disponibile.")


    except Exception as e:
        st.error(f"An error occurred while generating the map:")
        st.exception(e)