from estaty.data_source.action import DataSource
from estaty.main import EstateModel

import warnings

from estaty.preprocessing.action import Preprocessor

warnings.filterwarnings('ignore')


def load_data_in_several_branches():
    """
    Demonstration how to construct processing model with several branches
    """
    parks_source = DataSource('osm', params={'category': 'parks'})
    lights_source = DataSource('osm', params={'category': 'lights'})

    dummy_preprocessing = Preprocessor('dummy', {},
                                       from_actions=[parks_source, lights_source])

    # Launch data loading (may be time consuming)
    model = EstateModel().for_property({'lat': 52.518168945198845,
                                        'lon': 13.385957678169396},
                                       radius=500)

    loaded_data = model.compose(dummy_preprocessing)

    print(f'List with the following dataclasses number: {len(loaded_data)}')
    for data_block in loaded_data:
        print(f'Information about obtained data {data_block.description}')


if __name__ == '__main__':
    load_data_in_several_branches()