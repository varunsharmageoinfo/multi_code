'''
Problem Statement:
You are given:
A shapefile called villages.shp containing village boundaries.
Two GeoTIFF raster files: B04.tif (Red band), B08.tif (NIR band)

Your task is to:
Read and reproject villages.shp to EPSG:4326 (if not already).
Clip both raster bands to the extent of all villages combined.
Calculate NDVI and save the output as ndvi_output.tif.
Calculate the average NDVI for each village polygon, and print the top 5 villages with the highest NDVI.
'''
import geopandas as gpd
import rasterio
from rasterio.mask import mask
import numpy as np
from rasterstats import zonal_stats
import matplotlib.pyplot as plt

# STEP 1: Load and reproject village shapefile
villages = gpd.read_file("villages.shp")
if villages.crs != "EPSG:4326":
    villages = villages.to_crs("EPSG:4326")

# STEP 2: Clip raster bands
def clip_raster_to_shape(raster_path, shapes):
    with rasterio.open(raster_path) as src:
        clipped, transform = mask(src, shapes.geometry, crop=True)
        profile = src.meta.copy()
    profile.update({"height": clipped.shape[1], "width": clipped.shape[2], "transform": transform})
    return clipped[0], profile

red_band, red_profile = clip_raster_to_shape("B04.tif", villages)
nir_band, nir_profile = clip_raster_to_shape("B08.tif", villages)

# STEP 3: Calculate NDVI
ndvi = (nir_band.astype(float) - red_band.astype(float)) / \
       (nir_band.astype(float) + red_band.astype(float))
ndvi = np.nan_to_num(ndvi, nan=-9999)

# Save NDVI raster
ndvi_profile = red_profile
ndvi_profile.update(dtype=rasterio.float32, count=1, nodata=-9999)
with rasterio.open("ndvi_output.tif", "w", **ndvi_profile) as dst:
    dst.write(ndvi.astype(rasterio.float32), 1)

# STEP 4: Zonal NDVI summary
stats = zonal_stats(villages, ndvi, affine=ndvi_profile["transform"],
                    nodata=-9999, stats=["mean"], geojson_out=True)

# Extract top 5 villages by NDVI
village_ndvi = [(f["properties"]["mean"], f["properties"]) for f in stats if f["properties"]["mean"] is not None]
top5 = sorted(village_ndvi, key=lambda x: x[0], reverse=True)[:5]
for i, (mean_ndvi, props) in enumerate(top5):
    print(f"{i+1}. Village: {props.get('name', 'Unknown')}, Mean NDVI: {mean_ndvi:.4f}")
