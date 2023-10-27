# Proximity analysis

In this section scripts for "Proximity analysis" use case are prepared. 
Proximity analysis is an analysis of the availability of infrastructural facilities on the real estate object

## Calculation description

Proximity analysis allows finding the distance to objects, to police stations, for example.

<img src="https://raw.githubusercontent.com/red5ai/estaty/main/docs/media/proximity_preview_spb.png" width="700"/>

The calculation is based on the OSM road graph. Using this graph, routes to each geographical object are created

<img src="https://raw.githubusercontent.com/red5ai/estaty/main/docs/media/spb_graph.png" width="500"/>

## Scripts 

Three scripts have been prepared for this use case:

- [path_to_bars.py](path_to_bars.py) - calculate the routes to the bars using OpenStreetMap data
- [path_to_parks.py](path_to_parks.py) - calculate the routes to the parks using OpenStreetMap data
- [path_to_parks_with_quercus.py](path_to_parks_with_quercus.py) - calculate the routes to the parks (OpenStreetMap data) 
    with Quercus robur ([GBIF | Global Biodiversity Information Facility](https://www.gbif.org/)). GBIF.org (20 October 2023) GBIF Occurrence Download https://doi.org/10.15468/dl.f487j5


## Related materials

- [Proximity Analysis to Find the Nearest Bar Using Python](https://medium.com/towards-data-science/proximity-analysis-to-find-the-nearest-bar-using-python-a29d29a3754d) (eng)
- [“Ну и долго мне ещё до магазина?” Или пара слов о геоинформационном анализе с помощью Python](https://habr.com/ru/articles/770216/) (rus)
