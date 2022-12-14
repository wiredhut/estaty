from typing import List

from estaty.action import SecondaryAction, Action


class Preprocessor(SecondaryAction):
    """ Class for processing data """

    def __init__(self, action_name: str, params: dict = None,
                 from_actions: List[Action] = None):
        super().__init__(action_name, params, from_actions)

    def execute(self):
        pass
