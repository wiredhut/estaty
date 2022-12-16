from typing import List, Union

from estaty.actions import SecondaryAction, Action
from estaty.data.data import CommonData


class Preprocessor(SecondaryAction):
    """ Class for preprocessing data """

    def __init__(self, action_name: str, params: dict = None,
                 from_actions: List[Action] = None):
        super().__init__(action_name, params, from_actions)

    def execute(self, input_data: Union[CommonData, None] = None):
        """ Get data from previous actions and apply preprocessing """
        if isinstance(self.execution_pool, list):
            raise ValueError('Preprocessor does not support multiple stages processing')

        data = self.execute_previous_actions(input_data)

        # Launch preprocessor on obtained data
        data = self.execution_pool(**self.params).apply(data)
        return data
