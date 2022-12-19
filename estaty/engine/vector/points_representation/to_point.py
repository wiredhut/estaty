from typing import Optional
import networkx as nx
import osmnx as ox

import pandas as pd
from geopandas import GeoDataFrame

from estaty.data.data import VectorData
from estaty.engine.vector.convert import transform_coordinates_in_dataframe
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
                  target_point_info: Optional[dict] = None,
                  network_graph: Optional[nx.MultiDiGraph] = None) -> VectorData:
        """
        Transform each geometry into point in dataframe. So sequentially process
        each row in GeoPandas DataFrame

        :param vector_data: dataclass with vector data in it
        :param target_point_info: dictionary with information about first point
        :param network_graph: graph from Open Street Map
        """
        metric_epsg = vector_data.epsg
        # Get information about nodes coordinates
        gdf_nodes, _ = ox.graph_to_gdfs(network_graph)
        gdf_nodes = gdf_nodes.to_crs(metric_epsg)
        gdf_nodes = transform_coordinates_in_dataframe(gdf_nodes, 4326, metric_epsg,
                                                       'y', 'x')
        # For each polygon object reduce to point

    @staticmethod
    def use_reducer(reducer: ReducerToPoint, vector_data: VectorData,
                    target_point_info: Optional[dict] = None):
        updated_rows = []
        for row_id, row in vector_data.points.iterrows():
            updated_row = reducer.reduce_to_point(row, target_point_info)
            updated_rows.append(updated_row)

        updated_rows = pd.concat(updated_rows)
        return updated_rows
