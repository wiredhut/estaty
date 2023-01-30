from typing import Dict, Union

from geopandas import GeoDataFrame
from shapely.geometry import Point

from estaty.actions import SecondaryAction
from estaty.api_utils.property import PropertyObjectConfiguration
from estaty.presets.green import GreenCaseAdvancedPreset


class EstateModel:
    """
    Class for aggregating information from different sources for desired
    object (particular building - properties) or area
    """
    preset_by_name = {'green_advanced': GreenCaseAdvancedPreset}

    def __init__(self):
        self.area_object = None
        self.property_object = None

    def for_area(self, coordinates: Dict):
        """ Add area for analysis """
        raise NotImplementedError('estaty does not support area processing for now')

    def for_property(self, coordinates: Dict = None,
                     address: str = None,
                     radius: int = None):
        """
        Add property for analysis. Can be defined as point with coordinates
        in WGS84 or address of building

        :param coordinates: dictionary with 'lat' 'lon' coordinates
        :param address: string with address
        :param radius: radius for buffer in metres
        """
        preparer = PropertyObjectConfiguration(coordinates, address)
        self.property_object = preparer.configure_object()

        if radius is None or not isinstance(radius, int):
            raise ValueError('Parameter radius must be defined as int value '
                             '(meters) buffer to start analysis')
        self.property_object['radius'] = radius
        return self

    def compose(self, configuration: Union[str, SecondaryAction]):
        """ Launch analysis process with predefined parameters """
        if isinstance(configuration, str):
            # Configuration set through preset name
            preset_to_launch = self.preset_by_name[configuration]()
            final_action = preset_to_launch.return_final_action()
        else:
            # Set as sequence of actions
            final_action = configuration

        final_action.set_object(self.property_object)
        return final_action.execute()

    def get_property_as_dataframe(self):
        """ Return property as spatial object in a form of spatial dataframe """
        geometry = Point([self.property_object['lon'], self.property_object['lat']])
        target_point = GeoDataFrame(index=[0], crs=f"EPSG:4326", geometry=[geometry])
        return target_point
