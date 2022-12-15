from estaty.analysis.action import Analyzer
from estaty.data_source.action import DataSource
from estaty.main import EstateModel
from estaty.merge.action import Merger
from estaty.preprocessing.action import Preprocessor
from estaty.report.action import Report

import warnings
warnings.filterwarnings('ignore')


def launch_green_case_analysis_for_property():
    """
    Demonstration of estaty functionality on green case advanced version with
    parks for particular real estate object (property)
    """
    # Example for Berlin, Neustädtische Kirchstraße 4-7
    model = EstateModel().for_property({'lat': 52.518168945198845,
                                        'lon': 13.385957678169396})
    model.compose('green_advanced')


def launch_green_case_analysis_for_property_manually():
    """
    Demonstration how to launch green case advanced version manually from nodes.
    There are several actions to construct analysis pipelines from:
        * DataSource - sources of data, API or files
        * Preprocessor - preprocessing obtained data
        * Merger - how to merge data
        * Analyzer - launch desired spatial analysis
        * Report - analysis results visualization or reporting
    """

    # 1 Stage - define data sources and get data from them
    osm_source = DataSource('osm', params={'category': 'parks'})
    bio_source = DataSource('gbif_local', params={'species': ['ambrosia']})

    # 2 Stage - re project layers into metric projection
    osm_reprojected = Preprocessor('reproject',
                                   params={'to': 32633},
                                   from_actions=[osm_source])
    bio_reprojected = Preprocessor('reproject',
                                   params={'to': 32633},
                                   from_actions=[bio_source])

    # 3 Stage - merge data into OSM polygons (method match) - order is important
    merged_vector = Merger('vector', params={'method': 'match'},
                           from_actions=[osm_reprojected, bio_reprojected])

    # 4 Stage - calculate distances from open source
    analysis = Analyzer('distance', params={'restriction': 'only_roads',
                                            'radius': 500},
                        from_actions=[merged_vector])

    # 5 Stage - display all prepared output calculations into console
    report = Report('stdout', from_actions=[analysis])

    # Launch model
    model = EstateModel().for_property({'lat': 52.518168945198845,
                                        'lon': 13.385957678169396})

    model.compose(report)


if __name__ == '__main__':
    launch_green_case_analysis_for_property_manually()
