from estaty.experiment.explore import CaseExploration

import warnings
warnings.filterwarnings('ignore')


def calculate_green_area_for_several_objects():
    """
    Launch experiments to calculate possible values of green index for different
    locations
    """
    # Define coordinates (WGS84) for experiments
    locations = {'min_x': 13.0, 'max_x': 13.7, 'min_y': 52.3, 'max_y': 52.7}

    exploration = CaseExploration(400, locations, 'simple_green_case_scale.gpkg', True)
    exploration.launch_green_experiment()


if __name__ == '__main__':
    calculate_green_area_for_several_objects()
