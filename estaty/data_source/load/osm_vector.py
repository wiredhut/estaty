from pathlib import Path
from typing import Optional, Union

import geopandas
import osmnx as ox
import pandas as pd

import warnings

from loguru import logger

from estaty.data.data import CommonData, VectorData
from estaty.data_source.load.osm_save_load import save_geodataframe_into_file, \
    load_geodataframe_from_file
from estaty.data_source.load.repository.locations import WGS_LOCATION_BOUNDS
from estaty.data_source.load.repository.osm_tags import WATER_TAGS, PARKS_TAGS, \
    LIGHTS_TAGS
from estaty.paths import get_tmp_folder_path
from estaty.stages import Stage

warnings.filterwarnings('ignore')


class LoadOSMStage(Stage):
    """
    Class for loading OSM data. Can be used for loading data within
    predefined areas boundaries
    """

    tags_by_category = {'water': WATER_TAGS,
                        'parks': PARKS_TAGS,
                        'lights': LIGHTS_TAGS}

    allowed_geom_by_category = {'water': ['LineString', 'Polygon', 'MultiPolygon'],
                                'parks': ['Polygon', 'MultiPolygon']}

    def __init__(self, **params):
        super().__init__(**params)
        self.category = params['category']
        self.location = params['location']
        self.max_y, self.min_y, self.min_x, self.max_x = WGS_LOCATION_BOUNDS[self.location]

        # Use temporary folder to save results
        self.folder = Path(get_tmp_folder_path(), self.location)
        self.folder.mkdir(parents=True, exist_ok=True)

    def apply(self, input_data: Union[CommonData, None]) -> CommonData:
        """ Load data with all available categories """
        file_path = Path(self.folder, f'{self.category}.gpkg')
        if file_path.is_file():
            # File exists - load it
            osm_data = load_geodataframe_from_file(file_path)
            logger.debug(f'Successfully load file {file_path} from temporary folder')
        else:
            # Request data from Open Street Map
            desired_tags = self.tags_by_category[self.category]
            bbox_info = ox.geometries_from_bbox(self.max_y, self.min_y,
                                                self.min_x, self.max_x,
                                                tags=desired_tags)
            # Parse data by geometries types
            osm_data = self.filter_data_by_category(bbox_info)

            if osm_data is None or len(osm_data) < 1:
                raise ValueError(f'Can not obtain any data for {self.location} and {self.category}')
            osm_data = osm_data.reset_index()
            logger.debug(f'Successfully get data via osmnx')

            # Save data into gpkg file
            if self.category == 'lights':
                save_geodataframe_into_file(osm_data, file_path,
                                            save_only_geometries=True)
            else:
                save_geodataframe_into_file(osm_data, file_path)

        # Always load vector data
        return self.compose_vector_data(osm_data)

    def filter_data_by_category(self, bbox_info: geopandas.geodataframe.DataFrame):
        """ Remain only desired geometries in OSM data """
        allowed_geometries = self.allowed_geom_by_category.get(self.category)
        if allowed_geometries is None:
            # All geometries is allowed
            return bbox_info

        # Parse data by geometries types
        geom_types = list(bbox_info.geometry.geometry.type.unique())
        osm_data = []
        for geom_type in geom_types:
            if geom_type in allowed_geometries:
                g_bbox = bbox_info.loc[bbox_info.geometry.geometry.type == geom_type]
                osm_data.append(g_bbox)

        osm_data = pd.concat(osm_data)
        return osm_data

    def compose_vector_data(self, osm_data: geopandas.geodataframe.DataFrame) -> VectorData:
        """ Generate VectorData with desired fields """
        vector_data = VectorData()

        geom_types = list(osm_data.geometry.geometry.type.unique())
        for geom_type in geom_types:
            geom_df = osm_data.loc[osm_data.geometry.geometry.type == geom_type]
            if geom_type == 'Point':
                vector_data.points = geom_df
            elif geom_type == 'LineString':
                vector_data.lines = geom_df
            elif geom_type == 'Polygon' or geom_type == 'MultiPolygon':
                if vector_data.polygons is not None:
                    vector_data.polygons = pd.concat([vector_data.polygons, geom_df])
                else:
                    vector_data.polygons = geom_df
            else:
                raise ValueError(f'Unknown type {geom_type} of geometries detected.')

        return vector_data
