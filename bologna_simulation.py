"""Bologna geographical data visualization tool."""

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import os
import folium
from folium.plugins import MarkerCluster
import sys
import data

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
CRS = "EPSG:4326"

def load_data(filename, delimiter=','):
    filepath = os.path.join(DATA_DIR, filename)
    try:
        return pd.read_csv(filepath, delimiter=delimiter)
    except FileNotFoundError:
        print(f"ERROR: Data file not found at {filepath}")
        sys.exit(1)

porte_dict = {key: data.porte_data[key]["coords"] for key in data.porte_data.keys()}
porte_df = pd.DataFrame.from_dict(porte_dict, orient='index', columns=['latitude', 'longitude'])
porte_df = porte_df.reset_index().rename(columns={"index":"name"})
aree_verdi_df = load_data("carta-tecnica-comunale-toponimi-parchi-e-giardini.csv", delimiter=';')
scuole_df = load_data("elenco-delle-scuole.csv", delimiter=';')

def parse_coordinates(geopoint):
    if pd.isna(geopoint) or not isinstance(geopoint, str):
        return None, None
    try:
        lat_str, lon_str = geopoint.split(',')
        return float(lon_str.strip()), float(lat_str.strip())
    except (ValueError, IndexError):
        return None, None

def create_gdf_from_points(df):
    temp_df = df.copy()
    lon_col, lat_col = 'longitude', 'latitude'

    if 'Geo Point' in temp_df.columns:
        coords = temp_df['Geo Point'].apply(parse_coordinates)
        valid_coords_mask = coords.notna() & coords.apply(lambda x: x != (None, None))
        if valid_coords_mask.any():
            temp_df = temp_df.loc[valid_coords_mask].copy()
            temp_df[[lon_col, lat_col]] = pd.DataFrame(coords[valid_coords_mask].tolist(), index=temp_df.index)
        else:
            return gpd.GeoDataFrame(crs=CRS)
    elif lon_col in temp_df.columns and lat_col in temp_df.columns:
        temp_df[lon_col] = pd.to_numeric(temp_df[lon_col], errors='coerce')
        temp_df[lat_col] = pd.to_numeric(temp_df[lat_col], errors='coerce')
        temp_df.dropna(subset=[lon_col, lat_col], inplace=True)
        if temp_df.empty:
            return gpd.GeoDataFrame(crs=CRS)
    elif 'Geo Shape' in temp_df.columns:
        try:
            temp_df[['lat_tmp', 'lon_tmp']] = temp_df['Geo Shape'].str.extract(r'"coordinates":\s*\[\s*(\d+\.\d+)\s*,\s*(\d+\.\d+)\s*\]', expand=True)
            temp_df[lon_col] = pd.to_numeric(temp_df['lon_tmp'], errors='coerce')
            temp_df[lat_col] = pd.to_numeric(temp_df['lat_tmp'], errors='coerce')
            temp_df.dropna(subset=[lon_col, lat_col], inplace=True)
        except Exception:
            return gpd.GeoDataFrame(crs=CRS)
    else:
        return gpd.GeoDataFrame(crs=CRS)

    if lon_col in temp_df.columns and lat_col in temp_df.columns and not temp_df.empty:
        try:
            geometry = [Point(xy) for xy in zip(temp_df[lon_col], temp_df[lat_col])]
            cols_to_drop = [c for c in [lon_col, lat_col, 'lat_tmp', 'lon_tmp'] if c in temp_df.columns]
            return gpd.GeoDataFrame(temp_df.drop(columns=cols_to_drop, errors='ignore'), geometry=geometry, crs=CRS)
        except Exception:
            return gpd.GeoDataFrame(crs=CRS)
    else:
        return gpd.GeoDataFrame(crs=CRS)

porte_gdf = create_gdf_from_points(porte_df)
aree_verdi_gdf = create_gdf_from_points(aree_verdi_df)
scuole_gdf = create_gdf_from_points(scuole_df)

# Prepare hover text
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
        scuole_gdf['hover_text'] = 'Scuola'

if not porte_gdf.empty and 'name' in porte_gdf.columns:
    porte_gdf['hover_text'] = '<b>' + porte_gdf['name'].astype(str) + '</b>' + '<extra></extra>'
else:
    porte_gdf['hover_text'] = 'Porta'

