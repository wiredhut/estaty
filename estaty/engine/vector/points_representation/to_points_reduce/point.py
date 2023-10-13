from typing import Union, Any

import geopandas
import pandas as pd
import numpy as np

from geopandas import GeoDataFrame

from estaty.engine.vector.point.distance import DistanceToPointsCalculator
from estaty.engine.vector.points_representation.to_points_reduce.common import ReducerToPoint


class PointToPointReducer(ReducerToPoint):

    def __init__(self, epsg: int, **params):
        super().__init__(epsg, **params)

    def reduce_to_point(self, row: pd.Series, additional_info: Union[Any, None]) -> GeoDataFrame:
        """ Method allows reducing geometry to a single point """
        point = row.geometry
        x_coord, y_coord = point.x, point.y

        # Put point coordinates and calculate the distance
        additional_info['point_x'] = x_coord
        additional_info['point_y'] = y_coord
        distance_calculator = DistanceToPointsCalculator(additional_info)
        dist_column = 'distance_from_node_to_point'
        df = distance_calculator.calculate_euclidean_by_columns(['x', 'y'],['point_x', 'point_y'], dist_column)
        df['common_distance'] = df['distance_from_node_to_point'] + df['distance_from_target_to_nodes']
        df = df.reset_index()
        nearest_point = df['common_distance'].argmin()
        point_representation = df.iloc[nearest_point]
        point_representation = pd.DataFrame(point_representation).T[['point_x', 'point_y', 'distance_from_node_to_point']]

        geometry = geopandas.points_from_xy(point_representation.point_x, point_representation.point_y)
        gdf = GeoDataFrame(point_representation, crs=f"EPSG:{self.epsg}", geometry=geometry)
        gdf = gdf.rename(columns={'point_x': 'x', 'point_y': 'y', 'distance_from_node_to_point': 'residual_distance'})
        return gdf
