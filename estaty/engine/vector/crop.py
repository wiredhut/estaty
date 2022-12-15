from shapely.geometry import Polygon
import geopandas

from geopandas import GeoDataFrame


def crop_points_by_polygon(dataframe: GeoDataFrame, polygon: Polygon) -> GeoDataFrame:
    """ Remain only points (rows in dataframe), which lay within polygon """
    pol_gpd = geopandas.GeoDataFrame()
    pol_gpd['geometry'] = None
    pol_gpd.loc[0, 'geometry'] = polygon

    cropped_data = geopandas.sjoin(dataframe, pol_gpd, op='within')

    return cropped_data
