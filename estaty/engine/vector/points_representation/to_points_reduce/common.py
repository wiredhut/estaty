from abc import abstractmethod
from typing import Union, Any

from geopandas import GeoDataFrame


class ReducerToPoint:
    """
    Base class for processing single geometry and transform it into a point
    """

    def __init__(self, epsg: int, **params):
        self.epsg = epsg
        self.params = params

    @abstractmethod
    def reduce_to_point(self, row, additional_info: Union[Any, None]) -> GeoDataFrame:
        """ Method allows reducing geometry to a single point """
        raise NotImplementedError()
