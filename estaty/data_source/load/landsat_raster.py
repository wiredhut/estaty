from pathlib import Path
from typing import Union

import geopandas
import pandas as pd
import numpy as np


import rasterio
from shapely.geometry import Polygon

from estaty.constants import WGS_EPSG
from estaty.data.data import CommonData, RasterData
from estaty.engine.vector.convert import create_polygon_from_point, \
    transform_coordinates_in_dataframe
from estaty.paths import get_local_files_storage_path
from estaty.stages import Stage

import warnings
warnings.filterwarnings('ignore')


class NDVILandsatLocallyStage(Stage):
    """
    Load Landsat data which already was prepared and stored in folder locally.
    NDVI field is pre-calculated
    """

    def __init__(self, **params):
        super().__init__(**params)
        self.object_for_analysis = params['object_for_analysis']
        path_to_files = Path(get_local_files_storage_path(), 'landsat', 'ndvi')

        # Configure polygon for area of interest
        self.polygon = create_polygon_from_point(self.object_for_analysis,
                                                 buffer=self.object_for_analysis['radius'])

        # Get path to file with species data
        self.path_to_file = None
        self.get_file_name_by_extend(path_to_files)

    def apply(self, input_data: Union[CommonData, None]) -> RasterData:
        """ Load data from local file """
        with rasterio.open(self.path_to_file) as src:
            raster_crs = src.crs
            raster_epsg = str(raster_crs).split(':')[-1]

        # Create raster dataset for further usage
        return RasterData(raster=self.path_to_file, epsg=int(raster_epsg),
                          area_of_interest=self.polygon)

    def get_file_name_by_extend(self, path_to_files: Path):
        """ Load appropriate file based on buffer coordinates """
        # TODO temporary solution - integrate with DB and indexing
        raster_to_use = None
        for file in path_to_files.iterdir():
            with rasterio.open(file) as src:
                raster_crs = src.crs
                raster_epsg = str(raster_crs).split(':')[-1]

                # Get extend of raster
                bbox = pd.DataFrame({'lon': [src.bounds.left, src.bounds.left, src.bounds.right, src.bounds.right],
                                     'lat': [src.bounds.bottom, src.bounds.top, src.bounds.bottom, src.bounds.top]})

                bbox = transform_coordinates_in_dataframe(bbox, raster_epsg, WGS_EPSG)
                # Create polygon based on bbox coordinates
                raster_extend = Polygon(np.array(bbox[['lon', 'lat']])).convex_hull

                if raster_extend.contains(self.polygon):
                    # Appropriate file because area of interest lies in raster extend
                    raster_to_use = file
                    break

        if raster_to_use is None:
            raise ValueError(f'Cannot find appropriate raster file for analysis')
        self.path_to_file = raster_to_use
