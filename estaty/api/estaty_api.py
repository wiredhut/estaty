from loguru import logger

from estaty.analysis.action import Analyzer
from estaty.api.default import *
from estaty.data_source.action import DataSource
from estaty.main import EstateModel
from estaty.preprocessing.action import Preprocessor


DUMMY_ADDRESS = 'put here your address'


class Estaty:
    """ Binding above low-level abstractions """

    def __init__(self, place, radius: int):
        self.radius = radius

        # Parse information about spatial coordinates or related info
        self.property_info = {'lat': place.lat, 'lon': place.lon}
        if place.address != DEFAULT_ADDRESS and are_coordinates_default(place.lat, place.lon):
            # New address were assigned
            self.property_info = place.address

        logger.info(f'Start processing case for object {self.property_info} with radius {self.radius} metres')

    def launch_green_area_calculation_case(self, mode_name: str):
        """
        Launch green area case calculation
        """
        if mode_name == 'simple':
            osm_source = DataSource('osm', params={'category': 'parks'})
            osm_reprojected = Preprocessor('reproject', params={'to': 'auto'},
                                           from_actions=[osm_source])
            analysis = Analyzer('area', from_actions=[osm_reprojected])
            if isinstance(self.property_info, dict):
                model = EstateModel().for_property(coordinates=self.property_info,
                                                   radius=self.radius)
            else:
                model = EstateModel().for_property(address=self.property_info,
                                                   radius=self.radius)
            calculated_areas = model.compose(analysis)

            green_area = calculated_areas.polygons['area'].sum()
            # Convert into WGS 84
            calculated_areas.to_crs(epsg=4326)
            return green_area, calculated_areas.polygons.to_json()
        elif mode_name == 'advanced':
            # Launch advanced pipeline
            pass
        else:
            raise NotImplementedError(f'Does not support mode {mode_name} for green area calculation')
