from copy import deepcopy
from typing import Union, List

import geopandas
import numpy as np
from geopandas import GeoDataFrame
from matplotlib import pyplot as plt
from shapely import Point
import contextily as cx

from estaty.constants import WGS_EPSG
from estaty.data.data import VectorData
from estaty.engine.vector.convert import polygons_aggregation
from estaty.stages import Stage


class VectorDataMergingStage(Stage):
    """ Load data and stored in csv locally """

    def __init__(self, **params):
        super().__init__(**params)
        self.object_for_analysis = params['object_for_analysis']
        self.method = params['method']
        self.buffer = params.get('buffer')

        self.visualize = False
        if self.params.get('visualize') is not None:
            self.visualize = self.params.get('visualize')

    def apply(self, input_data: List[VectorData]) -> VectorData:
        basic_geometries: VectorData = input_data[0]
        matching_geometries: VectorData = input_data[1]

        if self.visualize:
            # TODO - refactor that visualization part
            basic_geometries_copy = deepcopy(basic_geometries)
            matching_geometries_copy = deepcopy(matching_geometries)

            basic_geometries_copy.to_crs(3857)
            matching_geometries_copy.to_crs(3857)

            # Create layer with central (target) point
            geometry = Point([self.object_for_analysis['lon'], self.object_for_analysis['lat']])
            target_point = GeoDataFrame(crs=f"EPSG:{WGS_EPSG}", geometry=[geometry])
            target_point = target_point.to_crs(epsg=3857)

            ax = basic_geometries_copy.area_of_interest_as_dataframe.plot(color='#ffffff', edgecolor='black',
                                                                          alpha=0.1, linewidth=2)
            ax = basic_geometries_copy.all.plot(ax=ax, color='green', edgecolor='black')
            ax = matching_geometries_copy.points.plot(ax=ax, alpha=1.0, markersize=30, legend=True,
                                                      color='#26D00B', zorder=1)
            ax = target_point.plot(ax=ax, color='red', alpha=1.0, markersize=40, edgecolor='black')
            cx.add_basemap(ax, crs=target_point.crs.to_string(), source=cx.providers.CartoDB.Voyager)
            plt.show()

        # Match - remain only polygons which matched with second data
        # See: https://gis.stackexchange.com/questions/446097/intersection-of-two-geopandas-dataframes
        polygons_to_filter = basic_geometries.all
        polygons_to_filter["polygons_to_filter_row"] = np.arange(0, polygons_to_filter.shape[0]).astype(int)

        geometries_to_overlay = matching_geometries.all
        if self.buffer is not None:
            geometries_to_overlay['geometry'] = geometries_to_overlay.geometry.buffer(self.buffer)
        geometries_to_overlay["row"] = np.arange(0, geometries_to_overlay.shape[0]).astype(int).astype(str)

        join = geopandas.sjoin(left_df=polygons_to_filter[["polygons_to_filter_row", "geometry"]],
                               right_df=geometries_to_overlay[["row", "geometry"]], how="left", predicate="intersects")
        # Remove all empty paths
        join = join.dropna()
        return VectorData(polygons=join, epsg=basic_geometries.epsg, area_of_interest=basic_geometries.area_of_interest)
