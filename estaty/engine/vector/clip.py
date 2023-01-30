from geopandas import GeoDataFrame
from shapely.geometry import Polygon


def clip_dataframe_by_polygon(dataframe: GeoDataFrame, polygon: Polygon):
    """
    Clip geopandas dataframe with polygon. Number of polygons (or other
    spatial objects) may remain the same as in source dataframe, but their
    boundaries will be clipped
    """
    dataframe = dataframe.clip(polygon)
    return dataframe
