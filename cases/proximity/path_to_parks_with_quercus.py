from estaty.analysis.action import Analyzer
from estaty.data_source.action import DataSource
from estaty.main import EstateModel
from estaty.merge.action import Merger
from estaty.preprocessing.action import Preprocessor
from estaty.report.action import Report

import warnings
warnings.filterwarnings('ignore')


def launch_parks_with_quercus_proximity_analysis():
    """
    Calculate proximity to parks using OpenStreetMap data and
    GBIF.org (20 October 2023) GBIF Occurrence Download https://doi.org/10.15468/dl.f487j5
    """
    # 1 Stage - define data sources and get data from them
    osm_source = DataSource('osm', params={'category': 'park'})
    bio_source = DataSource('csv', params={'path': './data/quercus_berlin.csv',
                                           'lat': 'decimalLatitude', 'lon': 'decimalLongitude',
                                           'crs': 4326, 'sep': '\t'})

    # 2 Stage - re project layers into metric projection
    osm_reprojected = Preprocessor('reproject', params={'to': 'auto'}, from_actions=[osm_source])
    bio_reprojected = Preprocessor('reproject', params={'to': 'auto'}, from_actions=[bio_source])

    # 3 Stage - merge data into OSM polygons (method match) - order is important
    merged_vector = Merger('vector', params={'method': 'match', 'buffer': 10},
                           from_actions=[osm_reprojected, bio_reprojected])

    # 4 Stage - calculate distances from open source
    analysis = Analyzer('distance', params={'network_type': 'walk', 'visualize': True, 'color': 'green',
                                            'edgecolor': 'black', 'title': 'Bars'},
                        from_actions=[merged_vector])

    # 5 Stage - display all prepared output calculations into console
    report = Report('stdout', from_actions=[analysis])

    # Launch model
    model = EstateModel().for_property({'lat': 52.5171411, 'lon': 13.3857187}, radius=2000)

    model.compose(report)


if __name__ == '__main__':
    launch_parks_with_quercus_proximity_analysis()
