from enum import Enum
from typing import Optional
from fastapi import FastAPI, Query
from pydantic import BaseModel

from estaty.api.default import *
from estaty.api.estaty_api import Estaty

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
                                 title="Latitude in WGS84 of desired place for analysis",
                                 description="Float object - latitude coordinate. Longitude coordinate is also reqiured")
    lon: Optional[float] = Query(default=DEFAULT_LON,
                                 title="Longitude in WGS84 of desired place for analysis",
                                 description="Float object - longitude coordinate. Latitude coordinate is also reqiured")


@app.get("/")
def read_root():
    response = {"service": "estaty use cases demo",
                "description": "Service for spatial data fusion and processing "
                               "for real estate objects"}
    return response


@app.post("/green/{mode}")
def green_case(mode: ModeName, place: Place, radius: int = 1000):
    """
    Launch green area calculation for desired place. The analysis can be
    launched in two different modes - 'simple' and advanced. Simple mode include
    area calculation with usage Open Street Map data 'as is'. For 'advanced'
    mode more complicated processing pipeline is launched: load data from OSM,
    prepare NDVI data from Landsat and launch polygons clarification
    """
    service = Estaty(place, radius)
    calc_area, geometries = service.launch_green_area_calculation_case(mode)
    return {"green_zone_area": calc_area, "geometries": geometries}
