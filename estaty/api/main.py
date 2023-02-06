from enum import Enum
from typing import Optional
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel

from estaty.api.default import *
from estaty.api.estaty_api import Estaty
from estaty.api_utils.property import PropertyObjectConfiguration

app = FastAPI()


class ModeName(str, Enum):
    simple = "simple"
    advanced = "advanced"


class Place(BaseModel):
    address: Optional[str] = Query(default=DEFAULT_ADDRESS,
                                   title="Address of desired place for analysis",
                                   description="String object. For example 'Berlin, Neustädtische Kirchstraße 4-7'. "
                                               "If coordinates are set together with the address, the coordinates "
                                               "will be used (have higher priority)")
    lat: Optional[float] = Query(default=DEFAULT_LAT,
                                 title="Latitude (CRS: WGS84) of desired place for analysis",
                                 description="Float object - latitude coordinate. Longitude coordinate is also reqiured")
    lon: Optional[float] = Query(default=DEFAULT_LON,
                                 title="Longitude (CRS: WGS84) of desired place for analysis",
                                 description="Float object - longitude coordinate. Latitude coordinate is also reqiured")


class GreenCaseOutput(BaseModel):
    green_zone_area: float = Query(title="Calculated green zone area ratio related to buffer, %")
    geometries: str = Query(title="Green areas geometries. CRS: WGS84")
    buffer: str = Query(title="Buffer geometry. CRS: WGS84")


@app.get("/")
def read_root():
    """ Common description of the service """
    response = {"service": "estaty use cases demo",
                "description": "Service for spatial data fusion and processing "
                               "for real estate objects"}
    return response


@app.post("/green/{mode}", response_model=GreenCaseOutput)
def green_case(mode: ModeName, place: Place, radius: int = 1000):
    """
    Launch green area calculation for desired place. The analysis can be
    launched in two different modes - 'simple' and advanced. 'Simple' mode include
    area calculation with usage Open Street Map data 'as is'. For 'advanced'
    mode more complicated processing pipeline is launched: load data from OSM,
    prepare NDVI data from Landsat and launch polygons clarification
    """
    exception_for_advanced_case(mode, place)
    service = Estaty(place, radius)
    calc_area, geometries, buffer = service.launch_green_area_calculation_case(mode)
    return {"green_zone_area": calc_area, "geometries": geometries, "buffer": buffer}


def exception_for_advanced_case(mode: ModeName, place: Place):
    """ Temporary exception """
    if mode == 'simple':
        return

    property_info = {'lat': place.lat, 'lon': place.lon}
    if place.address != DEFAULT_ADDRESS and are_coordinates_default(place.lat,
                                                                    place.lon):
        # New address were assigned
        property_info = place.address
        preparer = PropertyObjectConfiguration(None, property_info)
        property_info = preparer.configure_object()

    message = f'For desired extend it is impossible to apply advanced approach. ' \
              f'Please, try choose area nearby Berlin'
    if property_info['lon'] < 12.53 or property_info['lon'] > 14.41:
        raise HTTPException(status_code=404, detail=message)
    if property_info['lat'] < 52.47 or property_info['lat'] > 53.70:
        raise HTTPException(status_code=404, detail=message)
