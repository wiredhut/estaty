from typing import List, Union

from estaty.actions import SecondaryAction
from estaty.data.data import CommonData


class Analyzer(SecondaryAction):
    """ Action for performing analysis """

    def __init__(self, action_name: str, params: dict = None,
                 from_actions: List[SecondaryAction] = None):
        super().__init__(action_name, params, from_actions)

    def execute(self, input_data: Union[CommonData, None] = None):
        data = self.execute_previous_actions(input_data)
