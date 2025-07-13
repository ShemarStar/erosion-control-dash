import geopandas as gpd
import os
os.environ['GDAL_SHAPE_RESTORE_SHX'] = 'YES'
gdf = gpd.read_file('sachsen_roads_near_water_deduped.shp')
# Save with WGS84 projection (adjust CRS if your data uses a different one, e.g., EPSG:25833 for Saxony)
gdf.to_file('sachsen_roads_near_water_deduped.shp', crs='EPSG:4326')
print('Shapefile saved with all components')
