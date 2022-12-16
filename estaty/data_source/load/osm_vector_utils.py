from shapely.geometry import Polygon


def convert_osm_bbox_coordinates(bbox_coordinates: list):
    """ Convert OSM bbox coordinates into shapely polygon """
    polygon = [(bbox_coordinates[2], bbox_coordinates[1]),
               (bbox_coordinates[2], bbox_coordinates[0]),
               (bbox_coordinates[3], bbox_coordinates[0]),
               (bbox_coordinates[3], bbox_coordinates[1])]
    return Polygon(polygon).convex_hull
