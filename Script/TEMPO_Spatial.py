# Script: TEMPO-NO-Visualization-and-Shapefile-Masking
# Description: Process and visualize TEMPO NO₂ data over a defined study region.

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
import os

# === User-defined Paths (Update these) ===
DATA_DIR = "Data"  # Folder where .nc files are stored
SHAPEFILE_OPTIONS = {
    "karnes_county": "Data/shapefiles/karnes_county.shp",
    "efs_counties": "Data/shapefiles/efs_counties.shp"
}
SELECTED_SHAPE = "efs_counties"  # Change to "karnes_county" if needed

# --- Load Shapefile ---
shapefile_path = SHAPEFILE_OPTIONS[SELECTED_SHAPE]
gdf = gpd.read_file(shapefile_path).to_crs(epsg=4326)
print("Shapefile CRS:", gdf.crs)

# --- Load NO₂ Data from NetCDF files ---
nc_files = sorted(glob.glob(os.path.join(DATA_DIR, "*.nc")))

no2_values, lat_values, lon_values = [], [], []

for file in nc_files:
    no2_ds = xr.open_dataset(file, group="product")
    geo_ds = xr.open_dataset(file, group="geolocation")

    no2_data = no2_ds["vertical_column_troposphere"].values.flatten()
    lat = geo_ds["latitude"].values.flatten()
    lon = geo_ds["longitude"].values.flatten()

    mask = ~np.isnan(no2_data)
    no2_values.extend(no2_data[mask])
    lat_values.extend(lat[mask])
    lon_values.extend(lon[mask])

no2_values = np.array(no2_values)
lat_values = np.array(lat_values)
lon_values = np.array(lon_values)

# --- Mask Data Using Shapefile ---
study_area = gdf.geometry.unary_union
points = gpd.GeoDataFrame(geometry=[Point(lon, lat) for lon, lat in zip(lon_values, lat_values)], crs="EPSG:4326")
points = points.sjoin(gdf, how="inner")

no2_values = no2_values[points.index]
lat_values = lat_values[points.index]
lon_values = lon_values[points.index]

# --- Regrid to Regular Grid ---
grid_lat = np.linspace(lat_values.min(), lat_values.max(), 200)
grid_lon = np.linspace(lon_values.min(), lon_values.max(), 200)
grid_lon, grid_lat = np.meshgrid(grid_lon, grid_lat)
grid_no2 = griddata((lon_values, lat_values), no2_values, (grid_lon, grid_lat), method="linear")

# --- Apply Mask to Grid ---
mask = np.array([[Point(lon, lat).within(study_area) for lon, lat in zip(lon_row, lat_row)] for lon_row, lat_row in zip(grid_lon, grid_lat)])
grid_no2[~mask] = np.nan
grid_no2[grid_no2 < 0] = 0  # Ensure non-negative values

# --- Plotting ---
fig, ax = plt.subplots(figsize=(12, 6), subplot_kw={'projection': ccrs.PlateCarree()})

minx, miny, maxx, maxy = gdf.total_bounds
ax.set_extent([minx, maxx, miny, maxy], crs=ccrs.PlateCarree())

img = ax.pcolormesh(grid_lon, grid_lat, grid_no2, cmap="inferno", shading="auto", transform=ccrs.PlateCarree(), vmin=0)
gdf.boundary.plot(ax=ax, edgecolor="white", linewidth=0.1)

ax.coastlines()
ax.add_feature(cfeature.BORDERS, linestyle=":")
ax.set_title("TEMPO NO₂ Concentration Over Study Area")

gl = ax.gridlines(draw_labels=True, linestyle="--", color="gray", alpha=0.5)
gl.top_labels = False
gl.right_labels = False
gl.xlabel_style = {'size': 10, 'color': 'black'}
gl.ylabel_style = {'size': 10, 'color': 'black'}

cbar = plt.colorbar(img, ax=ax, orientation="horizontal", fraction=0.05)
cbar.set_label("NO₂ (molecules/cm²)")

plt.savefig("Results/mean_no2_map.png", dpi=300, bbox_inches="tight")
plt.show()
