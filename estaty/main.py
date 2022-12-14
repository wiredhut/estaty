from typing import Dict, Union

from estaty.actions import SecondaryAction
from estaty.api_utils.property import PropertyObjectConfiguration
from estaty.data.search import find_location_name
from estaty.presets.green import GreenCasePreset


class EstateModel:
    """
    Class for aggregating information from different sources for desired
    object (particular building - properties) or area
    """
    preset_by_name = {'green': GreenCasePreset}

    def __init__(self):
        self.area_object = None
        self.property_object = None

    def for_area(self, coordinates: Dict):
        """ Add area for analysis """
        raise NotImplementedError('estaty does not support area processing for now')

    def for_property(self, coordinates: Dict = None, address: str = None):
        """
        Add property for analysis. Can be defined as point with coordinates
        in WGS84 or address of building
        """
        preparer = PropertyObjectConfiguration(coordinates, address)
        self.property_object = preparer.configure_object()
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

        # Get location name based on property coordinates
        self.property_object = find_location_name(self.property_object)
        final_action.set_object(self.property_object)
        return final_action.execute()
