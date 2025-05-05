# TEMPO-NO2-Visualization-and-Shapefile-Masking

This project processes and visualizes tropospheric NO₂ column data from NASA TEMPO satellite NetCDF files and overlays them with shapefiles representing a study region (e.g., Karnes County or EFS region).

## 🛰️ What This Script Does
- Loads tropospheric NO₂ data from TEMPO `.nc` files.
- Extracts geolocation (latitude, longitude) and NO₂ values.
- Filters and interpolates the data onto a uniform grid.
- Masks the results using a shapefile boundary.
- Generates a clear, publication-ready NO₂ heatmap using Cartopy.
## 📁 Folder Structure
├── script/
│ └── visualize_no2.py # Main Python script
├── data/
│ ├── shapefiles/ # Put .shp files here
│ └── sample_NO2_data.nc # Optional: sample NetCDF
├── results/
│ └── no2_plot_example.png # Example output


Downloading TEMPO Satellite NetCDF Files
You can download NetCDF files of TEMPO (satellite data) from NASA's Earthdata Search portal.

🔗 Data Source
Visit: NASA Earthdata Search
📥 How to Download
Go to the link above.
Use the search bar to look for datasets related to "TEMPO satellite NetCDF" or other related keywords.
Apply filters
Select the datasets you're interested in.
Click Download and follow the instructions (you may need to create a free Earthdata login or use the Chrono Download Manager extension if you're using the Chrome browser).
