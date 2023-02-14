from estaty.experiment.explore import CaseExploration

import warnings
warnings.filterwarnings('ignore')


def calculate_green_area_for_several_objects_using_bbox():
    """
    Launch experiments to calculate possible values of green index for different
    locations.

    Set location for experiments using bbox coordinates
    """
    # Define coordinates (WGS84) for experiments
    locations = {'min_x': 13.0, 'max_x': 13.7, 'min_y': 52.3, 'max_y': 52.7}

    exploration = CaseExploration(400, locations, 'simple_green_scale_bbox.gpkg', True)
    exploration.launch_green_experiment()


def calculate_green_area_for_several_objects_using_name():
    """
    Launch experiments to calculate possible values of green index for different
    locations

    Set location for experiments using city name and administrative borders
    """
    locations = 'Berlin'

    exploration = CaseExploration(400, locations,
                                  f'simple_green_scale_{locations}.gpkg', True)
    exploration.launch_green_experiment()


if __name__ == '__main__':
    calculate_green_area_for_several_objects_using_name()
