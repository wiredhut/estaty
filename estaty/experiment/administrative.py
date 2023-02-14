from shapely.geometry import Polygon
import osmnx as ox


class AdministrativeBoundaries:
    """ Load polygon of administrative boundaries for desired city """

    def __init__(self, city_name: str):
        self.city_name = city_name

    def get_city_polygon(self) -> Polygon:
        """ Query data from OSM and return geometry of obtained polygon """
        gdf = ox.geocode_to_gdf({'city': self.city_name})

        return gdf.geometry.iloc[0]
