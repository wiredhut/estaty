from typing import Dict, Union


class PropertyObjectConfiguration:
    """
    Configure point location as dictionary with coordinates for further usage
    """

    def __init__(self, coordinates: Union[Dict, None],
                 address: Union[str, None]):
        if coordinates is not None and address is not None:
            raise ValueError('Property locations must be defined by coordinates'
                             ' or address, not by both fields')

        self.coordinates = coordinates
        self.address = address

    def configure_object(self):
        if self.address is not None:
            self.coordinates = self._get_coordinates_by_address()

        if all(coord_name in self.coordinates.keys() for coord_name in ['lat', 'lon']):
            return self.coordinates
        else:
            raise ValueError('Coordinates must be set by dictionary with keys '
                             '"lat" for latitude and "lon" for longitude')

    def _get_coordinates_by_address(self):
        raise NotImplementedError('Getting location by address is not available'
                                  'for now')
