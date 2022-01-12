import pdal
from osgeo import gdal
from osgeo import gdalconst
import glob
import os

def Raster_Bild_erstellen(extent, path, prefix):
    # Get all las or laz Files in Directory
    files = glob.glob(path + "*.la*")

    for i in range(len(files)):
        files[i] = files[i].replace('\\', '/')

    # write Tiff file from importiert Pointclouds one Cloud at a time
    for i in range(len(files)):
        pdal_json = '''
        [
            "{}",

            {}
            "filename": "outpython_{}_{}.tif",
            "gdaldriver": "GTiff",
            "output_type": "min",
            "resolution": "1",
            "radius": "1.4",
            {}
            "type": "writers.gdal"
            {}
        ]
        '''
        # alters the pdal pipeline with the missing information (Filenames, Filepaths, extent and the missing {}-brackets)
        if extent == None:
            pdal_json = pdal_json.format(files[i], '{', prefix, i, '', '}')
        else:
            pdal_json = pdal_json.format(files[i], '{', prefix, i, extent, '}')

        # runs the Pipeline
        pipeline = pdal.Pipeline(pdal_json)
        count = pipeline.execute()
        arrays = pipeline.arrays
        metadata = pipeline.metadata
        log = pipeline.log

    # list all files in directory that match pattern of generetaed Tif files
    demList = glob.glob("outpython_" + prefix + "_*.tif")

    # build virtual raster and merge all tif
    vrt = gdal.BuildVRT("merged_" + prefix + ".vrt", demList)
    gdal.Translate("merged_" + prefix + ".tif", vrt, xRes=1, yRes=-1)
    vrt = None

    # delete generatet Tiff Tiles (exept the big merged one)
    for i in range(len(files)):
        os.remove("outpython_" + prefix + "_" + str(i) + ".tif")

    # output extets
    data = gdal.Open('merged_' + prefix + '.tif', gdalconst.GA_ReadOnly)
    geoTransform = data.GetGeoTransform()
    minx = geoTransform[0]
    maxy = geoTransform[3]
    maxx = minx + geoTransform[1] * data.RasterXSize
    miny = maxy + geoTransform[5] * data.RasterYSize

    # Exent for the next File, so that the Pixels and the extent alligns
    extent = '"bounds": "([' + str(minx) + ', ' + str(maxx) + '],[' + str(miny) + ', ' + str(maxy) + '])",'
    # releaf memory
    data = None

    return extent


extent = None

# path a und path b sowie praefixe aus Gui uebernehmen

path_a = "C:/Users/joelb/lidardaten/testeroni/"
prefix_a = "2014"

extent = Raster_Bild_erstellen(extent, path_a, prefix_a)

path_b = "C:/Users/joelb/lidardaten/testeroni2/"
prefix_b = "2019"

Raster_Bild_erstellen(extent, path_b, prefix_b)

extent = None
