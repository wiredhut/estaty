# Proximity use case

A crucial characteristic of a real estate object is its proximity to important infrastructural elements 
of the urban environment.

## Calculation description

Proximity analysis allows finding the distance to objects, to police stations, for example.

<img src="https://raw.githubusercontent.com/red5ai/estaty/main/docs/media/proximity_preview_spb.png" width="700"/>

The calculation is based on the OSM road graph. Using this graph, routes to each geographical object are created

<img src="https://raw.githubusercontent.com/red5ai/estaty/main/docs/media/spb_graph.png" width="500"/>

## Scripts 

Three scripts have been prepared for this use case in [cases folder](https://github.com/red5ai/estaty/tree/main/cases/proximity):

- [path_to_bars.py](https://github.com/red5ai/estaty/blob/main/cases/proximity/path_to_bars.py) - calculate the routes to the bars using OpenStreetMap data
- [path_to_parks.py](https://github.com/red5ai/estaty/blob/main/cases/proximity/path_to_parks.py) - calculate the routes to the parks using OpenStreetMap data
- [path_to_parks_with_quercus.py](https://github.com/red5ai/estaty/blob/main/cases/proximity/path_to_parks_with_quercus.py) - calculate the routes to the parks (OpenStreetMap data) 
    with Quercus robur ([GBIF | Global Biodiversity Information Facility](https://www.gbif.org/)). GBIF.org (20 October 2023) GBIF Occurrence Download https://doi.org/10.15468/dl.f487j5


## Related materials

In progress
