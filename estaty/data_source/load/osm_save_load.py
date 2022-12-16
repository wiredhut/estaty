from pathlib import Path
import warnings

import geopandas
from geopandas import geodataframe
from loguru import logger
warnings.filterwarnings('ignore')


def save_geodataframe_into_file(dataframe: geodataframe.DataFrame,
                                path_to_file: Path,
                                save_only_geometries: bool = False):
    """ Save geopandas DataFrame into desired file locally """
    dataframe = correct_non_serializable_columns(dataframe)
    if save_only_geometries:
        columns_to_take = ['geometry']
        if 'nodes' in list(dataframe.columns):
            columns_to_take.append('nodes')
        dataframe = dataframe[columns_to_take]
    try:
        if '.geojson' in path_to_file.name:
            # Save as geojson
            dataframe.to_file(path_to_file)
        elif '.gpkg' in path_to_file.name:
            # Save empty file as gpkg - only geometries without attributes
            dataframe.to_file(path_to_file,  driver='GPKG')
        else:
            raise ValueError('Unknown file extension for file.')
    except Exception as ex:
        logger.info(f'Saving file {path_to_file} failed due to {ex}. Continue')


def load_geodataframe_from_file(path_to_file: Path):
    """ Load geopandas geodataframe from """
    spatial_objects = geopandas.read_file(path_to_file)
    return spatial_objects


def replace_list_with_str(cell):
    if isinstance(cell, list):
        return str(cell)
    return cell


def correct_non_serializable_columns(dataframe: geodataframe.DataFrame) -> geodataframe.DataFrame:
    """ Find columns with list in cells. Remove that columns from table """
    list_columns = []
    for col in dataframe.columns:
        if any(isinstance(val, list) for val in dataframe[col]):
            list_columns.append(col)

    # Replace list with nodes with tuples for serialization
    for col in list_columns:
        dataframe[col] = dataframe[col].apply(replace_list_with_str)
    return dataframe
