from abc import abstractmethod
from typing import Union, List

from estaty.data.data import CommonData, RasterData, VectorData

SPATIAL_DATA_LIST = List[Union[RasterData, VectorData]]


class Stage:
    """ Class for performing particular stage in actions """

    def __init__(self, **params):
        self.params = params

    @abstractmethod
    def apply(self, input_data: SPATIAL_DATA_LIST) -> Union[CommonData, SPATIAL_DATA_LIST]:
        """
        Apply processing stage on desired data.

        :param input_data: input data to apply processing logic on it.
        Pass as list with input data classes
        """
        raise NotImplementedError()

    @staticmethod
    def take_first_element_from_list(input_data: SPATIAL_DATA_LIST):
        """ Take first element in the list """
        if isinstance(input_data, list):
            if len(input_data) > 1:
                raise ValueError('There is no option to take first element from list with several objects!')
            return input_data[0]

        return input_data


class DummyStage(Stage):
    """
    Class to pass data directly without any transformations
    """

    def __init__(self, **params):
        super().__init__(**params)

    def apply(self, input_data: SPATIAL_DATA_LIST) -> Union[CommonData, SPATIAL_DATA_LIST]:
        """ Pass data further 'as is' """
        return input_data
