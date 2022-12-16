import warnings
import osmnx as ox
import networkx as nx

import matplotlib.pyplot as plt

from loguru import logger

from estaty.data.data import VectorData
from estaty.engine.vector.points_representation.nearest import \
    get_nearest_nodes_from_layer
from estaty.stages import Stage

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

    def apply(self, input_data: VectorData) -> VectorData:
        """ Launch analysis with distance metrics """
        # Get MultiDiGraph (networkx object) neat POI
        point = (self.object_for_analysis['lat'], self.object_for_analysis['lon'])
        streets_graph = ox.graph_from_point(point, dist=self.radius,
                                            network_type=self.network_type)
        streets_graph = ox.add_edge_speeds(streets_graph)
        streets_graph = ox.add_edge_travel_times(streets_graph)

        # Find nodes to search for paths between them
        origin_node = ox.nearest_nodes(streets_graph,
                                       self.object_for_analysis['lon'],
                                       self.object_for_analysis['lat'])
        df_for_analysis = get_nearest_nodes_from_layer(input_data,
                                                       self.object_for_analysis)

        route = nx.shortest_path(streets_graph, origin_node, 2603295463,
                                 weight='length')
        len = nx.shortest_path_length(streets_graph, origin_node, 2603295463,
                                      weight='length')
        print(len)
        fig, ax = ox.plot_graph_route(streets_graph, route,
                                      route_linewidth=6,
                                      node_size=0,
                                      bgcolor='k')
        plt.show()
        logger.debug(f'Distance analysis was performed successfully')
        return input_data
