from abc import abstractmethod
from typing import Union, List

from estaty.data.data import CommonData

INPUT_LIST = List[CommonData]


class Stage:
    """ Class for performing particular stage in actions """

    def __init__(self, **params):
        self.params = params

    @abstractmethod
    def apply(self, input_data: INPUT_LIST) -> Union[CommonData, INPUT_LIST]:
        """
        Apply processing stage on desired data.

        :param input_data: input data to apply processing logic on it.
        Pass as list with input data classes
        """
        raise NotImplementedError()


class DummyStage(Stage):
    """
    Class to pass data directly without any transformations
    """

    def __init__(self, **params):
        super().__init__(**params)

    def apply(self, input_data: INPUT_LIST) -> Union[CommonData, INPUT_LIST]:
        """ Pass data further 'as is' """
        return input_data
