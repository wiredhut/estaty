from estaty.constants import WGS_EPSG
from estaty.data.data import VectorData
from estaty.stages import Stage, SPATIAL_DATA_LIST

import warnings
warnings.filterwarnings('ignore')


class AreaAnalysisStage(Stage):
    """
    Class to perform area calculation for objects into the defined area
    """

    def __init__(self, **params):
        super().__init__(**params)
        self.object_for_analysis = params['object_for_analysis']
        self.radius = self.object_for_analysis['radius']

        self.visualize = False
        if self.params.get('visualize') is not None:
            self.visualize = self.params.get('visualize')

    def apply(self, input_data: SPATIAL_DATA_LIST) -> VectorData:
        """
        Launch analysis with area calculation. Ignore all non-polygons elements
        """
        input_data = self.take_first_element_from_list(input_data)

        # Perform polygons merging into single geometry
        input_data.polygons['new_column'] = 0
        input_data.polygons = input_data.polygons.dissolve(by='new_column')

        if int(input_data.epsg) == WGS_EPSG:
            raise ValueError(f'Area calculation must be performed not with WGS coordinates')

        input_data.polygons['area'] = input_data.polygons.area

        # Calculate full area
        full_area = input_data.area_of_interest_as_dataframe
        full_area['area'] = full_area.area
        full_area_value = full_area['area'].iloc[0]

        # Calculate relative area
        input_data.polygons['full_area'] = [full_area_value] * len(input_data.polygons)
        input_data.polygons['area'] = input_data.polygons['area'] / input_data.polygons['full_area']
        input_data.polygons['area'] = input_data.polygons['area'] * 100

        return input_data
