from pathlib import Path
from typing import List, Union, Dict
import random

import geopandas
import pandas as pd
from geopandas import GeoDataFrame
from loguru import logger
from shapely.geometry import Polygon, Point

from app.main import Place
from estaty.api.estaty_api import Estaty
from estaty.constants import WGS_EPSG
from estaty.experiment.administrative import AdministrativeBoundaries


class CaseExploration:
    """
    Class for launching desired cases multiple times to compute metrics
    Results of such experiments can be used during comparison of new results
    """

    def __init__(self, number_of_experiments: int = 100,
                 locations: Union[Dict, List[Dict], str, Union[str], Union[Polygon]] = None,
                 file_to_save_results: Union[Path, str] = None,
                 vis: bool = False):
        self.number_of_experiments = number_of_experiments

        # Configure locations
        if locations is None:
            # Use default location for experiments
            locations = {'min_x': 13.0, 'max_x': 13.7, 'min_y': 52.3, 'max_y': 52.7}
        if isinstance(locations, list) is False:
            locations = [locations]
        self.locations = locations
        self._convert_locations_into_geometries()

        # Configure path to file where there is a need to save results
        if file_to_save_results is None:
            file_to_save_results = 'exploration_results.gpkg'
        if isinstance(file_to_save_results, str):
            file_to_save_results = Path(file_to_save_results)
            file_to_save_results = file_to_save_results.resolve()
        self.file_to_save_results = file_to_save_results

        self.vis = vis

    def launch_green_experiment(self, radius_to_check: List[int] = None):
        """
        Launch simple green index calculation to calculate several

        :param radius_to_check: list with possible radius for experiments
        """
        if radius_to_check is None:
            radius_to_check = [250, 500, 1000, 1500, 2000]

        if self.file_to_save_results.is_file() and self.vis:
            # File already exist and there is need to display plot
            report = geopandas.read_file(self.file_to_save_results)
            self.show_green_index_plot(report, radius_to_check)
            return

        report = []
        for experiment_id in range(self.number_of_experiments):
            # Randomly choose location to perform launch
            location = self.choose_location()
            place = self.generate_random_place(location)
            # Choose radius for experiment
            radius = self.choose_radius(radius_to_check)

            try:
                service = Estaty(place, radius)
                logger.debug(f'Perform experiment {experiment_id} for {place.lat, place.lon} with radius {radius}')
                calc_area, geometries, buffer = service.launch_green_area_calculation_case('OpenStreetMap')
            except Exception as ex:
                logger.info(f'Skip experiment number {experiment_id} due to {ex}')
                continue

            report.append([place.lat, place.lon, calc_area, radius])

        report = pd.DataFrame(report, columns=['lat', 'lon', 'area', 'radius'])
        report = geopandas.GeoDataFrame(report, geometry=geopandas.points_from_xy(report.lon, report.lat),
                                        crs=WGS_EPSG)
        report.to_file(self.file_to_save_results, driver='GPKG')
        if self.vis:
            self.show_green_index_plot(report, radius_to_check)

    def choose_location(self):
        if len(self.locations) == 1:
            return self.locations[0]

        location_id_to_take = random.randint(0, len(self.locations) - 1)
        return self.locations[location_id_to_take]

    def _convert_locations_into_geometries(self):
        locations_as_geometries = []
        for location in self.locations:
            if isinstance(location, dict):
                coordinates = [[location['min_x'], location['min_y']],
                               [location['min_x'], location['max_y']],
                               [location['max_x'], location['max_y']],
                               [location['max_x'], location['min_y']]]
                polygon = Polygon(coordinates).convex_hull
            elif isinstance(location, str):
                # Load data from OSM
                boundaries = AdministrativeBoundaries(location)
                polygon = boundaries.get_city_polygon()
            else:
                raise ValueError('Unsupported type for location')
            locations_as_geometries.append(polygon)

        self.locations: List[Polygon] = locations_as_geometries

    @staticmethod
    def generate_random_place(location):
        """
        Based on location generate randomly coordinates of point, which
        lies within polygon
        """
        min_x, min_y, max_x, max_y = location.bounds
        while True:
            random_x = random.uniform(min_x, max_x)
            random_y = random.uniform(min_y, max_y)
            point = Point(random_x, random_y)
            if location.contains(point):
                return Place(lat=random_y, lon=random_x)

    @staticmethod
    def choose_radius(radius_to_check: List[int]):
        if len(radius_to_check) == 1:
            return radius_to_check[0]

        radius_id_to_take = random.randint(0, len(radius_to_check) - 1)
        return radius_to_check[radius_id_to_take]

    @staticmethod
    def show_green_index_plot(report: GeoDataFrame, radius_to_check: List[int]):
        """ Display plot with calculated areas """
        import contextily as cx
        import matplotlib.pyplot as plt
        import seaborn as sns

        report = report.to_crs(3857)
        ax = report.plot(column='area', legend=True, alpha=1.0,
                         cmap='Greens', markersize=30, edgecolor="black",
                         legend_kwds={'label': "Green index, %"})
        cx.add_basemap(ax)
        plt.show()

        report = report.rename(columns={'area': 'Green index, %'})

        # Create histogram
        with sns.axes_style('darkgrid'):
            sns.histplot(data=report, x="Green index, %", color='green',
                         kde=True)
            plt.show()

        with sns.axes_style('darkgrid'):
            sns.histplot(data=report, x="Green index, %", kde=True, palette='Greens',
                         hue='radius', hue_order=radius_to_check)
            plt.show()
