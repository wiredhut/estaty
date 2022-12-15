from estaty.data_source.action import DataSource
from estaty.main import EstateModel
import matplotlib.pyplot as plt
import contextily as cx

import warnings
warnings.filterwarnings('ignore')


def load_data_with_water_from_osm():
    """
    Demonstration how to load data from Open Street Map
    In this example we will know how to load water data in a form of geopandas
    """
    # Define data sources and get data from it as parks
    osm_source = DataSource('osm', params={'category': 'water'})

    # Launch data loading
    model = EstateModel().for_property({'lat': 52.518168945198845,
                                        'lon': 13.385957678169396})

    loaded_data = model.compose(osm_source)

    # Take a look at the obtained data - it take several seconds to generate
    # plot and display it
    print(loaded_data.polygons)
    df = loaded_data.polygons.to_crs(epsg=3857)
    ax = df.plot(color='blue', alpha=0.5, edgecolor='k')
    cx.add_basemap(ax)
    plt.show()


if __name__ == '__main__':
    load_data_with_water_from_osm()
