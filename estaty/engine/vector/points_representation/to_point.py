from typing import Optional

import pandas as pd
from geopandas import GeoDataFrame

from estaty.data.data import VectorData
from estaty.engine.vector.points_representation.to_points_reduce.common import \
    ReducerToPoint


class VectorToPointsRepresentation:
    """
    Base class for processing geopandas dataframes and transform each geometry
    type (point, line, polygon or multipolygon) into points. So polygon can be
    represented as single point. The same processing trick is capable for line
    also

    Responsibility zone: process dataframes with all possible geometries and
    convert each row into point geometry
    """

    reducer_by_type = {'LineString': None,
                       'Polygon': None,
                       'MultiPolygon': None}

    def __init__(self, **params):
        self.params = params

    def to_points(self, vector_data: VectorData,
                  target_point_info: Optional[dict] = None) -> VectorData:
        """
        Transform each geometry into point in dataframe. So sequentially process
        each row in GeoPandas DataFrame

        :param vector_data: dataclass with vector data in it
        :param target_point_info: dictionary with information about first point
        """
        if vector_data.lines is not None:
            pass

    @staticmethod
    def use_reducer(reducer: ReducerToPoint, vector_data: VectorData,
                    target_point_info: Optional[dict] = None):
        updated_rows = []
        for row_id, row in vector_data.points.iterrows():
            updated_row = reducer.reduce_to_point(row, target_point_info)
            updated_rows.append(updated_row)

        updated_rows = pd.concat(updated_rows)
        return updated_rows
