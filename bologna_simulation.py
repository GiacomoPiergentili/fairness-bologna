import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import os
import folium
from folium.plugins import MarkerCluster
import sys # Import sys for sys.exit
import data

# --- Configuration ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
CRS = "EPSG:4326" # Define Coordinate Reference System

# --- Data Loading ---
def load_data(filename, delimiter=','):
    """Loads a CSV file from the data directory."""
    filepath = os.path.join(DATA_DIR, filename)
    try:
        return pd.read_csv(filepath, delimiter=delimiter)
    except FileNotFoundError:
        print(f"ERROR: Data file not found at {filepath}. Make sure the 'data' folder exists and contains the file.")
        sys.exit(1) # Exit if essential data is missing


porte_dict= {key: data.porte_data[key]["coords"] for key in data.porte_data.keys()}
porte_df = pd.DataFrame.from_dict(porte_dict, orient='index', columns=['latitude', 'longitude'])
porte_df = porte_df.reset_index().rename(columns={"index":"name"})
aree_verdi_df = load_data("carta-tecnica-comunale-toponimi-parchi-e-giardini.csv", delimiter=';')
scuole_df = load_data("elenco-delle-scuole.csv", delimiter=';')

# --- Coordinate Parsing and GeoDataFrame Creation ---
def parse_coordinates(geopoint: str) -> tuple[float | None, float | None]:
    """Parses 'lat, lon' string into (longitude, latitude) tuple."""
    if pd.isna(geopoint) or not isinstance(geopoint, str):
        return None, None
    try:
        lat_str, lon_str = geopoint.split(',')
        # Return longitude first, then latitude
        return float(lon_str.strip()), float(lat_str.strip())
    except (ValueError, IndexError):
        print(f"Warning: Could not parse coordinates: {geopoint}")
        return None, None

def create_gdf_from_points(df: pd.DataFrame) -> gpd.GeoDataFrame:
    """Creates a GeoDataFrame from a DataFrame with point coordinates."""
    temp_df = df.copy()
    geometry = None
    lon_col, lat_col = 'longitude', 'latitude'

    if 'Geo Point' in temp_df.columns:
        print("Attempting to parse 'Geo Point' column...")
        coords = temp_df['Geo Point'].apply(parse_coordinates)
        valid_coords_mask = coords.notna() & coords.apply(lambda x: x != (None, None))

        if valid_coords_mask.any():
            temp_df = temp_df.loc[valid_coords_mask].copy() # Keep only rows with valid coords
            temp_df[[lon_col, lat_col]] = pd.DataFrame(coords[valid_coords_mask].tolist(), index=temp_df.index)
            print(f"Successfully parsed {len(temp_df)} points from 'Geo Point'.")
        else:
            print("Warning: No valid coordinates found in 'Geo Point'.")
            return gpd.GeoDataFrame(crs=CRS) # Return empty GDF

    elif lon_col in temp_df.columns and lat_col in temp_df.columns:
        print("Using existing 'longitude' and 'latitude' columns...")
        temp_df[lon_col] = pd.to_numeric(temp_df[lon_col], errors='coerce')
        temp_df[lat_col] = pd.to_numeric(temp_df[lat_col], errors='coerce')
        original_count = len(temp_df)
        temp_df.dropna(subset=[lon_col, lat_col], inplace=True)
        dropped_count = original_count - len(temp_df)
        if dropped_count > 0:
            print(f"Warning: Dropped {dropped_count} rows with invalid coordinate values.")
        if temp_df.empty:
             print("Warning: DataFrame is empty after handling longitude/latitude columns.")
             return gpd.GeoDataFrame(crs=CRS)

    # --- Placeholder for Geo Shape ---
    elif 'Geo Shape' in temp_df.columns:
        print("Warning: Found 'Geo Shape' column. Current logic cannot process Polygon/LineString geometries reliably from this format.")
        print("         The resulting GeoDataFrame for this input might be empty or incorrect.")
        try:
            temp_df[['lat_tmp', 'lon_tmp']] = temp_df['Geo Shape'].str.extract(r'"coordinates":\s*\[\s*(\d+\.\d+)\s*,\s*(\d+\.\d+)\s*\]', expand=True)
            temp_df[lon_col] = pd.to_numeric(temp_df['lon_tmp'], errors='coerce')
            temp_df[lat_col] = pd.to_numeric(temp_df['lat_tmp'], errors='coerce')
            temp_df.dropna(subset=[lon_col, lat_col], inplace=True)
        except Exception:
             print("Failed to extract basic coordinates from 'Geo Shape'.")
             return gpd.GeoDataFrame(crs=CRS) # Return empty if extraction fails

    else:
        print("Error: Could not find suitable coordinate columns ('Geo Point' or 'longitude'/'latitude').")
        return gpd.GeoDataFrame(crs=CRS) # Return empty GDF

    # --- Create Geometry ---
    if lon_col in temp_df.columns and lat_col in temp_df.columns and not temp_df.empty:
        try:
            geometry = [Point(xy) for xy in zip(temp_df[lon_col], temp_df[lat_col])]
            # Ensure required columns for drop exist before dropping
            cols_to_drop = [c for c in [lon_col, lat_col, 'lat_tmp', 'lon_tmp'] if c in temp_df.columns]
            gdf = gpd.GeoDataFrame(temp_df.drop(columns=cols_to_drop, errors='ignore'), geometry=geometry, crs=CRS)
            print(f"Successfully created GeoDataFrame with {len(gdf)} geometries.")
            return gdf
        except Exception as e:
            print(f"Error creating GeoDataFrame geometry: {e}")
            return gpd.GeoDataFrame(crs=CRS)
    else:
        print("Warning: No valid coordinates available to create geometry.")
        return gpd.GeoDataFrame(crs=CRS)


