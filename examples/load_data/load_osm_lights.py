from estaty.data_source.action import DataSource
from estaty.main import EstateModel
import matplotlib.pyplot as plt
import contextily as cx

import warnings
warnings.filterwarnings('ignore')


def load_data_with_lights_from_osm():
    """
    Demonstration how to load data from Open Street Map
    In this example we will know how to load street lights in a form of geopandas

    Points to check:
    Berlin: {'lat': 52.518168945198845, 'lon': 13.385957678169396}
    Munich: {'lat': 48.13884230541626, 'lon': 11.568211350731131}
    """
    # Define data sources and get data from it as parks
    osm_source = DataSource('osm', params={'category': 'light'})

    # Launch data loading (may be time consuming)
    model = EstateModel().for_property({'lat': 52.518168945198845,
                                        'lon': 13.385957678169396},
                                       radius=500)

    loaded_data = model.compose(osm_source)

    # Take a look at the obtained data - it take several seconds to generate
    # plot and display it
    print(loaded_data.lines)
    loaded_data.to_crs(3857)
    poly = loaded_data.polygons.plot(color='#F1FF4C', alpha=0.9)
    lines = loaded_data.lines.plot(ax=poly, color='#F1FF4C', alpha=0.5)
    ax = loaded_data.points.plot(ax=lines, color='orange', alpha=0.5, markersize=5)
    cx.add_basemap(ax, crs=loaded_data.polygons.crs.to_string(), source=cx.providers.CartoDB.Voyager)
    plt.suptitle('Street lights according to Open Street Map data')
    plt.show()


if __name__ == '__main__':
    values = [1, 1.1, 1.4, 1.6, 1.8, 2.0]
    ranks = [1, 3, 4]
    velocity_per_rank = [1.7, 1.1, 1]

    plt.scatter(ranks, velocity_per_rank)
    plt.grid()
    plt.xlabel('Rank')
    plt.ylabel('Flow velocity, m/s')
    plt.show()
