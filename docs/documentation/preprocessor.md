# Preprocessor

An intermediate node that allows preparing data for further interactions (for merging or analysis)

<img src="https://raw.githubusercontent.com/wiredhut/estaty/main/docs/media/preprocessing.png" width="700"/>

*Raster data spatial resolution is under development

## reproject

Action name: `reproject`

Description: Assign new coordinate reference system (CRS) to the data

Parameters: 

- `to`: category of data to load. Possible options:

    - `int`: any relevant EPSG code;
    - `auto`: automatically assignment new metric CRS to the data;

`from_actions`: link to the previous nodes

Usage example: 

```Python
from estaty.data_source.action import DataSource
from estaty.preprocessing.action import Preprocessor

osm_source = DataSource('osm', params={'category': 'park'})
osm_reprojected = Preprocessor('reproject', params={'to': 'auto'}, from_actions=[osm_source])
```