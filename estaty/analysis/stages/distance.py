import warnings
from copy import deepcopy

import geopandas
import osmnx as ox
import networkx as nx
import numpy as np
import pandas as pd
import contextily as cx

import matplotlib.pyplot as plt
from geopandas import GeoDataFrame
from shapely.geometry import LineString, Point

from estaty.constants import WGS_EPSG
from estaty.data.data import VectorData, CommonData
from estaty.engine.vector.convert import polygons_aggregation
from estaty.engine.vector.points_representation.to_point import \
    VectorToPointsRepresentation
from estaty.stages import Stage, SPATIAL_DATA_LIST

warnings.filterwarnings('ignore')


class DistanceAnalysisStage(Stage):
    """
    Class to perform accessibility analysis by using distance metrics to
    objects. Distance calculation is performing

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
        source_geometries = None
        input_data = self.take_first_element_from_list(input_data)
        input_data.polygons = polygons_aggregation(input_data.polygons)

        if self.visualize:
            # Get copy of source data
            source_geometries = deepcopy(input_data)

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

        input_data.to_crs(WGS_EPSG)

        paths = []
        for row_id, row in input_data.all.iterrows():
            # For each object perform analysis - calculate path
            finish_node = ox.nearest_nodes(streets_graph, row.geometry.x, row.geometry.y)

            # Distance from node to desired point
            residual_distance = row['residual_distance']
            try:
                route = nx.shortest_path(streets_graph, origin_node,
                                         finish_node, weight='length')
            except nx.NetworkXNoPath:
                # There is no networkx path between this nodes
                continue

            # Calculate path length
            path_length = nx.shortest_path_length(streets_graph, origin_node,
                                                  finish_node, weight='length')
            # Generate geo dataframe with line object
            line_object = []
            for node in route:
                node_info = streets_graph.nodes[node]
                line_object.append([node_info['x'], node_info['y']])
            # Add final destination point
            line_object.append([row.geometry.x, row.geometry.y])

            line_object = LineString(line_object)
            line_df = GeoDataFrame(pd.DataFrame({'Length': [path_length + residual_distance]}),
                                   geometry=[line_object], crs=WGS_EPSG)
            paths.append(line_df)

        # Generate new vector data with lines objects (founded paths)
        input_data = VectorData(lines=pd.concat(paths), epsg=WGS_EPSG)
        if self.visualize and source_geometries is not None:
            color = 'red'
            if self.params.get('color') is not None:
                color = self.params.get('color')

            edgecolor = None
            if self.params.get('edgecolor') is not None:
                edgecolor = self.params.get('edgecolor')

            # Prepare visualizations with founded routes
            source_geometries.to_crs(3857)
            input_data.to_crs(3857)

            # Create layer with central (target) point
            geometry = Point([self.object_for_analysis['lon'], self.object_for_analysis['lat']])
            target_point = GeoDataFrame(crs=f"EPSG:{WGS_EPSG}", geometry=[geometry])
            target_point = target_point.to_crs(epsg=3857)

            ax = source_geometries.area_of_interest_as_dataframe.plot(color='#ffffff', edgecolor='black', alpha=0.1,
                                                                      linewidth=2)
            ax = source_geometries.all.plot(ax=ax, color=color, edgecolor=edgecolor)
            ax = input_data.lines.plot(ax=ax, column='Length', alpha=0.6, legend=True,
                                       cmap='Reds', legend_kwds={'label': "Route length, m"},
                                       zorder=1, vmin=0)
            ax = target_point.plot(ax=ax, color='red', alpha=1.0, markersize=40, edgecolor='black')
            if self.params.get('title') is not None:
                plt.suptitle(self.params.get('title'))
            cx.add_basemap(ax, crs=target_point.crs.to_string(), source=cx.providers.CartoDB.Voyager)
            plt.show()

            # Return WGS 84 projection
            input_data.to_crs(WGS_EPSG)

        return input_data
