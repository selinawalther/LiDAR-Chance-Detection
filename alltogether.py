from typing import List, Any, Union

import pdal
from osgeo import gdal
from osgeo import gdalconst
import glob
from PyQt5.uic import *
from PyQt5.QtWidgets import *


# define GUI functions
class ChangeDetection(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('gui_v2.ui', self)

        self.input = self.findChild(QLineEdit, 'pfad_a')
        print(self.input.text())

        self.button = self.findChild(QPushButton, 'berechnen')  # Find the button
        self.button.clicked.connect(print("gugus")) #self.calculate

        self.show()


    def get_files(self):
        global path_a
        global path_b
        path_a = QInputDialog.getText(self, "pfad_a", "Pfad zu Dateien")
        path_b = QInputDialog.getText(self, "pfad_b", "Pfad zu Dateien")
        print(path_a)


    def cooridnates(self):
        global minx
        global miny
        global maxx
        global maxy
        global extent
        minx = QInputDialog.getInt(self, "x_coord_min", "Minimale X-Koordinate", deicmals=3)
        miny = QInputDialog.getInt(self, "y_coord_min", "Minimale X-Koordinate", deicmals=3)
        maxx = QInputDialog.getInt(self, "x_coord_max", "Minimale X-Koordinate", deicmals=3)
        maxy = QInputDialog.getInt(self, "y_coord_max", "Minimale X-Koordinate", deicmals=3)
        extent = (minx, miny, maxx, maxy)

    def year(self):
        global prefix_a
        global prefix_b
        prefix_a = year_a.currentText()
        prefix_b = year_b.currentText()

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

    def calculate(self):
        path_a = self.pfad_a.text()
        print(path_a)
        path_b = self.pfad_b.text()
        prefix_a = self.year_a.text()
        prefix_b = self.year_b.text()
        extent = None
        extent = Raster_Bild_erstellen(extent, path_a, prefix_a)
        Raster_Bild_erstellen(extent, path_b, prefix_b)
        extent = None

app = QApplication([])
window = ChangeDetection()
app.exec()