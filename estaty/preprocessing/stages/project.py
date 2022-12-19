import warnings
from typing import Union

from loguru import logger

from estaty.data.data import CommonData
from estaty.stages import Stage, SPATIAL_DATA_LIST

warnings.filterwarnings('ignore')


class VectorProjectionStage(Stage):
    """
    Class to perform projection operations on vector data
    """

    def __init__(self, **params):
        super().__init__(**params)
        self.to_epsg = int(params['to'])

    def apply(self, input_data: SPATIAL_DATA_LIST) -> Union[CommonData, SPATIAL_DATA_LIST]:
        """ Transform vector data into desired projection """
        for data in input_data:
            data.to_crs(self.to_epsg)

        logger.debug(f'Re-projection to {self.to_epsg} performed successfully')
        return input_data
