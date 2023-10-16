from estaty.analysis.action import Analyzer
from estaty.data_source.action import DataSource
from estaty.main import EstateModel
from estaty.preprocessing.action import Preprocessor

import warnings
warnings.filterwarnings('ignore')


def launch_proximity_analysis_for_street_lights_objects():
    # TODO remove - example to be able to process lines and multi lines objects
    osm_source = DataSource('osm', params={'category': 'lights'})

    osm_reprojected = Preprocessor('reproject', params={'to': 'auto'}, from_actions=[osm_source])

    analysis = Analyzer('distance', params={'network_type': 'walk', 'visualize': True, 'color': 'yellow'},
                        from_actions=[osm_reprojected])

    model = EstateModel().for_property({'lat': 52.5171411, 'lon': 13.3857187}, radius=250)
    founded_routes = model.compose(analysis)

    print(founded_routes.lines)
    print(f'Min length: {founded_routes.lines["Length"].min():.2f}, m')
    print(f'Mean length: {founded_routes.lines["Length"].mean():.2f}, m')
    print(f'Max length: {founded_routes.lines["Length"].max():.2f}, m')


if __name__ == '__main__':
    launch_proximity_analysis_for_street_lights_objects()
