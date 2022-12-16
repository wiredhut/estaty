from estaty.data_source.action import DataSource
from estaty.main import EstateModel
import matplotlib.pyplot as plt
import contextily as cx

import warnings
warnings.filterwarnings('ignore')


def load_data_with_parks_from_osm():
    """
    Demonstration how to load data from Open Street Map
    In this example we will know how to load parks data in a form of geopandas

    Points to check:
    Berlin: {'lat': 52.518168945198845, 'lon': 13.385957678169396}
    Munich: {'lat': 48.13884230541626, 'lon': 11.568211350731131}
    """
    # Define data sources and get data from it as parks
    osm_source = DataSource('osm', params={'category': 'parks'})

    # Launch data loading
    model = EstateModel().for_property({'lat': 52.518168945198845,
                                        'lon': 13.385957678169396},
                                       radius=1000)

    loaded_data = model.compose(osm_source)

    # Take a look at the obtained data - it take several seconds to generate
    # plot and display it
    print(loaded_data.polygons)
    loaded_data.to_crs(3857)
    ax = loaded_data.all.plot(color='green', alpha=0.3, edgecolor='k')
    cx.add_basemap(ax)
    plt.suptitle('Parks according to Open Street Map data')
    plt.show()


if __name__ == '__main__':
    load_data_with_parks_from_osm()
