from dataclasses import dataclass
from typing import Optional
from geopandas import geodataframe


@dataclass
class CommonData:
    """ Common dataclass to store information """
    # Optional path to the file with desired data
    path_to_file: Optional[str] = None


@dataclass
class VectorData(CommonData):
    """ Hold vector data. Support three main types: point, lines, polygons """
    points: Optional[geodataframe.DataFrame] = None
    lines: Optional[geodataframe.DataFrame] = None
    polygons: Optional[geodataframe.DataFrame] = None


@dataclass
class RasterData(CommonData):
    """ Hold raster datasets """
    raster: Optional[dict] = None
