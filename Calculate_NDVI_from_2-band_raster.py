import rasterio
from rasterio.plot import show

with rasterio.open("band4.tif") as red:
    red_band = red.read(1).astype(float)
with rasterio.open("band8.tif") as nir:
    nir_band = nir.read(1).astype(float)

ndvi = (nir_band - red_band) / (nir_band + red_band)

profile = red.profile
profile.update(dtype=rasterio.float32, count=1)
with rasterio.open("ndvi.tif", "w", **profile) as dst:
    dst.write(ndvi.astype(rasterio.float32), 1)
