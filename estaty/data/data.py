from abc import abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union
import numpy as np
import rasterio
from rasterio import Affine
from rasterio.warp import reproject, Resampling, calculate_default_transform

import geopandas
from geopandas import GeoDataFrame
import pandas as pd
from shapely.geometry import Polygon

from estaty.constants import WGS_EPSG


@dataclass
class CommonData:
    """ Common dataclass to store information """
    # Optional path to the file with desired data
    path_to_file: Optional[str] = None
    description: Optional[str] = None
    # Shapely Polygon always with WGS84 coordinates
    area_of_interest: Optional[Polygon] = None

    # Current EPSG code
    epsg: int = None

    @abstractmethod
    def to_crs(self, epsg_code: int):
        raise NotImplementedError()

    @property
    def area_of_interest_as_dataframe(self):
        """ Return polygon in a form of Geo dataframe """
        area = geopandas.GeoDataFrame(index=[0], crs=f'epsg:{WGS_EPSG}',
                                      geometry=[self.area_of_interest])
        # Assign the same projection
        area = area.to_crs(self.epsg)
        return area


@dataclass
class VectorData(CommonData):
    """ Hold vector data. Support three main types: point, lines, polygons """
    points: Optional[GeoDataFrame] = None
    lines: Optional[GeoDataFrame] = None
    polygons: Optional[GeoDataFrame] = None

    def to_crs(self, epsg: Union[str, int]):
        """ Assign new CRS to all vector layers in the dataset """
        epsg = int(epsg)
        self.epsg = epsg
        if self.points is not None:
            self.points = self.points.to_crs(epsg=epsg)
        if self.lines is not None:
            self.lines = self.lines.to_crs(epsg=epsg)
        if self.polygons is not None:
            self.polygons = self.polygons.to_crs(epsg=epsg)

    @property
    def all(self):
        """ Return all dataframes in single structure """
        return pd.concat([self.points, self.lines, self.polygons])


@dataclass
class RasterData(CommonData):
    """ Hold raster datasets """
    # Raster in most cases represent as path to file due to it can be too
    # computationally expensive to keep raster in memory all the time
    raster: Optional[Union[Path, np.ndarray]] = None

    def to_crs(self, epsg_code: int):
        """ Load raster from file and create new file in temporary folder """
        if epsg_code == self.epsg:
            return None

        # Perform re-projection for raster
        dst_crs = f'EPSG:{epsg_code}'
        current_name = self.raster.name
        base_name = str(current_name).split('.')[0]
        new_path = Path(self.raster.parent, f'{base_name}_reprojected.tif')
        with rasterio.open(self.raster) as src:
            transform, width, height = calculate_default_transform(src.crs, dst_crs, src.width,
                                                                   src.height, *src.bounds)
            kwargs = src.meta.copy()
            kwargs.update({'crs': dst_crs, 'transform': transform,
                           'width': width, 'height': height})

            with rasterio.open(new_path, 'w', **kwargs) as dst:
                for i in range(1, src.count + 1):
                    reproject(source=rasterio.band(src, i),
                              destination=rasterio.band(dst, i),
                              src_transform=src.transform,
                              src_crs=src.crs,
                              dst_transform=transform,
                              dst_crs=dst_crs,
                              resampling=Resampling.nearest)

        # Assign new file
        self.raster = new_path
        self.epsg = epsg_code
