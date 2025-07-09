import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
st.title("Erosion Control Monitoring System")
st.write("Identify high-risk roads near water bodies for construction compliance.")
try:
    st.write("Loading data...")
    df = pd.read_csv("/Users/Shemar/projects/erosion_predictions.csv")
    st.write("CSV loaded, rows:", len(df))
    gdf = gpd.read_file("/Users/Shemar/projects/sachsen_roads_near_water_deduped.shp")
    st.write("Shapefile loaded, rows:", len(gdf))
    gdf["osm_id"] = gdf["osm_id"].astype("int64")
    df["osm_id"] = df["osm_id"].astype("int64")
    gdf = gdf.merge(df[["osm_id", "predicted_risk"]], on="osm_id", how="left")
    st.write("Merged rows:", len(gdf))
    gdf["predicted_risk"] = gdf["predicted_risk"].fillna("Unknown")
    filtered_gdf = gdf.head(1000)
    st.write("Filtered rows:", len(filtered_gdf))
    if filtered_gdf.empty or filtered_gdf['geometry'].isna().all():
        st.error("No valid data available.")
    else:
        st.write(f"Loaded {len(filtered_gdf)} roads with valid geometries.")
except Exception as e:
    st.error(f"Error loading data: {e}")
st.sidebar.header("Filter Options")
fclass_filter = st.sidebar.multiselect("Select Road Types", 
options=filtered_gdf["fclass"].unique(), default=filtered_gdf["fclass"].unique())
risk_filter = st.sidebar.multiselect("Select Risk Levels", options=["High", "Low", "Unknown"], 
default=["Low"])
filtered_df = df[df["fclass"].isin(fclass_filter) & df["predicted_risk"].isin(risk_filter)]
filtered_gdf = filtered_gdf[filtered_gdf["fclass"].isin(fclass_filter) & 
filtered_gdf["predicted_risk"].isin(risk_filter)]
st.subheader("Filtered Roads")
st.write(filtered_df[["osm_id", "fclass", "length_m", "predicted_risk"]])
# st.subheader("Download Data")
# csv = filtered_df.to_csv(index=False)
# st.download_button("Download Filtered Data", csv, "filtered_roads.csv", "text/csv")
st.subheader("Map of Roads Near Water")
if not filtered_gdf.empty and not filtered_gdf['geometry'].isna().all():
    m = folium.Map(location=[51.053, 13.738], zoom_start=15)
    try:
        st.write("Rendering map...")
        for idx, row in filtered_gdf.iterrows():
            geojson = row.geometry.__geo_interface__
            logger.debug(f"Row {idx+1}/{len(filtered_gdf)}: Geometry type: {row.geometry.geom_type}") 
            color = "green" if row["predicted_risk"] == "Low" else "red"
            folium.GeoJson(geojson, style_function=lambda x, color=color: {"color": color, 
"weight": 2}).add_to(m)
        map_data = st_folium(m, width=700, height=500)
        st.write("Map data returned:", map_data)
    except Exception as e:
        st.error(f"Error rendering map: {e}")
else:
    st.error("Map cannot be generated due to missing or invalid data.")

