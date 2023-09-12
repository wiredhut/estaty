from shapely.geometry import Polygon
import osmnx as ox
import matplotlib.pyplot as plt

from estaty.engine.vector.clip import clip_dataframe_by_polygon


class AdministrativeBoundaries:
    """ Load polygon of administrative boundaries for desired city

    :param city_name: name of the city for analysis
    """

    def __init__(self, city_name: str):
        self.use_only_buildings = False
        if 'building' in city_name:
            city_name = city_name.split('_building')[0]
            self.use_only_buildings = True

        self.city_name = city_name

    def get_city_polygon(self) -> Polygon:
        """ Query data from OSM and return geometry of obtained polygon """
        gdf = ox.geocode_to_gdf({'city': self.city_name})
        city_polygon = gdf.geometry.iloc[0]
        if self.use_only_buildings is False:
            return city_polygon

        # Add only buildings
        buildings_tags = {'building': ['apartments', 'barracks', 'bungalow',
                                       'cabin', 'detached', 'dormitory', 'farm',
                                       'ger', 'hotel', 'house', 'houseboat',
                                       'residential', 'semidetached_house',
                                       'static_caravan', 'stilt_house',
                                       'terrace', 'tree_house', 'commercial',
                                       'industrial', 'kiosk', 'office', 'retail',
                                       'supermarket', 'warehouse']}
        bbox_info = ox.geometries_from_polygon(polygon=city_polygon,
                                               tags=buildings_tags)
        bbox_info = clip_dataframe_by_polygon(bbox_info, city_polygon)

        # Perform polygons merging into single geometry
        bbox_info['new_column'] = 0
        bbox_info = bbox_info.dissolve(by='new_column')
        return bbox_info.geometry.iloc[0]
