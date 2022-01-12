import pdal
from osgeo import gdal
from osgeo import gdalconst
import glob
import os

path = "C:/Users/joelb/lidardaten/2014_transformiert/"
prefix = "2014"

files = glob.glob(path + "*.la*")

for i in range(len(files)):
    files[i] = files[i].replace('\\', '/')

for i in range(len(files)):
    pdal_json = '''
    [
        "{}",



        {}
        "filename": "outpython_{}_{}.tif",
        "gdaldriver": "GTiff",
        "output_type": "min",
        "resolution": "1",
        "type": "writers.gdal"
        {}
    ]
    '''

    pdal_json = pdal_json.format(files[i], '{', prefix, i, '}')

    pipeline = pdal.Pipeline(pdal_json)
    count = pipeline.execute()
    arrays = pipeline.arrays
    metadata = pipeline.metadata
    log = pipeline.log


# list all files in directory that match pattern
demList = glob.glob("outpython_" + prefix + "_*.tif")

# build virtual raster and convert to geotiff
vrt = gdal.BuildVRT("merged_" + prefix + ".vrt", demList)
gdal.Translate("merged_" + prefix + ".tif", vrt, xRes = 1, yRes = -1)
vrt = None

#delete generatet Tiff Tiles
for i in range(len(files)):
    os.remove("outpython_" + prefix + "_"+ str(i) + ".tif")


#output extets
data = gdal.Open('merged_' + prefix + '.tif', gdalconst.GA_ReadOnly)
geoTransform = data.GetGeoTransform()
minx = geoTransform[0]
maxy = geoTransform[3]
maxx = minx + geoTransform[1] * data.RasterXSize
miny = maxy + geoTransform[5] * data.RasterYSize
print(minx, miny, maxx, maxy)
data = None