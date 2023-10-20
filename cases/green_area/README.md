# Green area calculation 

In this section scripts for "Green area calculation" use case are prepared. 
Green area (or **greendex**) is an estimation of how green the area around a property is.

## Calculation description 

To obtain the green area value, two important components need to be calculated: 

- A: Area of the zone of interest (defined by the radius)
- B: Area of green spaces

Then: *Green area percentage = (B / A) x 100*

<img src="https://raw.githubusercontent.com/red5ai/estaty/main/docs/media/greendex_example.png" width="650"/>

## Scripts 

Three scripts have been prepared for this use case:

- [simple_with_osm_only.py](simple_with_osm_only.py) - simplified version of the calculations. 
    Only OpenStreetMap data is used to obtain geometries of green areas
- [advanced_with_landsat.py](advanced_with_landsat.py) - advanced version of the calculations. 
    In addition to OpenStreetMap data Landast NDVI images is used to obtain geometries of green areas
- [benchmark.py](benchmark.py) - launch simple version of the calculations for several locations to obtain scale. 
    Results of benchmark script can be visualized as follows:

<img src="https://raw.githubusercontent.com/red5ai/estaty/main/docs/media/greendex_berlin_benchmark_map.png" width="650"/>


## Related materials

- [Combining Open Street Map and Landsat open data to verify areas of green zones](https://medium.com/towards-data-science/combining-open-street-map-and-landsat-open-data-to-verify-areas-of-green-zones-b1956e561321) (eng)
- [Объединение открытых данных Open Street Map и Landsat для уточнения площадей зеленых зон](https://habr.com/ru/articles/764686/) (rus)
