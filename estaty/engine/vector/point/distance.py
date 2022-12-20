from typing import Union

import pandas as pd
from geopandas import GeoDataFrame


class DistanceToPointsCalculator:
    """
    Class for calculating distances to points into the dataframe.
    Allows to calculate metrics in n-dimensional space
    """

    def __init__(self, table: Union[pd.DataFrame, GeoDataFrame]):
        self.table = table

    def calculate_euclidean_by_columns(self,
                                       coordinates_columns_first: list,
                                       coordinate_columns_second: list,
                                       name_for_distance_column: str = 'distance'):
        """
        Calculate Euclidean distances in dataframe with coordinates

        :param coordinates_columns_first: list with names of coordinates columns
        for points batch number 1
        :param coordinate_columns_second: list with names of coordinates columns
        for points batch number 2
        :param name_for_distance_column: name of new column
        """
        if len(coordinates_columns_first) != len(coordinate_columns_second):
            raise ValueError('Coordinates lists must match')

        self.table[name_for_distance_column] = [0] * len(self.table)
        for coord_id in range(len(coordinates_columns_first)):
            first_coord = coordinates_columns_first[coord_id]
            second_coord = coordinate_columns_second[coord_id]

            coordinate_diff = self.table[first_coord] - self.table[second_coord]
            coordinate_diff = coordinate_diff ** 2

            self.table[name_for_distance_column] = self.table[name_for_distance_column] + coordinate_diff

        self.table[name_for_distance_column] = self.table[name_for_distance_column] ** 0.5
        return self.table
