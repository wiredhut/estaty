from abc import abstractmethod
from typing import Union

from estaty.data.data import CommonData


class Stage:
    """ Class for performing particular stage in actions """

    def __init__(self, **params):
        self.params = params

    @abstractmethod
    def apply(self, input_data: Union[CommonData, None]) -> CommonData:
        """
        Apply processing stage on desired data.

        :param input_data: input data to apply processing logic on it. May be
        None
        """
        raise NotImplementedError()
