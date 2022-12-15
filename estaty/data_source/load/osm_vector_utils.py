from shapely.geometry import Point, Polygon

from estaty.data_source.load.repository.locations import WGS_LOCATION_BOUNDS


def find_location_name_for_point(object_for_analysis: dict):
    """
    Based on point coordinates determine location name

    :param object_for_analysis: dictionary with point coordinates. Keys 'lat'
    and 'lon'
    """
    point = Point(object_for_analysis['lon'], object_for_analysis['lat'])
    determined_location = None
    for location, coordinates in WGS_LOCATION_BOUNDS.items():
        # Get shapely polygon vector layer
        location_polygon = convert_osm_bbox_coordinates(coordinates)
        if location_polygon.contains(point):
            determined_location = location

    if determined_location is None:
        raise ValueError(f'Does not find appropriate location for {object_for_analysis}')
    object_for_analysis['location'] = determined_location
    return object_for_analysis


def convert_osm_bbox_coordinates(bbox_coordinates: list):
    """ Convert OSM bbox coordinates into shapely polygon """
    polygon = [(bbox_coordinates[2], bbox_coordinates[1]),
               (bbox_coordinates[2], bbox_coordinates[0]),
               (bbox_coordinates[3], bbox_coordinates[0]),
               (bbox_coordinates[3], bbox_coordinates[1])]
    return Polygon(polygon).convex_hull
