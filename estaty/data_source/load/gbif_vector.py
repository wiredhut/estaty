from pathlib import Path
from typing import Union

import pandas as pd

import warnings

from estaty.data.data import CommonData, VectorData
from estaty.data_source.load.osm_vector_utils import \
    convert_osm_bbox_coordinates
from estaty.data_source.load.repository.locations import WGS_LOCATION_BOUNDS
from estaty.engine.vector.crop import crop_points_by_polygon
from estaty.engine.vector.vector import prepare_points_layer
from estaty.paths import get_local_files_storage_path
from estaty.stages import Stage

warnings.filterwarnings('ignore')


class LoadGBIFLocallyStage(Stage):
    """ Load GBIF data which already was prepared and stored in csv locally """

    def __init__(self, **params):
        super().__init__(**params)
        self.location = params['location']
        self.path_to_file = Path(get_local_files_storage_path(), 'gbif_ambrosia.csv')

    def apply(self, input_data: Union[CommonData, None]) -> CommonData:
        """ Load data from local file """
        dataframe = pd.read_csv(self.path_to_file, sep='\t')
        dataframe = prepare_points_layer(dataframe,
                                         lon='decimalLongitude',
                                         lat='decimalLatitude')
        # Coordinates must be in WGS
        dataframe = dataframe.to_crs(4326)

        # Crop geo dataframe by location polygon
        polygon = convert_osm_bbox_coordinates(WGS_LOCATION_BOUNDS[self.location])
        cropped_data = crop_points_by_polygon(dataframe, polygon)
        return VectorData(polygons=cropped_data)
