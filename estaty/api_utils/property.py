from typing import Dict, Union

import requests
from loguru import logger


class PropertyObjectConfiguration:
    """
    Configure point location as dictionary with coordinates for further usage
    """

    def __init__(self, coordinates: Union[Dict, None],
                 address: Union[str, None]):
        if coordinates is not None and address is not None:
            raise ValueError('Property locations must be defined by coordinates'
                             ' or address, not by both fields')

        if coordinates is not None and len(coordinates.keys()) != 2:
            raise ValueError('"coordinates" parameter must contain exactly two pairs - '
                             'coordinates "lat" and "lon" and they values')

        elif coordinates is not None and any(coord_name not in coordinates.keys() for coord_name in ['lat', 'lon']):
            raise ValueError(f'Keys in "coordinates" dictionary must be "lat" and "lon"')

        self.coordinates = coordinates
        self.address = address

    def configure_object(self):
        if self.address is not None:
            self.coordinates = self._get_coordinates_by_address()
            logger.debug(f'Successfully determined coordinates for '
                         f'address {self.address}: {self.coordinates}')

        if all(coord_name in self.coordinates.keys() for coord_name in ['lat', 'lon']):
            return self.coordinates
        else:
            raise ValueError('Coordinates must be set by dictionary with keys '
                             '"lat" for latitude and "lon" for longitude')

    def _get_coordinates_by_address(self) -> Dict:
        """ Use Nominatim API for geocoding """
        params = {'q': self.address, 'format': 'json'}
        response = requests.get('https://nominatim.openstreetmap.org/search',
                                params=params)
        poi_information = eval(response.text)[0]
        return {'lat': float(poi_information['lat']),
                'lon': float(poi_information['lon'])}
