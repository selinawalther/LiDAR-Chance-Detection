import os
import pylas
import numpy as np
import open3d
import time

class DTM():

    def __init__(self, x_min, x_max, y_min, y_max, raster_size):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.raster_size = raster_size
        self.raster = np.full(self.xy_to_uv(x_max, y_max, x_min, y_min, raster_size), 999.9)

    @staticmethod
    def xy_to_uv(x, y, x_min, y_min, raster_size):
        return int((x - x_min) / raster_size), int((y - y_min) / raster_size)

    @staticmethod
    def uv_to_xy(u, v, x_min, y_min, raster_size):
        return float(u * raster_size + x_min), float(v * raster_size + y_min)

    def add_pointcloud(self, points, z_min, z_max):
        # values needed for transformation uv -> xy
        x_min = self.x_min
        y_min = self.y_min
        raster_size = self.raster_size
        raster_u, _ = self.xy_to_uv(self.x_max, self.y_max, x_min, y_min, raster_size)
        height_values = self.raster.flatten()

        # initialize open3d point cloud
        point_cloud = open3d.geometry.PointCloud()
        point_cloud.points = open3d.utility.Vector3dVector(points)
        # initialize open3d selection polygon volume => used for point selection
        bounding_volume = open3d.visualization.SelectionPolygonVolume()
        bounding_volume.orthogonal_axis = "Y"

        # iterate trough image and select the lowest point from point cloud given
        for i, height in enumerate(height_values):
            u = i % raster_u
            v = i // raster_u
            cell_x_min, cell_y_min = self.uv_to_xy(u, v, x_min, y_min, raster_size)
            cell_x_max = cell_x_min + raster_size
            cell_y_max = cell_y_min + raster_size
            bounding_polygon = np.array([
                [cell_x_min, cell_y_min, z_min],
                [cell_x_min, cell_y_max, z_min],
                [cell_x_max, cell_y_max, z_min],
                [cell_x_max, cell_y_min, z_min],
                [cell_x_min, cell_y_min, z_max],
                [cell_x_min, cell_y_max, z_max],
                [cell_x_max, cell_y_max, z_max],
                [cell_x_max, cell_y_min, z_max]]).astype("float64")
            bounding_volume.axis_max = np.max(bounding_polygon[:, 1])
            bounding_volume.axis_min = np.min(bounding_polygon[:, 1])
            bounding_volume.bounding_polygon = open3d.utility.Vector3dVector(bounding_polygon)
            cell_point_cloud = bounding_volume.crop_point_cloud(point_cloud)
            cell_points = np.asarray(cell_point_cloud.points)
            if len(cell_points) == 0:
                cell_points = np.array([[0.0, 0.0, 999.0]])
            height_values[i] = min(height, min(cell_points[:, 2]))
        
        self.raster = height_values.reshape(-1, raster_u)
        return True


# inputs
str_las_input = "C:/Users/joelb/lidardaten/2014/laz2014_609225.laz"


las = pylas.read(str_las_input)

flt_x_min = np.amin(las.x)
flt_x_max = np.amax(las.x)
flt_y_min = np.amin(las.y)
flt_y_max = np.amax(las.y)
flt_z_min = np.amin(las.z)
flt_z_max = np.amin(las.z)

flt_raster_size = 2

dtm = DTM(flt_x_min, flt_x_max, flt_y_min, flt_y_max, flt_raster_size)


points = np.vstack((las.x, las.y, las.z)).T
las = None
t_start = time.time()
dtm.add_pointcloud(points, min(points[:, 2]), max(points[:, 2]))
t_stop = time.time()
print(dtm.raster)
print('well done! - within {} s'.format(t_stop - t_start))



import numpy as np
from osgeo import gdal
from osgeo import osr

array = dtm.raster
# My image array

# For each pixel I know it's latitude and longitude.
# As you'll see below you only really need the coordinates of
# one corner, and the resolution of the file.

nrows,ncols = np.shape(array)
geotransform=(flt_x_min,flt_raster_size,0,flt_y_max,0, -flt_raster_size)

# That's (top left x, w-e pixel resolution, rotation (0 if North is up),
#         top left y, rotation (0 if North is up), n-s pixel resolution)
# I don't know why rotation is in twice???

output_raster = gdal.GetDriverByName('GTiff').Create('myraster.tif',ncols, nrows, 1 ,gdal.GDT_Float32)  # Open the file
output_raster.SetGeoTransform(geotransform)  # Specify its coordinates
srs = osr.SpatialReference()                 # Establish its coordinate encoding
srs.ImportFromEPSG(2056)                     # This one specifies LV95.

output_raster.SetProjection( srs.ExportToWkt() )   # Exports the coordinate system
                                                   # to the file
output_raster.GetRasterBand(1).WriteArray(array)   # Writes my array to the raster

output_raster.FlushCache()
