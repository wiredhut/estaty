from pathlib import Path
from typing import Union

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

import rasterio
from rasterio.mask import mask

from shapely.geometry import mapping

from estaty.data.data import CommonData, RasterData
from estaty.engine.vector.convert import create_polygon_from_point
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

        # Get path to file with species data
        self.path_to_file = None
        self.get_file_name_by_extend(path_to_files)

    def apply(self, input_data: Union[CommonData, None]) -> RasterData:
        """ Load data from local file """
        with rasterio.open(self.path_to_file) as src:
            raster_crs = src.crs
            raster_epsg = str(raster_crs).split(':')[-1]

        # Create raster dataset for further usage
        return RasterData(raster=self.path_to_file, epsg=int(raster_epsg))

    def get_file_name_by_extend(self, path_to_files: Path):
        self.path_to_file = Path(path_to_files, 'spb_ndvi.tif')
