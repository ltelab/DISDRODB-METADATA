import os
import folium
import numpy as np
import disdrodb
import html
from pathlib import Path

# Configurable output dir for CI
dst_dir = os.environ.get("OUTPUT_DIR", "public")  # locally create on /public directory
Path(dst_dir).mkdir(parents=True, exist_ok=True)
map_filepath = os.path.join(dst_dir, "stations_map.html")

# Define temporary directory where to save Metadata Archive
tmp_dir = os.environ.get(
    "TMPDIR", "/tmp/"
)  # locally create on /tmp directory (on Linux)
tmp_metadata_dir = os.path.join(tmp_dir, "DISDRODB-METADATA", "DISDRODB")

# Download metadata
disdrodb.download_metadata_archive(tmp_dir, force=True)

# Load & filter
df = disdrodb.read_metadata_archive(metadata_archive_dir=tmp_metadata_dir)
df = df[
    (df["platform_type"] == "fixed")
    & (df["longitude"] != -9999)
    & (df["latitude"] != -9999)
]


# Jitter stations coordinates to avoid overlapping
def jitter_lat_lon(latitudes, longitudes, max_meters=10):
    """Add random jitter up to ±max_meters to avoid overlapping points."""
    latitudes = np.asarray(latitudes)
    longitudes = np.asarray(longitudes)

    # Latitude: constant conversion
    meters_per_deg_lat = 111_320
    dlat = (
        np.random.uniform(-max_meters, max_meters, size=len(latitudes))
        / meters_per_deg_lat
    )

    # Longitude: depends on latitude
    meters_per_deg_lon = meters_per_deg_lat * np.cos(np.radians(latitudes))
    dlon = (
        np.random.uniform(-max_meters, max_meters, size=len(longitudes))
        / meters_per_deg_lon
    )

    return latitudes + dlat, longitudes + dlon


lats, lons = jitter_lat_lon(
    latitudes=df["latitude"], longitudes=df["longitude"], max_meters=10
)
df["latitude"] = lats
df["longitude"] = lons


# Define popup
def row_popup_html(row):
    parts = []
    for col in df.columns:
        val = row[col]
        parts.append(f"<b>{html.escape(str(col))}</b>: {html.escape(str(val))}")
    return (
        "<div style='max-width:320px; font-family:system-ui, sans-serif; font-size:12px'>"
        + "<br>".join(parts)
        + "</div>"
    )


# Create map
m = folium.Map(
    location=[0, 0],
    tiles=None,
    world_copy_jump=False,
    no_wrap=True,
    max_bounds=True,
    prefer_canvas=True,
)
folium.TileLayer("OpenStreetMap", name="OSM", max_zoom=19, no_wrap=True).add_to(m)
folium.TileLayer("CartoDB positron", name="Light", max_zoom=19, no_wrap=True).add_to(m)
folium.TileLayer("CartoDB dark_matter", name="Dark", max_zoom=19, no_wrap=True).add_to(
    m
)
folium.LayerControl().add_to(m)
m.fit_bounds([[-90, -180], [90, 180]], padding=(0, 0))

# Add points
for _, row in df.iterrows():
    folium.CircleMarker(
        location=[row.latitude, row.longitude],
        radius=2,
        color="#2563eb",
        weight=1,
        fill=True,
        fill_color="#2563eb",
        fill_opacity=0.75,
        popup=folium.Popup(row_popup_html(row), max_width=300),
    ).add_to(m)

# Save map
m.save(map_filepath)
print(f"Map written to: {map_filepath}")
