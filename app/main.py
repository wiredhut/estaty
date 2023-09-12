from enum import Enum
from typing import Optional, Dict
import numpy as np

from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel, root_validator

from estaty.api.default import *
from estaty.api.estaty_api import Estaty
from estaty.api_utils.property import PropertyObjectConfiguration

app = FastAPI()


class ModeName(str, Enum):
    simple = "OpenStreetMap"
    advanced = "OpenStreetMap_Landsat"


class Place(BaseModel):
    address: Optional[str] = Query(default=DEFAULT_ADDRESS,
                                   title="Address of desired place for analysis",
                                   description="String object. For example 'Berlin, Neustädtische Kirchstraße 4-7'. "
                                               "If coordinates are set together with the address, the coordinates "
                                               "will be used (have higher priority)")

    @root_validator(pre=True)
    def check_parameters_correctness(cls, values: Dict):
        # Check address
        address_was_set = False
        if values.get('address') is not None and values['address'] != DEFAULT_ADDRESS:
            address_was_set = True

        # Check coordinates
        both_coordinates_not_none = values.get('lat') is not None and values.get('lon') is not None
        if address_was_set and both_coordinates_not_none:
            # Coordinates must be default
            if are_coordinates_default(values['lat'], values['lon']) is False:
                message = 'If address was defined coordinates must not be passed'
                raise HTTPException(status_code=404, detail=message)
        return values


class GreenCaseOutput(BaseModel):
    green_zone_area: float = Query(title="Calculated green zone area ratio related to buffer, %")
    geometries: dict = Query(title="Green areas geometries. CRS: WGS84")
    buffer: dict = Query(title="Buffer geometry. CRS: WGS84")


@app.get("/")
def read_root():
    """ Common description of the service """
    response = {"service": "estaty use cases demo",
                "description": "Service for spatial data fusion and processing "
                               "for real estate objects"}
    return response


@app.post("/green/{mode}", response_model=GreenCaseOutput)
def green_case(mode: ModeName, place: Place,
               radius: int = Query(title="Buffer radius in metres", default=1000,
                                   gt=100, le=2000)):
    """
    Launch green area calculation for desired place. The analysis can be
    launched in two different modes:

    - **"OpenStreetMap"** - include area calculation with usage Open Street Map data 'as is'
    - **"OpenStreetMap_Landsat"** - more complicated processing pipeline is launched: load data
    from OSM, prepare NDVI data from Landsat and launch polygons clarification

    Return geometries of obtained green areas and calculated green index (percentage)
    """
    exception_for_advanced_case(mode, place)
    service = Estaty(place, radius)
    calc_area, geometries, buffer = service.launch_green_area_calculation_case(mode)
    return {"green_zone_area": calc_area, "geometries": eval(geometries), "buffer": eval(buffer)}


def exception_for_advanced_case(mode: ModeName, place: Place):
    """ Temporary exception """
    if mode == 'OpenStreetMap':
        return

    # New address was assigned
    property_info = place.address
    preparer = PropertyObjectConfiguration(None, property_info)
    property_info = preparer.configure_object()

    message = f'For desired extend it is impossible to apply advanced approach. ' \
              f'Please, try choose area nearby Berlin'
    if property_info['lon'] < 12.53 or property_info['lon'] > 14.41:
        raise HTTPException(status_code=404, detail=message)
    if property_info['lat'] < 52.47 or property_info['lat'] > 53.70:
        raise HTTPException(status_code=404, detail=message)
