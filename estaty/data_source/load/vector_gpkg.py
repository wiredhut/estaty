from pathlib import Path
from typing import Union

import geopandas
import pandas as pd

from estaty.data.data import CommonData, VectorData
from estaty.engine.vector.crop import crop_points_by_polygon
from estaty.engine.vector.convert import prepare_points_layer, \
    create_polygon_from_point
from estaty.stages import Stage

import warnings
warnings.filterwarnings('ignore')


class LoadGeoPackageVectorStage(Stage):
    """ Load data and stored in gpkg locally """

    def __init__(self, **params):
        super().__init__(**params)
        self.object_for_analysis = params['object_for_analysis']
        self.path = Path(params['path']).resolve()

        # Optional parameters
        self.layer = params.get('layer')

    def apply(self, input_data: Union[CommonData, None]) -> VectorData:
        """ Load data from local file """
        if self.layer is None:
            dataframe = geopandas.read_file(self.path)
        else:
            dataframe = geopandas.read_file(self.path, layer=self.layer)

        # Crop geo dataframe by location polygon
        polygon = create_polygon_from_point(self.object_for_analysis,
                                            buffer=self.object_for_analysis['radius'])
        cropped_data = crop_points_by_polygon(dataframe, polygon)
        return VectorData(points=cropped_data)
