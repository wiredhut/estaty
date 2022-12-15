import pandas as pd
import geopandas

from geopandas import GeoDataFrame

import warnings
warnings.filterwarnings('ignore')


def prepare_points_layer(spatial_dataframe: pd.DataFrame,
                         epsg_code: str = "4326",
                         lon: str = 'lon',
                         lat: str = 'lat') -> geopandas.geodataframe:
    """
    Prepare geopandas dataframe with points and spatial geometries from pandas
    DataFrame

    :param spatial_dataframe: table to convert
    :param epsg_code: code for CRS
    :param lon: name of column in pandas DataFrame with info about longitude
    :param lat: name of column in pandas DataFrame with info about latitude
    """
    geometry = geopandas.points_from_xy(spatial_dataframe[lon], spatial_dataframe[lat])
    gdf = GeoDataFrame(spatial_dataframe, crs=f"EPSG:{epsg_code}", geometry=geometry)
    return gdf
