from loguru import logger

from estaty.analysis.action import Analyzer
from estaty.constants import WGS_EPSG
from estaty.data_source.action import DataSource
from estaty.main import EstateModel
from estaty.preprocessing.action import Preprocessor


DUMMY_ADDRESS = 'put here your address'


class Estaty:
    """ Binding above low-level abstractions """

    def __init__(self, place, radius: int):
        self.radius = radius

        # Parse information about spatial coordinates or related info
        self.property_info = place.address
        logger.info(f'Start processing case for object {self.property_info} with radius {self.radius} metres')

    def launch_green_area_calculation_case(self, mode_name: str = 'OpenStreetMap'):
        """
        Launch green area case calculation. Default mode name is 'OpenStreetMap'.
        """
        if mode_name == 'OpenStreetMap':
            osm_source = DataSource('osm', params={'category': 'park', 'local_cache': False})
            osm_reprojected = Preprocessor('reproject', params={'to': 'auto'},
                                           from_actions=[osm_source])
            analysis = Analyzer('area', from_actions=[osm_reprojected])
            model = self._configure_estaty_model()
            calculated_areas = model.compose(analysis)

            green_area = calculated_areas.polygons['area'].sum()
            # Convert into WGS 84
            calculated_areas.to_crs(epsg=WGS_EPSG)
            buffer = calculated_areas.area_of_interest_as_dataframe
            return green_area, calculated_areas.polygons.to_json(), buffer.to_json()

        elif mode_name == 'OpenStreetMap_Landsat':
            # Launch advanced pipeline
            osm_source = DataSource('osm', params={'category': 'park', 'local_cache': False})
            osm_reprojected = Preprocessor('reproject', params={'to': 'auto'},
                                           from_actions=[osm_source])
            landsat_source = DataSource('ndvi_local')
            ndvi_reprojected = Preprocessor('reproject', params={'to': 'auto'},
                                            from_actions=[landsat_source])
            clarified_boundaries = Analyzer('extend_clarification',
                                            params={'visualize': False},
                                            from_actions=[osm_reprojected,
                                                          ndvi_reprojected])
            analysis = Analyzer('area', from_actions=[clarified_boundaries])

            # Launch model for desired location
            model = self._configure_estaty_model()
            calculated_areas = model.compose(analysis)
            green_area = calculated_areas.polygons['area'].sum()

            # Convert into WGS 84
            calculated_areas.to_crs(epsg=WGS_EPSG)
            buffer = calculated_areas.area_of_interest_as_dataframe
            return green_area, calculated_areas.polygons.to_json(), buffer.to_json()
        else:
            raise NotImplementedError(f'Does not support mode {mode_name} for green area calculation')

    def _configure_estaty_model(self):
        if isinstance(self.property_info, dict):
            model = EstateModel().for_property(coordinates=self.property_info,
                                               radius=self.radius)
        else:
            model = EstateModel().for_property(address=self.property_info,
                                               radius=self.radius)
        return model
