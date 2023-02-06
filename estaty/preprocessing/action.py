from typing import List, Union

from estaty.actions import SecondaryAction, Action
from estaty.data.data import CommonData


class Preprocessor(SecondaryAction):
    """
    Class for preprocessing data

    Apply different strategies for effective vector and raster data
    preprocessing
    """

    def __init__(self, action_name: str, params: dict = None,
                 from_actions: List[Action] = None):
        super().__init__(action_name, params, from_actions)

    def execute(self):
        """ Get data from previous actions and apply preprocessing """
        if isinstance(self.execution_pool, list):
            raise ValueError('Preprocessor does not support multiple stages processing')

        data = self.execute_previous_actions()
        if self.action_name != 'dummy' and len(data) > 1:
            raise ValueError(f'Preprocessor does not support merging operations from '
                             f'several sources. Please reduce sources number from {len(data)} to 1')

        # Launch preprocessor on obtained data
        params = {**self.params, **{'object_for_analysis': self.object_for_analysis}}
        data = self.execution_pool(**params).apply(data)
        return data
