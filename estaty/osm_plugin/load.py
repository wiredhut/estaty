from pathlib import Path
from typing import Optional, Union

import geopandas
import osmnx as ox

import warnings

from loguru import logger

from estaty.paths import get_tmp_folder_path

warnings.filterwarnings('ignore')


WATER_TAGS = {'natural': ['water', 'strait', 'wetland'],
              'water': ['river', 'oxbow', 'canal', 'lake', 'ditch', 'lock',
                        'fish_pass', 'reservoir', 'pond', 'basin']}

PARKS_TAGS = {'boundary': ['national_park', 'forest'],
              'leisure': ['park'],
              'landuse': ['forest', 'meadow', 'orchard'],
              'natural': ['grassland', 'wood']}


class LoadOSMData:
    """ Class for loading OSM data """

    tags_by_category = {'water': WATER_TAGS,
                        'parks': PARKS_TAGS}

    # Lower left and upper right coordinates (lat and long) of location in WGS84
    location_by_name = {'Berlin': [52.68, 52.37, 13.04, 13.75]}

    def __init__(self, location: str = None,
                 max_y: Optional[float] = None,
                 min_y: Optional[float] = None,
                 min_x: Optional[float] = None,
                 max_x: Optional[float] = None,
                 folder_to_save_data: Union[str, Path] = None):
        if location is not None:
            # Location was defined by name
            self.max_y, self.min_y, self.min_x, self.max_x = self.location_by_name[location]
        else:
            # Create name for location
            location = f'Location {str(min_x).replace(".", "_")}, ' \
                       f'{str(min_y).replace(".", "_")} and ' \
                       f'{str(max_x).replace(".", "_")}, ' \
                       f'{str(max_x).replace(".", "_")}'
            # Configure location by coordinates directly
            self.max_y = max_y
            self.min_y = min_y
            self.min_x = min_x
            self.max_x = max_x

        if folder_to_save_data is None:
            # Use own TMP folder
            self.folder = Path(get_tmp_folder_path(), location)
        else:
            if isinstance(folder_to_save_data, str):
                folder_to_save_data = Path(folder_to_save_data)
                folder_to_save_data = folder_to_save_data.resolve()

            self.folder = Path(folder_to_save_data, location)

        self.folder.mkdir(parents=True, exist_ok=True)

    def get_data(self, category: str):
        """ Load data with all available categories """
        if self._was_data_saved(category):
            osm_data = self._load_saved_data(category)
        else:
            # Request data from Open Street Map
            desired_tags = self.tags_by_category[category]
            bbox_info = ox.geometries_from_bbox(self.max_y, self.min_y,
                                                self.min_x, self.max_x,
                                                tags=desired_tags)
            # Parse data by geometries types
            geom_types = list(bbox_info.geometry.geometry.type.unique())
            osm_data = {}
            for geom_type in geom_types:
                g_bbox = bbox_info.loc[bbox_info.geometry.geometry.type == geom_type]
                osm_data.update({geom_type: g_bbox})

            self._save_data(category, osm_data)

        return osm_data

    def _was_data_saved(self, category: str):
        """ Check was the required data already loaded or not """
        return any(category in str(file.name) for file in self.folder.iterdir())

    def _load_saved_data(self, category: str):
        """ Load data into one dictionary """
        osm_data = {}
        for file in self.folder.iterdir():
            if '.geojson' in file.name and category in file.name:
                full_file_name = str(file.name).split('.geojson')[0]
                geom_type = full_file_name.split('_')
                # Load data from geojson file
                spatial_objects = geopandas.read_file(file)
                spatial_objects = spatial_objects[['geometry']]
                osm_data.update({geom_type: spatial_objects})

        return osm_data

    def _save_data(self, category: str, osm_data: dict):
        """ Save all geometries into files """
        for geom_type, objects in osm_data.items():
            # Save as geojson
            objects[['geometry']].to_file(Path(self.folder, f'{category}_{geom_type}.geojson'))

            try:
                # Save empty file as gpkg
                objects[['geometry']].to_file(Path(self.folder, f'{category}_{geom_type}.gpkg'),
                                              driver='GPKG', layer=f'{category}_{geom_type}')
            except Exception as ex:
                logger.info(f'Saving geometry {geom_type} into GPKG file failed due to {ex}. Continue')
