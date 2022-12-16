from pathlib import Path
from typing import Union

import pandas as pd

from estaty.data.data import CommonData, VectorData
from estaty.engine.vector.crop import crop_points_by_polygon
from estaty.engine.vector.convert import prepare_points_layer, \
    create_polygon_from_point
from estaty.paths import get_local_files_storage_path
from estaty.stages import Stage

import warnings
warnings.filterwarnings('ignore')


class LoadGBIFLocallyStage(Stage):
    """ Load GBIF data which already was prepared and stored in csv locally """

    def __init__(self, **params):
        super().__init__(**params)
        self.object_for_analysis = params['object_for_analysis']
        # TODO improve to allow several species processing
        self.plant = params['species'][0]
        path_to_files = Path(get_local_files_storage_path(), 'gbif')

        # Get path to file with species data
        self.path_to_file = None
        for file in path_to_files.iterdir():
            if self.plant in file.name:
                self.path_to_file = file
                break

    def apply(self, input_data: Union[CommonData, None]) -> CommonData:
        """ Load data from local file """
        dataframe = pd.read_csv(self.path_to_file, sep='\t')
        dataframe = prepare_points_layer(dataframe,
                                         lon='decimalLongitude',
                                         lat='decimalLatitude')
        # Coordinates must be in WGS
        dataframe = dataframe.to_crs(4326)

        # Crop geo dataframe by location polygon
        polygon = create_polygon_from_point(self.object_for_analysis,
                                            buffer=self.object_for_analysis['radius'])
        cropped_data = crop_points_by_polygon(dataframe, polygon)
        return VectorData(points=cropped_data)
