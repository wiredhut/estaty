import warnings
import osmnx as ox
import networkx as nx
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from estaty.data.data import VectorData, CommonData
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

        self.visualize = False
        if self.params.get('visualize') is not None:
            self.visualize = self.params.get('visualize')

        # Information about the transport network
        # "all_private", "all", "bike", "drive", "drive_service", "walk"
        self.network_type = params['network_type']

    def apply(self, input_data: SPATIAL_DATA_LIST) -> CommonData:
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

        input_data.to_crs(4326)

        paths = []
        for row_id, row in input_data.all.iterrows():
            # For each object perform analysis - calculate path
            finish_node = ox.nearest_nodes(streets_graph, row.geometry.x, row.geometry.y)

            # Distance from node to desired point
            residual_distance = row['residual_distance']
            route = nx.shortest_path(streets_graph, origin_node,
                                     finish_node, weight='length')

            # Calculate path length
            path_length = nx.shortest_path_length(streets_graph, origin_node,
                                                  finish_node, weight='length')
            if self.visualize is not False:
                print(f'Path length: {path_length}')
                print(f'Residual metres: {residual_distance}')
                fig, ax = ox.plot_graph_route(streets_graph, route,
                                              route_linewidth=6,
                                              node_size=0, bgcolor='k')
                plt.show()

            # Generate geo dataframe with line object

            paths.append([path_length + residual_distance])
        paths = np.array(paths)

        print(f'Mean path length: {np.mean(paths)}')
        print(f'Min path length: {np.min(paths)}')
        exit()
        # Generate new vector data with lines objects (founded paths)
        input_data = VectorData(lines=pd.concat(paths), epsg=4326)
        return input_data