# --- Create GeoDataFrames ---
print("\nCreating GeoDataFrames...")
porte_gdf = create_gdf_from_points(porte_df)
print(porte_gdf)
aree_verdi_gdf = create_gdf_from_points(aree_verdi_df)
scuole_gdf = create_gdf_from_points(scuole_df)
print("Finished creating GeoDataFrames.\n")

# --- Prepare Hover Text ---
# (Keep existing hover text preparation for scuole, porte, aree_verdi)
if not scuole_gdf.empty:
    required_cols = ['NOME', 'SERVIZIO', 'ISTITUZIONE_SCOLASTICA', 'Indirizzo scuola', 'CIVICO']
    if all(col in scuole_gdf.columns for col in required_cols):
        scuole_gdf['hover_text'] = (
            '<b>' + scuole_gdf['NOME'].astype(str) + '</b><br>' +
            'Servizio: ' + scuole_gdf['SERVIZIO'].astype(str) + '<br>' +
            'Istituto: ' + scuole_gdf['ISTITUZIONE_SCOLASTICA'].astype(str) + '<br>' +
            'Indirizzo: ' + scuole_gdf['Indirizzo scuola'].astype(str) + ' ' + scuole_gdf['CIVICO'].astype(str) +
            '<extra></extra>'
        )
    else:
        print("Warning: Missing columns required for 'scuole' hover text. Using default.")
        scuole_gdf['hover_text'] = 'Scuola'
else:
    print("Info: Scuole GeoDataFrame is empty, skipping hover text generation.")

if not porte_gdf.empty:
    required_cols = ['name']
    if all(col in porte_gdf.columns for col in required_cols):
        porte_gdf['hover_text'] = '<b>' + porte_gdf['name'].astype(str) + '</b>' + '<extra></extra>'
    else:
        print("Warning: Missing 'name' column required for 'porte' hover text. Using default.")
        porte_gdf['hover_text'] = 'Porta'
else:
    print("Info: Porte GeoDataFrame is empty, skipping hover text generation.")

if not aree_verdi_gdf.empty:
    required_cols = ['DENOMINAZIONE']
    if all(col in aree_verdi_gdf.columns for col in required_cols):
        aree_verdi_gdf['hover_text'] = '<b>' + aree_verdi_gdf['DENOMINAZIONE'].astype(str) + '</b>' + '<extra></extra>'
    else:
        print("Warning: Missing 'DENOMINAZIONE' column required for 'aree_verdi' hover text. Using default.")
        aree_verdi_gdf['hover_text'] = 'Area Verde'
else:
    print("Info: Aree Verdi GeoDataFrame is empty, skipping hover text generation.")


# --- Folium Map Plotting ---
def add_markers_to_map(
    m,
    gdf,
    feature_group, # Pass the FeatureGroup to add markers to
    color,
    radius,
    id_col,
    name_col,
    hover_col=None,
    add_range_circles=False, # New: Flag to add range circles
    range_radius=0,          # New: Radius for range circles (meters)
    range_feature_group=None # New: FeatureGroup for range circles
    ):
    """Helper function to add markers and optional range circles to Folium FeatureGroups."""
    if gdf is None or gdf.empty:
        print(f"Skipping empty or None GeoDataFrame for color {color}.")
        return

    if 'geometry' not in gdf.columns:
        print(f"Warning: No 'geometry' column found for {feature_group.layer_name}. Cannot add markers.")
        return

    for idx, row in gdf.iterrows():
        if row.geometry is None or not hasattr(row.geometry, 'y') or not hasattr(row.geometry, 'x'):
            print(f"Warning: Skipping row {idx} due to invalid geometry.")
            continue

        lat, lon = row.geometry.y, row.geometry.x
        popup_text = str(row.get(name_col, f"ID: {row.get(id_col, idx)}"))
        tooltip_text = str(row.get(hover_col if hover_col and hover_col in row else name_col, popup_text))

        # Add the marker
        folium.CircleMarker(
            location=[lat, lon],
            radius=radius,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=folium.Popup(popup_text, max_width=300),
            tooltip=tooltip_text
        ).add_to(feature_group) # Add marker to its group

        # Add the range circle if requested and valid
        if add_range_circles and range_radius > 0 and range_feature_group is not None:
            folium.Circle(
                location=[lat, lon],
                radius=range_radius, # Radius in meters
                color=color,       # Use same color or choose another like 'orange'
                weight=1,          # Line weight
                fill=True,
                fill_color=color,
                fill_opacity=0.1   # Make range circles more transparent
            ).add_to(range_feature_group) # Add circle to its specific group


