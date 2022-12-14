from typing import List

from estaty.action import SecondaryAction


class Analyzer(SecondaryAction):
    """ Action for performing analysis """

    def __init__(self, action_name: str, params: dict = None,
                 from_actions: List[SecondaryAction] = None):
        super().__init__(action_name, params, from_actions)

    def execute(self):
        pass
