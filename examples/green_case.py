from estaty.osm_plugin.green_case import GreenAnalysis
from estaty.osm_plugin.load import LoadOSMData

import warnings
warnings.filterwarnings('ignore')


def load_and_show():
    """ Load and show data from OSM """
    loader = LoadOSMData('Berlin')
    osm_data = loader.get_data('parks')

    # x and y coordinates of estate object
    object_for_analysis = [13.383872, 52.512176]

    analyser = GreenAnalysis(osm_data)
    analyser.calculate_metric(*object_for_analysis)


if __name__ == '__main__':
    load_and_show()