if not aree_verdi_gdf.empty and 'DENOMINAZIONE' in aree_verdi_gdf.columns:
    aree_verdi_gdf['hover_text'] = '<b>' + aree_verdi_gdf['DENOMINAZIONE'].astype(str) + '</b>' + '<extra></extra>'
else:
    aree_verdi_gdf['hover_text'] = 'Area Verde'

def add_markers_to_map(m, gdf, feature_group, color, radius, id_col, name_col, hover_col=None, 
                      add_range_circles=False, range_radius=0, range_feature_group=None):
    if gdf is None or gdf.empty or 'geometry' not in gdf.columns:
        return

    for idx, row in gdf.iterrows():
        if row.geometry is None or not hasattr(row.geometry, 'y'):
            continue

        lat, lon = row.geometry.y, row.geometry.x
        popup_text = str(row.get(name_col, f"ID: {row.get(id_col, idx)}"))
        tooltip_text = str(row.get(hover_col if hover_col and hover_col in row else name_col, popup_text))

        folium.CircleMarker(
            location=[lat, lon],
            radius=radius,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=folium.Popup(popup_text, max_width=300),
            tooltip=tooltip_text
        ).add_to(feature_group)

        if add_range_circles and range_radius > 0 and range_feature_group is not None:
            folium.Circle(
                location=[lat, lon],
                radius=range_radius,
                color=color,
                weight=1,
                fill=True,
                fill_color=color,
                fill_opacity=0.1
            ).add_to(range_feature_group)

def plot_map_folium(center_location=[44.4949, 11.3426], zoom=13.5, show_scuole=True,
                   show_porte=True, show_aree_verdi=True, show_porte_range=False, 
                   porte_range_radius=650):
    m = folium.Map(location=center_location, zoom_start=zoom, tiles="CartoDB positron")
    
    porte_range_fg = folium.FeatureGroup(name=f"Porte Range ({porte_range_radius}m)", show=show_porte_range).add_to(m)
    scuole_fg = folium.FeatureGroup(name="Scuole", show=show_scuole)
    porte_fg = folium.FeatureGroup(name="Porte", show=show_porte)
    aree_verdi_fg = folium.FeatureGroup(name="Aree Verdi", show=show_aree_verdi)

    if not scuole_gdf.empty:
        add_markers_to_map(m, scuole_gdf, scuole_fg, 'blue', 5, 'CODICE_SCUOLA', 'NOME', 'hover_text')

    if not porte_gdf.empty:
        add_markers_to_map(
            m=m,
            gdf=porte_gdf,
            feature_group=porte_fg,
            color='red',
            radius=7,
            id_col='id',
            name_col='name',
            hover_col='hover_text',
            add_range_circles=True,
            range_radius=porte_range_radius,
            range_feature_group=porte_range_fg
        )

    if not aree_verdi_gdf.empty:
        add_markers_to_map(m, aree_verdi_gdf, aree_verdi_fg, 'green', 6, 'ID_OGGETTO', 'DENOMINAZIONE', 'hover_text')

    scuole_fg.add_to(m)
    porte_fg.add_to(m)
    aree_verdi_fg.add_to(m)
    folium.LayerControl().add_to(m)

    return m

def find_points_in_range(lat, lon, radius):
    projected_crs = "EPSG:32632"
    original_crs = scuole_gdf.crs

    point_geom = gpd.GeoSeries([Point(lon, lat)], crs=original_crs)
    point_proj = point_geom.to_crs(projected_crs).iloc[0]

    scuole_proj = scuole_gdf.to_crs(projected_crs)
    aree_verdi_proj = aree_verdi_gdf.to_crs(projected_crs)

    nearby_schools_indices = scuole_proj[scuole_proj.distance(point_proj) <= radius].index
    nearby_parks_indices = aree_verdi_proj[aree_verdi_proj.distance(point_proj) <= radius].index

    nearby_schools = scuole_gdf.loc[nearby_schools_indices]
    nearby_parks = aree_verdi_gdf.loc[nearby_parks_indices]

    return nearby_schools, nearby_parks


# Helpful for debugging
if __name__ == "__main__":
    bologna_map = plot_map_folium(
        show_porte_range=True,
        porte_range_radius=750
    )

    map_filepath = os.path.join(BASE_DIR, "bologna_map_with_range.html")
    bologna_map.save(map_filepath)
    print(f"Map saved to {map_filepath}")

    try:
        import webbrowser
        webbrowser.open(f"file://{os.path.realpath(map_filepath)}")
    except Exception as e:
        print(f"Could not automatically open the map: {e}")