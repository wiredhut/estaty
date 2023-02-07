import numpy as np


DEFAULT_ADDRESS = 'put here your address'
DEFAULT_LAT = 52.5171411
DEFAULT_LON = 13.3857187


def are_coordinates_default(current_lat: float, current_lon: float):
    """ Check that coordinates equal to default """
    is_lat_default = np.isclose(current_lat, DEFAULT_LAT)
    is_lon_default = np.isclose(current_lon, DEFAULT_LON)

    return bool(is_lat_default and is_lon_default)
