from pathlib import Path
from typing import Union

import geopandas
import osmnx as ox
import pandas as pd

import warnings

from loguru import logger

from estaty.data.data import CommonData, VectorData
from estaty.data_source.load.osm_save_load import save_geodataframe_into_file, \
    load_geodataframe_from_file
from estaty.data_source.load.repository.osm_tags import *
from estaty.engine.vector.clip import clip_dataframe_by_polygon
from estaty.engine.vector.convert import create_polygon_from_point
from estaty.paths import get_tmp_folder_path
from estaty.stages import Stage

warnings.filterwarnings('ignore')


class LoadOSMStage(Stage):
    """
    Class for loading OSM data. Can be used for loading data within
    predefined areas boundaries
    """

    tags_by_category = {'water': WATER_TAGS,
                        'park': PARKS_TAGS,
                        'light': LIGHTS_TAGS,
                        'municipality': MUNICIPALITY_TAGS,
                        'school': SCHOOL_TAGS,
                        'driving_school': DRIVING_SCHOOL_TAGS,
                        'bar': BARS_TAGS,
                        'waste_disposal': WASTE_DISPOSAL_TAGS,
                        'toilet': TOILETS_TAGS,
                        'police': POLICE}

    # Several spatial objects must include only particular geometries types
    allowed_geom_by_category = {'water': ['LineString', 'Polygon', 'MultiPolygon'],
                                'park': ['Polygon', 'MultiPolygon'],
                                'municipality': ['Polygon', 'MultiPolygon']}

    def __init__(self, **params):
        super().__init__(**params)
        self.category = params['category']

        self.local_cache = params.get('local_cache')
        if self.local_cache is None:
            self.local_cache = True

        analysis_point = params['object_for_analysis']
        self.object_for_analysis = analysis_point

        # Use temporary folder to save results
        lat = str(round(analysis_point["lat"], 3)).replace('.', '_')
        lon = str(round(analysis_point["lon"], 3)).replace('.', '_')
        self.location_name = f'Point_{lat}_{lon}_with_buffer_{analysis_point["radius"]}'

        self.folder = Path(get_tmp_folder_path(), self.location_name)
        self.folder.mkdir(parents=True, exist_ok=True)

    def apply(self, input_data: Union[CommonData, None]) -> CommonData:
        """ Load data with all available categories """
        file_path = Path(self.folder, f'{self.category}.gpkg')
        if file_path.is_file():
            # File exists - load it
            osm_data = load_geodataframe_from_file(file_path)
            logger.debug(f'Successfully load file {file_path} from temporary folder')

            # Clip all the data if required
            polygon = create_polygon_from_point(self.object_for_analysis,
                                                buffer=self.object_for_analysis[
                                                    'radius'])
            osm_data = clip_dataframe_by_polygon(osm_data, polygon)
        else:
            # Request data from Open Street Map
            desired_tags = self.tags_by_category[self.category]

            # Configure polygon for request and define tags
            polygon = create_polygon_from_point(self.object_for_analysis,
                                                buffer=self.object_for_analysis['radius'])
            bbox_info = ox.geometries_from_polygon(polygon=polygon,
                                                   tags=desired_tags)
            bbox_info = clip_dataframe_by_polygon(bbox_info, polygon)

            # Parse data by geometries types
            osm_data = self.filter_data_by_category(bbox_info)

            if osm_data is None or len(osm_data) < 1:
                raise ValueError(f'Can not obtain any data for {self.location_name} and {self.category}')

            osm_data = osm_data.reset_index()
            logger.debug(f'Successfully get data via osmnx')

            # Save data into gpkg file (if it is required)
            if self.local_cache:
                if self.category == 'light':
                    save_geodataframe_into_file(osm_data, file_path,
                                                save_only_geometries=True)
                else:
                    save_geodataframe_into_file(osm_data, file_path)

        # Always load vector data
        vector_data = self.compose_vector_data(osm_data)
        vector_data.area_of_interest = polygon

        # Does not allow multipolygons presence
        if vector_data.polygons is not None:
            vector_data.polygons = vector_data.polygons.explode(index_parts=True)
        if vector_data.lines is not None:
            vector_data.lines = vector_data.lines.explode(index_parts=True)
        return vector_data

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

        if len(osm_data) < 1:
            raise ValueError('There are no requested category data for desired area according to OSM')
        osm_data = pd.concat(osm_data)
        return osm_data

    @staticmethod
    def compose_vector_data(osm_data: geopandas.geodataframe.DataFrame) -> VectorData:
        """ Generate VectorData with desired fields """
        vector_data = VectorData()

        geom_types = list(osm_data.geometry.geometry.type.unique())
        for geom_type in geom_types:
            geom_df = osm_data.loc[osm_data.geometry.geometry.type == geom_type]
            if geom_type == 'Point':
                vector_data.points = geom_df
            elif geom_type == 'LineString' or geom_type == 'MultiLineString':
                vector_data.lines = geom_df
            elif geom_type == 'Polygon' or geom_type == 'MultiPolygon':
                if vector_data.polygons is not None:
                    vector_data.polygons = pd.concat([vector_data.polygons, geom_df])
                else:
                    vector_data.polygons = geom_df
            else:
                raise ValueError(f'Unknown type {geom_type} of geometries detected.')

        # Always return Vector data with WSG 84 CRS
        vector_data.to_crs(4326)
        return vector_data
