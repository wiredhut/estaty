import warnings
import osmnx as ox
import networkx as nx
import numpy as np

import matplotlib.pyplot as plt

from estaty.data.data import VectorData
from estaty.engine.vector.points_representation.to_point import \
    VectorToPointsRepresentation
from estaty.stages import Stage, SPATIAL_DATA_LIST

warnings.filterwarnings('ignore')


class DistanceAnalysisStage(Stage):
    """
    Class to perform accessibility analysis by using distance metrics to
    objects.

    Useful links:
    https://geoffboeing.com/2016/11/osmnx-python-street-networks/
    """

    def __init__(self, **params):
        super().__init__(**params)
        self.object_for_analysis = params['object_for_analysis']
        self.radius = self.object_for_analysis['radius']

        # Information about the transport network
        # "all_private", "all", "bike", "drive", "drive_service", "walk"
        self.network_type = params['network_type']

    def apply(self, input_data: SPATIAL_DATA_LIST) -> VectorData:
        """
        Launch analysis with distance metrics calculation
        Analysis steps:
            * Get street network graph from OSM
            * Convert all objects in vector data into points (not centroids!)
            * For each point in vector data search for nearest street path
            * Calculate distances of that paths
            * Store into new vector data paths and their lengths as attributes
        """
        input_data = self.take_first_element_from_list(input_data)
        # Get MultiDiGraph (networkx object) neat POI
        point = (self.object_for_analysis['lat'], self.object_for_analysis['lon'])
        streets_graph = ox.graph_from_point(point, dist=self.radius,
                                            network_type=self.network_type)
        streets_graph = ox.add_edge_speeds(streets_graph)
        streets_graph = ox.add_edge_travel_times(streets_graph)

        # Find nodes to search for paths between them
        # NB: We assume that node not so far from target point location
        origin_node = ox.nearest_nodes(streets_graph,
                                       self.object_for_analysis['lon'],
                                       self.object_for_analysis['lat'])

        # Replace all polygons and lines with points objects
        points_converter = VectorToPointsRepresentation(**{'reduce': 'nearest'})
        input_data = points_converter.to_points(input_data, self.object_for_analysis,
                                                network_graph=streets_graph)

        paths = []
        for row_id, row in input_data.points.iterrows():
            # For each object perform analysis
            geometry = row['geometry']

            # TODO get x and y from geometry
            lat_coord, lon_coord = 0, 0
            finish_node = ox.nearest_nodes(streets_graph, lon_coord, lat_coord)

            # TODO Calculate residual distance from finish node to actual finish
            #  location
            residual_distance = 0

            route = nx.shortest_path(streets_graph, origin_node,
                                     finish_node, weight='length')
            fig, ax = ox.plot_graph_route(streets_graph, route, route_linewidth=6,
                                          node_size=0, bgcolor='k')
            plt.show()

            # Calculate
            path_length = nx.shortest_path_length(streets_graph, origin_node,
                                                  finish_node, weight='length')
            paths.append([path_length + residual_distance, route])

        # Generate new vector data with lengths attributes
        input_data = 0
        return None
