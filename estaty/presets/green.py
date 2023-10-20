from estaty.presets.interface import Preset
from estaty.analysis.action import Analyzer
from estaty.data_source.action import DataSource
from estaty.merge.action import Merger
from estaty.preprocessing.action import Preprocessor
from estaty.report.action import Report


class GreenCaseAdvancedPreset(Preset):
    """ Preset for processing green areas case """

    def return_final_action(self):
        """ Using predefined structure of pipeline for analysis """
        # 1 Stage - define data sources and get data from them
        osm_source = DataSource('osm', params={'category': 'park'})
        bio_source = DataSource('gbif', params={'species': ['ambrosia']})

        # 2 Stage - re project layers into metric projection
        osm_reprojected = Preprocessor('reproject',
                                       params={'from': '4326', 'to': '4685'},
                                       from_actions=[osm_source])
        bio_reprojected = Preprocessor('reproject',
                                       params={'from': '4326', 'to': '4685'},
                                       from_actions=[bio_source])

        # 3 Stage - merge data into OSM polygons (method match)
        merged_vector = Merger('vector', params={'method': 'match'},
                               from_actions=[osm_reprojected, bio_reprojected])

        # 4 Stage - calculate distances from open source
        analysis = Analyzer('distance', params={'restriction': 'only_roads',
                                                'radius': 500},
                            from_actions=[merged_vector])

        # 5 Stage - display all prepared output calculations into console
        report = Report('stdout', from_actions=[analysis])

        return report
