from estaty.analysis.action import Analyzer
from estaty.data_source.action import DataSource
from estaty.main import EstateModel
from estaty.merge.action import Merger
from estaty.preprocessing.action import Preprocessor
from estaty.report.action import Report

import warnings
warnings.filterwarnings('ignore')


def read_file():
    file_source = DataSource('gpkg', params={'path': './package.gpkg', 'layer': 'countries'})

    # Launch model
    model = EstateModel().for_property({'lat': 52.5171411, 'lon': 13.3857187}, radius=2000)

    model.compose(file_source)


if __name__ == '__main__':
    read_file()
