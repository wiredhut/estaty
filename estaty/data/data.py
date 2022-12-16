from abc import abstractmethod
from dataclasses import dataclass
from typing import Optional, Union
from geopandas import geodataframe
import pandas as pd


@dataclass
class CommonData:
    """ Common dataclass to store information """
    # Optional path to the file with desired data
    path_to_file: Optional[str] = None

    # Current EPSG code
    epsg: int = None

    @abstractmethod
    def to_crs(self, epsg_code: int):
        raise NotImplementedError()


@dataclass
class VectorData(CommonData):
    """ Hold vector data. Support three main types: point, lines, polygons """
    points: Optional[geodataframe.DataFrame] = None
    lines: Optional[geodataframe.DataFrame] = None
    polygons: Optional[geodataframe.DataFrame] = None

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
    raster: Optional[dict] = None

    def to_crs(self, epsg_code: int):
        raise NotImplementedError('Raster re-projection does not supported yet')
