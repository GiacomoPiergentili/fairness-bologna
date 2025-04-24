import pandas as pd
import geopandas as gpd
# import plotly.express as px # Not used if only using go
import plotly.graph_objects as go
from shapely.geometry import Point
import os # <-- Import os

# --- Define Base Directory ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

# --- Load Data using absolute paths ---
try:
    porte_df = pd.read_csv(os.path.join(DATA_DIR, "porte.csv"))
    aree_verdi_df = pd.read_csv(os.path.join(DATA_DIR, "carta-tecnica-comunale-toponimi-parchi-e-giardini.csv"), delimiter=';')
    scuole_df = pd.read_csv(os.path.join(DATA_DIR, "elenco-delle-scuole.csv"), delimiter=';')
except FileNotFoundError as e:
    print(f"ERROR: Data file not found. Make sure the 'data' folder is in the same directory as the script. {e}")
    # Optionally, raise the error or exit if data is critical
    raise e # Or sys.exit(1) after importing sys

# --- Keep coordinate parsing and df_to_gdf ---
# (Note: df_to_gdf still has limitations for aree_verdi_df, consider using the robust create_gdf if issues arise)
def parse_coordinates(geopoint):
    try: # Add basic error handling
        if pd.isna(geopoint) or not isinstance(geopoint, str): return None, None
        lat_str, lon_str = geopoint.split(',')
        return float(lon_str.strip()), float(lat_str.strip())
    except: return None, None

def df_to_gdf(df):
    temp_df = df.copy() # Work on a copy
    lon_col, lat_col = 'longitude', 'latitude' # Default names

    if 'Geo Point' in temp_df.columns:
        print("Parsing Geo Point...")
        # Apply parsing and handle potential None values
        coords = temp_df['Geo Point'].apply(parse_coordinates)
        # Filter out None results before unpacking
        valid_coords = coords.dropna()
        if not valid_coords.empty:
            temp_df = temp_df.loc[valid_coords.index] # Keep only rows with valid coords
            temp_df[lon_col], temp_df[lat_col] = zip(*valid_coords)
        else:
            print("Warning: No valid coordinates found in 'Geo Point'.")
            return gpd.GeoDataFrame() # Return empty if no valid coords
    elif 'longitude' in temp_df.columns and 'latitude' in temp_df.columns:
        print("Using Longitude/Latitude columns...")
        lon_col, lat_col = 'longitude', 'latitude' # Use existing columns
        # Ensure they are numeric, coercing errors
        temp_df[lon_col] = pd.to_numeric(temp_df[lon_col], errors='coerce')
        temp_df[lat_col] = pd.to_numeric(temp_df[lat_col], errors='coerce')
        temp_df.dropna(subset=[lon_col, lat_col], inplace=True) # Drop rows where conversion failed
    elif 'Geo Shape' in temp_df.columns:
        print("Parsing Geo Shape (basic)...") # Add basic Geo Shape handling if needed
        # Add the robust GeoJSON parsing logic here if required for aree_verdi
        # For now, this branch might lead to errors or empty GDF for parks
        print("Warning: Basic df_to_gdf doesn't fully support 'Geo Shape'. Aree Verdi might be empty/incorrect.")
        return gpd.GeoDataFrame() # Placeholder
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


# --- Create GeoDataFrames ---
print("Creating GDFs...")
porte_gdf = df_to_gdf(porte_df)
aree_verdi_gdf = df_to_gdf(aree_verdi_df) # This will likely be empty/fail with basic df_to_gdf
scuole_gdf = df_to_gdf(scuole_df)
print("Finished creating GDFs.")

# --- Keep hover text creation ---
# Add checks for empty GDFs before creating hover text
hover_text_scuole = ""
if not scuole_gdf.empty:
    hover_text_scuole = (
                '<b>' + scuole_gdf['NOME'].astype(str) + '</b><br>' +
                'Servizio: ' + scuole_gdf['SERVIZIO'].astype(str) + '<br>' +
                'Istituto: ' + scuole_gdf['ISTITUZIONE_SCOLASTICA'].astype(str) + '<br>' +
                'Indirizzo: ' + scuole_gdf['Indirizzo scuola'].astype(str) + ' ' + scuole_gdf['CIVICO'].astype(str) +
                '<extra></extra>' # Add extra to hide trace info
            )

# --- Modify plot_map ---
def plot_map(show_scuole=True, show_porte=True, show_aree_verdi=True):
    layers_to_plot = []
    # Use the globally defined GDFs, checking if they exist and are not empty
    if show_scuole and 'scuole_gdf' in globals() and not scuole_gdf.empty:
        layers_to_plot.append(
            go.Scattermapbox(
                lat=scuole_gdf['latitude'], lon=scuole_gdf['longitude'], mode='markers',
                marker=go.scattermapbox.Marker(size=9, color='blue', symbol='circle', opacity=1.0), # Use working style
                text=hover_text_scuole, hoverinfo='text', # name='Scuole'
            )
        )
    if show_porte and 'porte_gdf' in globals() and not porte_gdf.empty:
         layers_to_plot.append(
            go.Scattermapbox(
                lat=porte_gdf['latitude'], lon=porte_gdf['longitude'], mode='markers', # Assuming 'latitude' exists after df_to_gdf
                marker=go.scattermapbox.Marker(size=12, color='red', symbol='circle', opacity=1.0), # Use working style
                text=porte_gdf['name'], hoverinfo='text', # name='Porte'
            )
        )
    if show_aree_verdi and 'aree_verdi_gdf' in globals() and not aree_verdi_gdf.empty:
        layers_to_plot.append(
            go.Scattermapbox(
                lat=aree_verdi_gdf['latitude'], lon=aree_verdi_gdf['longitude'], mode='markers', # Assuming these exist
                marker=go.scattermapbox.Marker(size=8, color='green', symbol='circle', opacity=1.0), # Use working style
                text=aree_verdi_gdf['DENOMINAZIONE'], hoverinfo='text', # name='Aree Verdi'
            )
        )

    if not layers_to_plot:
        print("No layers selected or valid GeoDataFrames are available. Nothing to plot.")
        return go.Figure()

    fig = go.Figure(data=layers_to_plot)

    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox_center={"lat": 44.4949, "lon": 11.3426},
        mapbox_zoom=13,
        margin={"r":0,"t":30,"l":0,"b":0},
        title="Mappa di Bologna",
        showlegend=False,
        # legend_title_text='Legenda',
        height=750,
    )

    return fig