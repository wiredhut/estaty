from estaty.data_source.action import DataSource
from estaty.main import EstateModel
import matplotlib.pyplot as plt
import contextily as cx

import warnings
warnings.filterwarnings('ignore')


def load_data_with_parks_from_osm():
    """
    Demonstration how to load data from file in local storage
    In this example we will know how to load parks data in a form of geopandas
    """
    # Define data sources and get data from it as parks
    osm_source = DataSource('gbif_local', params={'species': ['ambrosia']})

    # Launch data loading
    model = EstateModel().for_property({'lat': 52.518168945198845,
                                        'lon': 13.385957678169396},
                                       radius=3000)

    loaded_data = model.compose(osm_source)

    # Take a look at the obtained data - it take several seconds to generate
    # plot and display it
    print(loaded_data.all)
    loaded_data.to_crs(3857)
    ax = loaded_data.all.plot(color='red', alpha=0.6, edgecolor='k', markersize=15)
    cx.add_basemap(ax)
    plt.suptitle('Ambrosia artemisiifolia occurrences')
    plt.show()


if __name__ == '__main__':
    load_data_with_parks_from_osm()
