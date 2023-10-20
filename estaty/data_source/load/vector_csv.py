from pathlib import Path
from typing import Union

import pandas as pd

from estaty.data.data import CommonData, VectorData
from estaty.engine.vector.crop import crop_points_by_polygon
from estaty.engine.vector.convert import prepare_points_layer, \
    create_polygon_from_point
from estaty.stages import Stage

import warnings
warnings.filterwarnings('ignore')


class LoadCsvVectorStage(Stage):
    """ Load data and stored in csv locally """

    def __init__(self, **params):
        super().__init__(**params)
        self.object_for_analysis = params['object_for_analysis']
        self.path = Path(params['path']).resolve()
        self.lat = params['lat']
        self.lon = params['lon']

        # Optional parameters
        self.crs = params.get('crs')
        self.separator = params.get('sep')

    def apply(self, input_data: Union[CommonData, None]) -> VectorData:
        """ Load data from local file """
        if self.separator is None:
            dataframe = pd.read_csv(self.path, sep='\t')
        else:
            dataframe = pd.read_csv(self.path, sep=self.separator)

        dataframe = prepare_points_layer(dataframe, lon=self.lon, lat=self.lat)
        # Coordinates must be in WGS
        dataframe = dataframe.to_crs(self.crs)

        # Crop geo dataframe by location polygon
        polygon = create_polygon_from_point(self.object_for_analysis,
                                            buffer=self.object_for_analysis['radius'])
        cropped_data = crop_points_by_polygon(dataframe, polygon)
        return VectorData(points=cropped_data)
