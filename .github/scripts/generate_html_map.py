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


# Jitter coordinates to avoid overlapping
def rand_jitter(arr):
    thr_degs = 0.01
    return arr + np.random.randn(len(arr)) * thr_degs


df["latitude"] = rand_jitter(df["latitude"])
df["longitude"] = rand_jitter(df["longitude"])


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
