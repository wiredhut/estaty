# GREENDEX service

<img src="https://raw.githubusercontent.com/red5ai/estaty/main/docs/media/greendex_logo.png" width="600"/>

**"Greendex"**: 

1. Service with API which can calculate simple Environmental, Social, and Governance (ESG) parameter 
    for real estate assets using addresses: Swagger UI [https://api.greendex.wiredhut.com/docs](https://api.greendex.wiredhut.com/docs)
2. A Google spreadsheet add on which can be executed as Excel function like `SUM` (or any other familiar function) which can calculate simple characteristic how "green" the building's surrounding is. 

<img src="https://raw.githubusercontent.com/red5ai/estaty/main/docs/media/greendex_example.png" width="650"/>

The service allows users to estimate the “greenness” of a building's (asset’s) location. For this purpose, the area of green spaces is calculated using open sources of cartographic data. The ratio of this “green” area to the total area within the geometry is then calculated. Green space includes parks, flowerbeds, etc. 
The size of the area to be analyzed is determined by the radius (in meters). 

## Spreadsheet usage example

Use function `=GREENDEX(P1, P2)` with two parameters:

- `P1`. First parameter, address as text. Example: `Berlin, Neustädtische Kirchstraße 4-7`
- `P2`. Second parameter, radius for area in meters. Example: `500`

## How to understand is the obtained green value good or not 

As is clear from the description of the indicator, it can vary from 0 to 100. 
But to understand how good a number is obtained for the selected asset, it is better to have statistics on several launches. 

For example, using the greendex service the benchmark for Berlin was prepared: 

<img src="https://raw.githubusercontent.com/red5ai/estaty/main/docs/media/greendex_berlin_benchmark_map.png" width="650"/>

On the map is shown green index evaluation for randomly chosen points in administrative boundaries of Berlin in buildings extent. 

Histogram of green index values for Berlin: 

<img src="https://raw.githubusercontent.com/red5ai/estaty/main/docs/media/greendex_berlin_benchmark_scale.png" width="650"/>

In this way, the obtained value can be compared with other buildings in Berlin and it is possible to figure out whether it is "greener" than other objects.

## Contacts 

If you want to ask questions to the developers personally or learn about custom development, 
then feel free to visit the official website of the company that develops this product: [Wiredhut](https://wiredhut.com/)