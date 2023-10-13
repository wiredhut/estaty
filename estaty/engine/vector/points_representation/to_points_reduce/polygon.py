from typing import Union, Any

import geopandas
import pandas as pd
import numpy as np

from geopandas import GeoDataFrame

from estaty.engine.vector.point.distance import DistanceToPointsCalculator
from estaty.engine.vector.points_representation.to_points_reduce.common import \
    ReducerToPoint


class PolygonToPointReducer(ReducerToPoint):

    def __init__(self, epsg: int, **params):
        super().__init__(epsg, **params)

    def reduce_to_point(self, row: pd.Series, additional_info: Union[Any, None]) -> GeoDataFrame:
        """ Method allows reducing geometry to a single point

        additional_info in this method is geo dataframe with nodes
        """
        polygon = row.geometry
        xx, yy = polygon.exterior.coords.xy

        # Configure table with points
        polygons_points = pd.DataFrame({'polygon_x': xx.tolist(),
                                        'polygon_y': yy.tolist()})
        polygons_points['index'] = np.arange(0, len(polygons_points))

        # Create table with pairwise
        common_table = []
        for i, polygon_point in polygons_points.iterrows():
            additional_info = additional_info.copy()
            additional_info['polygon_x'] = [polygon_point.polygon_x] * len(additional_info)
            additional_info['polygon_y'] = [polygon_point.polygon_y] * len(additional_info)
            common_table.append(additional_info)

        common_table = pd.concat(common_table)
        distance_calculator = DistanceToPointsCalculator(common_table)
        dist_column = 'distance_from_node_to_point'
        common_table = distance_calculator.calculate_euclidean_by_columns(['x', 'y'],
                                                                          ['polygon_x', 'polygon_y'],
                                                                          dist_column)
        common_table['common_distance'] = common_table['distance_from_node_to_point'] + common_table['distance_from_target_to_nodes']
        common_table = common_table.reset_index()
        # Find suitable point for path search problem
        nearest_point = common_table['common_distance'].argmin()
        point_representation = common_table.iloc[nearest_point]
        point_representation = pd.DataFrame(point_representation).T[['polygon_x', 'polygon_y', 'distance_from_node_to_point']]

        geometry = geopandas.points_from_xy(point_representation.polygon_x,
                                            point_representation.polygon_y)
        gdf = GeoDataFrame(point_representation, crs=f"EPSG:{self.epsg}", geometry=geometry)
        gdf = gdf.rename(columns={'polygon_x': 'x', 'polygon_y': 'y',
                                  'distance_from_node_to_point': 'residual_distance'})

        return gdf
