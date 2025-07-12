# Erosion Control Monitoring Dashboard

This Streamlit dashboard is designed to identify high-risk roads near water bodies for construction compliance, focusing on the Saxony region. All data are projected in a suitable coordinate system (e.g., EPSG:25833 for Germany) with units in meters unless otherwise specified. The dataset integrates geospatial data from multiple sources, and their respective licenses must be respected by users.

## Data Sources

### 1) Saxony Roads Near Water (Shapefile)
- **Description**: A processed vector dataset (`sachsen_roads_near_water_deduped.shp`) containing roads near water bodies in Saxony, Germany, derived from OpenStreetMap (OSM) data. The dataset includes attributes like `osm_id`, `fclass`, `length_m`, and `predicted_risk`.
- **Source**: Adapted from OpenStreetMap (OSM) data, available at [openstreetmap.org](https://www.openstreetmap.org).
- **License**: Open Database License (ODbL) - users must attribute OSM and share alike.

### 2) Erosion Predictions (CSV)
- **Description**: A CSV file (`erosion_predictions.csv`) with 619 rows, containing `osm_id` and `predicted_risk` (e.g., "Low") for roads based on erosion risk analysis.
- **Source**: Custom predictions generated for this project.
- **License**: Freely available for academic and non-commercial use under project terms.

## Project Details
- **Purpose**: Monitors erosion risk for roads near water, aiding construction compliance in Saxony.
- **Tools**: Built with Python 3.13.5, Streamlit, pandas, geopandas, and folium.
- **Deployment**: Hosted on Render (e.g., `erosion-control-dash.onrender.com`).

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/ShemarStar/erosion-control-dash.git

