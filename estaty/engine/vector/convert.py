from typing import Union

import pandas as pd
import numpy as np

import geopandas

from geopandas import GeoDataFrame

import warnings

from pyproj import Transformer
from shapely.geometry import Polygon, Point

warnings.filterwarnings('ignore')


def prepare_points_layer(spatial_dataframe: pd.DataFrame,
                         epsg_code: str = "4326",
                         lon: str = 'lon',
                         lat: str = 'lat') -> geopandas.geodataframe:
    """
    Prepare geopandas dataframe with points and spatial geometries from simple
    pandas DataFrame

    :param spatial_dataframe: table to convert
    :param epsg_code: code for CRS
    :param lon: name of column in pandas DataFrame with info about longitude
    :param lat: name of column in pandas DataFrame with info about latitude
    """
    geometry = geopandas.points_from_xy(spatial_dataframe[lon], spatial_dataframe[lat])
    gdf = GeoDataFrame(spatial_dataframe, crs=f"EPSG:{epsg_code}", geometry=geometry)
    return gdf


def create_polygon_from_point(point_coordinates: dict, buffer: int) -> Polygon:
    """ Generate polygon from point coordinates

    :param point_coordinates: dictionary with 'lat' 'lon' coordinates in WGS 84
    :param buffer: buffer in metres
    """
    # TODO fix this function - does not work
    # Convert coordinates from WGS into appropriate metric projection
    metric_point_coordinates, utm_code = get_utm_code_from_extent(point_coordinates['lat'],
                                                                  point_coordinates['lon'])
    # Lat ang lon coordinates
    metric_polygon = Point((metric_point_coordinates['lat'],
                            metric_point_coordinates['lon'])).buffer(buffer)

    # Convert coordinates into WGS84 projection
    lats, lons = metric_polygon.exterior.coords.xy
    # Transform coordinates to WGS 84
    df_with_coordinates = pd.DataFrame({'lat': lats.tolist(), 'lon': lons.tolist()})
    df_with_coordinates = transform_coordinates_in_dataframe(df_with_coordinates,
                                                             utm_code, 4326)
    buffer_polygon = Polygon(np.array(df_with_coordinates[['lon', 'lat']])).convex_hull
    return buffer_polygon


def get_utm_code_from_extent(lat_coord: float, lon_coord: float):
    """
    Search for appropriate EPSG code of metric projection for point coordinates

    """
    # 326NN or 327NN - where NN is the zone number
    if lat_coord < 0:
        base_code = 32700
    else:
        base_code = 32600

    zone = int(((lon_coord + 180) / 6.0) % 60) + 1
    utm_code = base_code + zone

    transformer = Transformer.from_crs("EPSG:4326", f"EPSG:{utm_code}",
                                       always_xy=True)
    metric_point_coordinates = transformer.transform(*[lon_coord, lat_coord])
    return {'lat': metric_point_coordinates[-1],
            'lon': metric_point_coordinates[0]}, utm_code


def transform_coordinates_in_dataframe(dataframe: Union[pd.DataFrame, GeoDataFrame],
                                       current_projection_code: Union[int, str],
                                       new_projection_code: Union[int, str],
                                       lat_column: str = 'lat',
                                       lon_column: str = 'lon'):
    """
    Transform coordinates from one coordinate system into another using
    simple Pandas Dataframes
    """
    current_long = np.array(dataframe[lon_column])
    current_lat = np.array(dataframe[lat_column])
    transformer = Transformer.from_crs(f"EPSG:{current_projection_code}",
                                       f"EPSG:{new_projection_code}",
                                       always_xy=True)
    new_long, new_lat = transformer.transform(*[current_long, current_lat])
    dataframe[lon_column] = new_long
    dataframe[lat_column] = new_lat

    dataframe = dataframe.drop_duplicates()
    return dataframe
