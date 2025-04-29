import geopandas as gpd
import rasterio
from rasterio.mask import mask

shapefile = gpd.read_file("boundary.shp")
with rasterio.open("image.tif") as src:
    out_image, out_transform = mask(src, shapefile.geometry, crop=True)
    out_meta = src.meta.copy()

out_meta.update({"height": out_image.shape[1], "width": out_image.shape[2], "transform": out_transform})
with rasterio.open("clipped.tif", "w", **out_meta) as dest:
    dest.write(out_image)
