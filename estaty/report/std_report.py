from typing import Union

from estaty.data.data import VectorData
from estaty.stages import Stage


class StdReportStage(Stage):
    """ Show calculated dataframe to the terminal """

    def __init__(self, **params):
        super().__init__(**params)
        self.object_for_analysis = params['object_for_analysis']

    def apply(self, input_data: Union[VectorData, None]):
        input_data = input_data[0]
        print(f'EPSG code: {input_data.epsg}')
        print(input_data.all)
