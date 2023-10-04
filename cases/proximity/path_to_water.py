from estaty.analysis.action import Analyzer
from estaty.data_source.action import DataSource
from estaty.main import EstateModel
from estaty.preprocessing.action import Preprocessor

import warnings
warnings.filterwarnings('ignore')


def launch_parks_proximity_analysis_for_water_objects():
    """
    Aim: To assess the accessibility of parks for the selected property

    Demonstration how to launch green case simple version manually from nodes.
    There are several actions to construct analysis pipelines from:
        * DataSource - sources of data, API or files
        * Preprocessor - preprocessing obtained data
        * Merger - how to merge data
        * Analyzer - launch desired spatial analysis
        * Report - analysis results visualization or reporting
    """

    osm_source = DataSource('osm', params={'category': 'water'})

    osm_reprojected = Preprocessor('reproject', params={'to': 'auto'}, from_actions=[osm_source])

    analysis = Analyzer('distance', params={'network_type': 'walk', 'visualize': True, 'color': 'blue'},
                        from_actions=[osm_reprojected])

    model = EstateModel().for_property({'lat': 52.5171411, 'lon': 13.3857187}, radius=2000)
    founded_routes = model.compose(analysis)

    print(founded_routes.lines)
    print(f'Min length: {founded_routes.lines["Length"].min():.2f}, m')
    print(f'Mean length: {founded_routes.lines["Length"].mean():.2f}, m')
    print(f'Max length: {founded_routes.lines["Length"].max():.2f}, m')


if __name__ == '__main__':
    launch_parks_proximity_analysis_for_water_objects()
