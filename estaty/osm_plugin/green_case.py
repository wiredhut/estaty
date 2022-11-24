import geopandas
import pandas as pd


class GreenAnalysis:
    """ Launch analysis with distance metrics calculation """

    def __init__(self, osm_data: dict, radius: float = 500):
        gdf = []
        for geom_type, spatial_object in osm_data.items():
            if geom_type == 'Polygon' or geom_type == 'MultiPolygon':
                gdf.append(spatial_object)

        gdf = pd.concat(gdf)
        gdf['dummy_column'] = 0
        self.gdf = gdf.dissolve(by='dummy_column')
        self.gdf = self.gdf.explode()
        self.radius = radius

    def calculate_metric(self, x_coord: float, y_coord: float):
        pass
