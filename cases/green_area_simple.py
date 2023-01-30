import contextily as cx
import matplotlib.pyplot as plt
import numpy as np

from estaty.analysis.action import Analyzer
from estaty.data_source.action import DataSource
from estaty.main import EstateModel
from estaty.preprocessing.action import Preprocessor

import warnings
warnings.filterwarnings('ignore')


def calculate_green_area(radius: int = 1000):
    """
    Example how to perform "green" area calculation using data

    Possible addresses to try:
        - 'Berlin, Neustädtische Kirchstraße 4-7' or {'lat': 52.5171411, 'lon': 13.3857187}
        - 'Munich, Kaulbachstraße, Alt-Schwabing, Schwabing - Ost, Schwabing-Freimann'
        or {'lat': 48.1558976, 'lon': 11.5858327}
    """

    # 1 Stage - load data about parks
    osm_source = DataSource('osm', params={'category': 'parks'})

    # 2 Stage - re project layers obtained from OSM into UTM zone 33N
    osm_reprojected = Preprocessor('reproject', params={'to': 32633},
                                   from_actions=[osm_source])

    # 4 Stage - calculate area
    analysis = Analyzer('area', from_actions=[osm_reprojected])

    # Launch model for desired location
    model = EstateModel().for_property({'lat': 48.1558976, 'lon': 11.5858327},
                                       radius=radius)
    calculated_areas = model.compose(analysis)

    green_area = calculated_areas.polygons['area'].sum()
    msg = f'"green" area nearby property (buffer {radius} metres): {green_area:.2f}, %'
    print(msg)

    # Some visualizations
    calculated_areas.to_crs(3857)
    # Create layer with central (target) point
    target_point = model.get_property_as_dataframe()
    target_point = target_point.to_crs(epsg=3857)

    ax = calculated_areas.area_of_interest_as_dataframe.plot(color='red', alpha=0.4)
    ax = calculated_areas.polygons.plot(ax=ax, column='area', legend=True,
                                        cmap='Greens', zorder=1,
                                        legend_kwds={'label': "Relative area, %"})
    ax = target_point.plot(ax=ax, color='red', alpha=1.0, markersize=40,
                           edgecolor='black')
    plt.suptitle(msg)
    cx.add_basemap(ax)
    plt.show()


if __name__ == '__main__':
    calculate_green_area(500)