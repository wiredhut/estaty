import os
import osmnx as ox

import warnings
warnings.filterwarnings('ignore')


def load_area_from_osm(max_y: float, min_y: float, min_x: float, max_x: float,
                       tags_to_check: dict):
    """
    Load data from Open Street Map and represent it as geo dataframe.
    Merges the polygons into one layer
    :param max_y: maximum latitude for boundaries (WGS)
    :param min_y: minimum latitude for boundaries (WGS)
    :param min_x: minimum longitude for boundaries (WGS)
    :param max_x: maximum longitude for boundaries (WGS)
    :param tags_to_check: dictionary with tags
    """
    bbox_info = ox.geometries_from_bbox(max_y, min_y, min_x, max_x,
                                        tags=tags_to_check)

    # Get only polygons from dataframe
    bbox_info = bbox_info.loc[bbox_info.geometry.geometry.type == 'Polygon']

    # Perform union into one Multipolygon
    bbox_info['dummy_column'] = 0
    bbox_info = bbox_info.dissolve(by='dummy_column')
    return bbox_info
