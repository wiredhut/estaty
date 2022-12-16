from abc import abstractmethod
from typing import Union

from geopandas import GeoDataFrame


class ReducerToPoint:
    """
    Base class for processing single geometry and transform it into a point
    """

    def __init__(self, **params):
        self.params = params

    @abstractmethod
    def reduce_to_point(self, row, target_point_info: Union[dict, None]) -> GeoDataFrame:
        """ Method allows reducing geometry to a single point """
        raise NotImplementedError()
