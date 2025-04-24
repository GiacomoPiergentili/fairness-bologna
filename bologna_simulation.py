import pandas as pd
import geopandas as gpd
import plotly.graph_objects as go
from shapely.geometry import Point
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

try:
    porte_df = pd.read_csv(os.path.join(DATA_DIR, "porte.csv"))
    aree_verdi_df = pd.read_csv(os.path.join(DATA_DIR, "carta-tecnica-comunale-toponimi-parchi-e-giardini.csv"), delimiter=';')
    scuole_df = pd.read_csv(os.path.join(DATA_DIR, "elenco-delle-scuole.csv"), delimiter=';')
except FileNotFoundError as e:
    print(f"ERROR: Data file not found. Make sure the 'data' folder is in the same directory as the script. {e}")
    raise e

def parse_coordinates(geopoint):
    try:
        if pd.isna(geopoint) or not isinstance(geopoint, str): return None, None
        lat_str, lon_str = geopoint.split(',')
        return float(lon_str.strip()), float(lat_str.strip())
    except: return None, None

def df_to_gdf(df):
    temp_df = df.copy()
    lon_col, lat_col = 'longitude', 'latitude'

    if 'Geo Point' in temp_df.columns:
        print("Parsing Geo Point...")
        coords = temp_df['Geo Point'].apply(parse_coordinates)
        valid_coords = coords.dropna()
        if not valid_coords.empty:
            temp_df = temp_df.loc[valid_coords.index]
            temp_df[lon_col], temp_df[lat_col] = zip(*valid_coords)
        else:
            print("Warning: No valid coordinates found in 'Geo Point'.")
            return gpd.GeoDataFrame()
    elif 'longitude' in temp_df.columns and 'latitude' in temp_df.columns:
        print("Using Longitude/Latitude columns...")
        lon_col, lat_col = 'longitude', 'latitude'
        temp_df[lon_col] = pd.to_numeric(temp_df[lon_col], errors='coerce')
        temp_df[lat_col] = pd.to_numeric(temp_df[lat_col], errors='coerce')
        temp_df.dropna(subset=[lon_col, lat_col], inplace=True)
    elif 'Geo Shape' in temp_df.columns:
        print("Parsing Geo Shape (basic)...")
        print("Warning: Basic df_to_gdf doesn't fully support 'Geo Shape'. Aree Verdi might be empty/incorrect.")
        return gpd.GeoDataFrame()
    else:
        print("Error: Could not find suitable coordinate columns.")
        return gpd.GeoDataFrame()

    if temp_df.empty:
        print("DataFrame is empty after coordinate processing.")
        return gpd.GeoDataFrame()

    try:
        geometry = [Point(xy) for xy in zip(temp_df[lon_col], temp_df[lat_col])]
        gdf = gpd.GeoDataFrame(temp_df, geometry=geometry, crs="EPSG:4326")
        print(f"Created GDF with {len(gdf)} rows.")
        return gdf
    except Exception as e:
        print(f"Error creating GeoDataFrame geometry: {e}")
        return gpd.GeoDataFrame()


print("Creating GDFs...")
porte_gdf = df_to_gdf(porte_df)
aree_verdi_gdf = df_to_gdf(aree_verdi_df)
scuole_gdf = df_to_gdf(scuole_df)
print("Finished creating GDFs.")

hover_text_scuole = ""
hover_text_porte = ""
hover_text_aree_verdi = ""

