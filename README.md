# TEMPO-NO2-Visualization-and-Shapefile-Masking

This project processes and visualizes tropospheric NO₂ column data from NASA TEMPO satellite NetCDF files and overlays them with shapefiles representing a study region (e.g., Karnes County or EFS region).

## 🛰️ What This Script Does
- Loads tropospheric NO₂ data from TEMPO `.nc` files.
- Extracts geolocation (latitude, longitude) and NO₂ values.
- Filters and interpolates the data onto a uniform grid.
- Masks the results using a shapefile boundary.
- Generates a clear, publication-ready NO₂ heatmap using Cartopy.
  
## 📁 Folder Structure

| **Folder/File**            | **Description**                                                                  |
| -------------------------- | -------------------------------------------------------------------------------- |
| `Script`    | Main Python script for processing, masking, interpolating, and plotting NO₂ data |
| `Results` | 📸 Example output plot showing NO₂ concentrations over the selected region       |
| `Data`                    | Folder containing TEMPO NetCDF files NetCDF files (included in release v1.0.0) and shapefiles       |
| `README.md`                | Project overview, setup instructions, and module descriptions                    |



📄 Script Overview

The script loads tropospheric NO₂ data from TEMPO NetCDF files, filters and interpolates the data within a defined study area using a shapefile, and visualizes the results on a map. It handles data cleaning, spatial masking, and regridding before producing a high-resolution heatmap of NO₂ concentrations.
Downloading TEMPO Satellite NetCDF Files
You can download NetCDF files of TEMPO (satellite data) from NASA's Earthdata Search portal.

🔗 Data Source
Visit: [NASA Earthdata Search](https://search.earthdata.nasa.gov/search)

📥 How to Download
Go to the link above.
Use the search bar to look for datasets related to "TEMPO satellite NetCDF" or other related keywords.
Apply filters
Select the datasets you're interested in.
Click Download and follow the instructions (you may need to create a free Earthdata login or use the Chrono Download Manager extension if you're using the Chrome browser).

📦 Required Modules Here’s what each package does in the script:
| **Module**                   | **Alias**  | **Purpose in Script**                                                                 |
| ---------------------------- | ---------- | ------------------------------------------------------------------------------------- |
| `xarray`                     | `xr`       | Reads multi-dimensional NetCDF files (e.g., NO₂ and geolocation datasets from TEMPO). |
| `numpy`                      | `np`       | Performs numerical operations such as array manipulation and filtering.               |
| `matplotlib.pyplot`          | `plt`      | Creates static visualizations (e.g., NO₂ heatmap, colorbars, titles).                 |
| `cartopy.crs`                | `ccrs`     | Defines map projections for accurate geospatial plotting.                             |
| `cartopy.feature`            | `cfeature` | Adds map features like coastlines and borders to plots.                               |
| `geopandas`                  | `gpd`      | Loads, manipulates, and spatially joins shapefiles (e.g., study region boundaries).   |
| `glob`                       | –          | Finds all matching `.nc` files in a directory (e.g., loads all TEMPO data files).     |
| `scipy.interpolate.griddata` | –          | Interpolates scattered NO₂ data onto a regular lat/lon grid for smooth mapping.       |
| `shapely.geometry.Point`     | –          | Creates point geometries to check which locations fall within the shapefile boundary. |
| `cartopy.mpl.gridliner`      | –          | Adds latitude and longitude gridlines with labels to the Cartopy map.                 |

