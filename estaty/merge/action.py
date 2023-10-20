from typing import List, Union

from estaty.actions import SecondaryAction
from estaty.data.data import CommonData


class Merger(SecondaryAction):
    """ Action for merging data from different sources """

    def __init__(self, action_name: str, params: dict = None,
                 from_actions: List[SecondaryAction] = None):
        super().__init__(action_name, params, from_actions)

    def execute(self):
        data = self.execute_previous_actions()

        # Launch merging on obtained data
        params = {**self.params, **{'object_for_analysis': self.object_for_analysis}}
        data = self.execution_pool(**params).apply(data)
        return data
