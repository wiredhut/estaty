import warnings

from loguru import logger

from estaty.data.data import CommonData
from estaty.stages import Stage

warnings.filterwarnings('ignore')


class VectorProjectionStage(Stage):
    """
    Class to perform projection operations on vector data
    """

    def __init__(self, **params):
        super().__init__(**params)
        self.to_epsg = int(params['to'])

    def apply(self, input_data: CommonData) -> CommonData:
        """ Transform vector data into desired projection """
        input_data.to_crs(self.to_epsg)
        logger.debug(f'Re-projection to {self.to_epsg} performed successfully')
        return input_data