def plot_map(scuole_gdf, porte_gdf, aree_verdi_gdf, show_scuole=True, show_porte=True, show_aree_verdi=True, porte_radius_meters=0):
    layers_to_plot = []
    porte_circles_geojson = None

    # Define CRS constants
    WGS84 = "EPSG:4326"
    UTM_ZONE_32N = "EPSG:32632"

    if show_porte and porte_gdf is not None and not porte_gdf.empty and porte_radius_meters > 0:
        try:
            temp_porte_gdf = porte_gdf.copy()
            if temp_porte_gdf.crs is None:
                temp_porte_gdf.set_crs(WGS84, inplace=True)
            elif temp_porte_gdf.crs.to_string() != WGS84:
                 temp_porte_gdf = temp_porte_gdf.to_crs(WGS84)

            porte_gdf_proj = temp_porte_gdf.to_crs(UTM_ZONE_32N)

            porte_circles_proj = porte_gdf_proj.geometry.buffer(porte_radius_meters)

            porte_circles_wgs84 = porte_circles_proj.to_crs(WGS84)

            circles_gdf = gpd.GeoDataFrame(geometry=porte_circles_wgs84, crs=WGS84)

            porte_circles_geojson = json.loads(circles_gdf.to_json())

        except Exception as e:
            print(f"Error generating porte circles: {e}")

    if show_scuole and scuole_gdf is not None and not scuole_gdf.empty:
        hover_text_scuole = (
            '<b>' + scuole_gdf['NOME'].astype(str) + '</b><br>' +
            'Servizio: ' + scuole_gdf['SERVIZIO'].astype(str) + '<br>' +
            'Istituto: ' + scuole_gdf['ISTITUZIONE_SCOLASTICA'].astype(str) + '<br>' +
            'Indirizzo: ' + scuole_gdf['Indirizzo scuola'].astype(str) + ' ' + scuole_gdf['CIVICO'].astype(str) +
            '<extra></extra>'
        )
        layers_to_plot.append(
            go.Scattermapbox(
                lat=scuole_gdf['latitude'], lon=scuole_gdf['longitude'], mode='markers',
                marker=go.scattermapbox.Marker(size=9, color='blue', symbol='circle', opacity=1.0),
                text=hover_text_scuole, hoverinfo='text',
            )
        )
    if show_porte and porte_gdf is not None and not porte_gdf.empty:
         layers_to_plot.append(
            go.Scattermapbox(
                lat=porte_gdf['latitude'], lon=porte_gdf['longitude'], mode='markers',
                marker=go.scattermapbox.Marker(size=12, color='red', symbol='circle', opacity=1.0),
                text=porte_gdf['name'], hoverinfo='text',
            )
        )
    if show_aree_verdi and aree_verdi_gdf is not None and not aree_verdi_gdf.empty:
        if 'latitude' in aree_verdi_gdf.columns and 'longitude' in aree_verdi_gdf.columns and 'DENOMINAZIONE' in aree_verdi_gdf.columns:
            layers_to_plot.append(
                go.Scattermapbox(
                    lat=aree_verdi_gdf['latitude'], lon=aree_verdi_gdf['longitude'], mode='markers',
                    marker=go.scattermapbox.Marker(size=8, color='green', symbol='circle', opacity=1.0),
                    text=aree_verdi_gdf['DENOMINAZIONE'], hoverinfo='text',
                )
            )
        else:
            print("Warning: Aree Verdi GDF is missing required columns (latitude, longitude, DENOMINAZIONE). Skipping layer.")


    if not layers_to_plot and not porte_circles_geojson:
        print("No layers selected or valid GeoDataFrames/circles are available. Nothing to plot.")
        fig = go.Figure()
        fig.update_layout(
            mapbox_style="open-street-map",
            mapbox_center={"lat": 44.4949, "lon": 11.3426},
            mapbox_zoom=12,
            margin={"r":0,"t":30,"l":0,"b":0},
            title="Mappa di Bologna - Nessun dato da visualizzare",
            height=750,
        )
        return fig


    fig = go.Figure(data=layers_to_plot)

    mapbox_layers = []
    if porte_circles_geojson:
        mapbox_layers.append(
            {
                "source": porte_circles_geojson,
                "type": "fill",
                "color": "rgba(255, 0, 0, 0.2)",
                "below": "traces",
            }
        )

    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox_center={"lat": 44.4949, "lon": 11.3426},
        mapbox_zoom=13.5,
        margin={"r":0,"t":30,"l":0,"b":0},
        title="Mappa di Bologna",
        showlegend=False,
        height=750,
        mapbox_layers=mapbox_layers if mapbox_layers else None
    )

    return fig
