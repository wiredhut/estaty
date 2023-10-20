from typing import List, Any, Union

from estaty.actions import SecondaryAction, Action
from estaty.data.data import CommonData


class Report(SecondaryAction):
    """ Class for preparing reports and visualizations """

    def __init__(self, action_name: str, params: dict = None,
                 from_actions: List[Action] = None):
        super().__init__(action_name, params, from_actions)

    def execute(self):
        data = self.execute_previous_actions()

        params = {**self.params, **{'object_for_analysis': self.object_for_analysis}}
        data = self.execution_pool(**params).apply(data)
        return data
