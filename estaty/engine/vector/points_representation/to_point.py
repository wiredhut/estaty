from typing import Optional
import networkx as nx
import osmnx as ox

import pandas as pd
from geopandas import GeoDataFrame
from pyproj import Transformer
from shapely.geometry import MultiPolygon

from estaty.data.data import VectorData
from estaty.engine.vector.convert import transform_coordinates_in_dataframe
from estaty.engine.vector.point.distance import DistanceToPointsCalculator
from estaty.engine.vector.points_representation.to_points_reduce.common import \
    ReducerToPoint
from estaty.engine.vector.points_representation.to_points_reduce.polygon import \
    PolygonToPointReducer


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
                       'Polygon': PolygonToPointReducer}

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
        # Add information about target point coordinates
        transformer = Transformer.from_crs("EPSG:4326", f"EPSG:{metric_epsg}",
                                           always_xy=True)
        new_long, new_lat = transformer.transform(*[target_point_info['lon'], target_point_info['lat']])

        gdf_nodes['x_target'] = [new_long] * len(gdf_nodes)
        gdf_nodes['y_target'] = [new_lat] * len(gdf_nodes)

        # Calculate first component - distance between
        distance_calculator = DistanceToPointsCalculator(gdf_nodes)
        dist_column = 'distance_from_target_to_nodes'
        gdf_nodes = distance_calculator.calculate_euclidean_by_columns(['x', 'y'],
                                                                       ['x_target', 'y_target'],
                                                                       dist_column)

        # Apply transformation on polygons
        if vector_data.polygons is not None:
            updated_rows = self.use_reducer(self.reducer_by_type['Polygon'](metric_epsg),
                                            vector_data.polygons, gdf_nodes)
            vector_data.polygons = updated_rows

        if vector_data.lines is not None:
            updated_rows = self.use_reducer(self.reducer_by_type['LineString'](metric_epsg),
                                            vector_data.lines, gdf_nodes)
            vector_data.polygons = updated_rows

        return vector_data

    @staticmethod
    def use_reducer(reducer: ReducerToPoint,
                    vector_dataframe: GeoDataFrame,
                    nodes_information: Optional[GeoDataFrame] = None):
        updated_rows = []
        for row_id, row in vector_dataframe.iterrows():
            if isinstance(row.geometry, MultiPolygon):
                print('Pass multipolygon')
                continue
            updated_row = reducer.reduce_to_point(row, nodes_information)
            updated_rows.append(updated_row)

        updated_rows = pd.concat(updated_rows)
        return updated_rows
