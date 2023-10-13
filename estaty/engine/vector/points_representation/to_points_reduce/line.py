from typing import Union, Any

import geopandas
import pandas as pd
import numpy as np

from geopandas import GeoDataFrame

from estaty.engine.vector.point.distance import DistanceToPointsCalculator
from estaty.engine.vector.points_representation.to_points_reduce.common import ReducerToPoint


class LineToPointReducer(ReducerToPoint):

    def __init__(self, epsg: int, **params):
        super().__init__(epsg, **params)

    def reduce_to_point(self, row: pd.Series, additional_info: Union[Any, None]) -> GeoDataFrame:
        line = row.geometry
        x_coordinates, y_coordinates = line.xy

        # TODO set range between points
        line_points = pd.DataFrame({'line_x': x_coordinates.tolist(),
                                    'line_y': y_coordinates.tolist()})
        line_points['index'] = np.arange(0, len(line_points))

        # Put point coordinates and calculate the distance
        # Create table with pairwise
        common_table = []
        for i, line_point in line_points.iterrows():
            additional_info = additional_info.copy()
            additional_info['line_x'] = [line_point.line_x] * len(additional_info)
            additional_info['line_y'] = [line_point.line_y] * len(additional_info)
            common_table.append(additional_info)

        common_table = pd.concat(common_table)
        distance_calculator = DistanceToPointsCalculator(common_table)
        dist_column = 'distance_from_node_to_point'
        df = distance_calculator.calculate_euclidean_by_columns(['x', 'y'],
                                                                ['line_x', 'line_y'],
                                                                dist_column)

        df['common_distance'] = df['distance_from_node_to_point'] + df['distance_from_target_to_nodes']
        df = df.reset_index()
        nearest_point = df['common_distance'].argmin()
        line_representation = df.iloc[nearest_point]
        line_representation = pd.DataFrame(line_representation).T[['line_x', 'line_y', 'distance_from_node_to_point']]

        geometry = geopandas.points_from_xy(line_representation.line_x, line_representation.line_y)
        gdf = GeoDataFrame(line_representation, crs=f"EPSG:{self.epsg}", geometry=geometry)
        gdf = gdf.rename(columns={'line_x': 'x', 'line_y': 'y', 'distance_from_node_to_point': 'residual_distance'})
        return gdf
