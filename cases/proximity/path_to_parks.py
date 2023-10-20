from estaty.analysis.action import Analyzer
from estaty.data_source.action import DataSource
from estaty.main import EstateModel
from estaty.preprocessing.action import Preprocessor

import warnings
warnings.filterwarnings('ignore')


def launch_parks_proximity_analysis():
    # 1 Stage - define data sources and get data from them
    osm_source = DataSource('osm', params={'category': 'parks'})

    # 2 Stage - re project layers obtained from OSM: UTM zone 33N - EPSG:32633
    osm_reprojected = Preprocessor('reproject',
                                   params={'to': 32633},
                                   from_actions=[osm_source])

    # 4 Stage - calculate distances from open source
    analysis = Analyzer('distance', params={'network_type': 'walk', 'visualize': True, 'color': 'green',
                                            'title': 'Parks'},
                        from_actions=[osm_reprojected])

    # Launch model for desired location
    model = EstateModel().for_property({'lat': 52.5171411, 'lon': 13.3857187}, radius=2000)
    founded_routes = model.compose(analysis)

    print(founded_routes.lines)
    print(f'Min length: {founded_routes.lines["Length"].min():.2f}, m')
    print(f'Mean length: {founded_routes.lines["Length"].mean():.2f}, m')
    print(f'Max length: {founded_routes.lines["Length"].max():.2f}, m')


if __name__ == '__main__':
    launch_parks_proximity_analysis()
