import streamlit as st
import osmnx as ox
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import pandas as pd
from shapely.geometry import LineString
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

st.title("Dynamic Erosion Control Monitoring Dashboard")
st.write("Identify high-risk roads near water bodies for construction compliance 
in Sachsen, Germany (or any region). Data fetched live from OpenStreetMap.")

# User inputs
region = st.text_input("Enter Region (e.g., 'Dresden, Sachsen, Germany')", 
value="Dresden, Sachsen, Germany")
buffer_distance = st.slider("Water Buffer Distance (meters) for Risk Assessment", 
10, 200, 50)
fetch_data = st.button("Fetch and Analyze Data")

if fetch_data:
    try:
        st.write("Fetching roads and water bodies...")
        
        # Fetch road network as graph, then convert to GeoDataFrame
        graph = ox.graph_from_place(region, network_type="all")
        roads_gdf = ox.graph_to_gdfs(graph, nodes=False, edges=True)
        roads_gdf = roads_gdf.to_crs("EPSG:4326")  # Ensure consistent CRS
        roads_gdf["length_m"] = roads_gdf.length * 111320  # Approx meters 
(simplified)
        roads_gdf["fclass"] = roads_gdf["highway"]  # OSM equivalent to fclass
        
        # Fetch water bodies
        water_tags = {"natural": "water", "waterway": True}
        water_gdf = ox.geometries_from_place(region, tags=water_tags)
        water_gdf = water_gdf.to_crs("EPSG:4326")
        
        # Buffer water bodies
        water_buffer = water_gdf.buffer(buffer_distance / 111320)  # Approx 
degrees to meters
        
        # Find roads near water (intersect buffer)
        roads_near_water = gpd.sjoin(roads_gdf, 
gpd.GeoDataFrame(geometry=water_buffer), how="inner", predicate="intersects")
        roads_near_water = roads_near_water.drop_duplicates(subset="osmid")  # 
Dedupe like your original
        
        # Simulate erosion risk (heuristic: high if close and certain types; 
expand to ML)
        def calculate_risk(row):
            if row["length_m"] > 100 and row["fclass"] in ["path", "track", 
"footway"]:  # Unpaved, long roads higher risk
                return "High"
            else:
                return "Low"
        
        roads_near_water["predicted_risk"] = 
roads_near_water.apply(calculate_risk, axis=1)
        
        # Limit to 1000 for performance
        filtered_gdf = roads_near_water.head(1000)
        st.write(f"Analyzed {len(filtered_gdf)} roads near water.")
        
    except Exception as e:
        st.error(f"Error fetching/processing data: {e}")
        logger.error(e)

else:
    filtered_gdf = pd.DataFrame()  # Empty placeholder

# Filters (applied after fetch)
if not filtered_gdf.empty:
    st.sidebar.header("Filter Options")
    fclass_options = filtered_gdf["fclass"].unique()
    fclass_filter = st.sidebar.multiselect("Select Road Types", 
options=fclass_options, default=fclass_options)
    
    risk_options = filtered_gdf["predicted_risk"].unique()
    risk_filter = st.sidebar.multiselect("Select Risk Levels", 
options=risk_options, default=risk_options)
    
    filtered_gdf = filtered_gdf[filtered_gdf["fclass"].isin(fclass_filter) & 
filtered_gdf["predicted_risk"].isin(risk_filter)]
    
    st.subheader("Filtered Roads Table")
    display_df = filtered_gdf[["osmid", "fclass", "length_m", 
"predicted_risk"]].rename(columns={"osmid": "osm_id"})
    st.dataframe(display_df)
    
    # Download
    csv = display_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download Filtered Data", csv, "filtered_roads.csv", 
"text/csv")
    
    # Map
    st.subheader("Map of Roads Near Water (Colored by Risk)")
    if not filtered_gdf.empty:
        m = folium.Map(location=[51.053, 13.738], zoom_start=12)  # Centered on 
Dresden
        
        def style_function(feature):
            risk = feature["properties"]["predicted_risk"]
            color = "red" if risk == "High" else "green"
            return {"color": color, "weight": 2}
        
        folium.GeoJson(filtered_gdf.to_json(), style_function=style_function, 
tooltip=folium.GeoJsonTooltip(fields=["fclass", "predicted_risk", 
"length_m"])).add_to(m)
        
        st_folium(m, width=700, height=500)

# Fallback: Upload your original files if needed
st.sidebar.header("Upload Custom Data (Optional)")
uploaded_csv = st.sidebar.file_uploader("Upload erosion_predictions.csv", 
type="csv")
uploaded_shp = st.sidebar.file_uploader("Upload 
sachsen_roads_near_water_deduped.shp", type="shp")
# Add logic to load/merge if uploaded (similar to your original)

st.write("Note: Risk is simulated; integrate your ML model for accurate 
predictions.")
