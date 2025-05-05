import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import geopandas as gpd
import glob
from scipy.interpolate import griddata
from shapely.geometry import Point
import cartopy.mpl.gridliner as gridliner

# --- Load Shapefile ---
shapefiles = {
    "karnes_county": "/Users/mbohloul/Desktop/ne_50/tl_2023_48255_faces/tl_2023_48255_faces.shp",
    "efs_counties": "/Users/mbohloul/Desktop/EFS-Project/Main files/Shape files/Data_to_exposure_team/Data_to_exposure_team/EFS_counties_shapefile/EFS Counties.shp"
}

# Select the desired shapefile
shapefile_path = shapefiles["efs_counties"]   # Change key to switch files


gdf = gpd.read_file(shapefile_path)
gdf = gdf.to_crs(epsg=4326)  # Ensure CRS matches NO₂ data
print("Shapefile CRS:", gdf.crs)

# --- Load NO₂ Data ---
nc_files = sorted(glob.glob("/Users/mbohloul/Desktop/TEMPO/DATA/*.nc"))

no2_values, lat_values, lon_values = [], [], []

for file in nc_files:
    no2_ds = xr.open_dataset(file, group="product")
    geo_ds = xr.open_dataset(file, group="geolocation")

    # Extract NO₂ and geolocation data
    no2_data = no2_ds["vertical_column_troposphere"].values.flatten()
    lat = geo_ds["latitude"].values.flatten()
    lon = geo_ds["longitude"].values.flatten()

    # Remove NaN values
    mask = ~np.isnan(no2_data)
    no2_values.extend(no2_data[mask])
    lat_values.extend(lat[mask])
    lon_values.extend(lon[mask])

# Convert lists to numpy arrays
no2_values = np.array(no2_values)
lat_values = np.array(lat_values)
lon_values = np.array(lon_values)

# --- Mask Data Using Shapefile ---
study_area = gdf.geometry.unary_union  # Merge all geometries into one
points = gpd.GeoDataFrame(geometry=[Point(lon, lat) for lon, lat in zip(lon_values, lat_values)], crs="EPSG:4326")

# Use spatial join to quickly filter points inside the study area
points = points.sjoin(gdf, how="inner")

# Apply the mask
no2_values = no2_values[points.index]
lat_values = lat_values[points.index]
lon_values = lon_values[points.index]

# --- Regrid Data to Uniform Grid ---
grid_lat = np.linspace(lat_values.min(), lat_values.max(), 200)
grid_lon = np.linspace(lon_values.min(), lon_values.max(), 200)
grid_lon, grid_lat = np.meshgrid(grid_lon, grid_lat)
grid_no2 = griddata((lon_values, lat_values), no2_values, (grid_lon, grid_lat), method="linear")

# --- Apply Mask to Interpolated Grid ---
mask = np.array([[Point(lon, lat).within(study_area) for lon, lat in zip(lon_row, lat_row)] for lon_row, lat_row in zip(grid_lon, grid_lat)])
grid_no2[~mask] = np.nan  # Remove values outside the study area

# --- Ensure NO₂ Data Starts from Zero ---
grid_no2[grid_no2 < 0] = 0  # Clip negative values

# --- Visualization ---
fig, ax = plt.subplots(figsize=(12, 6), subplot_kw={'projection': ccrs.PlateCarree()})

# Set extent to match the study area
minx, miny, maxx, maxy = gdf.total_bounds
ax.set_extent([minx, maxx, miny, maxy], crs=ccrs.PlateCarree())

# Plot NO₂ data with masked areas removed, starting from zero
img = ax.pcolormesh(grid_lon, grid_lat, grid_no2, cmap="inferno", shading="auto", transform=ccrs.PlateCarree(), vmin=0)

# Overlay shapefile boundary
gdf.boundary.plot(ax=ax, edgecolor="white", linewidth=0.1)

# Add map features
ax.coastlines()
ax.add_feature(cfeature.BORDERS, linestyle=":")
ax.set_title("TEMPO NO₂ Concentration Over Karnes County")

# --- Add Gridlines with Latitude and Longitude Labels ---
gl = ax.gridlines(draw_labels=True, linestyle="--", color="gray", alpha=0.5)
gl.top_labels = False  # Hide labels on the top
gl.right_labels = False  # Hide labels on the right
gl.xlabel_style = {'size': 10, 'color': 'black'}
gl.ylabel_style = {'size': 10, 'color': 'black'}

# Colorbar, starting from 0
cbar = plt.colorbar(img, ax=ax, orientation="horizontal", fraction=0.05)
cbar.set_label("NO₂ (molecules/cm²)")

# Show plot
plt.show()
