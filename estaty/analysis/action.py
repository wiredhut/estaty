from typing import List

from estaty.actions import SecondaryAction


class Analyzer(SecondaryAction):
    """
    Action for performing analysis on obtained data

    Possible analyses:
        - 'distance':
            - network_type - calculate distances using only specific roads
            - visualize - is there a need to create visualizations
    """

    def __init__(self, action_name: str, params: dict = None,
                 from_actions: List[SecondaryAction] = None):
        super().__init__(action_name, params, from_actions)

    def execute(self):
        """ Launch desired analysis """
        if isinstance(self.execution_pool, list):
            raise ValueError('Analyzer does not support multiple stages processing')

        data = self.execute_previous_actions()

        # Launch analysis on obtained data
        params = {**self.params, **{'object_for_analysis': self.object_for_analysis}}
        data = self.execution_pool(**params).apply(data)
        return data