def plot_map_folium(
    center_location=[44.4949, 11.3426],
    zoom=13.5,
    show_scuole=True,
    show_porte=True,
    show_aree_verdi=True,
    show_porte_range=False,   # Control initial visibility of porte range
    porte_range_radius=650    # Define porte range radius in meters
    ):
    """Creates and returns a Folium map with specified layers."""
    print(f"Generating map with Porte range radius: {porte_range_radius}m (Visible: {show_porte_range})")
    # Create base map
    m = folium.Map(location=center_location, zoom_start=zoom, tiles="CartoDB positron")

    # --- Layer Order Control ---
    # 1. Create and add the Range Circle layer FIRST (so it's underneath)
    porte_range_fg = folium.FeatureGroup(name=f"Porte Range ({porte_range_radius}m)", show=show_porte_range).add_to(m)

    # 2. Create the Marker layers (but don't add them to the map yet)
    scuole_fg = folium.FeatureGroup(name="Scuole", show=show_scuole)
    porte_fg = folium.FeatureGroup(name="Porte", show=show_porte)
    aree_verdi_fg = folium.FeatureGroup(name="Aree Verdi", show=show_aree_verdi)

    # 3. Populate the layers with data using the helper function
    #    (The helper adds markers/circles to the FeatureGroups passed to it)
    if 'scuole_gdf' in globals() and not scuole_gdf.empty:
        add_markers_to_map(m, scuole_gdf, scuole_fg, 'blue', 5, 'CODICE_SCUOLA', 'NOME', 'hover_text')

    if 'porte_gdf' in globals() and not porte_gdf.empty:
        # Note: add_markers_to_map now adds markers to porte_fg and circles to porte_range_fg
        add_markers_to_map(
            m=m, # Pass map context if needed by helper, though not strictly necessary here
            gdf=porte_gdf,
            feature_group=porte_fg,           # Add markers to this group
            color='red',
            radius=7,
            id_col='id',
            name_col='name',
            hover_col='hover_text',
            add_range_circles=True,           # Tell function to add circles
            range_radius=porte_range_radius,  # Pass the radius
            range_feature_group=porte_range_fg # Pass the dedicated group for circles
        )

    if 'aree_verdi_gdf' in globals() and not aree_verdi_gdf.empty:
        add_markers_to_map(m, aree_verdi_gdf, aree_verdi_fg, 'green', 6, 'ID_OGGETTO', 'DENOMINAZIONE', 'hover_text')

    # 4. Add the Marker layers to the map AFTER the range layer
    scuole_fg.add_to(m)
    porte_fg.add_to(m)
    aree_verdi_fg.add_to(m)

    # 5. Add Layer Control - it will pick up all FeatureGroups added to the map
    folium.LayerControl().add_to(m)

    return m

# --- Example Usage ---
if __name__ == "__main__":
    print("Generating Folium map...")
    if 'scuole_gdf' not in globals() or 'porte_gdf' not in globals() or 'aree_verdi_gdf' not in globals():
         print("Error: GeoDataFrames not initialized properly before plotting.")
    else:
        # --- Customize Map Generation Here ---
        map_porte_range_visible = True # Set to True to show range circles initially
        map_porte_radius_meters = 750  # Set desired radius in meters

        bologna_map = plot_map_folium(
            show_scuole=True,
            show_porte=True,
            show_aree_verdi=True,
            show_porte_range=map_porte_range_visible, # Pass visibility flag
            porte_range_radius=map_porte_radius_meters # Pass radius value
        )

        # Save the map to an HTML file
        map_filename = "bologna_map_with_range.html" # Changed filename
        map_filepath = os.path.join(BASE_DIR, map_filename)
        bologna_map.save(map_filepath)
        print(f"Map saved to {map_filepath}")

        # Optional: Open the map
        try:
            import webbrowser
            webbrowser.open(f"file://{os.path.realpath(map_filepath)}")
        except ImportError:
            print("Install 'webbrowser' module to automatically open the map.")
        except Exception as e:
            print(f"Could not automatically open the map: {e}")