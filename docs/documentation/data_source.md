# Data source

The first node that every pipelines starts with is the DataSource. 
Using DataSource it is possible to get data directly from third-party services with which **estaty** has integrations, 
for example OpenStreetMap. Or spatial data can be loaded from files. 

## osm

Action name: `osm`

Description: Load data directly from OpenStreetMap using `osmnx` module

Parameters: 

- `category`: category of data to load. Possible options:
  - `water`: water objects 
  - `park`: parks,
  - `light`: streetlights,
  - `municipality` : administrative borders,
  - `school`: schools,
  - `driving_school`: driving school,
  - `bar`: bars,
  - `waste_disposal`: waste disposal,
  - `toilet`: public toilets,
  - `police`: police
- `local_cache`: bool. is there a need to use local caching for OSM data or not (save downloaded data into files)

Usage example: 

```Python
from estaty.data_source.action import DataSource

osm_source = DataSource('osm', params={'category': 'park'})
```

## csv

Action name: `csv`

Description: Load data from csv and create based on it geo dataframe with **point** geometries

Parameters: 

- `path`: path to the file
- `lat`: name of column in the file with latitude information
- `lon`: name of column in the file with longitude information
- `crs`: coordinate reference system EPSG code
- `sep`: separator for csv file

Usage example: 

```Python
from estaty.data_source.action import DataSource

file_source = DataSource('csv', params={'path': './data/quercus_berlin.csv',
                                        'lat': 'decimalLatitude', 'lon': 'decimalLongitude',
                                        'crs': 4326, 'sep': '\t'})
```

## Usage example

End to end example of data source usages 

```Python
from estaty.data_source.action import DataSource
from estaty.main import EstateModel

import warnings
warnings.filterwarnings('ignore')


def load_data_from_osm():
    osm_source = DataSource('osm', params={'category': 'park'})
    model = EstateModel().for_property({'lat': 52.5171411, 'lon': 13.3857187}, radius=2000)
    loaded_data = model.compose(osm_source)

    print(loaded_data)


if __name__ == '__main__':
    load_data_from_osm()
```