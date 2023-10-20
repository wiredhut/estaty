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
    Demonstration how to launch green case advanced version manually from nodes.
    There are using several data sources to perform analysis
    There are several actions to construct analysis pipelines from:
        * DataSource - sources of data, API or files
        * Preprocessor - preprocessing obtained data
        * Merger - how to merge data
        * Analyzer - launch desired spatial analysis
        * Report - analysis results visualization or reporting
    """

    # 1 Stage - define data sources and get data from them
    osm_source = DataSource('osm', params={'category': 'parks'})
    bio_source = DataSource('csv', params={'path': './data/quercus_data.csv',
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
    model = EstateModel().for_property({'lat': 59.944843895537566, 'lon': 30.294778398601856}, radius=2000)

    model.compose(report)


if __name__ == '__main__':
    launch_parks_with_quercus_proximity_analysis()
